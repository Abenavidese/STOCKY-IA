from core.celery_config import celery_app
import time
import random   

@celery_app.task
def train_model(file_path: str, user_id: str):
    print(f"Entrenando modelo para el archivo: {file_path}, usuario: {user_id}")
    time.sleep(random.randint(15, 30)) 
    print(" Entrenamiento finalizado.")
    return {"status": "done", "file": file_path}
