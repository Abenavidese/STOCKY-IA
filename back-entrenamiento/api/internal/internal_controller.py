# backend-modelo/api/internal_controller.py

from fastapi import APIRouter, HTTPException
from controllers.prediction_controller import handle_prediction
from schemas.prediction_request import PredictRequest

router = APIRouter()

@router.post("/predict")
def predict_demand(request: PredictRequest):
    try:
        result = handle_prediction(request)
        return {"status": "ok", "predictions": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
