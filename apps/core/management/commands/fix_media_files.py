from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from apps.core.models import CompanyProfile
from apps.accounts.models import User
from apps.job_orders.models import Product
from apps.inventory.models import InventoryLayout
import os
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fix media files and clean up orphaned references'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing media files and cleaning up orphaned references...")
        
        fixed_count = 0
        
        # Fix company profiles with missing logo/signature files
        self.stdout.write("\n📋 Checking company profiles...")
        for profile in CompanyProfile.objects.all():
            profile_updated = False
            
            # Check logo
            if profile.logo and profile.logo.name:
                if not default_storage.exists(profile.logo.name):
                    self.stdout.write(f"❌ Missing logo: {profile.logo.name} for company {profile.company_name}")
                    profile.logo = None
                    profile_updated = True
                    fixed_count += 1
            
            # Check signature
            if profile.signature and profile.signature.name:
                if not default_storage.exists(profile.signature.name):
                    self.stdout.write(f"❌ Missing signature: {profile.signature.name} for company {profile.company_name}")
                    profile.signature = None
                    profile_updated = True
                    fixed_count += 1
            
            if profile_updated:
                profile.save(update_fields=['logo', 'signature'])
                self.stdout.write(f"✅ Fixed company profile: {profile.company_name}")
        
        # Fix user profile pictures
        self.stdout.write("\n👤 Checking user profile pictures...")
        for user in User.objects.filter(profile_picture__isnull=False):
            if user.profile_picture and user.profile_picture.name:
                if not default_storage.exists(user.profile_picture.name):
                    self.stdout.write(f"❌ Missing profile picture: {user.profile_picture.name} for user {user.email}")
                    user.profile_picture = None
                    user.save(update_fields=['profile_picture'])
                    fixed_count += 1
                    self.stdout.write(f"✅ Fixed user profile: {user.email}")
        
        # Fix product images
        self.stdout.write("\n📦 Checking product images...")
        for product in Product.objects.filter(image__isnull=False):
            if product.image and product.image.name:
                if not default_storage.exists(product.image.name):
                    self.stdout.write(f"❌ Missing product image: {product.image.name} for product {product.job_order}")
                    product.image = None
                    product.save(update_fields=['image'])
                    fixed_count += 1
                    self.stdout.write(f"✅ Fixed product: {product.job_order}")
        
        # Fix inventory company logos
        self.stdout.write("\n📊 Checking inventory company logos...")
        for layout in InventoryLayout.objects.filter(company_logo__isnull=False):
            if layout.company_logo and layout.company_logo.name:
                if not default_storage.exists(layout.company_logo.name):
                    self.stdout.write(f"❌ Missing inventory logo: {layout.company_logo.name} for layout {layout.name}")
                    layout.company_logo = None
                    layout.save(update_fields=['company_logo'])
                    fixed_count += 1
                    self.stdout.write(f"✅ Fixed inventory layout: {layout.name}")
        
        self.stdout.write(f"\n🎉 Media files fix completed!")
        self.stdout.write(f"✅ Fixed {fixed_count} orphaned media file references")
        self.stdout.write("🚀 All media file references are now valid!")
