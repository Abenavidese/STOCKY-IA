import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import ApexCharts from 'apexcharts';
import { AnalyticsService, AnalyticsResponse } from '../../../services/analytics';
import { AuthService } from '../../../services/auth';

@Component({
  selector: 'app-graficas',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './graficas.html',
  styleUrls: ['./graficas.scss']
})
export class Graficas implements OnInit {
  analyticsData: AnalyticsResponse = {
    ventas_por_categoria: {},
    top_productos: {},
    productos_menos_consumidos: {},
    ventas_tiempo: [],
    ventas_totales_usd: 0,
    ventas_promedio_dia: 0,
    producto_top: '',
    distribucion_precios: {
      count: 0,
      mean: 0,
      std: 0,
      min: 0,
      '25%': 0,
      '50%': 0,
      '75%': 0,
      max: 0
    }
  };
  productoMenosConsumido: string = '';

  constructor(
    private analyticsService: AnalyticsService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const userId = this.authService.getUid();
    if (userId) {
      this.loadAnalytics(userId);
    } else {
      console.error('No se encontró un usuario autenticado.');
    }
  }

  private loadAnalytics(userId: string): void {
    this.analyticsService.getAnalyticsByUser(userId).subscribe((data) => {
      if (!data) {
        console.warn('No se recibieron datos de analytics.');
        return;
      }

      this.analyticsData = data;

      // Producto menos consumido
      const productos = Object.entries(this.analyticsData.productos_menos_consumidos || {});
      if (productos.length > 0) {
        this.productoMenosConsumido = productos.reduce((min, actual) =>
          actual[1] < min[1] ? actual : min
        )[0];
      }

      this.cdr.detectChanges();
      this.renderCharts();
    });
  }

  private renderCharts(): void {
    this.renderVentasPorCategoria();
    this.renderTopProductos();
    this.renderProductosMenosConsumidos();
    this.renderVentasTiempo();
  }

  private truncateLabel(label: string, maxLength: number = 15): string {
    return label.length > maxLength ? label.slice(0, maxLength) + '...' : label;
  }

  private renderVentasPorCategoria(): void {
    const categories = Object.keys(this.analyticsData.ventas_por_categoria);
    const values = Object.values(this.analyticsData.ventas_por_categoria);

    const options = {
      chart: { type: 'pie', height: 350 },
      labels: categories.map(c => this.truncateLabel(c, 20)),
      tooltip: { y: { formatter: (val: number) => `$${val.toFixed(2)}` } },
      series: values,
      legend: {
        labels: { colors: '#fff' },
        formatter: (seriesName: string) => this.truncateLabel(seriesName, 20)
      },
      colors: ['#3e65cf', '#185c68', '#444243', '#0e5a1b', '#f39c12', '#d35400']
    };

    document.querySelector('#ventas-categoria')!.innerHTML = '';
    new ApexCharts(document.querySelector('#ventas-categoria'), options).render();
  }

  private renderTopProductos(): void {
    const categories = Object.keys(this.analyticsData.top_productos);
    const values = Object.values(this.analyticsData.top_productos);

    const options = {
      chart: { type: 'bar', height: 350 },
      series: [{ data: values }],
      xaxis: {
        categories: categories.map(c => this.truncateLabel(c, 20)),
        labels: { rotate: -35, style: { fontSize: '12px', colors: '#fff' } }
      },
      colors: ['#2998ff'],
      dataLabels: { enabled: true, style: { fontSize: '11px', colors: ['#fff'] } }
    };

    document.querySelector('#top-productos')!.innerHTML = '';
    new ApexCharts(document.querySelector('#top-productos'), options).render();
  }

  private renderProductosMenosConsumidos(): void {
    const categories = Object.keys(this.analyticsData.productos_menos_consumidos);
    const values = Object.values(this.analyticsData.productos_menos_consumidos);

    const options = {
      chart: { type: 'bar', height: 350 },
      series: [{ data: values }],
      xaxis: {
        categories: categories.map(c => this.truncateLabel(c, 20)),
        labels: { rotate: -35, style: { fontSize: '12px', colors: '#fff' } }
      },
      colors: ['#d50680'],
      dataLabels: { enabled: true, style: { fontSize: '11px', colors: ['#fff'] } }
    };

    document.querySelector('#productos-menos')!.innerHTML = '';
    new ApexCharts(document.querySelector('#productos-menos'), options).render();
  }

  private renderVentasTiempo(): void {
    const fechas = this.analyticsData.ventas_tiempo.map(v => v.fecha);
    const ventas = this.analyticsData.ventas_tiempo.map(v => v.ventas_usd);

    const options = {
      chart: { type: 'line', height: 350 },
      series: [{ name: 'Ventas USD', data: ventas }],
      xaxis: {
        categories: fechas,
        labels: { rotate: -30, style: { fontSize: '12px', colors: '#fff' } }
      },
      colors: ['#00ab57'],
      tooltip: { y: { formatter: (val: number) => `$${val.toFixed(2)}` } }
    };

    document.querySelector('#ventas-tiempo')!.innerHTML = '';
    new ApexCharts(document.querySelector('#ventas-tiempo'), options).render();
  }
}
