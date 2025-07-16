import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Home } from './pages/home/home';
import { Datasets } from './pages/datasets/datasets';
import { authGuard } from './auth.guard'; 
export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },

  {
    path: 'home',
    component: Home,
    canActivate: [authGuard], 
    children: [
      { path: '', redirectTo: 'inicio', pathMatch: 'full' },
      { path: 'datasets', component: Datasets },
      {
        path: 'inicio',
        loadComponent: () =>
          import('./pages/home/inicio').then((m) => m.Inicio),
      },
      {
        path: 'politicas',
        loadComponent: () =>
          import('./pages/politicas/politicas').then((m) => m.Politicas),
      }
    ]
  }
];
