from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'ticket_number', 'title', 'status', 'priority', 'student', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['ticket_number', 'title', 'description', 'student__username']
    readonly_fields = ['ticket_number', 'created_at', 'updated_at']