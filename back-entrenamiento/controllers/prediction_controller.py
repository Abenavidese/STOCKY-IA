# backend-modelo/controllers/prediction_controller.py

from schemas.prediction_request import PredictRequest

def handle_prediction(request: PredictRequest):
    # Temporal: devuelve una respuesta simulada para pruebas
    return [
        {
            "product_id": request.product_id or 999,
            "fecha": request.fecha or "2025-07-09",
            "prediccion": 123.45
        }
    ]
