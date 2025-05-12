from celery import Celery
from back_hot.src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "back_hot.src.tasks.tasks",
    ]
)