from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from apps.users.api import router as users_router

api = NinjaAPI()
api.add_router("/users/", users_router)

@api.get("/health")
def health_check(request):
    return {"status": "ok"}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

