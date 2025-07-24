import { Injectable } from '@angular/core';
import { Auth, onAuthStateChanged, User, signOut } from '@angular/fire/auth';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUid: string | null = null;
  private currentEmail: string | null = null;

  constructor(private auth: Auth) {
    // Escuchar cambios de autenticación
    onAuthStateChanged(this.auth, (user: User | null) => {
      if (user) {
        this.currentUid = user.uid;
        this.currentEmail = user.email || null;
        console.log('UID actualizado:', this.currentUid);
        console.log('Email actualizado:', this.currentEmail);

        // Guardar en localStorage
        localStorage.setItem('userUID', this.currentUid);
        if (this.currentEmail) {
          localStorage.setItem('userEmail', this.currentEmail);
        }
      } else {
        this.currentUid = null;
        this.currentEmail = null;
        console.log('Usuario no autenticado.');

        // Eliminar datos de localStorage
        localStorage.removeItem('userUID');
        localStorage.removeItem('userEmail');
      }
    });
  }

  // Obtener UID
  getUid(): string | null {
    return this.currentUid || localStorage.getItem('userUID');
  }

  // Obtener Email
  getEmail(): string | null {
    return this.currentEmail || localStorage.getItem('userEmail');
  }

  // Cerrar sesión
  async logout() {
    await signOut(this.auth);
    // Limpiar localStorage al cerrar sesión
    localStorage.removeItem('userUID');
    localStorage.removeItem('userEmail');
  }
}
