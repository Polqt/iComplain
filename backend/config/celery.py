import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('icomplain')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Scheduled tasks can be added here using the @app.on_after_finalize.connect decorator
app.conf.beat_schedule = {
    "auto-escalate-sla": {
        "task": "apps.tickets.tasks.auto_escalate_tickets",
        "schedule": crontab(minute="*/30") # Run every 30 minutes
    },
    "daily-summary-report": {
        "task": "apps.tickets.tasks.send_daily_summary",
        "schedule": crontab(hour=8, minute=0) # Run daily at 8:00 AM
    },
    "weekly-performance-review": {
        "task": "apps.tickets.tasks.send_weekly_report",
        "schedule": crontab(hour=9, minute=0, day_of_week=1)
    }
}