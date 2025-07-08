from core.celery_config import celery_app

# Importa las tareas para que Celery las registre
import services.tasks

if __name__ == "__main__":
    celery_app.worker_main()
