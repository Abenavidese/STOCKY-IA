import sys
import os
from fastapi import APIRouter
from .internal.internal_getter import obtener_csvs_disponibles
from services.tasks.train_model import train_model_task
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # agregar el path actual

router = APIRouter()

@router.post("/train-from-uploads")
def entrenar_desde_csvs():
    archivos = obtener_csvs_disponibles()
    resultados = []

    for path in archivos:
        task = train_model_task.apply_async(args=[path, "123"], queue="training-queue")
        resultados.append({"file": path, "task_id": task.id})

    return {"launched_tasks": resultados}
