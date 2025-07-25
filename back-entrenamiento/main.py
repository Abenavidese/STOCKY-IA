# backend-modelo/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.internal.internal_controller import router as internal_router
from api.train import router as train_router
from api.internal.internal_predictions import router as internal_predictions_router
from api.internal.prediction import router as prediction_router
from api.tasks_router import tasks_router
from api.train_status_router import train_status_router
from api.analytics_router import analytics_router
app = FastAPI(title="Backend del Modelo de IA")

# Habilita CORS si el backend general o frontend hacen llamadas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # cámbialo por dominios seguros en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta los endpoints internos
app.include_router(internal_router, prefix="/internal")
app.include_router(internal_predictions_router, prefix="/api/internal/predictions", tags=["Internal Predictions"])
app.include_router(train_status_router, prefix="/api/train", tags=["Train Status"])
app.include_router(train_router, prefix="/api/train", tags=["Training"])
app.include_router(prediction_router, prefix="/api/prediction", tags=["Prediction"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(analytics_router, prefix="/api/internal", tags=["Analytics"])


@app.get("/health")
def health_check():
    return {"status": "modelo-backend-ok"}
