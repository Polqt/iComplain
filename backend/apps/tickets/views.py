from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from ninja import File, Form, Router, UploadedFile
from ninja.security import SessionAuth
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .utils import (
    format_date,
    format_timestamp,
    history_action_for_status_change,
    map_priority_for_history,
    map_status_for_history,
)
from .validation import validate_file
from apps.notifications.utils import notify_ticket_status_change, notify_ticket_comment

from .schemas import (
    CategorySchema,
    TicketAdminUpdateSchema,
    TicketCommentCreateSchema,
    TicketCommentSchema,
    TicketCommentUpdateSchema,
    TicketCreateSchema,
    TicketHistoryItemSchema,
    TicketPrioritySchema,
    TicketSchema,
    TicketUpdateSchema,
    TicketFeedbackSchema,
    TicketFeedbackCreateSchema,
    TicketFeedbackUpdateSchema,
)
from .models import Category, Ticket, TicketAttachment, TicketComment, TicketPriority, TicketFeedback, TicketStatusHistory

router = Router(auth=SessionAuth())
User = get_user_model()
channel_layer = get_channel_layer()


@router.get("/expensive-data", response=dict)
def expensive_data(request):
    cache_key = "expensive_data"
    data = cache.get(cache_key)
    if not data:
        data = ...
        cache.set(cache_key, data, timeout=300)
    return data

@router.get("/categories", response=list[CategorySchema])
def get_categories(request):
    return Category.objects.all()

@router.get("/priorities", response=list[TicketPrioritySchema])
def get_priorities(request):
    return TicketPriority.objects.all()

@router.get("/community", response=list[TicketSchema])
def community_tickets(request):
    qs = Ticket.objects.select_related("category", "priority", "student") \
            .prefetch_related('attachments_tickets') \
            .order_by('-created_at')
    return [TicketSchema.from_orm(ticket) for ticket in qs]

# Ticket Views
@router.get("/", response=list[TicketSchema])
def ticket_list(request):
    qs = Ticket.objects.select_related(
        'category', 'priority', 'student'
    ).prefetch_related('attachments_tickets')
    if request.user.is_staff:
        return [TicketSchema.from_orm(ticket, request) for ticket in qs]
    return [TicketSchema.from_orm(ticket, request) for ticket in qs.filter(student=request.user)]
    

@router.get("/history", response=list[TicketHistoryItemSchema])
def ticket_history(request):
    status_history_qs = TicketStatusHistory.objects.select_related("changed_by").order_by("changed_at")
    comments_qs = TicketComment.objects.select_related("user").order_by("created_at")
    base = Ticket.objects.select_related("category", "priority", "student").prefetch_related(
        Prefetch("status_history", queryset=status_history_qs),
        Prefetch("comments", queryset=comments_qs),
    )
    if request.user.is_staff:
        tickets = base.all()
    else:
        tickets = base.filter(student=request.user)

    events = []
    for ticket in tickets:
        # Created
        events.append({
            "at": ticket.created_at,
            "id": f"created-{ticket.id}-{ticket.created_at.isoformat()}",
            "ticket": ticket,
            "action": "created",
            "description": "Ticket created",
            "event_status": "pending",
        })
        # Status history
        for h in ticket.status_history.all():
            action = history_action_for_status_change(h.old_status, h.new_status)
            events.append({
                "at": h.changed_at,
                "id": f"status-{h.id}",
                "ticket": ticket,
                "action": action,
                "new_status": h.new_status,
                "description": (
                    f"Status changed from {map_status_for_history(h.old_status)} "
                    f"to {map_status_for_history(h.new_status)}"
                ),
                "event_status": h.new_status,
            })
        # Comments
        for c in ticket.comments.all():
            events.append({
                "at": c.created_at,
                "id": f"comment-{c.id}",
                "ticket": ticket,
                "action": "commented",
                "description": f"Comment: {c.message[:100]}{'…' if len(c.message) > 100 else ''}",
            })

    events.sort(key=lambda e: e["at"], reverse=True)
    status_change_actions = ("updated", "resolved", "closed", "reopened")
    out = []
    for e in events:
        t = e["ticket"]
        priority_name = t.priority.name if t.priority else ""
        category_name = t.category.name if t.category else None
        event_status = e.get("event_status", t.status)
        if e["action"] in status_change_actions:
            event_status = map_status_for_history(e["new_status"])
        elif e["action"] == "created":
            event_status = map_status_for_history("pending")
        else:
            event_status = map_status_for_history(t.status)
        out.append(TicketHistoryItemSchema(
            id=e["id"],
            ticketPk=t.id,
            ticketId=t.ticket_number,
            title=t.title,
            action=e["action"],
            description=e["description"],
            timestamp=format_timestamp(e["at"]),
            date=format_date(e["at"]),
            status=map_status_for_history(event_status),
            priority=map_priority_for_history(priority_name),
            category=category_name,
        ))
    return out

@router.get("/{ticket_id}", response={200: TicketSchema, 404: dict})
def ticket_detail(request, ticket_id: str):
    if ticket_id.isdigit():
        ticket = get_object_or_404(Ticket, id=int(ticket_id))
    else:
        ticket = get_object_or_404(Ticket, ticket_number=ticket_id)
    if ticket.student != request.user and not request.user.is_staff:
        return {"detail": "Not found."}, 404
    return 200, TicketSchema.from_orm(ticket, request)

@router.post("/", response=TicketSchema)
def create_ticket(request, ticket: TicketCreateSchema = Form(...), attachment: UploadedFile = File(None)):
    category = Category.objects.get(id=ticket.category)
    priority = TicketPriority.objects.get(name="Medium")
    ticket_obj = Ticket.objects.create(
        title=ticket.title,
        description=ticket.description,
        student=request.user,
        category=category,
        priority=priority,
        building=ticket.building,
        room_name=ticket.room_name,
        status='pending'
    )
    
    if attachment:
        validate_file(attachment)
        TicketAttachment.objects.create(
        ticket=ticket_obj,
            uploaded_by=request.user,
            file_path=attachment,
            file_type=attachment.content_type,
        )
    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_ticket_update",
            "data": {
                "action": "created",  # or "updated", "commented", etc.
                "ticket_id": ticket_obj.id,
                "message": "A ticket was created",
            }
        }
    )
    
    ticket_obj.refresh_from_db()
    ticket_obj = Ticket.objects.prefetch_related('attachments_tickets').get(pk=ticket_obj.id)
    return TicketSchema.from_orm(ticket_obj, request)

@router.put("/{id}", response=TicketSchema)
def update_ticket(request, id: int, payload: TicketUpdateSchema = Form(...), attachment: UploadedFile = File(None)):
    ticket = get_object_or_404(Ticket, id=id)

    # Permission check
    if ticket.student != request.user and not request.user.is_staff:
        return {"detail": "You do not have permission to edit this ticket."}, 403

    # Students can only edit tickets with "pending" status
    if not request.user.is_staff and ticket.status != 'pending':
        return {"detail": "You cannot edit tickets that are being processed by admin."}, 400

    if payload.title is not None:
        ticket.title = payload.title
    if payload.description is not None:
        ticket.description = payload.description
    if payload.category is not None:
        ticket.category = Category.objects.get(id=payload.category)
    if payload.priority is not None:
        ticket.priority = TicketPriority.objects.get(id=payload.priority)
    if payload.building is not None:
        ticket.building = payload.building
    if payload.room_name is not None:
        ticket.room_name = payload.room_name
    if payload.status is not None:
        old_status = ticket.status
        if old_status != payload.status:
            TicketStatusHistory.objects.create(
                ticket=ticket,
                old_status=old_status,
                new_status=payload.status,
                changed_by=request.user,
                changed_at=timezone.now(),
            )
            notify_ticket_status_change(student=ticket.student, ticket_id=ticket.id, ticket_number=ticket.ticket_number, ticket_title=ticket.title, new_status=payload.status)
        ticket.status = payload.status

    ticket.updated_at = timezone.now()
    ticket.save()
    
    if attachment:
        validate_file(attachment)
        existing = ticket.attachments_tickets.first()
        if existing:
            # Delete old file and replace
            existing.file_path.delete(save=False)
            existing.file_path.save(attachment.name, attachment, save=False)
            existing.file_type = attachment.content_type
            existing.save()
        else:
            TicketAttachment.objects.create(
                ticket=ticket,
                uploaded_by=request.user,
                file_path=attachment,
                file_type=attachment.content_type,
            )
        
    ticket = Ticket.objects.prefetch_related('attachments_tickets').get(pk=ticket.id)
    return TicketSchema.from_orm(ticket, request)

@router.patch("/{id}/admin", response=TicketSchema)
def admin_update_ticket(request, id: int, payload: TicketAdminUpdateSchema):
    if not request.user.is_staff:
        return {"detail": "You do not have permission to perform this action."}, 403
    
    ticket = get_object_or_404(Ticket, id=id)
    
    if payload.status is not None:
        old_status = ticket.status
        if old_status != payload.status:
            TicketStatusHistory.objects.create(
                ticket=ticket,
                old_status=old_status,
                new_status=payload.status,
                changed_by=request.user,
                changed_at=timezone.now(),
            )
            notify_ticket_status_change(student=ticket.student, ticket_id=ticket.id, ticket_number=ticket.ticket_number, ticket_title=ticket.title, new_status=payload.status)
        ticket.status = payload.status
        
    if payload.priority is not None:
        ticket.priority = TicketPriority.objects.get(id=payload.priority)
    
    ticket.updated_at = timezone.now()
    ticket.save()
    
    ticket = Ticket.objects.prefetch_related('attachments_tickets').get(pk=ticket.id)
    return 200, TicketSchema.from_orm(ticket, request)
    

@router.delete("/{id}", response={204: None})
def delete_ticket(request, id: int):
    ticket = get_object_or_404(Ticket, id=id)
    
    # Permission check
    if ticket.student != request.user and not request.user.is_staff:
        return {"detail": "You do not have permission to delete this ticket."}, 403
    
    # Students can only delete tickets with "pending" status
    if not request.user.is_staff and ticket.status != 'pending':
        return {"detail": "You cannot delete tickets that are being processed by admin."}, 400

    ticket.delete()
    return 204, None

# Ticket Comments Views
@router.get("/{id}/comments", response=list[TicketCommentSchema])
def get_comments(request, id: int):
    ticket = get_object_or_404(Ticket, id=id)
    comments = TicketComment.objects.select_related('user').filter(ticket=ticket).order_by('created_at')
    return [TicketCommentSchema.from_orm(comment) for comment in comments]

@router.post("/{id}/comments", response=TicketCommentSchema)
def create_comment(request, id: int, payload: TicketCommentCreateSchema, attachment: UploadedFile = File(None)):
    ticket = get_object_or_404(Ticket, id=id)

    if ticket.status == 'closed':
        return {"detail": "Cannot add comments to a closed ticket."}, 400
    
    comment = TicketComment.objects.create(
        ticket=ticket,
        user=request.user,
        message=payload.message
    )
    preview = (payload.message or "")[:80] + ("…" if len(payload.message or "") > 80 else "")
    if ticket.student != request.user:
        notify_ticket_comment(recipient_user=ticket.student, ticket_id=ticket.id, ticket_number=ticket.ticket_number, ticket_title=ticket.title, message_preview=preview)
    else:
        for staff_user in User.objects.filter(is_staff=True).exclude(pk=request.user.pk):
            notify_ticket_comment(recipient_user=staff_user, ticket_id=ticket.id, ticket_number=ticket.ticket_number, ticket_title=ticket.title, message_preview=preview)
    if attachment:
        validate_file(attachment)
        TicketAttachment.objects.create(
            comment=comment,
            uploaded_by=request.user,
            file_path=attachment,
            file_type=attachment.content_type,
        )
        
    comment.save()
    return TicketCommentSchema.from_orm(comment)


@router.put("/{id}/comments/{comment_id}", response=TicketCommentSchema)    
def edit_comment(request, id: int, comment_id: int, payload: TicketCommentUpdateSchema):
    ticket = get_object_or_404(Ticket, id=id)
    comment = get_object_or_404(TicketComment, id=comment_id, ticket=ticket)
    
    
    if comment.user != request.user:
        return {"detail": "You do not have permission to edit this comment."}, 403
    
    if payload.message is not None:
        comment.message = payload.message
    
    comment.save()
    
    return TicketCommentSchema.from_orm(comment)


@router.delete("/{id}/comments/{comment_id}", response={204: None, 400: dict})    
def delete_comment(request, id: int, comment_id: int):
    ticket = get_object_or_404(Ticket, id=id)
    comment = get_object_or_404(TicketComment, id=comment_id, ticket=ticket)
    
    if comment.user != request.user:
        return {"detail": "You do not have permission to delete this comment."}, 403
    
    comment.delete()
    return 204, None

    
# Ticket Feedback Views
@router.get("/{id}/feedback/", response=TicketFeedbackSchema)
def get_feedback(request, id: int):
    ticket = get_object_or_404(Ticket, id=id)
    # Allow owner or staff to view
    if ticket.student != request.user and not request.user.is_staff:
        return redirect('ticket_list')
    feedback = get_object_or_404(TicketFeedback, ticket=ticket)
    return feedback

@router.post("/{id}/feedback/", response={201: TicketFeedbackSchema, 400: dict})
def create_feedback(request, id: int, payload: TicketFeedbackCreateSchema, attachment: UploadedFile = File(None)):
    ticket = get_object_or_404(Ticket, id=id)

    # Only owner can submit feedback and only for resolved tickets
    if ticket.student != request.user:
        return {"detail": "You do not have permission to submit feedback."}, 403

    if ticket.status != 'resolved':
        return {"detail": "Feedback can only be submitted for resolved tickets."}, 400

    # Only one feedback per ticket
    if hasattr(ticket, 'feedback'):
        return {"detail": "Feedback already submitted for this ticket."}, 400

    feedback = TicketFeedback.objects.create(
        ticket=ticket,
        student=request.user,
        rating=payload.rating,
        comments=payload.comments
    )
    
    if attachment:
        validate_file(attachment)
        TicketAttachment.objects.create(
            feedback=feedback,
            uploaded_by=request.user,
            file_path=attachment,
            file_type=attachment.content_type,
        )

    # Auto-close ticket upon feedback; record status history like update_ticket
    old_status = ticket.status
    if old_status != "closed":
        TicketStatusHistory.objects.create(
            ticket=ticket,
            old_status=old_status,
            new_status="closed",
            changed_by=request.user,
            changed_at=timezone.now(),
        )
    ticket.status = "closed"
    ticket.save()

    return 201, feedback

@router.put("/{id}/feedback/{feedback_id}", response=TicketFeedbackSchema)
def update_feedback(request, id: int, feedback_id: int, payload: TicketFeedbackUpdateSchema):
    ticket = get_object_or_404(Ticket, id=id)
    feedback = get_object_or_404(TicketFeedback, id=feedback_id, ticket=ticket)

    # Only the student who submitted feedback can edit within 24 hours
    if feedback.student != request.user:
        return {"detail": "You do not have permission to edit this feedback."}, 403

    if timezone.now() > feedback.created_at + timedelta(hours=24):
        return {"detail": "Feedback can only be edited within 24 hours of submission."}, 400

    if payload.rating is not None:
        feedback.rating = payload.rating
    if payload.comments is not None:
        feedback.comments = payload.comments

    feedback.save()
    return feedback

@router.delete("/{id}/feedback/{feedback_id}", response={204: None, 400: dict})
def delete_feedback(request, id: int, feedback_id: int):
    ticket = get_object_or_404(Ticket, id=id)
    feedback = get_object_or_404(TicketFeedback, id=feedback_id, ticket=ticket)

    # Only the student who submitted feedback can delete within 24 hours
    if feedback.student != request.user:
        return {"detail": "You do not have permission to delete this feedback."}, 403

    if timezone.now() > feedback.created_at + timedelta(hours=24):
        return {"detail": "Feedback can only be deleted within 24 hours of submission."}, 400

    feedback.delete()
    return 204, None