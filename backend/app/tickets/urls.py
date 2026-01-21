from django.urls import path
from . import views

urlpatterns = [
    #REMOVE AUTH SINCE PRIO IS TICKET CRUD
    # Authentication
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    
    # Ticket CRUD
    path('', views.ticket_list, name='ticket_list'),
    path('<int:id>/', views.ticket_detail, name='ticket_detail'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('<int:id>/update/', views.update_ticket, name='update_ticket'),
    path('<int:id>/delete/', views.delete_ticket, name='delete_ticket'),
]