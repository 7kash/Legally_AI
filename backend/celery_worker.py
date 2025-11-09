"""
Celery Worker Entry Point
Start Celery worker for async tasks
"""

from app.tasks.celery_app import celery_app

if __name__ == "__main__":
    celery_app.start()
