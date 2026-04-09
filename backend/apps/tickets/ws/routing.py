
from django.urls import re_path

from .consumers import TicketNotificationConsumer


websocket_urlpatterns = [
    # Accept both `/ws/tickets` and `/ws/tickets/`, with or without leading slash.
    re_path(r"^/?ws/tickets/?$", TicketNotificationConsumer.as_asgi()),
]
