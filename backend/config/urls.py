from django.contrib import admin
from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from django.urls import path
from django.conf.urls.static import static
from ninja import NinjaAPI
from channels.layers import get_channel_layer
from config import settings

from apps.tickets.views import router as tickets_router
from apps.notifications.views import router as notifications_router
from apps.users.views import router as user_router

api = NinjaAPI()

api.add_router("tickets/", tickets_router)
api.add_router("notifications/", notifications_router)
api.add_router("/user/", user_router)


def healthcheck(_request):
    return JsonResponse({"status": "ok"})


def readiness_check(_request):
    checks = {"database": False, "cache": False, "channels": False}

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = True
    except Exception:
        checks["database"] = False

    try:
        cache.set("healthcheck:ready", "ok", timeout=10)
        checks["cache"] = cache.get("healthcheck:ready") == "ok"
    except Exception:
        checks["cache"] = False

    try:
        checks["channels"] = get_channel_layer() is not None
    except Exception:
        checks["channels"] = False

    all_ok = all(checks.values())
    return JsonResponse(
        {"status": "ready" if all_ok else "degraded", "checks": checks},
        status=200 if all_ok else 503,
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path("health/", healthcheck),
    path("health/ready", readiness_check),
    path("api/", api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
