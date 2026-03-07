import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


class EmailService:
    def send_notification(self, to: str, subject: str, body: str, fail_silently: bool = True) -> int:
        if not getattr(settings, "EMAIL_HOST_USER", None):
            if not fail_silently:
                logger.warning("EmailService: EMAIL_HOST_USER not configured, skipping send")
            return 0
        try:
            return send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                recipient_list=[to],
                fail_silently=fail_silently,
            )
        except Exception as e:
            logger.warning("EmailService.send_notification failed for %s: %s", to, e)
            return 0