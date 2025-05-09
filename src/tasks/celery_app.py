import eventlet
eventlet.monkey_patch()

from celery import Celery
from back_hot.src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "back_hot.src.tasks.tasks",
    ]
)