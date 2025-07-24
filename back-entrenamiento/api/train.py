import sys
import os
from fastapi import APIRouter, Body
from services.tasks.train_model import train_model_task
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # agregar el path actual

router = APIRouter()

@router.post("/train-from-uploads")
def entrenar_desde_csvs(payload: dict = Body(...)):
    """
    Lanza la tarea de entrenamiento usando el archivo CSV y el user_id
    enviados por el backend general.
    """
    user_id = payload.get("user_id")
    file_path = payload.get("file_path")

    if not user_id or not file_path:
        return {"error": "user_id y file_path son requeridos"}

    # Lanzar la tarea con Celery
    task = train_model_task.apply_async(args=[file_path, user_id], queue="training-queue")

    return {
        "launched_task": {
            "file": file_path,
            "task_id": task.id,
            "user_id": user_id
        }
    }
