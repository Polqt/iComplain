from ninja import Router
from ninja.security import SessionAuth

from .models import EmailNotification
from .schemas import EmailNotificationCreateSchema, EmailNotificationSchema

# Create your views here.
router = Router(auth=SessionAuth())


@router.get('/', response=EmailNotificationSchema)
def list_email_notifications(request):
    return EmailNotification.objects.all()

@router.post('/', response=EmailNotificationSchema)
def create_email_notification(request, payload: EmailNotificationCreateSchema):
    notification = EmailNotification.objects.create(
        user_id=payload.user,
        ticket_id=payload.ticket,
        event=payload.event,
        status=payload.status
    )
    
    return notification