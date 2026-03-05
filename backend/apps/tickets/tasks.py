import logging
from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Ticket
from apps.notifications.utils import create_in_app_notification
from django.db.models import Count

logger = logging.getLogger(__name__)


@shared_task(name="apps.tickets.tasks.auto_escalate_tickets")
def auto_escalate_tickets():

    # Example: mark or notify on tickets pending > 24h (configurable via settings later)
    threshold = timezone.now() - timezone.timedelta(hours=24)
    active = Ticket.objects.filter(archived_at__isnull=True)
    stale = active.filter(status="pending", created_at__lt=threshold)
    count = stale.count()
    if count:
        logger.info("auto_escalate_tickets: %s ticket(s) pending over 24h", count)
        # Optional: create in-app notifications for staff, or bump priority
    return {"escalated_count": 0, "stale_pending_count": count}


@shared_task(name="apps.tickets.tasks.send_daily_summary")
def send_daily_summary():

    User = get_user_model()
    today = timezone.now().date()
    active = Ticket.objects.filter(archived_at__isnull=True)
    created_today = active.filter(created_at__date=today).count()
    resolved_today = active.filter(status="resolved", updated_at__date=today).count()
    pending = active.filter(status="pending").count()

    message = (
        f"Daily summary: {created_today} created, {resolved_today} resolved, {pending} pending."
    )
    for admin in User.objects.filter(is_staff=True):
        try:
            create_in_app_notification(
                user=admin,
                ticket_id=None,
                event="daily_summary",
                title="Daily ticket summary",
                message=message,
                notification_type="info",
                action_url="",
            )
        except Exception as e:
            logger.warning("send_daily_summary notification failed for user %s: %s", admin.id, e)

    logger.info("send_daily_summary: %s", message)
    return {"created_today": created_today, "resolved_today": resolved_today, "pending": pending}


@shared_task(name="apps.tickets.tasks.send_weekly_report")
def send_weekly_report():
    User = get_user_model()
    week_start = timezone.now() - timezone.timedelta(days=7)
    active = Ticket.objects.filter(archived_at__isnull=True)
    created = active.filter(created_at__gte=week_start).count()
    resolved = active.filter(status="resolved", updated_at__gte=week_start).count()
    by_status = dict(
        active.filter(created_at__gte=week_start)
        .values("status")
        .annotate(count=Count("id"))
        .values_list("status", "count")
    )

    message = (
        f"Weekly report: {created} created, {resolved} resolved. By status: {by_status}"
    )
    for admin in User.objects.filter(is_staff=True):
        try:
            create_in_app_notification(
                user=admin,
                ticket_id=None,
                event="weekly_report",
                title="Weekly ticket report",
                message=message,
                notification_type="info",
                action_url="",
            )
        except Exception as e:
            logger.warning("send_weekly_report notification failed for user %s: %s", admin.id, e)

    logger.info("send_weekly_report: %s", message)
    return {"created": created, "resolved": resolved, "by_status": by_status}
