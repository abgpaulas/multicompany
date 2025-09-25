#!/usr/bin/env python3
"""
Debug what templates are actually receiving for image variables
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_app.settings')
django.setup()

from django.template import Template, Context
from django.template.loader import get_template
from apps.core.utils import get_company_context
from apps.accounts.models import User
from apps.core.models import CompanyProfile

def debug_template_context():
    print("🔍 DEBUGGING TEMPLATE CONTEXT FOR IMAGES")
    print("=" * 60)
    
    try:
        # Get a user with images
        user = User.objects.get(email='ubanghasteve@gmail.com')
        print(f"Testing with user: {user.email}")
        
        # Get company context
        context = get_company_context(user)
        print("\n📋 Company Context Variables:")
        for key, value in context.items():
            print(f"   {key}: {value}")
        
        # Test template rendering
        print("\n🧪 Testing Template Rendering:")
        
        # Test 1: Simple image template
        template_string = """
        {% load media_utils %}
        <div>
            <h3>Company Logo:</h3>
            {% if company_logo %}
                <img src="{{ company_logo|cache_bust }}" alt="Company Logo" style="max-width: 200px;">
                <p>Logo URL: {{ company_logo|cache_bust }}</p>
            {% else %}
                <p>No company logo found</p>
            {% endif %}
            
            <h3>Company Signature:</h3>
            {% if company_signature %}
                <img src="{{ company_signature|cache_bust }}" alt="Company Signature" style="max-width: 200px;">
                <p>Signature URL: {{ company_signature|cache_bust }}</p>
            {% else %}
                <p>No company signature found</p>
            {% endif %}
        </div>
        """
        
        template = Template(template_string)
        context_obj = Context(context)
        rendered = template.render(context_obj)
        
        print("Rendered HTML:")
        print(rendered)
        
        # Test 2: Check actual model fields
        print("\n📊 Direct Model Field Check:")
        try:
            profile = CompanyProfile.objects.get(user=user)
            print(f"Company Profile: {profile.company_name}")
            
            if profile.logo:
                print(f"Logo field exists: {profile.logo}")
                print(f"Logo name: {profile.logo.name}")
                print(f"Logo URL: {profile.logo.url}")
            else:
                print("No logo field")
            
            if profile.signature:
                print(f"Signature field exists: {profile.signature}")
                print(f"Signature name: {profile.signature.name}")
                print(f"Signature URL: {profile.signature.url}")
            else:
                print("No signature field")
                
        except CompanyProfile.DoesNotExist:
            print("No company profile found for this user")
        
        # Test 3: Check user profile picture
        print("\n👤 User Profile Picture Check:")
        if user.profile_picture:
            print(f"Profile picture exists: {user.profile_picture}")
            print(f"Profile picture name: {user.profile_picture.name}")
            print(f"Profile picture URL: {user.profile_picture.url}")
        else:
            print("No profile picture")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_template_context()
