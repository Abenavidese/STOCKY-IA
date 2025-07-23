import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import AOS from 'aos';
import 'aos/dist/aos.css';

@Component({
  selector: 'app-politicas',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './politicas.html',
  styleUrls: ['./politicas.scss']
})
export class Politicas implements OnInit {
  currentYear: number = new Date().getFullYear();

  ngOnInit(): void {
    AOS.init({
      duration: 800,
      easing: 'ease-in-out',
      once: true
    });
  }
}
