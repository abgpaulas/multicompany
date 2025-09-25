#!/usr/bin/env python3
"""
Migrate existing local images to GitHub storage
This script will upload all your local media files to GitHub
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_app.settings')
django.setup()

from django.conf import settings
from business_app.github_storage import GitHubStorage
from django.core.files.base import ContentFile

def migrate_images():
    """Migrate all local images to GitHub"""
    print("🔄 Starting image migration to GitHub...")
    
    # Initialize GitHub storage
    storage = GitHubStorage()
    
    if not storage.repo:
        print("❌ GitHub storage not configured. Please set up GITHUB_TOKEN first.")
        print("📖 See GITHUB_TOKEN_SETUP.md for instructions.")
        return False
    
    media_root = Path(settings.MEDIA_ROOT)
    if not media_root.exists():
        print("❌ Media directory not found.")
        return False
    
    migrated_count = 0
    error_count = 0
    
    # Walk through all files in media directory
    for file_path in media_root.rglob('*'):
        if file_path.is_file():
            try:
                # Get relative path from media root
                relative_path = file_path.relative_to(media_root)
                
                print(f"📤 Uploading: {relative_path}")
                
                # Read file content
                with open(file_path, 'rb') as f:
                    content = ContentFile(f.read())
                
                # Upload to GitHub
                github_path = storage._save(str(relative_path), content)
                print(f"✅ Uploaded: {github_path}")
                migrated_count += 1
                
            except Exception as e:
                print(f"❌ Error uploading {relative_path}: {e}")
                error_count += 1
    
    print(f"\n🎉 Migration complete!")
    print(f"✅ Successfully migrated: {migrated_count} files")
    if error_count > 0:
        print(f"❌ Errors: {error_count} files")
    
    return error_count == 0

if __name__ == "__main__":
    success = migrate_images()
    if success:
        print("\n🚀 All images have been migrated to GitHub!")
        print("Your images should now display correctly.")
    else:
        print("\n⚠️  Migration completed with some errors.")
        print("Check the output above for details.")
