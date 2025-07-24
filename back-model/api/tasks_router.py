from fastapi import APIRouter, HTTPException
import httpx  # Cliente HTTP asíncrono

tasks_router = APIRouter()

MODEL_BACKEND_URL = "http://127.0.0.1:8002"  # Backend de entrenamiento

@tasks_router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """
    Consulta el estado de una tarea al backend de entrenamiento (8002).
    """
    try:
        url = f"{MODEL_BACKEND_URL}/api/tasks/task-status/{task_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo obtener el estado de la tarea: {e}")
