from fastapi import APIRouter, UploadFile, Form, HTTPException
from services.utils import save_csv_file
from schemas.upload_schema import UploadResponse
import httpx

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile, user_id: str = Form(...)):
    file_path = save_csv_file(file, user_id)  # Guarda el archivo como {user_id}.csv

    try:
        notify_url = "http://localhost:8002/api/train/train-from-uploads"
        payload = {"user_id": user_id, "file_path": file_path}
        async with httpx.AsyncClient() as client:
            response = await client.post(notify_url, json=payload)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            response_data = response.json()

        task_id = response_data.get("task_id")  # <-- Task ID real de Celery
        if not task_id:
            raise HTTPException(status_code=500, detail="No se recibió task_id del backend de entrenamiento")

        print(f"[NOTIFY] Notificación enviada: {response.status_code}")
        print(f"[NOTIFY] Respuesta: {response_data}")

    except Exception as e:
        print(f"[ERROR] No se pudo notificar: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "task_id": task_id,
        "user_id": user_id,
        "file_path": file_path
    }
