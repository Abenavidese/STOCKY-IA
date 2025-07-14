# backend-modelo/celery_config.py
from celery import Celery

celery_app = Celery(
    "backend_modelo_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.task_routes = {
    "services.tasks.train_model.train_model_task": {"queue": "training-queue"}
}
