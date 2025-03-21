from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm  # For login
from django.contrib import messages
from .forms import CustomUserCreationForm, ClientProfileForm
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import User, ClientProfile
from django.db import transaction


class SignUpView(CreateView):
    """
    View for user registration.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')  # Redirect to login after successful signup
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log the user in automatically after signup
        messages.success(self.request, "Registration successful.")
        return super().form_valid(form)


def login_view(request):
    """
    View for user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  # This will be the email
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("survey_realestate:property_list")  # Redirect to a desired page
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    View for user logout.
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("survey_realestate:property_list")  # Redirect to login or another page


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile was updated successfully!')
        return super().form_valid(form)

@login_required
@transaction.atomic
def update_client_profile(request):
    """
    View to update client profile in one transaction.
    """
    if request.method == 'POST':
        profile_form = ClientProfileForm(request.POST, instance=request.user.client_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('accounts:update_client_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = ClientProfileForm(instance=request.user.client_profile)
    return render(request, 'accounts/update_client_profile.html', {'profile_form': profile_form})