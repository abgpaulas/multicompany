from django.core.management.base import BaseCommand
from django.conf import settings
from apps.core.models import CompanyProfile
from apps.core.utils import get_safe_media_url, get_media_url_with_cache_bust
from apps.accounts.models import User
from apps.job_orders.models import Product
import requests

class Command(BaseCommand):
    help = 'Test image URLs and their accessibility'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Testing image URLs and accessibility...")
        
        self.stdout.write(f"Storage backend: {settings.DEFAULT_FILE_STORAGE}")
        self.stdout.write(f"USE_GITHUB: {getattr(settings, 'USE_GITHUB', False)}")
        self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")
        
        # Test company profiles
        self.stdout.write("\n📋 Testing company profile images...")
        for profile in CompanyProfile.objects.filter(logo__isnull=False)[:3]:
            self.stdout.write(f"\nCompany: {profile.company_name}")
            
            if profile.logo:
                self.stdout.write(f"  Logo name: {profile.logo.name}")
                self.stdout.write(f"  Logo URL: {profile.logo.url}")
                self.stdout.write(f"  Safe media URL: {get_safe_media_url(profile.logo)}")
                self.stdout.write(f"  Cache bust URL: {get_media_url_with_cache_bust(profile.logo)}")
                
                # Test URL accessibility
                try:
                    response = requests.head(profile.logo.url, timeout=10)
                    if response.status_code == 200:
                        self.stdout.write(f"  ✅ Logo URL accessible (Status: {response.status_code})")
                    else:
                        self.stdout.write(f"  ❌ Logo URL not accessible (Status: {response.status_code})")
                except Exception as e:
                    self.stdout.write(f"  ❌ Logo URL error: {e}")
            
            if profile.signature:
                self.stdout.write(f"  Signature name: {profile.signature.name}")
                self.stdout.write(f"  Signature URL: {profile.signature.url}")
                
                try:
                    response = requests.head(profile.signature.url, timeout=10)
                    if response.status_code == 200:
                        self.stdout.write(f"  ✅ Signature URL accessible (Status: {response.status_code})")
                    else:
                        self.stdout.write(f"  ❌ Signature URL not accessible (Status: {response.status_code})")
                except Exception as e:
                    self.stdout.write(f"  ❌ Signature URL error: {e}")
        
        # Test user profile pictures
        self.stdout.write("\n👤 Testing user profile pictures...")
        for user in User.objects.filter(profile_picture__isnull=False)[:3]:
            self.stdout.write(f"\nUser: {user.email}")
            
            if user.profile_picture:
                self.stdout.write(f"  Profile picture name: {user.profile_picture.name}")
                self.stdout.write(f"  Profile picture URL: {user.profile_picture.url}")
                
                try:
                    response = requests.head(user.profile_picture.url, timeout=10)
                    if response.status_code == 200:
                        self.stdout.write(f"  ✅ Profile picture URL accessible (Status: {response.status_code})")
                    else:
                        self.stdout.write(f"  ❌ Profile picture URL not accessible (Status: {response.status_code})")
                except Exception as e:
                    self.stdout.write(f"  ❌ Profile picture URL error: {e}")
        
        # Test product images
        self.stdout.write("\n📦 Testing product images...")
        for product in Product.objects.filter(image__isnull=False)[:3]:
            self.stdout.write(f"\nProduct: {product.job_order}")
            
            if product.image:
                self.stdout.write(f"  Product image name: {product.image.name}")
                self.stdout.write(f"  Product image URL: {product.image.url}")
                
                try:
                    response = requests.head(product.image.url, timeout=10)
                    if response.status_code == 200:
                        self.stdout.write(f"  ✅ Product image URL accessible (Status: {response.status_code})")
                    else:
                        self.stdout.write(f"  ❌ Product image URL not accessible (Status: {response.status_code})")
                except Exception as e:
                    self.stdout.write(f"  ❌ Product image URL error: {e}")
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write("🎉 Image URL testing completed!")
