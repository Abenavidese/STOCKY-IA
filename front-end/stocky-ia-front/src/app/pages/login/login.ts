import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import {
  Auth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
} from '@angular/fire/auth';
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  constructor(private router: Router, private auth: Auth) {}

  // Estados del formulario
  isRegisterMode = false;

  // Campos de login
  loginEmail = '';
  loginPassword = '';

  // Campos de registro
  registerUsername = '';
  registerEmail = '';
  registerPassword = '';

  // Mensaje de error global
  errorMessage = '';

  toggleRegister(register: boolean) {
    this.isRegisterMode = register;
    this.errorMessage = '';
  }

  async login(event: Event) {
    event.preventDefault();
    this.errorMessage = '';

    // Forzar blur en inputs para que Angular marque campos como tocados
    this.forceInputsTouched();

    if (!this.loginEmail || !this.loginPassword) {
      this.errorMessage = 'Por favor completa todos los campos.';
      return;
    }

    try {
      await signInWithEmailAndPassword(this.auth, this.loginEmail, this.loginPassword);
      this.router.navigate(['/home']);
    } catch (error: any) {
      console.error('Firebase error (login):', error.code, error.message);
      this.errorMessage = this.getFirebaseError(error.code);
    }
  }

  async register(event: Event) {
    event.preventDefault();
    this.errorMessage = '';

    this.forceInputsTouched();

    if (!this.registerUsername || !this.registerEmail || !this.registerPassword) {
      this.errorMessage = 'Por favor completa todos los campos.';
      return;
    }

    if (this.registerPassword.length < 6) {
      this.errorMessage = 'La contraseña debe tener al menos 6 caracteres.';
      return;
    }

    try {
      await createUserWithEmailAndPassword(this.auth, this.registerEmail, this.registerPassword);
      alert('Registro exitoso');
      this.toggleRegister(false);
    } catch (error: any) {
      console.error('Firebase error (register):', error.code, error.message);
      this.errorMessage = this.getFirebaseError(error.code);
    }
  }

  private getFirebaseError(code: string): string {
    switch (code) {
      case 'auth/invalid-email':
        return 'El correo no es válido.';
      case 'auth/missing-email':
        return 'Debes ingresar un correo electrónico.';
      case 'auth/user-not-found':
        return 'Usuario no registrado.';
      case 'auth/wrong-password':
      case 'auth/invalid-credential':
        return 'Usuario o contraseña incorrectos.';
      case 'auth/email-already-in-use':
        return 'Este correo ya está registrado.';
      case 'auth/weak-password':
        return 'La contraseña debe tener al menos 6 caracteres.';
      case 'auth/missing-password':
        return 'Debes ingresar una contraseña.';
      case 'auth/too-many-requests':
        return 'Demasiados intentos fallidos. Intenta más tarde.';
      case 'auth/internal-error':
        return 'Error interno. Verifica tu conexión.';
      default:
        return `Error inesperado: ${code}`;
    }
  }

  private forceInputsTouched() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach((input) => {
      input.dispatchEvent(new Event('blur'));
    });
  }


}