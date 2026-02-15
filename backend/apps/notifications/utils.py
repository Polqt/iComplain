from django.utils import timezone

from .models import InAppNotification

def serialize_inapp_notification(n: InAppNotification) -> dict:
    ts = timezone.localtime(n.created_at).isoformat() if n.created_at else ""
    return {
        "id": str(n.id),
        "type": n.notification_type,
        "title": n.title,
        "message": n.message,
        "timestamp": ts,
        "read": n.read,
        "actionUrl": n.action_url or None,
        "actionLabel": None,
    }

def create_in_app_notification(
    user,
    *,
    ticket=None,
    event: str,
    title: str,
    message: str,
    notification_type: str = "info",
    action_url: str = "",
):
    InAppNotification.objects.create(
        user=user,
        ticket=ticket,
        event=event,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url or "",
    )

STATUS_LABELS = {
    "pending": ("Ticket updated", "Your ticket status was set to Pending.", "info"),
    "in_progress": ("Ticket in progress", "Your ticket is now being worked on.", "info"),
    "resolved": ("Ticket resolved", 'Your ticket "{title}" has been marked as resolved.', "success"),
    "closed": ("Ticket closed", 'Your ticket "{title}" has been closed.', "success"),
}


def notify_ticket_status_change(student, ticket_id: int, ticket_title: str, new_status: str):
    action_url = f"/tickets/{ticket_id}"
    tpl = STATUS_LABELS.get(
        new_status,
        ("Status updated", f"Your ticket status was changed to {new_status}.", "info"),
    )
    title, message_tpl, ntype = tpl
    message = message_tpl.format(title=ticket_title)
    create_in_app_notification(
        user=student,
        ticket=None,
        event=f"status_{new_status}",
        title=title,
        message=message,
        notification_type=ntype,
        action_url=action_url,
    )


def notify_ticket_comment(recipient_user, ticket_id: int, ticket_title: str, message_preview: str):
    create_in_app_notification(
        user=recipient_user,
        ticket=None,
        event="comment_added",
        title="New comment on your ticket",
        message=f'"{ticket_title}": {message_preview}',
        notification_type="info",
        action_url=f"/tickets/{ticket_id}",
    )
