from fastapi import APIRouter, UploadFile, Form
from services.utils import save_csv_file
from services.tasks import train_model
from schemas.upload_schema import UploadResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile, user_id: str = Form(...)):
    file_path = save_csv_file(file)
    task = train_model.delay(file_path, user_id)
    return {"task_id": task.id}
