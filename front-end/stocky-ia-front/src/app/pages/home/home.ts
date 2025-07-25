import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Sidebar } from './sidebar/sidebar';
import { Topbar } from './topbar/topbar';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, Sidebar, Topbar],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home {}
