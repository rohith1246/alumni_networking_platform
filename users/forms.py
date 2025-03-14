from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'batch', 'department', 'company', 'profile_pic']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        # Only allow profile_pic to be updated – the company field is intentionally omitted.
        fields = ['profile_pic']