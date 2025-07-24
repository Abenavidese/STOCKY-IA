import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import AOS from 'aos';
import 'aos/dist/aos.css';

interface Integrante {
  nombre: string;
  rol: string;
  foto: string;
  texto: string;
}

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.scss']
})
export class Inicio implements OnInit {
  mensajesBanner = [
    'Impulsa tus decisiones con inteligencia artificial avanzada',
    'Predicciones precisas para optimizar tu cadena de suministro',
    'Convierte los datos en estrategias con StockyIA',
    'Reduce costos y aumenta la rentabilidad con análisis inteligente',
    'Innovación en cada predicción, eficiencia en cada acción',
    'Visualiza el futuro de tu negocio con tecnología predictiva'
  ];

  mensajeActual = '';
  private index = 0;

  listaIntegrantes: Integrante[] = [
  {
    nombre: 'Anthony Benavides',
    rol: 'Project Manager',
    foto: 'assets/images/3.jpg',
    texto: `Anthony Benavides nació en Pasaje, El Oro, Ecuador, el 16 de diciembre del 2006.
    Actualmente estudia Ingeniería en Computación en la Universidad Politécnica Salesiana.
    Se especializa en la gestión de proyectos tecnológicos, liderando equipos de forma organizada
    y enfocándose en lograr objetivos con alta eficiencia y calidad.`
  },
  {
    nombre: 'Bryam Peralta',
    rol: 'Frontend Developer',
    foto: 'assets/images/4.jpg',
    texto: `Bryam Peralta nació en Cuenca, Ecuador, el 30 de diciembre del 2000.
    Estudia Computación en la Universidad Politécnica Salesiana. Es un apasionado por el diseño 
    y desarrollo frontend, creando interfaces intuitivas, modernas y optimizadas para ofrecer la 
    mejor experiencia de usuario.`
  },
  {
    nombre: 'Erick Zhigue',
    rol: 'Chatbot Developer',
    foto: 'assets/images/2.jpg',
    texto: `Erick Zhigue nació en Huaquillas, El Oro, el 11 de septiembre del 2004.
    Actualmente cursa la carrera de Computación en la Universidad Politécnica Salesiana.
    Le apasiona la inteligencia artificial, la automatización y el desarrollo de chatbots basados 
    en NLP (Procesamiento de Lenguaje Natural) para mejorar la interacción humano-máquina.`
  },
  {
    nombre: 'Henry Granda',
    rol: 'Backend Developer',
    foto: 'assets/images/1.jpg',
    texto: `Henry Granda nació en Cuenca, Ecuador, el 18 de enero del 2003.
    Estudia Computación en la Universidad Politécnica Salesiana.
    Le interesa el desarrollo de APIs robustas, arquitecturas backend escalables y modelos de 
    inteligencia artificial, aplicando siempre buenas prácticas y nuevas tecnologías.`
  }
];



  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    AOS.init({
      duration: 800,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });

    this.mensajeActual = this.mensajesBanner[this.index];

    setInterval(() => {
      this.index = (this.index + 1) % this.mensajesBanner.length;
      this.mensajeActual = this.mensajesBanner[this.index];
      this.cdr.detectChanges();
    }, 5000);
  }
}
