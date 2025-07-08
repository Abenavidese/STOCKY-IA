# backend-modelo/schemas/prediction_request.py

from pydantic import BaseModel
from typing import Optional

class PredictRequest(BaseModel):
    user_id: str
    model_id: str
    fecha: Optional[str] = None   # formato: YYYY-MM-DD
    product_id: Optional[int] = None
