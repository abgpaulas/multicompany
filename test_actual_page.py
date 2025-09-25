#!/usr/bin/env python3
"""
Test actual page rendering to see what's happening
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_app.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from apps.core.models import CompanyProfile

User = get_user_model()

def test_actual_page():
    print("🌐 TESTING ACTUAL PAGE RENDERING")
    print("=" * 60)
    
    try:
        # Create a test client
        client = Client()
        
        # Get a user and log them in
        user = User.objects.get(email='ubanghasteve@gmail.com')
        client.force_login(user)
        
        # Test different pages
        pages_to_test = [
            '/dashboard/',
            '/invoices/',
            '/waybills/',
            '/quotations/',
            '/receipts/',
            '/job-orders/',
        ]
        
        for page in pages_to_test:
            print(f"\n🔍 Testing page: {page}")
            try:
                response = client.get(page)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.content.decode('utf-8')
                    
                    # Check for GitHub URLs
                    if 'raw.githubusercontent.com' in content:
                        print("   ✅ GitHub URLs found in page")
                        
                        # Count image URLs
                        github_url_count = content.count('raw.githubusercontent.com')
                        print(f"   📊 Found {github_url_count} GitHub image URLs")
                        
                        # Check for specific images
                        if 'company_logo' in content and 'raw.githubusercontent.com' in content:
                            print("   ✅ Company logo URLs found")
                        if 'company_signature' in content and 'raw.githubusercontent.com' in content:
                            print("   ✅ Company signature URLs found")
                        if 'profile_picture' in content and 'raw.githubusercontent.com' in content:
                            print("   ✅ Profile picture URLs found")
                    else:
                        print("   ❌ No GitHub URLs found in page")
                        
                        # Check for local media URLs
                        if '/media/' in content:
                            local_media_count = content.count('/media/')
                            print(f"   ⚠️ Found {local_media_count} local media URLs (should be GitHub URLs)")
                        
                        # Check for broken image tags
                        if 'src=""' in content or 'src="None"' in content:
                            print("   ❌ Found empty or None image sources")
                else:
                    print(f"   ❌ Page returned status {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error testing page: {e}")
        
        # Test a specific invoice page if it exists
        print(f"\n🔍 Testing specific invoice page...")
        try:
            from apps.invoices.models import Invoice
            invoice = Invoice.objects.first()
            
            if invoice:
                response = client.get(f'/invoices/{invoice.id}/')
                print(f"   Invoice page status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.content.decode('utf-8')
                    
                    if 'raw.githubusercontent.com' in content:
                        print("   ✅ Invoice page has GitHub URLs")
                    else:
                        print("   ❌ Invoice page missing GitHub URLs")
                        print("   Content snippet:", content[:500])
            else:
                print("   No invoices found to test")
                
        except Exception as e:
            print(f"   Error testing invoice page: {e}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_actual_page()
