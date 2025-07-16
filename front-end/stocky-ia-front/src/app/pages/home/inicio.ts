import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import AOS from 'aos';
import 'aos/dist/aos.css';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.scss']
})
export class Inicio implements OnInit {
  mensajesBanner = [
    'Optimiza tu inventario con IA',
    'Predice la demanda y ahorra recursos',
    'Moderniza tu gestión empresarial',
    'Decisiones más inteligentes con StockyIA'
  ];

  mensajeActual = '';
  private index = 0;

  ngOnInit(): void {
    AOS.init({
      duration: 800,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });

    // Inicializar primer mensaje
    this.mensajeActual = this.mensajesBanner[this.index];

    // Cambiar mensaje cada 5 segundos
    setInterval(() => {
      this.index = (this.index + 1) % this.mensajesBanner.length;
      this.mensajeActual = this.mensajesBanner[this.index];
    }, 5000);
  }

  scrollToSeccion(id: string): void {
    const target = document.getElementById(id);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  }
}
