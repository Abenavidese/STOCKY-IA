import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import AOS from 'aos';
import 'aos/dist/aos.css';

interface Biografia {
  nombre: string;
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

  // Estado del modal
  bioVisible = false;
  bioSeleccionada: Biografia | null = null;

  // Datos de biografía
  biografias: Record<string, Biografia> = {
    anthony: {
      nombre: 'Anthony Benavides',
      texto: `Anthony Benavides nació en Pasaje, El Oro, Ecuador, el 16 de diciembre del 2006. 
      Realizó sus estudios primarios en la escuela Vicente Rocafuerte y sus estudios secundarios en el colegio Bachillerato Manuel A. Gonzales. 
      Ingresó a la universidad en el año 2023 para estudiar ingeniería en computación, en la cual se encuentra estudiando.`
    },
    bryam: {
      nombre: 'Bryam Peralta',
      texto: `Bryam Peralta nació en Cuenca, Ecuador, el 30 de diciembre del 2000. 
      Realizó sus estudios primarios en la escuela Manuel María Palacios Bravo y sus estudios secundarios en el colegio Bachillerato Ricaurte. 
      Ingresó a la Universidad Estatal de Cuenca en 2019 para estudiar ingeniería civil, pero en 2022 ingresó a la Universidad Politécnica Salesiana, donde estudia Computación.`
    },
    erick: {
      nombre: 'Erick Zhigue',
      texto: `Erick Zhigue nació en Loja, Ecuador, en 2002. 
      Realizó sus estudios en el Colegio Técnico Loja y se ha destacado por su interés en la inteligencia artificial y el desarrollo de chatbots. 
      Actualmente estudia en la Universidad Politécnica Salesiana, cursando la carrera de Computación.`
    },
    henry: {
      nombre: 'Henry Granda',
      texto: `Henry Granda nació en Cuenca, Ecuador, el 18 de enero de 2003. 
      Concluyó su bachillerato en el Colegio Técnico Nacional Huambí en la provincia de Morona Santiago. 
      Actualmente estudia la carrera de Computación en la Universidad Politécnica Salesiana en Cuenca.`
    }
  };

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
    }, 5000);
  }

  // Mostrar biografía
  mostrarBio(integrante: string): void {
    this.bioSeleccionada = this.biografias[integrante];
    this.bioVisible = true;
  }

  // Cerrar modal
  cerrarBio(): void {
    this.bioVisible = false;
    this.bioSeleccionada = null;
  }

  scrollToSeccion(id: string): void {
    const target = document.getElementById(id);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  }
}
