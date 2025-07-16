from core.celery_config import celery_app
import time
import random   
import os
@celery_app.task
def train_model(file_path: str, user_id: str):
    print(f"Entrenando modelo para el archivo: {file_path}, usuario: {user_id}")
    time.sleep(random.randint(15, 30)) 
    filename = os.path.basename(file_path)
    print(" Entrenamiento finalizado.")
    return {
    "status": "done",
    "file": f"uploads/{filename}"
}

