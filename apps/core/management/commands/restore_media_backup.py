from django.core.management.base import BaseCommand
from django.conf import settings
import os
import zipfile
import json
from pathlib import Path


class Command(BaseCommand):
    help = 'Restore media files from a backup archive'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='Path to the backup ZIP file to restore'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrite existing files without prompting',
        )

    def handle(self, *args, **options):
        backup_file = options['backup_file']
        
        # Check if backup file exists
        if not os.path.exists(backup_file):
            self.stdout.write(
                self.style.ERROR(f'❌ Backup file not found: {backup_file}')
            )
            return
        
        # Create media directory if it doesn't exist
        media_root = Path(settings.MEDIA_ROOT)
        media_root.mkdir(parents=True, exist_ok=True)
        
        # Extract backup
        restored_count = 0
        skipped_count = 0
        
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            # Read backup info if available
            try:
                backup_info = json.loads(zipf.read('backup_info.json'))
                self.stdout.write(f'📋 Backup created: {backup_info.get("created_at", "Unknown")}')
                self.stdout.write(f'📁 Total files: {backup_info.get("total_files", "Unknown")}')
            except:
                pass
            
            # Extract files
            for file_info in zipf.infolist():
                if file_info.filename == 'backup_info.json':
                    continue  # Skip info file
                
                # Determine destination path
                dest_path = media_root / file_info.filename
                
                # Check if file already exists
                if dest_path.exists() and not options['force']:
                    skipped_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Skipped (exists): {file_info.filename}')
                    )
                    continue
                
                # Create directory if needed
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Extract file
                with zipf.open(file_info) as source, open(dest_path, 'wb') as target:
                    target.write(source.read())
                
                restored_count += 1
                self.stdout.write(f'✓ Restored: {file_info.filename}')
        
        # Show results
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Restore completed!')
        )
        self.stdout.write(f'✓ Files restored: {restored_count}')
        self.stdout.write(f'⚠ Files skipped: {skipped_count}')
        self.stdout.write('\n' + '='*50)
        
        if skipped_count > 0:
            self.stdout.write('\n💡 Tip: Use --force to overwrite existing files')
        
        self.stdout.write('\n🎯 Your media files are now restored and ready to use!')
