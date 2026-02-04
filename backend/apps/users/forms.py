from django import forms
from backend.apps.users.models import CustomUserManager



class SignupForm(forms.Form):

    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@usls.edu.ph'):
            raise forms.ValidationError('Email must be a valid USLS email address')
        if self.model.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists')
        return email