import os
from fastapi import UploadFile
from core.config import UPLOAD_DIR
import shutil

def save_csv_file(file: UploadFile, user_id: str) -> str:
    """
    Guarda el CSV en UPLOAD_DIR con el nombre user_id.csv.
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}.csv")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path
