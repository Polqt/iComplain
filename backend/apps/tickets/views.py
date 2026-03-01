from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q, Count, Min, Prefetch
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from ninja import File, Form, Router, UploadedFile
from ninja.security import SessionAuth
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from asyncio.log import logger
from .utils import (
    format_date,
    format_timestamp,
    history_action_for_status_change,
    map_priority_for_history,
    map_status_for_history,
)
from .validation import validate_file
from apps.notifications.utils import notify_ticket_created, notify_ticket_status_change, notify_ticket_comment

from .schemas import (
    CategorySchema,
    DashboardMetricsSchema,
    DashboardStatsSchema,
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
    TicketVolumeDataPointSchema,
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

def _active_tickets():
    return Ticket.objects.filter(archived_at__isnull=True)


PAGE_SIZE_DEFAULT = 50
PAGE_SIZE_MAX = 100


@router.get("/community", response=dict)
def community_tickets(request, limit: int = PAGE_SIZE_DEFAULT, offset: int = 0):
    limit = min(max(1, limit), PAGE_SIZE_MAX)
    offset = max(0, offset)
    qs = _active_tickets().select_related("category", "priority", "student") \
        .prefetch_related('attachments_tickets') \
        .annotate(comments_count=Count('comments')) \
        .order_by('-created_at')
    total = qs.count()
    page = list(qs[offset : offset + limit])
    return {
        "items": [TicketSchema.from_orm(t) for t in page],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


# Ticket Views
@router.get("/", response=dict)
def ticket_list(request, limit: int = PAGE_SIZE_DEFAULT, offset: int = 0):
    limit = min(max(1, limit), PAGE_SIZE_MAX)
    offset = max(0, offset)
    qs = _active_tickets().select_related(
        'category', 'priority', 'student'
    ).prefetch_related('attachments_tickets').annotate(comments_count=Count('comments'))
    if not request.user.is_staff:
        qs = qs.filter(student=request.user)
    total = qs.count()
    page = list(qs[offset : offset + limit])
    return {
        "items": [TicketSchema.from_orm(ticket, request) for ticket in page],
        "total": total,
        "limit": limit,
        "offset": offset,
    }

@router.get("/history", response=list[TicketHistoryItemSchema])
def ticket_history(request):
    status_history_qs = TicketStatusHistory.objects.select_related("changed_by").order_by("changed_at")
    comments_qs = TicketComment.objects.select_related("user").order_by("created_at")
    base = _active_tickets().select_related("category", "priority", "student").prefetch_related(
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
            "performed_by": None,
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
                "performed_by": h.changed_by.full_name if h.changed_by else None,
            })
        # Comments
        for c in ticket.comments.all():
            events.append({
                "at": c.created_at,
                "id": f"comment-{c.id}",
                "ticket": ticket,
                "action": "commented",
                "description": f"Comment: {c.message[:100]}{'…' if len(c.message) > 100 else ''}",
                "performed_by": c.user.full_name if c.user else None,
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
            performedBy=e.get("performed_by"),
        ))
    return out

@router.get("/admin/history", response={200: list[TicketHistoryItemSchema], 403: dict})
def admin_ticket_history(request):
    """Admin-only endpoint to view all ticket history for accountability tracking."""
    if not request.user.is_staff:
        return {"detail": "Not authorized."}, 403
    
    status_history_qs = TicketStatusHistory.objects.select_related("changed_by").order_by("changed_at")
    comments_qs = TicketComment.objects.select_related("user").order_by("created_at")
    tickets = _active_tickets().select_related("category", "priority", "student").prefetch_related(
        Prefetch("status_history", queryset=status_history_qs),
        Prefetch("comments", queryset=comments_qs),
    ).all()

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
            "performed_by": None,
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
                "performed_by": h.changed_by.full_name if h.changed_by else None,
            })
        # Comments
        for c in ticket.comments.all():
            events.append({
                "at": c.created_at,
                "id": f"comment-{c.id}",
                "ticket": ticket,
                "action": "commented",
                "description": f"Comment: {c.message[:100]}{'…' if len(c.message) > 100 else ''}",
                "performed_by": c.user.full_name if c.user else None,
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
            performedBy=e.get("performed_by"),
        ))
    return 200, out

@router.get("/{id}", response={200: TicketSchema, 404: dict})
def ticket_detail(request, id: int):
    ticket = get_object_or_404(_active_tickets().annotate(comments_count=Count('comments')), id=id)
    if ticket.student != request.user and not request.user.is_staff:
        return {"detail": "Not found."}, 404
    return 200, TicketSchema.from_orm(ticket, request)

@router.get("/number/{ticket_number}", response={200: TicketSchema, 404: dict})
def ticket_detail_by_number(request, ticket_number: str):
    ticket = get_object_or_404(_active_tickets().annotate(comments_count=Count('comments')), ticket_number=ticket_number)
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
    # Notify admin users about the new ticket
    try:
        notify_ticket_created(
            ticket_id=ticket_obj.id,
            ticket_number=ticket_obj.ticket_number,
            ticket_title=ticket_obj.title,
            student_name=getattr(request.user, "name", None) or request.user.email,
        )
    except Exception:
        logger.exception("notify_ticket_created failed", extra={"ticket_id": ticket_obj.id})

    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_ticket_update",
            "data": {
                "action": "created",
                "ticket_id": ticket_obj.id,
                "name": getattr(ticket_obj.student, "name", None),
                "avatar": getattr(ticket_obj.student, "avatar", None),
                "message": "A ticket was created",
            }
        }
    )
    
    ticket_obj.refresh_from_db()
    ticket_obj = Ticket.objects.prefetch_related('attachments_tickets').get(pk=ticket_obj.id)
    return TicketSchema.from_orm(ticket_obj, request)

@router.put("/{id}", response=TicketSchema)
def update_ticket(request, id: int, payload: TicketUpdateSchema = Form(...), attachment: UploadedFile = File(None)):
    ticket = get_object_or_404(_active_tickets(), id=id)

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
    
    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_ticket_update",
            "data": {
                "action": "updated",
                "ticket_id": ticket.id,
                "name": getattr(ticket.student, "name", None),
                "avatar": getattr(ticket.student, "avatar", None),
                "message": f"A ticket was updated by {request.user.name}",
            }
        }
    )
        
    ticket = Ticket.objects.prefetch_related('attachments_tickets').get(pk=ticket.id)
    return TicketSchema.from_orm(ticket, request)

@router.patch("/{id}/admin", response=TicketSchema)
def admin_update_ticket(request, id: int, payload: TicketAdminUpdateSchema):
    if not request.user.is_staff:
        return {"detail": "You do not have permission to perform this action."}, 403

    ticket = get_object_or_404(_active_tickets(), id=id)
    
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
    
    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_ticket_update",
            "data": {
                "action": "updated",
                "ticket_id": ticket.id,
                "name": getattr(ticket.student, "name", None),
                "avatar": getattr(ticket.student, "avatar", None),
                "message": f"A ticket was updated to {payload.status}",
            }
        }
    )
    
    ticket = Ticket.objects.prefetch_related('attachments_tickets').get(pk=ticket.id)
    return 200, TicketSchema.from_orm(ticket, request)
    
@router.delete("/{id}", response={204: None})
def delete_ticket(request, id: int):
    ticket = get_object_or_404(_active_tickets(), id=id)

    # Permission check
    if ticket.student != request.user and not request.user.is_staff:
        return {"detail": "You do not have permission to delete this ticket."}, 403

    # Students can only delete tickets with "pending" status
    if not request.user.is_staff and ticket.status != 'pending':
        return {"detail": "You cannot delete tickets that are being processed by admin."}, 400

    # Soft delete: archive ticket instead of hard delete
    ticket.archived_at = timezone.now()
    ticket.save(update_fields=["archived_at"])
    
    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_ticket_update",
            "data": {
                "action": "deleted",
                "ticket_id": ticket.id,
                "name": getattr(ticket.student, "name", None),
                "avatar": getattr(ticket.student, "avatar", None),
                "message": f"A ticket was deleted by {request.user.name}",
            }
        }
    )
    return 204, None


# Ticket Comments Views
@router.get("/{id}/comments", response=list[TicketCommentSchema])
def get_comments(request, id: int):
    ticket = get_object_or_404(_active_tickets(), id=id)
    comments = TicketComment.objects.select_related('user').filter(ticket=ticket).order_by('created_at')
    return [TicketCommentSchema.from_orm(comment) for comment in comments]

@router.post("/{id}/comments", response=TicketCommentSchema)
def create_comment(request, id: int, payload: TicketCommentCreateSchema = Form(...), attachment: UploadedFile = File(None)):
    ticket = get_object_or_404(_active_tickets(), id=id)

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
    
    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_comment_update",
            "data": {
                "type": "comment_created",
                "ticket_id": ticket.id,
                "comment": {
                    "id": comment.id,
                    "ticket_id": ticket.id,
                    "user": {
                        "id": comment.user.id,
                        "email": comment.user.email,
                        "name": getattr(comment.user, "name", None),
                        "avatar": getattr(comment.user, "avatar", None),
                    },
                    "message": comment.message,
                    "created_at": comment.created_at.isoformat(),
                }
            }
        }
    )

    return 200, TicketCommentSchema.model_validate(comment)

@router.put("/{id}/comments/{comment_id}", response=TicketCommentSchema)
def edit_comment(request, id: int, comment_id: int, payload: TicketCommentUpdateSchema = Form(...)):
    ticket = get_object_or_404(_active_tickets(), id=id)
    comment = get_object_or_404(TicketComment, id=comment_id, ticket=ticket)
    
    
    if comment.user != request.user:
        return {"detail": "You do not have permission to edit this comment."}, 403
    
    if payload.message is not None:
        comment.message = payload.message
    
    comment.save()
    
    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_comment_update",
            "data": {
                "type": "comment_updated",
                "ticket_id": ticket.id,
                "comment": {
                    "id": comment.id,
                    "ticket_id": ticket.id,
                    "user": {
                        "id": comment.user.id,
                        "email": comment.user.email,
                        "name": getattr(comment.user, "name", None),
                        "avatar": getattr(comment.user, "avatar", None),
                    },
                    "message": comment.message,
                    "created_at": comment.created_at.isoformat(),
                }
            }
        }
    )
    
    return TicketCommentSchema.from_orm(comment)

@router.delete("/{id}/comments/{comment_id}", response={204: None, 400: dict})
def delete_comment(request, id: int, comment_id: int):
    ticket = get_object_or_404(_active_tickets(), id=id)
    comment = get_object_or_404(TicketComment, id=comment_id, ticket=ticket)
    
    if comment.user != request.user:
        return {"detail": "You do not have permission to delete this comment."}, 403
    
    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_comment_update",
            "data": {
                "type": "comment_deleted",
                "ticket_id": ticket.id,
                "comment": {
                    "id": comment.id,
                    "ticket_id": ticket.id,
                    "user": {
                        "id": comment.user.id,
                        "email": comment.user.email,
                        "name": getattr(comment.user, "name", None),
                        "avatar": getattr(comment.user, "avatar", None),
                    },
                    "message": comment.message,
                    "created_at": comment.created_at.isoformat(),
                }
            }
        }
    )
    
    comment.delete()
    return 204, None

    
# Ticket Feedback Views
@router.get("/{id}/feedback/", response={200: TicketFeedbackSchema, 403: dict, 404: dict})
def get_feedback(request, id: int):
    ticket = get_object_or_404(_active_tickets(), id=id)
    
    # Allow owner or staff to view
    if ticket.student != request.user and not request.user.is_staff:
        return 403, {"detail": "You do not have permission to view this feedback."}
    
    # Check if feedback exists
    if not hasattr(ticket, 'feedback') or ticket.feedback is None:
        return 404, {"detail": "No feedback found for this ticket."}
    return 200, TicketFeedbackSchema.from_orm(ticket.feedback)

@router.post("/{id}/feedback/", response={201: TicketFeedbackSchema, 400: dict, 403: dict})
def create_feedback(request, id: int, payload: TicketFeedbackCreateSchema = Form(...), attachment: UploadedFile = File(None)):
    ticket = get_object_or_404(_active_tickets(), id=id)

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

    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_feedback_update",
            "data": {
                "type": "feedback_created",
                "ticket_id": ticket.id,
                "feedback_id": feedback.id,
            }
        }
    )

    return 201, TicketFeedbackSchema.from_orm(feedback)

@router.put("/{id}/feedback/{feedback_id}", response={200: TicketFeedbackSchema, 400: dict, 403: dict})
def update_feedback(request, id: int, feedback_id: int, payload: TicketFeedbackUpdateSchema):
    ticket = get_object_or_404(_active_tickets(), id=id)
    feedback = get_object_or_404(TicketFeedback, id=feedback_id, ticket=ticket)

    # Only the student who submitted feedback can edit
    if feedback.student != request.user:
        return 403, {"detail": "You do not have permission to edit this feedback."}

    # Must be within 24 hours
    if timezone.now() > feedback.created_at + timedelta(hours=24):
        return 400, {"detail": "Feedback can only be edited within 24 hours of submission."}

    # Update fields
    if payload.rating is not None:
        feedback.rating = payload.rating
    if payload.comments is not None:
        feedback.comments = payload.comments

    feedback.save()
    
    # Send WebSocket update (optional)
    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_feedback_update",
            "data": {
                "type": "feedback_updated",
                "ticket_id": ticket.id,
                "feedback_id": feedback.id,
            }
        }
    )
    
    return 200, TicketFeedbackSchema.from_orm(feedback)

@router.delete("/{id}/feedback/{feedback_id}", response={204: None, 400: dict, 403: dict})
def delete_feedback(request, id: int, feedback_id: int):
    ticket = get_object_or_404(_active_tickets(), id=id)
    feedback = get_object_or_404(TicketFeedback, id=feedback_id, ticket=ticket)

    # Only the student who submitted feedback can delete
    if feedback.student != request.user:
        return 403, {"detail": "You do not have permission to delete this feedback."}

    # Must be within 24 hours
    if timezone.now() > feedback.created_at + timedelta(hours=24):
        return 400, {"detail": "Feedback can only be deleted within 24 hours of submission."}

    # Send WebSocket update before deleting
    async_to_sync(channel_layer.group_send)(
        "ticket_updates",
        {
            "type": "send_feedback_update",
            "data": {
                "type": "feedback_deleted",
                "ticket_id": ticket.id,
                "feedback_id": feedback.id,
            }
        }
    )
    
    feedback.delete()
    return 204, None


@router.get("/stats/dashboard", response=DashboardStatsSchema)
def dashboard_stats(request):
    if not request.user.is_staff:
        return {"detail": "You do not have permission to view this data."}, 403

    now = timezone.now()
    today = now.date()
    last_month_start = (now - timedelta(days=30)).date()
    this_week_start = (now - timedelta(days=7)).date()
    
    # Total Tickets Metrics (exclude archived)
    base = _active_tickets()
    total_tickets = base.count()
    last_month_tickets = base.filter(created_at__date__lt=last_month_start).count()
    
    if last_month_tickets > 0:
        total_change = ((total_tickets - last_month_tickets) / last_month_tickets) * 100
    else:
        total_change = 0
        
    # Resolved Tickets Metrics
    resolved_tickets = base.filter(status='resolved').count()
    last_month_resolved = base.filter(
        status='resolved',
        updated_at__date__lt=last_month_start
    ).count()
    
    
    if last_month_resolved > 0:
        resolved_change = ((resolved_tickets - last_month_resolved) / last_month_resolved) * 100
    else:
        resolved_change = 0
        
    # Pending Tickets Metrics
    pending_tickets = base.filter(status='pending').count()
    last_month_pending = base.filter(
        status='pending',
        updated_at__date__lt=last_month_start
    ).count()
    
    if last_month_pending > 0:
        pending_change = ((pending_tickets - last_month_pending) / last_month_pending) * 100
    else:
        pending_change = 0
        
    # Response time
    tickets_with_staff_comments = base.filter(
        comments__user__is_staff=True,
        created_at__gte=this_week_start
    ).annotate(
        first_staff_comment_time=Min('comments__created_at', filter=Q(comments__user__is_staff=True))
    )
    
    response_times = []
    for ticket in tickets_with_staff_comments:
        if ticket.first_staff_comment_time:
            delta = ticket.first_staff_comment_time - ticket.created_at
            response_times.append(delta.total_seconds() / 3600)
        
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    last_month_tickets_with_comments = base.filter(
        comments__user__is_staff=True,
        created_at__date__lt=last_month_start,
        created_at__date__gte=(last_month_start - timedelta(days=30))
    ).annotate(
        first_staff_comment_time=Min('comments__created_at', filter=Q(comments__user__is_staff=True))
    )
    
    last_month_response_times = []
    for ticket in last_month_tickets_with_comments:
        if ticket.first_staff_comment_time:
            delta = ticket.first_staff_comment_time - ticket.created_at
            last_month_response_times.append(delta.total_seconds() / 3600)
    
    last_month_avg_response = sum(last_month_response_times) / len(last_month_response_times) if last_month_response_times else avg_response_time
    
    metrics = [
        DashboardMetricsSchema(
            title="Total Tickets",
            value=str(total_tickets),
            change=f"+{abs(total_change):.0f}%" if total_change >= 0 else f"-{abs(total_change):.0f}%",
            subtitle="vs last month",
            trend="success" if total_change >= 0 else "error"
        ),
        DashboardMetricsSchema(
            title="Resolved Tickets",
            value=str(resolved_tickets),
            change=f"+{abs(resolved_change):.0f}%" if resolved_change >= 0 else f"-{abs(resolved_change):.0f}%",
            subtitle=f"Last Month {last_month_resolved}",
            trend="success" if resolved_change >= 0 else "error"
        ),
        DashboardMetricsSchema(
            title="Pending Tickets",
            value=str(pending_tickets),
            change=f"+{abs(pending_change):.0f}%" if pending_change >= 0 else f"-{abs(pending_change):.0f}%",
            subtitle=f"Last Month {last_month_pending}",
            trend="error" if pending_change >= 0 else "success"  # More pending = bad
        ),
        DashboardMetricsSchema(
            title="Response Time",
            value=f"{avg_response_time:.1f} hrs" if avg_response_time else "N/A",
            change=f"{(last_month_avg_response / avg_response_time):.1f}x faster" if avg_response_time and last_month_avg_response else "N/A",
            subtitle=f"Last Month {last_month_avg_response:.1f} hrs" if last_month_avg_response else "N/A",
            trend="success" if avg_response_time < last_month_avg_response else "error"
        ),
    ]
    
    volume_data = []
    days = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
    
    for i in range(7):
        day_date = today - timedelta(days=6-i)
        count = base.filter(created_at__date=day_date).count()
        volume_data.append(
            TicketVolumeDataPointSchema(
                day=days[(day_date.weekday() + 1) % 7],
                value=count
            )
        )
    
    status_breakdown = dict(
        base.values('status').annotate(count=Count('id')).values_list('status', 'count')
    )

    category_breakdown = dict(
        base.values('category__name').annotate(count=Count('id')).values_list('category__name', 'count')
    )
    
    return DashboardStatsSchema(
        metrics=metrics,
        volume=volume_data,
        status_breakdown=status_breakdown,
        category_breakdown=category_breakdown,
    )
