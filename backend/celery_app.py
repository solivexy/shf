import os
from celery import Celery
from config.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "shf_celery",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["workers.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    broker_connection_retry_on_startup=True,
    beat_schedule={
        "scheduled-daily-watchlist-scan": {
            "task": "workers.tasks.run_scheduled_watchlist_scan",
            "schedule": 3600.0,  # runs every hour by default or cron
        }
    }
)
