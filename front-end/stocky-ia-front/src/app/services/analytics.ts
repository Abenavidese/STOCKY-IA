import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface AnalyticsResponse {
  ventas_por_categoria: { [key: string]: number };
  top_productos: { [key: string]: number };
  productos_menos_consumidos: { [key: string]: number };
  ventas_tiempo: { fecha: string; ventas_usd: number }[];
  ventas_totales_usd: number;
  ventas_promedio_dia: number;
  producto_top: string;
  distribucion_precios: {
    count: number;
    mean: number;
    std: number;
    min: number;
    '25%': number;
    '50%': number;
    '75%': number;
    max: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private baseUrl = 'http://127.0.0.1:8002/api/internal/analytics';

  constructor(private http: HttpClient) {}

  getAnalyticsByUser(userId: string): Observable<AnalyticsResponse> {
    return this.http.get<AnalyticsResponse>(`${this.baseUrl}/${userId}`);
  }
}
