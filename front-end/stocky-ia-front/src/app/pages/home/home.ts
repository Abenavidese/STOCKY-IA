import { Component } from '@angular/core';
import { Sidebar } from './sidebar/sidebar';
import { Topbar } from './topbar/topbar';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [Sidebar, Topbar],
  templateUrl: './home.html',
  styleUrls: ['./home.scss']
})
export class Home {}
