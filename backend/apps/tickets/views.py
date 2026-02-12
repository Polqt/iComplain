from typing import List
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta


from ninja import File, Router, UploadedFile
from ninja.security import SessionAuth

from .validation import validate_file

from .schemas import TicketCommentCreateSchema, TicketCommentSchema, TicketCommentUpdateSchema, TicketCreateSchema, TicketSchema, TicketUpdateSchema, TicketFeedbackSchema, TicketFeedbackCreateSchema, TicketFeedbackUpdateSchema 
from .models import Category, Ticket, TicketAttachment, TicketComment, TicketPriority, TicketFeedback

router = Router(auth=SessionAuth())

@router.get("/expensive-data", response=dict)
def expensive_data(request):
    cache_key = "expensive_data"
    data = cache.get(cache_key)
    if not data:
        data = ...
        cache.set(cache_key, data, timeout=300)
    return data

# Ticket Views
@router.get("/", response=list[TicketSchema])
def ticket_list(request):
    if request.user.is_staff:
        return Ticket.objects.select_related('category', 'priority', 'student').all()
    else:
        return Ticket.objects.select_related('category', 'priority', 'student').filter(student=request.user)
    

@router.get("/{id}", response=TicketSchema)
def ticket_detail(request, id: int):
    ticket = get_object_or_404(Ticket, id=id)
    return TicketSchema.from_orm(ticket)
    

@router.post("/", response=TicketSchema)
def create_ticket(request, ticket: TicketCreateSchema, attachment: UploadedFile = File(None)):
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
    
    return TicketSchema.from_orm(ticket_obj)

@router.put("/{id}", response=TicketSchema)
def update_ticket(request, id: int, payload: TicketUpdateSchema):
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
        ticket.status = payload.status

    ticket.updated_at = timezone.now()
    ticket.save()
    return TicketSchema.from_orm(ticket)

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


@router.post("/{id}/comments/{comment_id}", response=TicketCommentSchema)    
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
    return redirect('ticket_list')

    
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

    # Auto-close ticket upon feedback
    ticket.status = 'closed'
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
    return redirect('ticket_list')
