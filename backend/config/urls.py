from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from apps.tickets.views import login_user, logout_user, router as tickets_router

api = NinjaAPI()

api.add_router("tickets/", tickets_router)
# api.add_router("/user/", user_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
]
