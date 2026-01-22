from django.db import models
from django.contrib.auth.models import User


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    CATEGORY_CHOICES = [
        ('facilities', 'Facilities'),
        ('academic', 'Academic'),
        ('technical', 'Technical'),
        ('administrative', 'Administrative'),
        ('other', 'Other'),
    ]
    
    ticket_number = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    building = models.CharField(max_length=100, default='Unknown')
    room_name = models.CharField(max_length=100, default='Unknown')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            # Get the last ticket to generate the next number
            last_ticket = Ticket.objects.all().order_by('id').last()
            if last_ticket and last_ticket.id:
                new_id = last_ticket.id + 1
            else:
                new_id = 1
            self.ticket_number = f"TKT-{new_id:05d}"  # Formats as TKT-00001, TKT-00002, etc.
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.ticket_number} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']