from django.core.management.base import BaseCommand
from django.conf import settings
import os
import zipfile
import json
from datetime import datetime


class Command(BaseCommand):
    help = 'Create a backup archive of all media files for download'

    def add_arguments(self, parser):
        parser.add_argument(
            '--download-url',
            action='store_true',
            help='Show download URL for the backup file',
        )

    def handle(self, *args, **options):
        # Create backup directory
        backup_dir = settings.BASE_DIR / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        # Generate backup filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"media_backup_{timestamp}.zip"
        backup_path = backup_dir / backup_filename
        
        # Create backup archive
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all media files
            media_root = settings.MEDIA_ROOT
            if os.path.exists(media_root):
                for root, dirs, files in os.walk(media_root):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, media_root)
                        zipf.write(file_path, arcname)
                        
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Added media files to backup')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠ No media directory found')
                )
            
            # Create backup info file
            backup_info = {
                'created_at': datetime.now().isoformat(),
                'total_files': len(zipf.namelist()),
                'backup_type': 'media_files',
                'instructions': [
                    '1. Download this backup file',
                    '2. After deployment, extract it to your media folder',
                    '3. Run: python manage.py restore_media_backup backup_file.zip'
                ]
            }
            
            # Add backup info as JSON
            zipf.writestr('backup_info.json', json.dumps(backup_info, indent=2))
        
        # Show results
        file_size = os.path.getsize(backup_path)
        size_mb = file_size / (1024 * 1024)
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Backup created successfully!')
        )
        self.stdout.write(f'📁 File: {backup_filename}')
        self.stdout.write(f'📏 Size: {size_mb:.2f} MB')
        self.stdout.write(f'📍 Location: {backup_path}')
        self.stdout.write('\n' + '='*50)
        
        self.stdout.write('\n📋 Next Steps:')
        self.stdout.write('1. Download the backup file from your server')
        self.stdout.write('2. Keep it safe on your computer')
        self.stdout.write('3. After each deployment, upload and restore it')
        self.stdout.write('\n💡 Tip: Run this command regularly to keep backups current!')
        
        if options['download_url']:
            self.stdout.write(f'\n🔗 Download URL: {backup_path}')
