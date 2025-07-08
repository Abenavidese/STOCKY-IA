# backend-modelo/tasks/train_model.py

from celery_config import celery_app
from services.training import train_with_darts
import requests

@celery_app.task(name="tasks.train_model.train_model_task")
def train_model_task(user_id: str, csv_path: str, task_id: str):
    try:
        print(f"Iniciando entrenamiento para {user_id} con archivo {csv_path}")
        model_path, model_id = train_with_darts(user_id, csv_path)

        if not model_path or not model_id:
            print("[ERROR] El modelo no fue generado.")
            return

        notify_url = "http://localhost:8001/internal/notify_model_ready"
        data = {
            "user_id": user_id,
            "model_id": model_id,
            "model_path": model_path
        }

        try:
            response = requests.post(notify_url, json=data)
            print(f"Notificación enviada: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[ERROR] Falló la notificación al backend general: {e}")

    except Exception as e:
        print(f"[ERROR] Entrenamiento fallido en Celery: {e}")
