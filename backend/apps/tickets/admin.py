from django.contrib import admin
from .models import Ticket, Category, TicketPriority


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']


@admin.register(TicketPriority)
class TicketPriorityAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'color_code']
    list_editable = ['level', 'color_code']
    ordering = ['level']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'title', 'status', 'priority', 'category', 'student', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['ticket_number', 'title', 'description', 'student__username', 'building', 'room_name']
    readonly_fields = ['ticket_number', 'created_at', 'updated_at']

    fieldsets = (
        ('Ticket Information', {
            'fields': ('ticket_number', 'title', 'description', 'student')
        }),
        ('Classification', {
            'fields': ('category', 'priority', 'status')
        }),
        ('Location', {
            'fields': ('building', 'room_name')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )