import { Component, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Prediction } from '../../services/prediction'
import { MarkdownPipe } from '../../pipe/markdown.pipe';

@Component({
  selector: 'app-datasets',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule, MarkdownPipe],
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

  userEmailPrefix: string | null = null;

  predictions: Prediction[] = [];
  fechasUnicas: string[] = [];
  productosPorFecha: Prediction[] = [];

  fechaSeleccionada: string = '';
  productoSeleccionado: number | null = null;

  minimized = false;

toggleMinimize() {
  this.minimized = !this.minimized;
}

  ngOnInit(): void {
    // Obtener UID al iniciar el componente
    const uid = this.authService.getUid();
    if (uid) {
      this.productId = uid; // <-- Aquí se asigna globalmente
      console.log('UID asignado globalmente a productId:', this.productId);
      this.loadPredictions(uid);
    } else {
      console.warn('No se encontró UID del usuario en AuthService.');
    }
    this.userEmailPrefix = this.authService.getUserEmailPrefix();
  }

  // Propiedades para el menú flotante (chat)
  posX = 100;
  posY = 100;
  isDragging = false;
  offsetX = 0;
  offsetY = 0;

  // Propiedades del chat
  chatMessage: string = '';
  // Ahora mensajes como objetos { sender: 'user'|'assistant'|'system', text: string }
  messages: { sender: string; text: string }[] = [];

  constructor(private http: HttpClient, private authService: AuthService, private predictionService: Prediction) {}

  loadPredictions(userId: string) {
    this.predictionService.getPredictions(userId).subscribe(data => {
      this.predictions = data;

      // Extraer fechas únicas para el selector
      const fechasSet = new Set(this.predictions.map(p => p.fecha));
      this.fechasUnicas = Array.from(fechasSet).sort();

      // Limpiar producto y fecha seleccionados al recargar
      this.fechaSeleccionada = '';
      this.productoSeleccionado = null;
      this.productosPorFecha = [];
    });
  }

  onFechaChange(event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    this.fechaSeleccionada = selectElement.value;
    this.productosPorFecha = this.predictions.filter(p => p.fecha === this.fechaSeleccionada);
    this.productoSeleccionado = null;
  }

  onProductoChange(event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    this.productoSeleccionado = Number(selectElement.value);
  }

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

  sendChatMessage() {
    if (!this.productId || !this.fechaSeleccionada || !this.productoSeleccionado) {
      alert('Por favor selecciona usuario, fecha y producto antes de enviar el mensaje.');
      return;
    }
    if (!this.chatMessage.trim()) {
      alert('Escribe un mensaje antes de enviar.');
      return;
    }

    // Buscar la predicción/contexto que corresponde a la fecha y producto seleccionados
    const contexto = this.predictions.find(
      p => p.fecha === this.fechaSeleccionada && p.product_id === this.productoSeleccionado
    );

    if (!contexto) {
      alert('No se encontró la predicción seleccionada.');
      return;
    }

    // Preparar payload para el backend chat
    const payload = {
      userId: this.productId,
      username: this.userEmailPrefix || '',  // o cualquier otro username que tengas
      productId: contexto.product_id,
      productName: contexto.product_name,
      fecha: this.fechaSeleccionada,
      message: this.chatMessage,
      contexto: {
        productName: contexto.product_name,
        categoryId: contexto.category_id,
        categoryName: contexto.category_name,
        prediccion: contexto.prediccion,
        ventaAnterior: contexto.venta_anterior,
        priceUsd: contexto.price_usd,
        createdAt: contexto.created_at,
        historico: contexto.historico,
      }
    };

    const chatApiUrl = 'http://localhost:8001/api/chat/message'; // Ajusta URL si necesario

    // Enviar mensaje al backend chat
    this.http.post<any>(chatApiUrl, payload).subscribe({
      next: (res) => {
        console.log('Respuesta del chat:', res);

        // Guardar respuesta en el array de mensajes para mostrar en UI
        this.messages.push({ sender: 'user', text: this.chatMessage });
        this.messages.push({ sender: 'assistant', text: res.response });

        // Limpiar input
        this.chatMessage = '';
      },
      error: (err) => {
        console.error('Error enviando mensaje al chat:', err);
        alert('Error al enviar mensaje al chat');
      }
    });
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
    const uid = this.authService.getUid();
    if (!uid) {
      console.error('No se encontró UID del usuario.');
      return;
    }

    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('user_id', uid);
      console.log('Subiendo archivo con user_id:', uid);

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
      this.http.get<any>(`http://127.0.0.1:8000/api/tasks/task-status/${taskId}`)
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
