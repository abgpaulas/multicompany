import os
import json
import zipfile
from datetime import datetime
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.management.base import BaseCommand


class SimpleBackupStorage(Storage):
    """
    Simple backup storage that creates downloadable backup files.
    Files are stored locally but backed up to a downloadable archive.
    """
    
    def __init__(self):
        self.backup_dir = BASE_DIR / 'backups'
        self.backup_dir.mkdir(exist_ok=True)
    
    def _save(self, name, content):
        """Save file locally and add to backup list"""
        # Save file locally
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with open(local_path, 'wb') as f:
            for chunk in content.chunks():
                f.write(chunk)
        
        # Add to backup tracking
        self._add_to_backup_list(name, local_path)
        
        return name
    
    def _add_to_backup_list(self, name, local_path):
        """Add file to backup tracking list"""
        backup_list_file = self.backup_dir / 'backup_list.json'
        
        try:
            with open(backup_list_file, 'r') as f:
                backup_list = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            backup_list = []
        
        # Add file info
        file_info = {
            'name': name,
            'path': local_path,
            'size': os.path.getsize(local_path),
            'uploaded_at': datetime.now().isoformat()
        }
        
        # Remove if already exists
        backup_list = [item for item in backup_list if item['name'] != name]
        backup_list.append(file_info)
        
        # Save updated list
        with open(backup_list_file, 'w') as f:
            json.dump(backup_list, f, indent=2)
    
    def delete(self, name):
        """Delete file and remove from backup list"""
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        if os.path.exists(local_path):
            os.remove(local_path)
        
        # Remove from backup list
        self._remove_from_backup_list(name)
    
    def _remove_from_backup_list(self, name):
        """Remove file from backup tracking list"""
        backup_list_file = self.backup_dir / 'backup_list.json'
        
        try:
            with open(backup_list_file, 'r') as f:
                backup_list = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        
        # Remove file from list
        backup_list = [item for item in backup_list if item['name'] != name]
        
        # Save updated list
        with open(backup_list_file, 'w') as f:
            json.dump(backup_list, f, indent=2)
    
    def exists(self, name):
        """Check if file exists"""
        return os.path.exists(os.path.join(settings.MEDIA_ROOT, name))
    
    def url(self, name):
        """Return file URL"""
        return f"{settings.MEDIA_URL}{name}"
    
    def size(self, name):
        """Get file size"""
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        if os.path.exists(local_path):
            return os.path.getsize(local_path)
        return 0
    
    def open(self, name, mode='rb'):
        """Open file for reading"""
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        return open(local_path, mode)
    
    def create_backup_archive(self):
        """Create a downloadable backup archive"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"media_backup_{timestamp}.zip"
        backup_path = self.backup_dir / backup_filename
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all media files
            media_root = settings.MEDIA_ROOT
            for root, dirs, files in os.walk(media_root):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, media_root)
                    zipf.write(file_path, arcname)
            
            # Add backup list
            backup_list_file = self.backup_dir / 'backup_list.json'
            if backup_list_file.exists():
                zipf.write(backup_list_file, 'backup_list.json')
        
        return backup_path


class CreateBackupCommand(BaseCommand):
    """Django management command to create backup archives"""
    help = 'Create a backup archive of all media files'
    
    def handle(self, *args, **options):
        storage = SimpleBackupStorage()
        backup_path = storage.create_backup_archive()
        
        self.stdout.write(
            self.style.SUCCESS(f'Backup created: {backup_path}')
        )
        self.stdout.write(
            self.style.WARNING(
                f'Download this file and keep it safe! '
                f'You can restore it after deployments.'
            )
        )
