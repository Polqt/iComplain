"""
Signals to automatically log ticket activities.
These ensure every important ticket change is recorded without duplication.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Ticket, TicketComment, ActivityLog, TicketStatusHistory


@receiver(post_save, sender=Ticket, dispatch_uid='log_ticket_activity')
def log_ticket_activity(sender, instance, created, **kwargs):
    """
    Log ticket creation or updates.
    Uses pre_save to detect changes to avoid duplicate logging.
    """
    if created:
        ActivityLog.objects.create(
            action='created',
            ticket=instance,
            performed_by=instance.student,  # Created by the student
            description=f"Ticket created: {instance.title}",
            new_value=instance.ticket_number,
        )


@receiver(pre_save, sender=Ticket, dispatch_uid='detect_ticket_changes')
def detect_ticket_changes(sender, instance, **kwargs):
    """
    Detect changes to ticket fields and log them via signals.
    This is called BEFORE the ticket is saved.
    """
    if not instance.pk:
        # New ticket, skip (handled by post_save created flag)
        return
    
    try:
        old_instance = Ticket.objects.get(pk=instance.pk)
    except Ticket.DoesNotExist:
        return
    
    # Check status change
    if old_instance.status != instance.status:
        ActivityLog.objects.create(
            action='status_changed',
            ticket=instance,
            performed_by=getattr(instance, '_changed_by', None),
            description=f"Status changed from {old_instance.get_status_display()} to {instance.get_status_display()}",
            old_value=old_instance.status,
            new_value=instance.status,
        )
        # Mark as resolved if status is resolved
        if instance.status == 'resolved':
            ActivityLog.objects.create(
                action='resolved',
                ticket=instance,
                performed_by=getattr(instance, '_changed_by', None),
                description="Ticket marked as resolved",
                new_value=instance.status,
            )
    
    # Check priority change
    if old_instance.priority_id != instance.priority_id:
        old_priority_name = old_instance.priority.name if old_instance.priority else "None"
        new_priority_name = instance.priority.name if instance.priority else "None"
        ActivityLog.objects.create(
            action='priority_changed',
            ticket=instance,
            performed_by=getattr(instance, '_changed_by', None),
            description=f"Priority changed from {old_priority_name} to {new_priority_name}",
            old_value=old_priority_name,
            new_value=new_priority_name,
        )


@receiver(post_save, sender=TicketComment, dispatch_uid='log_comment_activity')
def log_comment_activity(sender, instance, created, **kwargs):
    """
    Log when a comment is added to a ticket.
    """
    if created:
        is_internal = instance.user.is_staff
        ActivityLog.objects.create(
            action='commented',
            ticket=instance.ticket,
            performed_by=instance.user,
            description=f"{'Internal note' if is_internal else 'Comment'} added by {instance.user.name or instance.user.email}",
            new_value=instance.message[:100],  # First 100 chars
        )


@receiver(post_save, sender=TicketStatusHistory, dispatch_uid='log_status_history')
def log_status_history(sender, instance, created, **kwargs):
    """
    Alternative logging via TicketStatusHistory model.
    Only log if not already logged by pre_save.
    """
    # Check if we already logged this via pre_save
    recent_logs = ActivityLog.objects.filter(
        ticket=instance.ticket,
        action='status_changed',
        created_at__gte=timezone.now() - timezone.timedelta(seconds=5),
    ).count()
    
    if recent_logs == 0:
        # No recent log, create one
        ActivityLog.objects.create(
            action='status_changed',
            ticket=instance.ticket,
            performed_by=instance.changed_by,
            description=f"Status changed from {instance.old_status} to {instance.new_status}",
            old_value=instance.old_status,
            new_value=instance.new_status,
        )
