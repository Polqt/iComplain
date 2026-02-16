from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class EmailNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE)
    event = models.CharField(max_length=100)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='SENT') # SENT, FAILED


class InAppNotification(models.Model):
    TYPE_CHOICES = [
        ("info", "Info"),
        ("success", "Success"),
        ("warning", "Warning"),
        ("error", "Error"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inapp_notifications")
    ticket = models.ForeignKey("tickets.Ticket", on_delete=models.CASCADE, null=True, blank=True, related_name="inapp_notifications")
    event = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="info")
    read = models.BooleanField(default=False)
    action_url = models.CharField(max_length=500, blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]