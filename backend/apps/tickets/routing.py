
from django.urls import re_path
from .consumers import TicketNotificationConsumer


websocket_urlpatterns = [
    re_path(r'ws/tickets/$', TicketNotificationConsumer.as_asgi()),
]