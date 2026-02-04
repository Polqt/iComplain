from django.db import models
from django.conf import settings

# Create your models here.
class EmailNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE)
    event = models.CharField(max_length=100)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='SENT') # SENT, FAILED