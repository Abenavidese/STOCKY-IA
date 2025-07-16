from celery_config import celery_app
from services.training import train_lstm_model

@celery_app.task(name="services.tasks.train_model.train_model_task")
def train_model_task(csv_path: str, user_id: str):
    try:
        print(f"[TASK] Iniciando entrenamiento con archivo {csv_path} y usuario {user_id}")
        model_path, scaler_path, model_id = train_lstm_model(user_id, csv_path)

        if not model_path or not model_id:
            print("[ERROR] El modelo no fue generado.")
            return {"status": "error", "message": "Entrenamiento fallido"}

        print(f"[SUCCESS] Entrenamiento completo: modelo {model_id} guardado en {model_path}")
        return {
            "status": "ok",
            "model_path": model_path,
            "scaler_path": scaler_path, 
            "model_id": model_id
        }

    except Exception as e:
        print(f"[ERROR] Entrenamiento fallido en Celery: {e}")
        return {"status": "error", "message": str(e)}
