import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { Auth } from '@angular/fire/auth';

export const authGuard: CanActivateFn = async () => {
  const auth = inject(Auth);
  const router = inject(Router);

  const user = auth.currentUser;

  if (user) {
    return true;
  } else {
    await router.navigate(['/login']);
    return false;
  }
};
