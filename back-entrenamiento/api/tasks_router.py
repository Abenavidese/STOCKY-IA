from fastapi import APIRouter
from celery.result import AsyncResult
from celery_config import celery_app

tasks_router = APIRouter()

@tasks_router.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }
