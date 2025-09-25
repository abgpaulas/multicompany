#!/usr/bin/env python3
"""
Test image upload functionality
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_app.settings')
django.setup()

from apps.core.models import CompanyProfile
from django.core.files.uploadedfile import SimpleUploadedFile

def test_image_upload():
    """Test image upload functionality"""
    print("🧪 Testing image upload functionality...")
    
    # Create a test file
    test_file = SimpleUploadedFile(
        'test_logo.png', 
        b'fake image content', 
        content_type='image/png'
    )
    
    # Get or create a company profile
    profile, created = CompanyProfile.objects.get_or_create(
        user_id=1,  # Assuming user with ID 1 exists
        defaults={
            'company_name': 'Test Company',
            'email': 'test@example.com',
            'phone': '+1234567890',
            'address': 'Test Address'
        }
    )
    
    print(f"Company profile: {profile.company_name}")
    
    try:
        # Test logo upload
        print("📤 Uploading logo...")
        profile.logo = test_file
        profile.save()
        print("✅ Logo upload successful!")
        print(f"Logo URL: {profile.logo.url}")
        
        # Test signature upload
        print("📤 Uploading signature...")
        signature_file = SimpleUploadedFile(
            'test_signature.png', 
            b'fake signature content', 
            content_type='image/png'
        )
        profile.signature = signature_file
        profile.save()
        print("✅ Signature upload successful!")
        print(f"Signature URL: {profile.signature.url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

if __name__ == "__main__":
    success = test_image_upload()
    if success:
        print("\n🎉 Image upload test completed successfully!")
    else:
        print("\n⚠️ Image upload test failed!")
