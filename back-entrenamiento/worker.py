# backend-modelo/worker.py

from celery_config import celery_app

# 🔥 Esta línea es CRUCIAL para registrar las tareas al iniciar Celery
import tasks.train_model
