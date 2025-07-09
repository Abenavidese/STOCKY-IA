import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  constructor(private router: Router) {}

  isRegisterMode = false;

  toggleRegister(register: boolean) {
    this.isRegisterMode = register;
  }

  login(event: Event) {
    event.preventDefault();
    this.router.navigate(['/home']);
  }

  register(event: Event) {
    event.preventDefault();
    alert('Registro exitoso (aquí puedes integrar lógica)');
    this.toggleRegister(false);
  }
}