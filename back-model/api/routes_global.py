import os
from fastapi import APIRouter
from typing import List

router = APIRouter()

UPLOAD_DIR = "uploads"  # O donde sea que los guarde

@router.get("/files", response_model=List[str])
def list_uploaded_files():
    files = []
    for root, dirs, filenames in os.walk(UPLOAD_DIR):
        for f in filenames:
            if f.endswith(".csv"):
                files.append(os.path.join(root, f))
    return files
