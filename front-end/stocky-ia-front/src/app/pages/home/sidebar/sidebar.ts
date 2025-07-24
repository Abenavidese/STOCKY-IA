import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { Auth, signOut } from '@angular/fire/auth';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.scss'
})
export class Sidebar {
  menuClosed = false;

  constructor(private router: Router, private auth: Auth) {}

  toggleMenu() {
    this.menuClosed = !this.menuClosed;
  }

  async logout() {
    try {
      await signOut(this.auth);
      localStorage.removeItem('uid'); 
      this.router.navigate(['/login']);
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    }
  }
}
