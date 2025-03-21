from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, ClientProfile

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for creating new users (registration).
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'national_id')  # Add your custom fields


class CustomUserChangeForm(UserChangeForm):
    """
    Custom form for editing existing users.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'national_id')


class ClientProfileForm(forms.ModelForm):
    """
    Form for updating the ClientProfile.
    """
    class Meta:
        model = ClientProfile
        fields = ['contact_details']  # Add other client-specific fields