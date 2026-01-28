from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ninja import Router

from .schemas import TicketCommentSchema, TicketCreateSchema, TicketSchema, TicketUpdateSchema
from .models import Category, Ticket, TicketPriority

router = Router()

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

@login_required(login_url='login_user')
@router.get("/", response=TicketSchema)
def ticket_list(request):
    if request.user.is_staff:
        all_tickets = Ticket.objects.select_related('category', 'priority', 'student').all()
    else:
        all_tickets = Ticket.objects.select_related('category', 'priority').filter(student=request.user)
    
    return all_tickets
    

@login_required(login_url='login_user')
@router.get("/tickets/{id}", response=TicketSchema)
def ticket_detail(id: int):
    ticket = get_object_or_404(Ticket, id=id)
    return ticket
    

@login_required(login_url='login_user')
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
@login_required(login_url='login_user')
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
@login_required(login_url='login_user')
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
@login_required(login_url='login_user')
@router.post("/tickets/{id}/comments/create", response=TicketCommentSchema)
def create_comment(request, comment: TicketCreateSchema):
    
    return redirect('ticket_detail', id=id)

@login_required(login_url='login_user')
@router.post("/tickets/{id}/comments/{comment_id}/edit")    
def edit_comment(request, id, comment_id):
    return redirect('ticket_detail', id=id)

@login_required(login_url='login_user')
@router.delete("/tickets/{id}/comments/{comment_id}/delete")    
def delete_comment(request, id, comment_id):
    return redirect('ticket_detail', id=id)
    
    