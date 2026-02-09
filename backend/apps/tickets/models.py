from django.conf import settings
from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.db import transaction


# TABLE FOR CATEGORIES
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

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
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='tickets')
    priority = models.ForeignKey(TicketPriority, on_delete=models.PROTECT, related_name='tickets')

    building = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
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
class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(default=timezone.now)


#TABLE FOR TICKET STATUS HISTORY
class TicketStatusHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    changed_at = models.DateTimeField(default=timezone.now)


# TABLE FOR TICKET FEEDBACK
class TicketFeedback(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='feedback')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comments = models.TextField(null=True, blank=True, max_length=2000)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Feedback for {self.ticket.ticket_number} by {self.student}"


# TABLE FOR TICKET ATTACHMENTS    
class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments_tickets', null=True, blank=True)
    comment = models.ForeignKey(TicketComment, on_delete=models.CASCADE, related_name='attachments_comments', null=True, blank=True)
    feedback = models.ForeignKey(TicketFeedback, on_delete=models.CASCADE, related_name='attachments_feedback', null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to='ticket_attachments/')
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(ticket__isnull=False, comment__isnull=True, feedback__isnull=True)
                    | models.Q(ticket__isnull=True, comment__isnull=False, feedback__isnull=True)
                    | models.Q(ticket__isnull=True, comment__isnull=True, feedback__isnull=False)
                ),
                name="exactly_one_parent",
            ),
        ]
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def clean(self):
        fields = [self.ticket, self.comment, self.feedback]
        if sum(f is not None for f in fields) != 1:
            raise ValidationError("Exactly one of ticket, comment, or feedback must be set for an attachment.")