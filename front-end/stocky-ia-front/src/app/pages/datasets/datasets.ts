import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-datasets',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './datasets.html',
  styleUrls: ['./datasets.scss']
})
export class Datasets {
  selectedFile: File | null = null;
  previewData: string[][] = [];

  productId: string = '';
  fecha: string = '';
  resultado: string = '';

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      console.log('Archivo seleccionado:', this.selectedFile);

      const reader = new FileReader();
      reader.onload = (e: ProgressEvent<FileReader>) => {
        const text = e.target?.result as string;
        const lines = text.split('\n').slice(0, 5);
        this.previewData = lines.map(line => line.split(','));
        console.log('Vista previa del CSV:', this.previewData);
      };
      reader.readAsText(this.selectedFile);
    }
  }

  onUpload() {
    if (this.selectedFile) {
      console.log('Subiendo archivo:', this.selectedFile.name);
      // Aquí irá la lógica real de subida al backend cuando se implemente
    }
  }

  onPredict() {
    if (this.productId && this.fecha) {
      this.resultado = `Predicción generada para el producto ${this.productId} en la fecha ${this.fecha}`;
      console.log('Ejecutando predicción con:', this.productId, this.fecha);
    } else {
      this.resultado = 'Por favor, ingresa ID y fecha válidos.';
    }
  }
}
