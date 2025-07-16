from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/files/download")
def download_file(path: str):
    full_path = os.path.abspath(path)

    # Verificar que esté dentro del directorio 'uploads'
    uploads_dir = os.path.abspath("uploads")
    if not full_path.startswith(uploads_dir):
        raise HTTPException(status_code=400, detail="Ruta no permitida")

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return FileResponse(full_path, media_type="text/csv", filename=os.path.basename(full_path))
