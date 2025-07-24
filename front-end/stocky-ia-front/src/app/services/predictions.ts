import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Predictions {
  id: number;
  user_id: string;
  fecha: string;
  product_id: number;
  product_name: string;
  category_id: number;
  category_name: string;
  prediccion: number;
  venta_anterior: number;
  price_usd: number;
  created_at: string;
  historico: {
    rolling_mean_sale_7_t0: number;
    weekly_day_avg_t0: number;
    rolling_mean_sale_3_t0: number;
    max_last_5_t0: number;
    prev_day_sale_t0: number;
    rolling_mean_sale_7_t1: number;
    weekly_day_avg_t1: number;
    rolling_mean_sale_3_t1: number;
    max_last_5_t1: number;
    prev_day_sale_t1: number;
    rolling_mean_sale_7_t2: number;
    weekly_day_avg_t2: number;
    rolling_mean_sale_3_t2: number;
    max_last_5_t2: number;
    prev_day_sale_t2: number;
    rolling_mean_sale_7_t3: number;
    weekly_day_avg_t3: number;
    rolling_mean_sale_3_t3: number;
    max_last_5_t3: number;
    prev_day_sale_t3: number;
    rolling_mean_sale_7_t4: number;
    weekly_day_avg_t4: number;
    rolling_mean_sale_3_t4: number;
    max_last_5_t4: number;
    prev_day_sale_t4: number;
    target_y: number;
    product_id: number;
    dt_target: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class PredictionsService {
  private baseUrl = 'http://127.0.0.1:8002/api/internal/predictions/int_predictions';

  constructor(private http: HttpClient) {}

  /**
   * Obtiene las predicciones de un usuario.
   * @param userId ID único del usuario
   */
  getPredictionsByUser(userId: string): Observable<Predictions[]> {
    return this.http.get<Predictions[]>(`${this.baseUrl}/${userId}`);
  }
}
