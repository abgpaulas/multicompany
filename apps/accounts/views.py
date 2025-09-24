from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()

@csrf_exempt
def create_first_admin(request):
    """
    Create the first admin user if no superusers exist
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            # Check if any superusers exist
            if User.objects.filter(is_superuser=True).exists():
                return JsonResponse({'error': 'Admin user already exists'}, status=400)
            
            # Create superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Admin user "{username}" created successfully'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def check_admin_exists(request):
    """
    Check if any admin users exist
    """
    admin_exists = User.objects.filter(is_superuser=True).exists()
    return JsonResponse({'admin_exists': admin_exists})