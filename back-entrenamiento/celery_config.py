# backend-modelo/celery_config.py
from celery import Celery
#python -m celery -A worker.celery_app worker --loglevel=info -Q training-queue --pool=solo
celery_app = Celery(
    "backend_entrenamiento_services_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.task_routes = {
    "services.tasks.train_model.train_model_task": {"queue": "training-queue"}
}
