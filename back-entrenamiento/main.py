# backend-modelo/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.internal.internal_controller import router as internal_router
from api.train import router as train_router
from api.internal.prediction import router as prediction_router
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

app.include_router(train_router, prefix="/api/train", tags=["Training"])
app.include_router(prediction_router, prefix="/api/prediction", tags=["Prediction"])


@app.get("/health")
def health_check():
    return {"status": "modelo-backend-ok"}
