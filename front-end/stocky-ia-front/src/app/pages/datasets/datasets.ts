import { Component, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-datasets',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './datasets.html',
  styleUrls: ['./datasets.scss']
})
export class Datasets {
  selectedFile: File | null = null;
  previewData: string[][] = [];
  status: string | null = null;
  result: any = null;

  // Nuevas propiedades para predicción
  productId: string = '';
  productName: string = ''; 
  fecha: string = '';
  resultado: string = '';

  // Propiedades para el menú flotante (chat)
  posX = 100;
  posY = 100;
  isDragging = false;
  offsetX = 0;
  offsetY = 0;

  // Propiedades del chat
  chatMessage: string = '';
  messages: string[] = [];

  constructor(private http: HttpClient) {}

  // Método para manejar el archivo seleccionado
  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];

      const reader = new FileReader();
      reader.onload = (e: ProgressEvent<FileReader>) => {
        const text = e.target?.result as string;
        const lines = text.split('\n').slice(0, 5);
        this.previewData = lines.map(line => line.split(','));
      };
      reader.readAsText(this.selectedFile);
    }
  }

  // Método para cargar el archivo y enviar al backend
  onUpload() {
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('user_id', '2');

      this.http.post<{ task_id: string }>('http://127.0.0.1:8000/api/datasets/upload', formData)
        .subscribe({
          next: (res) => {
            console.log('Archivo subido, task_id:', res.task_id);
            this.status = 'PENDING';
            this.pollTaskStatus(res.task_id);
          },
          error: (err) => {
            console.error('Error al subir archivo:', err);
            this.status = 'FAILURE';
          }
        });
    }
  }

  // Método para hacer la predicción
  onPredict() {
    if (this.productId && this.fecha) {
      this.resultado = `Predicción generada para el producto ${this.productId} en la fecha ${this.fecha}`;
      console.log('Predicción ejecutada:', this.resultado);
    } else {
      this.resultado = 'Por favor, ingresa un ID de producto y una fecha válida.';
    }
  }

  pollTaskStatus(taskId: string) {
    const interval = setInterval(() => {
      this.http.get<any>(`http://127.0.0.1:8000/api/task-status/${taskId}`)
        .subscribe({
          next: (res) => {
            this.status = res.status;
            this.result = res.result;
            if (res.status === 'SUCCESS' || res.status === 'FAILURE') {
              clearInterval(interval);
            }
          },
          error: (err) => {
            console.error('Error al consultar estado:', err);
            clearInterval(interval);
            this.status = 'FAILURE';
          }
        });
    }, 3000);
  }

  sendMessage() {
    if (this.productId.trim() && this.productName.trim() && this.chatMessage.trim()) {
      const messageData = {
        productId: this.productId,
        productName: this.productName, // Enviar el nombre del producto
        message: this.chatMessage,
      };

      this.messages.push(`Producto ${this.productName} (ID: ${this.productId}): ${this.chatMessage}`);

      this.chatMessage = '';

      this.sendToApi(messageData);
    } else {
      this.messages.push('Por favor, ingresa todos los campos (ID, nombre del producto y mensaje).');
    }
  }

  // Función para enviar los datos del mensaje a la API
  sendToApi(messageData: any) {
    this.http.post('http://127.0.0.1:8000/api/chat', messageData)
      .subscribe({
        next: (response) => {
          console.log('Mensaje enviado:', response);
        },
        error: (err) => {
          console.error('Error al enviar el mensaje:', err);
        }
      });
  }

  // Métodos para hacer el chat movible
  startDrag(event: MouseEvent | TouchEvent) {
    this.isDragging = true;
    if (event instanceof MouseEvent) {
      this.offsetX = event.clientX - this.posX;
      this.offsetY = event.clientY - this.posY;
    } else if (event instanceof TouchEvent) {
      this.offsetX = event.touches[0].clientX - this.posX;
      this.offsetY = event.touches[0].clientY - this.posY;
    }
  }

  @HostListener('document:mousemove', ['$event'])
  @HostListener('document:touchmove', ['$event'])
  onDrag(event: MouseEvent | TouchEvent) {
    if (!this.isDragging) return;
    if (event instanceof MouseEvent) {
      this.posX = event.clientX - this.offsetX;
      this.posY = event.clientY - this.offsetY;
    } else if (event instanceof TouchEvent) {
      this.posX = event.touches[0].clientX - this.offsetX;
      this.posY = event.touches[0].clientY - this.offsetY;
    }
  }

  @HostListener('document:mouseup')
  @HostListener('document:touchend')
  stopDrag() {
    this.isDragging = false;
  }

  // Función para cerrar el chat
  toggleChat() {
    const chatElement = document.querySelector('.chat');
    if (chatElement) {
      chatElement.classList.toggle('hidden');
    }
  }
}
