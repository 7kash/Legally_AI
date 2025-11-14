"""
Celery configuration for background tasks.
"""

from celery import Celery
from .config import settings

# Create Celery app
celery_app = Celery(
    "legally_ai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.analyze_contract"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Optional: Celery Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "cleanup-old-analyses": {
        "task": "cleanup_old_analyses",
        "schedule": 86400.0,  # Run daily (24 hours)
    },
}
