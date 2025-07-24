from pydantic import BaseModel
from typing import Optional, Dict, Any

class Historico(BaseModel):
    rolling_mean_sale_7_t0: float
    weekly_day_avg_t0: float
    rolling_mean_sale_3_t0: float
    max_last_5_t0: float
    prev_day_sale_t0: float
    rolling_mean_sale_7_t1: float
    weekly_day_avg_t1: float
    rolling_mean_sale_3_t1: float
    max_last_5_t1: float
    prev_day_sale_t1: float
    rolling_mean_sale_7_t2: float
    weekly_day_avg_t2: float
    rolling_mean_sale_3_t2: float
    max_last_5_t2: float
    prev_day_sale_t2: float
    rolling_mean_sale_7_t3: float
    weekly_day_avg_t3: float
    rolling_mean_sale_3_t3: float
    max_last_5_t3: float
    prev_day_sale_t3: float
    rolling_mean_sale_7_t4: float
    weekly_day_avg_t4: float
    rolling_mean_sale_3_t4: float
    max_last_5_t4: float
    prev_day_sale_t4: float
    target_y: float
    product_id: int
    dt_target: str

class ContextoPrediccion(BaseModel):
    productName: str
    categoryId: int
    categoryName: str
    prediccion: float
    ventaAnterior: float
    priceUsd: float
    createdAt: str
    historico: Historico

class ChatMessage(BaseModel):
    userId: str
    username: Optional[str] = None  # Si tienes el username
    productId: int
    fecha: str
    message: str
    contexto: ContextoPrediccion