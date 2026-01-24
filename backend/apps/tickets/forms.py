from django import forms
from .models import Ticket


class TicketCreateForm(forms.ModelForm):
    """Form for students to create tickets"""
    
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'building', 'room_name']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief summary of the issue'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the issue in detail...'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'building': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., MM Building, Wester Building'
            }),
            'room_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., MM 22, CSL 1'
            }),
        }


class TicketUpdateForm(forms.ModelForm):
    """Form for students to update their own tickets (limited fields)"""
    
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'building', 'room_name']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'building': forms.TextInput(attrs={'class': 'form-control'}),
            'room_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AdminTicketUpdateForm(forms.ModelForm):
    """Form for admins to update tickets - only priority and status"""
    
    class Meta:
        model = Ticket
        fields = ['priority', 'status']
        widgets = {
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }