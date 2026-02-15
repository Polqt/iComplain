from ninja import Router
from ninja.errors import HttpError
from ninja.security import SessionAuth

from .models import EmailNotification, InAppNotification
from .schemas import (
    EmailNotificationCreateSchema,
    EmailNotificationSchema,
    InAppNotificationSchema,
    InAppNotificationMarkReadSchema,
)
from .utils import serialize_inapp_notification

router = Router(auth=SessionAuth())


@router.get("/inapp/", response=list[InAppNotificationSchema])
def list_inapp_notifications(request, limit: int = 50):
    qs = InAppNotification.objects.filter(user=request.user).select_related("ticket")[:limit]
    return [serialize_inapp_notification(n) for n in qs]


@router.patch("/inapp/{notification_id}/", response=InAppNotificationSchema)
def mark_inapp_read(request, notification_id: int, payload: InAppNotificationMarkReadSchema):
    n = InAppNotification.objects.filter(user=request.user, id=notification_id).first()
    if not n:
        raise HttpError(404, "Not found.")
    n.read = payload.read
    n.save(update_fields=["read"])
    return serialize_inapp_notification(n)


@router.post("/inapp/mark-all-read/", response={200: dict})
def mark_all_inapp_read(request):
    updated = InAppNotification.objects.filter(user=request.user, read=False).update(read=True)
    return 200, {"marked": updated}


@router.delete("/inapp/{notification_id}/", response={204: None})
def delete_inapp_notification(request, notification_id: int):
    n = InAppNotification.objects.filter(user=request.user, id=notification_id).first()
    if not n:
        raise HttpError(404, "Not found.")
    n.delete()
    return 204, None


@router.get("/", response=list[EmailNotificationSchema])
def list_email_notifications(request):
    return list(EmailNotification.objects.filter(user=request.user))


@router.post("/", response=EmailNotificationSchema)
def create_email_notification(request, payload: EmailNotificationCreateSchema):
    notification = EmailNotification.objects.create(
        user_id=payload.user,
        ticket_id=payload.ticket,
        event=payload.event,
        status=payload.status,
    )
    return notification