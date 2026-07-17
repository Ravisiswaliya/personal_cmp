import os

from celery import Celery

celery = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
)

# celery.autodiscover_task(["app.src.core.celery_tasks"])
import app.src.core.celery_tasks
