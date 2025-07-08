import os
from fastapi import UploadFile
from uuid import uuid4
from core.config import UPLOAD_DIR

def save_csv_file(file: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path
