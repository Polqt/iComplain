from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from ninja import Router
from ninja.security import SessionAuth

from .schemas import TicketCommentSchema, TicketCommentUpdateSchema, TicketCreateSchema, TicketSchema, TicketUpdateSchema, TicketFeedbackSchema, TicketFeedbackCreateSchema, TicketFeedbackUpdateSchema 
from .models import Category, Ticket, TicketComment, TicketPriority, TicketFeedback

router = Router(auth=SessionAuth())

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}!')
            return redirect('ticket_list')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'tickets/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('login_user')

# Ticket Views
@router.get("/", response=list[TicketSchema])
def ticket_list(request):
    if request.user.is_staff:
        all_tickets = Ticket.objects.select_related('category', 'priority', 'student').all()
    else:
        all_tickets = Ticket.objects.select_related('category', 'priority').filter(student=request.user)
    
    return all_tickets
    


@router.get("/{id}", response=TicketSchema)
def ticket_detail(id: int):
    ticket = get_object_or_404(Ticket, id=id)
    return ticket
    


@router.post("/", response=TicketSchema)
def create_ticket(request, ticket: TicketCreateSchema):
    category = Category.objects.get(id=ticket.category)
    priority = TicketPriority.objects.get(id=ticket.priority)
    ticket = Ticket.objects.create(
        title=ticket.title,
        description=ticket.description,
        student=request.user,
        category=category,
        priority=priority,
        building=ticket.building,
        room_name=ticket.room_name,
        status='pending'
    )
    return ticket

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
    return ticket

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
    return 204

# Ticket Comments Views

@router.post("/{id}", response=TicketCommentSchema)
def create_comment(request, ticket_id: int, payload: TicketCreateSchema):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.status == 'closed':
        return {"detail": "Cannot add comments to a closed ticket."}, 400
    
    comment = TicketComment.objects.create(
        ticket=ticket,
        user=request.user,
        message=payload.message
    )
    
    comment.save()
    return 201, comment


@router.post("/{id}/comments/{comment_id}", response=TicketCommentSchema)    
def edit_comment(request, comment_id: int, payload: TicketCommentUpdateSchema):
    ticket = get_object_or_404(Ticket, id=id)
    comment = get_object_or_404(TicketComment, id=comment_id, ticket=ticket)
    
    
    if comment.user != request.user:
        return {"detail": "You do not have permission to edit this comment."}, 403
    
    if payload.message is not None:
        comment.message = payload.message
    
    comment.save()
    return 200, comment


@router.delete("/{id}/comments/{comment_id}", response={204: None, 400: dict})    
def delete_comment(request, id: int, comment_id: int):
    ticket = get_object_or_404(Ticket, id=id)
    comment = get_object_or_404(TicketComment, id=comment_id, ticket=ticket)
    
    if comment.user != request.user:
        return {"detail": "You do not have permission to delete this comment."}, 403
    
    comment.delete()
    return redirect('ticket_detail', id=id)

    
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
def create_feedback(request, ticket_id: int, payload: TicketFeedbackCreateSchema):
    ticket = get_object_or_404(Ticket, id=ticket_id)

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
    return redirect('ticket_detail', id=id)