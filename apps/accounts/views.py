from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView
from django.contrib.auth.views import LoginView, PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm
import json

User = get_user_model()

# Authentication Views
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('accounts:dashboard')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

class RegisterView(View):
    template_name = 'accounts/register.html'
    
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('accounts:login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, self.template_name, {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

# Profile Views
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

class ProfileEditView(View):
    template_name = 'accounts/profile_edit.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        # Simple profile edit logic - you can enhance this later
        return redirect('accounts:profile')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

class ProfileView(View):
    template_name = 'accounts/profile.html'
    
    def get(self, request):
        return render(request, self.template_name)

def debug_auth_view(request):
    return JsonResponse({'status': 'debug', 'user': str(request.user)})

# Admin creation views
@csrf_exempt
def create_first_admin(request):
    """
    Create the first admin user if no superusers exist
    """
    if User.objects.filter(is_superuser=True).exists():
        return JsonResponse({'status': 'error', 'message': 'Admin user already exists.'}, status=403)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([username, email, password]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

        try:
            user = User.objects.create_superuser(username=username, email=email, password=password)
            return JsonResponse({'status': 'success', 'message': f'Admin user {username} created successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'info', 'message': 'Send POST request with username, email, password to create first admin.'})

def check_admin_exists(request):
    if User.objects.filter(is_superuser=True).exists():
        return JsonResponse({'status': 'exists', 'message': 'Admin user exists.'})
    else:
        return JsonResponse({'status': 'not_exists', 'message': 'No admin user found.'})