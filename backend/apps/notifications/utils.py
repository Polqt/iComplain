import logging
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

from .models import InAppNotification

logger = logging.getLogger(__name__)


def serialize_inapp_notification(n: InAppNotification) -> dict:
    ts = timezone.localtime(n.created_at).isoformat() if n.created_at else ""
    action_url = None
    if n.ticket_id:
        ticket_number = getattr(n.ticket, "ticket_number", None) if n.ticket else None
        if ticket_number:
            action_url = f"/tickets/{ticket_number}"
        else:
            action_url = n.action_url or None
    return {
        "id": str(n.id),
        "type": n.notification_type,
        "title": n.title,
        "message": n.message,
        "timestamp": ts,
        "read": n.read,
        "actionUrl": action_url,
        "actionLabel": None,
    }

def create_in_app_notification(
    user,
    *,
    ticket_id: int | None = None,
    event: str,
    title: str,
    message: str,
    notification_type: str = "info",
    action_url: str = "",
):
    notification = InAppNotification.objects.create(
        user=user,
        ticket_id=ticket_id,
        event=event,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url or "",
    )

    try:
        channel_layer = get_channel_layer()
        if channel_layer:
            ts = timezone.localtime(notification.created_at).isoformat() if notification.created_at else ""
            notification_data = {
                "id": str(notification.id),
                "type": notification.notification_type,
                "title": notification.title,
                "message": notification.message,
                "timestamp": ts,
                "read": notification.read,
                "actionUrl": action_url or None,
                "actionLabel": None,
            }
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "send_notification",
                    "data": {
                        "type": "new_notification",
                        "notification": notification_data,
                    },
                },
            )
    except Exception as e:
        logger.warning("WebSocket broadcast failed: %s", e)

STATUS_LABELS = {
    "pending": ("Ticket updated", 'Your ticket "{title}" status was set to Pending.', "info"),
    "in_progress": ("Ticket in progress", 'Your ticket "{title}" is now being worked on.', "info"),
    "resolved": ("Ticket resolved", 'Your ticket "{title}" has been marked as resolved.', "success"),
    "closed": ("Ticket closed", 'Your ticket "{title}" has been closed.', "success"),
}


def notify_ticket_status_change(
    *,
    student,
    ticket_id: int,
    ticket_number: str,
    ticket_title: str,
    new_status: str,
):
    action_url = f"/tickets/{ticket_number}"
    tpl = STATUS_LABELS.get(
        new_status,
        ("Status updated", f"Your ticket status was changed to {new_status}.", "info"),
    )
    title, message_tpl, ntype = tpl
    message = message_tpl.format(title=ticket_title)
    create_in_app_notification(
        user=student,
        ticket_id=ticket_id,
        event=f"status_{new_status}",
        title=title,
        message=message,
        notification_type=ntype,
        action_url=action_url,
    )


def notify_ticket_created(
    *,
    ticket_id: int,
    ticket_number: str,
    ticket_title: str,
    student_name: str,
):
    User = get_user_model()
    for admin_user in User.objects.filter(is_staff=True):
        create_in_app_notification(
            user=admin_user,
            ticket_id=ticket_id,
            event="ticket_created",
            title="New ticket submitted",
            message=f'{student_name} submitted: "{ticket_title}"',
            notification_type="info",
            action_url=f"/tickets/{ticket_number}",
        )


def notify_ticket_comment(
    *,
    recipient_user,
    ticket_id: int,
    ticket_number: str,
    ticket_title: str,
    message_preview: str,
):
    create_in_app_notification(
        user=recipient_user,
        ticket_id=ticket_id,
        event="comment_added",
        title="New comment on your ticket",
        message=f'"{ticket_title}": {message_preview}',
        notification_type="info",
        action_url=f"/tickets/{ticket_number}",
    )
