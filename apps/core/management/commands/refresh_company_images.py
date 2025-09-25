from django.core.management.base import BaseCommand
from django.core.cache import cache
from apps.core.models import CompanyProfile
import os


class Command(BaseCommand):
    help = 'Refresh company images and clear any cached URLs'

    def handle(self, *args, **options):
        self.stdout.write("Refreshing company images...")
        
        # Clear Django cache
        cache.clear()
        self.stdout.write("✅ Cleared Django cache")
        
        # Update company profiles to trigger URL regeneration
        updated_count = 0
        for company_profile in CompanyProfile.objects.all():
            if company_profile.logo:
                # Force URL regeneration by accessing the URL
                try:
                    logo_url = company_profile.logo.url
                    self.stdout.write(f"✅ Company '{company_profile.company_name}' logo URL: {logo_url}")
                    updated_count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"⚠️  Company '{company_profile.company_name}' logo error: {e}"))
            
            if company_profile.signature:
                # Force URL regeneration by accessing the URL
                try:
                    signature_url = company_profile.signature.url
                    self.stdout.write(f"✅ Company '{company_profile.company_name}' signature URL: {signature_url}")
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"⚠️  Company '{company_profile.company_name}' signature error: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f"✅ Refreshed {updated_count} company images"))
        self.stdout.write("🎉 Company images have been refreshed! They should now display correctly across all apps.")
