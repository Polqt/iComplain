from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from ninja import NinjaAPI
from config import settings

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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
