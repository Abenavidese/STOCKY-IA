from fastapi import APIRouter, Body, HTTPException
from services.tasks.train_model import train_model_task

train_status_router = APIRouter()

@train_status_router.post("/train-from-uploads")
def entrenar_desde_csv(payload: dict = Body(...)):
    user_id = payload.get("user_id")
    file_path = payload.get("file_path")

    if not user_id or not file_path:
        raise HTTPException(status_code=400, detail="user_id y file_path son requeridos")

    # Lanza la tarea Celery
    task = train_model_task.apply_async(args=[file_path, user_id], queue="training-queue")

    return {
        "task_id": task.id,
        "user_id": user_id,
        "file_path": file_path
    }
