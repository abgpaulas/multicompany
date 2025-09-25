from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings
from apps.core.models import CompanyProfile
from apps.accounts.models import User
from apps.job_orders.models import Product
from apps.inventory.models import InventoryLayout
import os
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fix image URLs and ensure they display correctly'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check-only',
            action='store_true',
            help='Only check for issues without fixing them',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )

    def handle(self, *args, **options):
        check_only = options.get('check_only', False)
        verbose = options.get('verbose', False)
        
        self.stdout.write("🔍 Checking and fixing image URLs...")
        
        if verbose:
            self.stdout.write(f"Storage backend: {default_storage.__class__.__name__}")
            self.stdout.write(f"USE_GITHUB: {getattr(settings, 'USE_GITHUB', False)}")
            self.stdout.write(f"MEDIA_URL: {settings.MEDIA_URL}")
        
        issues_found = 0
        issues_fixed = 0
        
        # Check company profiles
        self.stdout.write("\n📋 Checking company profiles...")
        for profile in CompanyProfile.objects.all():
            profile_issues = 0
            
            # Check logo
            if profile.logo and profile.logo.name:
                if verbose:
                    self.stdout.write(f"  Checking logo: {profile.logo.name}")
                
                # Check if file exists in storage
                if not default_storage.exists(profile.logo.name):
                    self.stdout.write(
                        self.style.WARNING(f"  ❌ Missing logo: {profile.logo.name}")
                    )
                    issues_found += 1
                    profile_issues += 1
                    
                    if not check_only:
                        # Try to find the file in local media directory
                        local_path = os.path.join(settings.MEDIA_ROOT, profile.logo.name)
                        if os.path.exists(local_path):
                            try:
                                # Copy to storage
                                with open(local_path, 'rb') as f:
                                    content = f.read()
                                saved_path = default_storage.save(profile.logo.name, content)
                                self.stdout.write(f"  ✅ Fixed logo: {saved_path}")
                                issues_fixed += 1
                            except Exception as e:
                                self.stdout.write(f"  ❌ Failed to fix logo: {e}")
                        else:
                            self.stdout.write(f"  ⚠️ Logo file not found locally: {local_path}")
                else:
                    if verbose:
                        self.stdout.write(f"  ✅ Logo exists: {profile.logo.name}")
            
            # Check signature
            if profile.signature and profile.signature.name:
                if verbose:
                    self.stdout.write(f"  Checking signature: {profile.signature.name}")
                
                if not default_storage.exists(profile.signature.name):
                    self.stdout.write(
                        self.style.WARNING(f"  ❌ Missing signature: {profile.signature.name}")
                    )
                    issues_found += 1
                    profile_issues += 1
                    
                    if not check_only:
                        local_path = os.path.join(settings.MEDIA_ROOT, profile.signature.name)
                        if os.path.exists(local_path):
                            try:
                                with open(local_path, 'rb') as f:
                                    content = f.read()
                                saved_path = default_storage.save(profile.signature.name, content)
                                self.stdout.write(f"  ✅ Fixed signature: {saved_path}")
                                issues_fixed += 1
                            except Exception as e:
                                self.stdout.write(f"  ❌ Failed to fix signature: {e}")
                        else:
                            self.stdout.write(f"  ⚠️ Signature file not found locally: {local_path}")
                else:
                    if verbose:
                        self.stdout.write(f"  ✅ Signature exists: {profile.signature.name}")
            
            if profile_issues == 0 and verbose:
                self.stdout.write(f"  ✅ Company {profile.company_name}: No issues")
        
        # Check user profile pictures
        self.stdout.write("\n👤 Checking user profile pictures...")
        for user in User.objects.filter(profile_picture__isnull=False):
            if user.profile_picture and user.profile_picture.name:
                if verbose:
                    self.stdout.write(f"  Checking profile picture: {user.profile_picture.name}")
                
                if not default_storage.exists(user.profile_picture.name):
                    self.stdout.write(
                        self.style.WARNING(f"  ❌ Missing profile picture: {user.profile_picture.name}")
                    )
                    issues_found += 1
                    
                    if not check_only:
                        local_path = os.path.join(settings.MEDIA_ROOT, user.profile_picture.name)
                        if os.path.exists(local_path):
                            try:
                                with open(local_path, 'rb') as f:
                                    content = f.read()
                                saved_path = default_storage.save(user.profile_picture.name, content)
                                self.stdout.write(f"  ✅ Fixed profile picture: {saved_path}")
                                issues_fixed += 1
                            except Exception as e:
                                self.stdout.write(f"  ❌ Failed to fix profile picture: {e}")
                        else:
                            self.stdout.write(f"  ⚠️ Profile picture not found locally: {local_path}")
                else:
                    if verbose:
                        self.stdout.write(f"  ✅ Profile picture exists: {user.profile_picture.name}")
        
        # Check product images
        self.stdout.write("\n📦 Checking product images...")
        for product in Product.objects.filter(image__isnull=False):
            if product.image and product.image.name:
                if verbose:
                    self.stdout.write(f"  Checking product image: {product.image.name}")
                
                if not default_storage.exists(product.image.name):
                    self.stdout.write(
                        self.style.WARNING(f"  ❌ Missing product image: {product.image.name}")
                    )
                    issues_found += 1
                    
                    if not check_only:
                        local_path = os.path.join(settings.MEDIA_ROOT, product.image.name)
                        if os.path.exists(local_path):
                            try:
                                with open(local_path, 'rb') as f:
                                    content = f.read()
                                saved_path = default_storage.save(product.image.name, content)
                                self.stdout.write(f"  ✅ Fixed product image: {saved_path}")
                                issues_fixed += 1
                            except Exception as e:
                                self.stdout.write(f"  ❌ Failed to fix product image: {e}")
                        else:
                            self.stdout.write(f"  ⚠️ Product image not found locally: {local_path}")
                else:
                    if verbose:
                        self.stdout.write(f"  ✅ Product image exists: {product.image.name}")
        
        # Check inventory company logos
        self.stdout.write("\n📊 Checking inventory company logos...")
        for layout in InventoryLayout.objects.filter(company_logo__isnull=False):
            if layout.company_logo and layout.company_logo.name:
                if verbose:
                    self.stdout.write(f"  Checking inventory logo: {layout.company_logo.name}")
                
                if not default_storage.exists(layout.company_logo.name):
                    self.stdout.write(
                        self.style.WARNING(f"  ❌ Missing inventory logo: {layout.company_logo.name}")
                    )
                    issues_found += 1
                    
                    if not check_only:
                        local_path = os.path.join(settings.MEDIA_ROOT, layout.company_logo.name)
                        if os.path.exists(local_path):
                            try:
                                with open(local_path, 'rb') as f:
                                    content = f.read()
                                saved_path = default_storage.save(layout.company_logo.name, content)
                                self.stdout.write(f"  ✅ Fixed inventory logo: {saved_path}")
                                issues_fixed += 1
                            except Exception as e:
                                self.stdout.write(f"  ❌ Failed to fix inventory logo: {e}")
                        else:
                            self.stdout.write(f"  ⚠️ Inventory logo not found locally: {local_path}")
                else:
                    if verbose:
                        self.stdout.write(f"  ✅ Inventory logo exists: {layout.company_logo.name}")
        
        # Summary
        self.stdout.write("\n" + "="*50)
        if issues_found == 0:
            self.stdout.write("🎉 No image URL issues found!")
            self.stdout.write("✅ All images are properly stored and accessible")
        else:
            if check_only:
                self.stdout.write(f"⚠️ Found {issues_found} image URL issues")
                self.stdout.write("Run without --check-only to fix them")
            else:
                self.stdout.write(f"🔧 Fixed {issues_fixed} out of {issues_found} issues")
                if issues_fixed < issues_found:
                    self.stdout.write("⚠️ Some issues could not be fixed automatically")
        
        # Recommendations
        if issues_found > 0:
            self.stdout.write("\n💡 Recommendations:")
            self.stdout.write("1. Ensure GitHub storage is properly configured")
            self.stdout.write("2. Set environment variables on Render:")
            self.stdout.write("   - USE_GITHUB=True")
            self.stdout.write("   - GITHUB_TOKEN=your_token_here")
            self.stdout.write("   - GITHUB_REPO_NAME=abgpaulas/multicompany")
            self.stdout.write("   - GITHUB_BRANCH=master")
            self.stdout.write("3. Run: python manage.py migrate_images_to_github")
