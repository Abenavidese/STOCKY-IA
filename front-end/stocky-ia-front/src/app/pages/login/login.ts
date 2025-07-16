import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {

  email: string = ''
  password: string = ''

  constructor(private router: Router, private http: HttpClient) {}

  isRegisterMode = false;

  toggleRegister(register: boolean) {
    this.isRegisterMode = register;
  }

  register(event: Event) {
    event.preventDefault();
    alert('Registro exitoso (aquí puedes integrar lógica)');
    this.toggleRegister(false);
  }

  login(event: Event) {
    event.preventDefault();

    this.http
      .post<{ user_id: string; email: string; username: string }>(
        'http://localhost:8000/user/login',
        { email: this.email }
      )
      .subscribe((response) => {
        localStorage.setItem('userId', response.user_id);
        localStorage.setItem('userEmail', response.email);
        localStorage.setItem('username', response.username);
        this.router.navigate(['/home']);
      });
  }

}