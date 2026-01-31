from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from ninja import Router
from ninja.security import SessionAuth

from .schemas import TicketCommentSchema, TicketCreateSchema, TicketSchema, TicketUpdateSchema, TicketFeedbackSchema, TicketFeedbackCreateSchema, TicketFeedbackUpdateSchema 
from .models import Category, Ticket, TicketPriority, TicketFeedback

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
    


@router.get("/tickets/{id}", response=TicketSchema)
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

# FRANZ WORK ON THIS

@router.put("/tickets/{id}", response=TicketSchema) 
def update_ticket(request, id: int, ticket: TicketUpdateSchema):
    ticket = get_object_or_404(Ticket, id=id)
    
    # Permission check
    if ticket.student != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this ticket.')
        return redirect('ticket_list')
    
    # Students can only edit tickets with "pending" status
    if not request.user.is_staff and ticket.status != 'pending':
        messages.error(request, 'You cannot edit tickets that are being processed by admin.')
        return redirect('ticket_detail', id=ticket.id)
    
    
    # Based the code above create_ticket/ticket_detail/
    # if request.method == 'POST':
    #     if request.user.is_staff:
    #         # Admin can only change priority and status
    #         form = AdminTicketUpdateForm(request.POST, instance=ticket)
    #         if form.is_valid():
    #             form.save()
    #             messages.success(request, 'Ticket updated successfully!')
    #             return redirect('ticket_detail', id=ticket.id)
    #     else:
    #         # Student can edit all fields
    #         form = TicketUpdateForm(request.POST, instance=ticket)
    #         if form.is_valid():
    #             form.save()
    #             messages.success(request, 'Ticket updated successfully!')
    #             return redirect('ticket_detail', id=ticket.id)
    # else:
    #     if request.user.is_staff:
    #         form = AdminTicketUpdateForm(instance=ticket)
    #     else:
    #         form = TicketUpdateForm(instance=ticket)
    
    # context = {
    #     'form': form,
    #     'ticket': ticket,
    #     'action': 'Update',
    #     'is_staff': request.user.is_staff
    # }
    # return render(request, 'tickets/ticket_form.html', context)


# FRANZ WORK ON THIS

@router.delete("/tickets/{id}", response={204: None})
def delete_ticket(request, id: int):
    ticket = get_object_or_404(Ticket, id=id)
    
    # Permission check
    if ticket.student != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this ticket.')
        return redirect('ticket_list')
    
    # Students can only delete tickets with "pending" status
    if not request.user.is_staff and ticket.status != 'pending':
        messages.error(request, 'You cannot delete tickets that are being processed by admin.')
        return redirect('ticket_detail', id=ticket.id)
    
    # Franz change this refer to create_ticket and test in Postman
    # try:
    #     ticket = get_object_or_404(TicketSchema, id=id)
    #     ticket.delete()
    #     return {
    #         "success": True,
    #         "redirect": redirect('ticket_list')
    #     }
    # except Exception as e:
    #     messages.error(request, f'An error occurred: {str(e)}')
    
    # context = {'ticket': ticket}
    # return render(request, 'tickets/ticket_confirm_delete.html', context)


# Ticket Comments Views

@router.post("/tickets/{id}/comments/create", response=TicketCommentSchema)
def create_comment(request, comment: TicketCreateSchema):
    
    return redirect('ticket_detail', id=id)


@router.post("/tickets/{id}/comments/{comment_id}", response=TicketCommentSchema)    
def edit_comment(request, id, comment_id):
    return redirect('ticket_detail', id=id)


@router.delete("/tickets/{id}/comments/{comment_id}", response={204: None})    
def delete_comment(request, id, comment_id):
    return redirect('ticket_detail', id=id)

    
# Ticket Feedback Views
@router.get("/tickets/{id}/feedback/", response=TicketFeedbackSchema)
def get_feedback(request, id: int):
    ticket = get_object_or_404(Ticket, id=id)
    # Allow owner or staff to view
    if ticket.student != request.user and not request.user.is_staff:
        return redirect('ticket_list')
    feedback = get_object_or_404(TicketFeedback, ticket=ticket)
    return feedback


@router.post("/tickets/{id}/feedback/", response={201: TicketFeedbackSchema, 400: dict})
def create_feedback(request, id: int, payload: TicketFeedbackCreateSchema):
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

    # Auto-close ticket upon feedback
    ticket.status = 'closed'
    ticket.save()

    return 201, feedback


@router.put("/tickets/{id}/feedback/", response=TicketFeedbackSchema)
def update_feedback(request, id: int, payload: TicketFeedbackUpdateSchema):
    ticket = get_object_or_404(Ticket, id=id)
    feedback = get_object_or_404(TicketFeedback, ticket=ticket)

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
