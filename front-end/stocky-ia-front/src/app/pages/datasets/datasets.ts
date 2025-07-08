import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-datasets',
  imports: [CommonModule, FormsModule],
  templateUrl: './datasets.html',
  styleUrl: './datasets.scss'
})
export class Datasets {

  selectedFile: File | null = null;

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      console.log('Archivo seleccionado:', this.selectedFile);
    }
  }

  onUpload() {
    if (this.selectedFile) {
      console.log('Subiendo archivo:', this.selectedFile.name);
      // Aquí puedes agregar lógica para subir el archivo al backend
    }
  }
}