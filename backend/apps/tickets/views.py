from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Ticket


def login_user(request):
    """
    Login page for students
    """
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
    """
    Logout user
    """
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('login_user')


@login_required(login_url='login_user')
def ticket_list(request):
    """
    SQL: SELECT * FROM tickets ORDER BY created_at DESC
    Get all tickets from database, grouped by status for Kanban board
    """
    # Get all tickets or just user's tickets
    if request.user.is_staff:
        all_tickets = Ticket.objects.all()
    else:
        all_tickets = Ticket.objects.filter(student=request.user)
    
    # Group tickets by status
    tickets_pending = all_tickets.filter(status='pending').order_by('-created_at')
    tickets_in_progress = all_tickets.filter(status='in_progress').order_by('-created_at')
    tickets_resolved = all_tickets.filter(status='resolved').order_by('-created_at')
    tickets_closed = all_tickets.filter(status='closed').order_by('-created_at')
    
    context = {
        'tickets_pending': tickets_pending,
        'tickets_in_progress': tickets_in_progress,
        'tickets_resolved': tickets_resolved,
        'tickets_closed': tickets_closed,
    }
    return render(request, 'tickets/ticket_list.html', context)


@login_required(login_url='login_user')
def ticket_detail(request, id):
    """
    SQL: SELECT * FROM tickets WHERE id = ?
    Get single ticket by ID
    """
    ticket = get_object_or_404(Ticket, id=id)
    
    context = {
        'ticket': ticket,
    }
    return render(request, 'tickets/ticket_detail.html', context)


@login_required(login_url='login_user')
def create_ticket(request):
    """
    SQL: INSERT INTO tickets (...) VALUES (...)
    Create a new ticket
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        building = request.POST.get('building')
        room_name = request.POST.get('room_name')
        priority = request.POST.get('priority', 'medium')
        
        ticket = Ticket.objects.create(
            title=title,
            description=description,
            category=category,
            building=building,
            room_name=room_name,
            priority=priority,
            student=request.user,
            status='pending'
        )
        
        messages.success(request, 'Ticket created successfully!')
        return redirect('ticket_detail', id=ticket.id)
    
    context = {
        'action': 'Create',
        'is_staff': request.user.is_staff
    }
    return render(request, 'tickets/ticket_form.html', context)


@login_required(login_url='login_user')
def update_ticket(request, id):
    """
    SQL: UPDATE tickets SET ... WHERE id = ?
    Update existing ticket
    """
    ticket = get_object_or_404(Ticket, id=id)
    
    # Permission check
    if ticket.student != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this ticket.')
        return redirect('ticket_list')
    
    # Students can only edit tickets with "pending" status
    if not request.user.is_staff and ticket.status != 'pending':
        messages.error(request, 'You cannot edit tickets that are being processed by admin. Status must be "Pending".')
        return redirect('ticket_detail', id=ticket.id)
    
    if request.method == 'POST':
        # Students can edit all fields (only for pending tickets)
        if not request.user.is_staff:
            ticket.title = request.POST.get('title')
            ticket.description = request.POST.get('description')
            ticket.category = request.POST.get('category')
            ticket.building = request.POST.get('building')
            ticket.room_name = request.POST.get('room_name')
        
        # Admins can ONLY change Priority and Status
        if request.user.is_staff:
            ticket.priority = request.POST.get('priority')
            ticket.status = request.POST.get('status')
        
        ticket.save()
        
        messages.success(request, 'Ticket updated successfully!')
        return redirect('ticket_detail', id=ticket.id)
    
    context = {
        'ticket': ticket,
        'action': 'Update',
        'is_staff': request.user.is_staff
    }
    return render(request, 'tickets/ticket_form.html', context)


@login_required(login_url='login_user')
def delete_ticket(request, id):
    """
    SQL: DELETE FROM tickets WHERE id = ?
    Delete ticket by ID
    """
    ticket = get_object_or_404(Ticket, id=id)
    
    # Permission check
    if ticket.student != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this ticket.')
        return redirect('ticket_list')
    
    # Students can only delete tickets with "pending" status
    if not request.user.is_staff and ticket.status != 'pending':
        messages.error(request, 'You cannot delete tickets that are being processed by admin. Status must be "Pending".')
        return redirect('ticket_detail', id=ticket.id)
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted successfully!')
        return redirect('ticket_list')
    
    context = {'ticket': ticket}
    return render(request, 'tickets/ticket_confirm_delete.html', context)