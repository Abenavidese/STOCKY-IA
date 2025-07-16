from fastapi import FastAPI
from api.routes_upload import router as upload_router
from core.celery_config import celery_app
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from api.routes_global import router as global_router   
from api.router_download import router as download_router
from api.routes_chat import router as chat_router  # Importa el router del chat
from fastapi.staticfiles import StaticFiles
from api.prediction_router import router as prediction_router
import os
import json
app = FastAPI()

# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(upload_router, prefix="/api/datasets", tags=["Upload"])
app.include_router(global_router, prefix="/api/datasets", tags=["files"])
app.include_router(download_router, prefix="/api/datasets", tags=["download"])
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])  # Incluye la ruta del chat
app.include_router(prediction_router, prefix="/api", tags=["Prediction Reports"])



UPLOAD_DIR = os.path.abspath("uploads")

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")



@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de entrenamiento"}

# Nuevo endpoint: consultar estado de la tarea
@app.get("/api/task-status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result
    }

# Nueva ruta para ver los mensajes guardados en messages.json
@app.get("/api/chat/messages")
async def get_messages():
    try:
        with open('messages.json', 'r') as file:
            messages = json.load(file)
        return {"messages": messages}
    except FileNotFoundError:
        return {"messages": []}  # Devuelve una lista vacía si no existe el archivo

# Nuevo endpoint: consultar estado de la tarea
#@app.get("/api/task-status/{task_id}")
#def get_task_status(task_id: str):
#    result = AsyncResult(task_id, app=celery_app)
#    return {
#        "task_id": task_id,
#        "status": result.status,
#        "result": result.result
#    }
