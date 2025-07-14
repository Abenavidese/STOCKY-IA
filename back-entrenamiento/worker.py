from celery_config import celery_app

# Importa todas las tareas en el directorio 'tasks'
import services.tasks.train_model
