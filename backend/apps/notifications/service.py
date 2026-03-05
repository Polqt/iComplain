import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


class NotificationService:
    def send_notification(self, user_email: str, subject: str, message: str, fail_silently: bool = True):
        if not getattr(settings, "EMAIL_HOST_USER", None):
            if not fail_silently:
                logger.warning("NotificationService.send_notification: EMAIL_HOST_USER not set")
            return 0
        try:
            return send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
                fail_silently=fail_silently,
            )
        except Exception as e:
            logger.warning("NotificationService.send_notification failed: %s", e)
            return 0