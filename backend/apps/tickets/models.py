from django.db import models
from django.contrib.auth.models import User
from django.db import transaction


# TABLE FOR CATEGORIES
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# TABLE FOR TICKET_PRIORITIES
class TicketPriority(models.Model):
    name = models.CharField(max_length=20, unique=True)
    level = models.IntegerField(unique=True)  # 1=Low, 2=Medium, 3=High, 4=Urgent
    color_code = models.CharField(max_length=7, default='#6b7280')  # Hex color for UI

    class Meta:
        verbose_name_plural = 'Ticket Priorities'
        ordering = ['level']

    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    ticket_number = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Foreign Keys for Category and Priority
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='tickets')
    priority = models.ForeignKey(TicketPriority, on_delete=models.PROTECT, related_name='tickets')

    building = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Fix race condition with transaction atomic
        if not self.ticket_number:
            with transaction.atomic():
                last_ticket = Ticket.objects.select_for_update().order_by('id').last()
                if last_ticket and last_ticket.id:
                    new_id = last_ticket.id + 1
                else:
                    new_id = 1
                self.ticket_number = f"TKT-{new_id:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_number} - {self.title}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['student', 'status']),
        ]

#TABLE FOR TICKET COMMENTS

#TABLE FOR TICKET STATUS HISTORY