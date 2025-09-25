from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Test GitHub storage functionality'

    def handle(self, *args, **options):
        self.stdout.write("Testing GitHub storage...")
        
        # Check if GitHub storage is enabled
        use_github = os.getenv('USE_GITHUB', 'False').lower() == 'true'
        github_token = os.getenv('GITHUB_TOKEN')
        repo_name = os.getenv('GITHUB_REPO_NAME', 'abgpaulas/multicompany')
        
        self.stdout.write(f"USE_GITHUB: {use_github}")
        self.stdout.write(f"GITHUB_TOKEN: {'Set' if github_token else 'Not set'}")
        self.stdout.write(f"GITHUB_REPO_NAME: {repo_name}")
        
        if not use_github:
            self.stdout.write(self.style.WARNING("GitHub storage is not enabled. Set USE_GITHUB=True"))
            return
        
        if not github_token:
            self.stdout.write(self.style.ERROR("GITHUB_TOKEN is not set. Please set your GitHub Personal Access Token"))
            return
        
        # Test the storage
        try:
            from business_app.github_storage import GitHubStorage
            
            storage = GitHubStorage()
            
            # Create a test file
            test_content = ContentFile(b"Test file content for GitHub storage")
            test_filename = "test_file.txt"
            
            self.stdout.write("Uploading test file to GitHub...")
            saved_path = storage._save(test_filename, test_content)
            
            self.stdout.write(self.style.SUCCESS(f"File saved successfully: {saved_path}"))
            
            # Test URL generation
            file_url = storage.url(saved_path)
            self.stdout.write(f"File URL: {file_url}")
            
            # Test if file exists
            exists = storage.exists(saved_path)
            self.stdout.write(f"File exists: {exists}")
            
            self.stdout.write(self.style.SUCCESS("GitHub storage test completed successfully!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"GitHub storage test failed: {e}"))
            self.stdout.write("Make sure your GITHUB_TOKEN has 'repo' permissions")
