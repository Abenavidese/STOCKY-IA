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

  // Propiedades para predicción
  productId: string = ''; // Este será tu user_id
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

  // --- MÉTODO onPredict() ACTUALIZADO ---
  onPredict() {
    // Usaremos this.productId como el user_id
    if (this.productId && this.fecha) {
      this.resultado = 'Generando y descargando reporte...'; // Mensaje de espera para el usuario

      const userId = this.productId;
      const reportDate = this.fecha;
      const backendUrl = 'http://127.0.0.1:8000'; // URL de tu Backend General

      this.http.get(`${backendUrl}/api/report/download/${userId}/${reportDate}`, {
        responseType: 'blob' // MUY IMPORTANTE: para recibir un archivo binario
      }).subscribe({
        next: (blob) => {
          // 1. Crear un enlace <a> en memoria
          const a = document.createElement('a');
          const objectUrl = URL.createObjectURL(blob);
          
          // 2. Apuntar el enlace al archivo Blob y darle un nombre de descarga
          a.href = objectUrl;
          a.download = `reporte_${userId}_${reportDate}.pdf`;
          
          // 3. Simular un clic en el enlace para iniciar la descarga
          a.click();
          
          // 4. Limpiar la URL del objeto para liberar memoria
          URL.revokeObjectURL(objectUrl);

          this.resultado = 'Reporte descargado con éxito.';
          console.log('Descarga completada.');
        },
        error: (err) => {
          console.error('Error al descargar el reporte:', err);
          // Intenta leer el mensaje de error específico del backend
          const reader = new FileReader();
          reader.onload = () => {
            try {
              const errorObj = JSON.parse(reader.result as string);
              this.resultado = `Error: ${errorObj.detail || 'Ocurrió un error en el servidor.'}`;
            } catch (e) {
              this.resultado = `Error al procesar la respuesta del servidor. Código: ${err.status}`;
            }
          };
          reader.readAsText(err.error);
        }
      });

    } else {
      this.resultado = 'Por favor, ingresa un ID de usuario y una fecha válida.';
    }
  }

  // --- El resto de tus métodos (sin cambios) ---

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

  onUpload() {
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('user_id', '2'); // O usa this.productId si aplica
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
        productName: this.productName,
        message: this.chatMessage,
      };
      this.messages.push(`Producto ${this.productName} (ID: ${this.productId}): ${this.chatMessage}`);
      this.chatMessage = '';
      this.sendToApi(messageData);
    } else {
      this.messages.push('Por favor, ingresa todos los campos (ID, nombre del producto y mensaje).');
    }
  }

  sendToApi(messageData: any) {
    this.http.post('http://127.0.0.1:8000/api/chat', messageData)
      .subscribe({
        next: (response) => console.log('Mensaje enviado:', response),
        error: (err) => console.error('Error al enviar el mensaje:', err)
      });
  }

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

  toggleChat() {
    const chatElement = document.querySelector('.chat');
    if (chatElement) {
      chatElement.classList.toggle('hidden');
    }
  }
}
