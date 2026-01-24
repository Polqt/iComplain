from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Ticket, TicketPriority
from .forms import TicketCreateForm, TicketUpdateForm, AdminTicketUpdateForm


def login_user(request):
    """Login page for students"""
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
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('login_user')


@login_required(login_url='login_user')
def ticket_list(request):
    """Get all tickets grouped by status for Kanban board"""
    if request.user.is_staff:
        all_tickets = Ticket.objects.select_related('category', 'priority', 'student').all()
    else:
        all_tickets = Ticket.objects.select_related('category', 'priority').filter(student=request.user)
    
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
    """View ticket details"""
    ticket = get_object_or_404(
        Ticket.objects.select_related('category', 'priority', 'student'),
        id=id
    )

    context = {
        'ticket': ticket,
    }
    return render(request, 'tickets/ticket_detail.html', context)


@login_required(login_url='login_user')
def create_ticket(request):
    """Create a new ticket"""
    if request.method == 'POST':
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.student = request.user
            
            # Set default priority to "Medium"
            try:
                medium_priority = TicketPriority.objects.get(name='Medium')
                ticket.priority = medium_priority
            except TicketPriority.DoesNotExist:
                messages.error(request, 'Default priority not found. Please contact admin.')
                return redirect('ticket_list')
            
            ticket.status = 'pending'
            ticket.save()
            
            messages.success(request, 'Ticket created successfully!')
            return redirect('ticket_detail', id=ticket.id)
        else:
            print("FORM ERRORS:", form.errors)  # Debug
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TicketCreateForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'is_staff': request.user.is_staff
    }
    return render(request, 'tickets/ticket_form.html', context)


@login_required(login_url='login_user')
def update_ticket(request, id):
    """Update existing ticket"""
    ticket = get_object_or_404(Ticket, id=id)
    
    # Permission check
    if ticket.student != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this ticket.')
        return redirect('ticket_list')
    
    # Students can only edit tickets with "pending" status
    if not request.user.is_staff and ticket.status != 'pending':
        messages.error(request, 'You cannot edit tickets that are being processed by admin.')
        return redirect('ticket_detail', id=ticket.id)
    
    if request.method == 'POST':
        if request.user.is_staff:
            # Admin can only change priority and status
            form = AdminTicketUpdateForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ticket updated successfully!')
                return redirect('ticket_detail', id=ticket.id)
        else:
            # Student can edit all fields
            form = TicketUpdateForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ticket updated successfully!')
                return redirect('ticket_detail', id=ticket.id)
    else:
        if request.user.is_staff:
            form = AdminTicketUpdateForm(instance=ticket)
        else:
            form = TicketUpdateForm(instance=ticket)
    
    context = {
        'form': form,
        'ticket': ticket,
        'action': 'Update',
        'is_staff': request.user.is_staff
    }
    return render(request, 'tickets/ticket_form.html', context)


@login_required(login_url='login_user')
def delete_ticket(request, id):
    """Delete ticket by ID"""
    ticket = get_object_or_404(Ticket, id=id)
    
    # Permission check
    if ticket.student != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this ticket.')
        return redirect('ticket_list')
    
    # Students can only delete tickets with "pending" status
    if not request.user.is_staff and ticket.status != 'pending':
        messages.error(request, 'You cannot delete tickets that are being processed by admin.')
        return redirect('ticket_detail', id=ticket.id)
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted successfully!')
        return redirect('ticket_list')
    
    context = {'ticket': ticket}
    return render(request, 'tickets/ticket_confirm_delete.html', context)