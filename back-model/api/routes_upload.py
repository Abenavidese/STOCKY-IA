from fastapi import APIRouter, UploadFile
from services.utils import save_csv_file
import uuid
from schemas.upload_schema import UploadResponse
import httpx  #  async HTTP client

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile):
    file_path = save_csv_file(file)

    task_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    # Notificación asíncrona al backend de entrenamiento
    try:
        notify_url = "http://localhost:8002/api/train/train-from-uploads"
        async with httpx.AsyncClient() as client:
            response = await client.post(notify_url)
            print(f"[NOTIFY] Notificación enviada: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] No se pudo notificar: {e}")

    return {
        "task_id": task_id,
        "user_id": user_id,
        "file_path": file_path
    }
