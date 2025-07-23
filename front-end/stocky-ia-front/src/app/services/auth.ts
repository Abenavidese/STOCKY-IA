import { Injectable } from '@angular/core';
import { Auth, onAuthStateChanged, User, signOut } from '@angular/fire/auth';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUid: string | null = null;

  constructor(private auth: Auth) {
    onAuthStateChanged(this.auth, (user: User | null) => {
      this.currentUid = user ? user.uid : null;
      console.log('UID actualizado:', this.currentUid);
    });
  }

  getUid(): string | null {
    return this.currentUid;
  }

  async logout() {
    await signOut(this.auth);
  }
}
