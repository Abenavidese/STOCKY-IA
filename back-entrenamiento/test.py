# test_send_task.py

from celery_config import celery_app

celery_app.send_task(
    "tasks.train_model.train_model_task",
    args=["test-user", "uploads/test.csv", "task-123"]
)
