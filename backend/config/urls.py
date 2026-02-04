from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from apps.tickets.views import router as tickets_router
from apps.notifications.views import router as notifications_router
from apps.users.views import router as user_router

api = NinjaAPI()

api.add_router("tickets/", tickets_router)
api.add_router("notifications/", notifications_router)
api.add_router("/user/", user_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
