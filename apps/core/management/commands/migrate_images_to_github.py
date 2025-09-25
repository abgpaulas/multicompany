from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings
import os
import shutil
from pathlib import Path

class Command(BaseCommand):
    help = 'Migrate existing images to GitHub storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--github-token',
            type=str,
            help='GitHub Personal Access Token',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force migration even if GitHub storage is not configured',
        )

    def handle(self, *args, **options):
        self.stdout.write("🔄 Migrating images to GitHub storage...")
        
        github_token = options.get('github_token')
        force = options.get('force', False)
        
        # Check if GitHub storage is configured
        if not hasattr(settings, 'USE_GITHUB') or not settings.USE_GITHUB:
            if not force:
                self.stdout.write(
                    self.style.WARNING(
                        "GitHub storage is not enabled. Use --force to proceed anyway."
                    )
                )
                return
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "GitHub storage is not enabled, but proceeding with --force."
                    )
                )
        
        # Set GitHub token if provided
        if github_token:
            os.environ['GITHUB_TOKEN'] = github_token
            self.stdout.write("✅ GitHub token set")
        
        # Check if we have a GitHub token
        if not os.getenv('GITHUB_TOKEN'):
            self.stdout.write(
                self.style.ERROR(
                    "GitHub token is required. Please provide it with --github-token or set GITHUB_TOKEN environment variable."
                )
            )
            return
        
        # Get media directory
        media_dir = Path(settings.MEDIA_ROOT)
        if not media_dir.exists():
            self.stdout.write(
                self.style.WARNING(f"Media directory {media_dir} does not exist.")
            )
            return
        
        # Count files to migrate
        total_files = 0
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                    total_files += 1
        
        if total_files == 0:
            self.stdout.write("No image files found to migrate.")
            return
        
        self.stdout.write(f"Found {total_files} image files to migrate.")
        
        # Migrate files
        migrated_count = 0
        failed_count = 0
        
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(media_dir)
                    
                    try:
                        # Read the file
                        with open(file_path, 'rb') as f:
                            content = f.read()
                        
                        # Save to GitHub storage
                        saved_path = default_storage.save(str(relative_path), content)
                        
                        self.stdout.write(f"✅ Migrated: {relative_path} -> {saved_path}")
                        migrated_count += 1
                        
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f"❌ Failed to migrate {relative_path}: {e}")
                        )
                        failed_count += 1
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(f"🎉 Migration completed!")
        self.stdout.write(f"✅ Successfully migrated: {migrated_count} files")
        if failed_count > 0:
            self.stdout.write(f"❌ Failed to migrate: {failed_count} files")
        
        if migrated_count > 0:
            self.stdout.write("\n🚀 Images are now stored in GitHub and will persist across deployments!")
            self.stdout.write("📝 Note: You may need to update your Render environment variables:")
            self.stdout.write("   - Set USE_GITHUB=True")
            self.stdout.write("   - Set GITHUB_TOKEN=your_token_here")
            self.stdout.write("   - Set GITHUB_REPO_NAME=abgpaulas/multicompany")
            self.stdout.write("   - Set GITHUB_BRANCH=master")
