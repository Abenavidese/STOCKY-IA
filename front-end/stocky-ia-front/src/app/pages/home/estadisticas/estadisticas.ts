import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule, DecimalPipe, CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Predictions, PredictionsService } from '../../../services/predictions';
import ApexCharts from 'apexcharts';
import { AuthService } from '../../../services/auth';

@Component({
  selector: 'app-estadisticas',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule, DecimalPipe, CurrencyPipe],
  templateUrl: './estadisticas.html',
  styleUrls: ['./estadisticas.scss']
})
export class Estadisticas implements OnInit {
  predictions: Predictions[] = [];
  filteredPredictions: Predictions[] = [];

  categories: string[] = [];
  products: string[] = [];
  dates: string[] = [];
  selectedCategory: string = '';
  selectedProduct: string = '';
  selectedDate: string = '';
  totalDinero: number = 0;  

  constructor(
    private predictionsService: PredictionsService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const userId = this.authService.getUid();
    if (userId) {
      this.loadPredictions(userId);
    } else {
      console.error('No se encontró un usuario autenticado.');
    }
  }

  private loadPredictions(userId: string): void {
    this.predictionsService.getPredictionsByUser(userId).subscribe((data) => {
      this.predictions = data.map(p => ({
        ...p,
        prediccion: p.prediccion * 7,
        venta_anterior: p.venta_anterior * 7
      }));

      this.filteredPredictions = [...this.predictions];
      this.categories = [...new Set(this.predictions.map(p => p.category_name))];
      this.products = [...new Set(this.predictions.map(p => p.product_name))];
      this.dates = [...new Set(this.predictions.map(p => p.fecha.split('T')[0]))];

      this.calculateTotalDinero();  // <-- Calcula al inicio

      this.cdr.detectChanges();
      this.renderCharts();
    });
  }

  filterData(): void {
    this.filteredPredictions = this.predictions.filter(p =>
      (this.selectedCategory ? p.category_name === this.selectedCategory : true) &&
      (this.selectedProduct ? p.product_name === this.selectedProduct : true) &&
      (this.selectedDate ? p.fecha.split('T')[0] === this.selectedDate : true)
    );
    this.calculateTotalDinero();  // <-- recalcula
    this.renderCharts();
  }

  resetFilters(): void {
    this.selectedCategory = '';
    this.selectedProduct = '';
    this.filteredPredictions = [...this.predictions];
    this.calculateTotalDinero();  // <-- recalcula
    this.renderCharts();
  }

  private calculateTotalDinero(): void {
    this.totalDinero = this.filteredPredictions
      .reduce((sum, p) => sum + (p.prediccion * p.price_usd), 0);
    this.totalDinero = parseFloat(this.totalDinero.toFixed(2));  // Redondeo solo al final
  }

  private renderCharts(): void {
    this.renderBarChart();
    this.renderAreaChart();
  }

  private renderBarChart(): void {
    const topProducts = this.filteredPredictions.slice(0, 5);
    const barChartOptions = {
      series: [{ data: topProducts.map(p => p.prediccion), name: 'Predicciones' }],
      chart: { type: 'bar', background: 'transparent', height: 350, toolbar: { show: false } },
      colors: ['#2998ff', '#d50680', '#1e9872', '#ff9800', '#5832b3'],
      plotOptions: { bar: { distributed: true, borderRadius: 4, horizontal: false, columnWidth: '40%' } },
      dataLabels: { enabled: false },
      grid: { borderColor: '#55596e' },
      xaxis: { categories: topProducts.map(p => p.product_name) }
    };
    document.querySelector('#bar-chart')!.innerHTML = '';
    const barChart = new ApexCharts(document.querySelector('#bar-chart'), barChartOptions);
    barChart.render();
  }

  private renderAreaChart(): void {
    const areaData = this.filteredPredictions.slice(0, 7);
    const areaChartOptions = {
      series: [
        { name: 'Predicciones', data: areaData.map(p => p.prediccion) },
        { name: 'Ventas Anteriores', data: areaData.map(p => p.venta_anterior) }
      ],
      chart: { type: 'area', background: 'transparent', height: 350 },
      colors: ['#00ab57', '#d50000'],
      labels: areaData.map(p => p.fecha),
      dataLabels: { enabled: false },
      stroke: { curve: 'smooth' }
    };
    document.querySelector('#area-chart')!.innerHTML = '';
    const areaChart = new ApexCharts(document.querySelector('#area-chart'), areaChartOptions);
    areaChart.render();
  }
}
