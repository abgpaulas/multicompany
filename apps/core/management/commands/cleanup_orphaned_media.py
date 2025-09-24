from django.core.management.base import BaseCommand
from django.conf import settings
from apps.core.models import CompanyProfile
from apps.accounts.models import User
from apps.job_orders.models import Product
import os


class Command(BaseCommand):
    help = 'Clean up orphaned media file references in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be cleaned up without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes will be made'))
        
        cleaned_count = 0
        
        # Check company profiles for orphaned logo files
        for profile in CompanyProfile.objects.filter(logo__isnull=False):
            if profile.logo and profile.logo.name:
                logo_path = os.path.join(settings.MEDIA_ROOT, profile.logo.name)
                if not os.path.exists(logo_path):
                    self.stdout.write(f'Found orphaned logo: {profile.logo.name} for company {profile.company_name}')
                    if not dry_run:
                        profile.logo = None
                        profile.save(update_fields=['logo'])
                    cleaned_count += 1
        
        # Check company profiles for orphaned signature files
        for profile in CompanyProfile.objects.filter(signature__isnull=False):
            if profile.signature and profile.signature.name:
                signature_path = os.path.join(settings.MEDIA_ROOT, profile.signature.name)
                if not os.path.exists(signature_path):
                    self.stdout.write(f'Found orphaned signature: {profile.signature.name} for company {profile.company_name}')
                    if not dry_run:
                        profile.signature = None
                        profile.save(update_fields=['signature'])
                    cleaned_count += 1
        
        # Check user profile pictures
        for user in User.objects.filter(profile_picture__isnull=False):
            if user.profile_picture and user.profile_picture.name:
                profile_path = os.path.join(settings.MEDIA_ROOT, user.profile_picture.name)
                if not os.path.exists(profile_path):
                    self.stdout.write(f'Found orphaned profile picture: {user.profile_picture.name} for user {user.email}')
                    if not dry_run:
                        user.profile_picture = None
                        user.save(update_fields=['profile_picture'])
                    cleaned_count += 1
        
        # Check product images
        for product in Product.objects.filter(image__isnull=False):
            if product.image and product.image.name:
                image_path = os.path.join(settings.MEDIA_ROOT, product.image.name)
                if not os.path.exists(image_path):
                    self.stdout.write(f'Found orphaned product image: {product.image.name} for product {product.job_order}')
                    if not dry_run:
                        product.image = None
                        product.save(update_fields=['image'])
                    cleaned_count += 1
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f'DRY RUN: Would clean up {cleaned_count} orphaned media references'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Cleaned up {cleaned_count} orphaned media references'))
