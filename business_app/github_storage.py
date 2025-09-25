import os
import base64
import hashlib
from datetime import datetime
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from github import Github


class GitHubStorage(Storage):
    """
    Free GitHub-based storage for uploaded files.
    Uses GitHub repository as file storage - completely free!
    """
    
    def __init__(self):
        from decouple import config
        self.github_token = config('GITHUB_TOKEN', default='')
        self.repo_name = config('GITHUB_REPO_NAME', default='abgpaulas/multicompany')
        self.branch = config('GITHUB_BRANCH', default='master')
        
        if self.github_token:
            try:
                self.github = Github(self.github_token)
                self.repo = self.github.get_repo(self.repo_name)
                print(f"GitHub storage initialized successfully for {self.repo_name}")
            except Exception as e:
                print(f"GitHub storage initialization failed: {e}")
                self.github = None
                self.repo = None
        else:
            print("GitHub token not found, GitHub storage disabled")
            self.github = None
            self.repo = None
    
    def get_valid_name(self, name):
        """Get a valid name for the file"""
        # Handle absolute paths by converting them to relative paths
        if name.startswith('/'):
            # Remove leading slash and any absolute path components
            name = name.lstrip('/')
        
        # Ensure it starts with media/ for organization
        if not name.startswith('media/'):
            name = f"media/{name}"
        
        return name
    
    def _get_file_path(self, name):
        """Generate a unique file path in the repository"""
        return self.get_valid_name(name)
    
    def _save(self, name, content):
        """Save file to GitHub repository"""
        if not self.repo:
            # Fallback to local storage if GitHub is not configured
            print("GitHub not configured, using local storage")
            return self._save_locally(name, content)
        
        try:
            # Read file content
            file_content = content.read()
            
            # Generate unique path
            file_path = self._get_file_path(name)
            
            # Encode file content to base64
            encoded_content = base64.b64encode(file_content).decode()
            
            # Create or update file in GitHub
            try:
                # Try to get existing file
                file_obj = self.repo.get_contents(file_path, ref=self.branch)
                # Update existing file
                self.repo.update_file(
                    path=file_path,
                    message=f"Update file: {name}",
                    content=encoded_content,
                    sha=file_obj.sha,
                    branch=self.branch
                )
                print(f"Updated file in GitHub: {file_path}")
            except Exception as e:
                # File doesn't exist, create new one
                self.repo.create_file(
                    path=file_path,
                    message=f"Add file: {name}",
                    content=encoded_content,
                    branch=self.branch
                )
                print(f"Created new file in GitHub: {file_path}")
            
            # Return the relative path for Django to store in database
            print(f"File saved to GitHub: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"GitHub storage error: {e}")
            # Fallback to local storage
            return self._save_locally(name, content)
    
    def _save_locally(self, name, content):
        """Fallback to local storage"""
        # Use get_valid_name to handle absolute paths
        valid_name = self.get_valid_name(name)
        local_path = os.path.join(settings.MEDIA_ROOT, valid_name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with open(local_path, 'wb') as f:
            for chunk in content.chunks():
                f.write(chunk)
        
        return valid_name
    
    def delete(self, name):
        """Delete file from GitHub repository"""
        if not self.repo:
            return self._delete_locally(name)
        
        try:
            # Extract file path from GitHub URL
            if name.startswith('https://raw.githubusercontent.com/'):
                # Extract path from GitHub URL
                parts = name.split('/')
                repo_part = '/'.join(parts[3:5])  # username/repo
                branch = parts[5]
                file_path = '/'.join(parts[6:])    # media/date/hash_filename
                
                if repo_part == self.repo_name and branch == self.branch:
                    file_obj = self.repo.get_contents(file_path, ref=self.branch)
                    self.repo.delete_file(
                        path=file_path,
                        message=f"Delete file: {name}",
                        sha=file_obj.sha,
                        branch=self.branch
                    )
        except Exception as e:
            print(f"GitHub delete error: {e}")
            # Fallback to local delete
            self._delete_locally(name)
    
    def _delete_locally(self, name):
        """Fallback to local deletion"""
        # Use get_valid_name to handle absolute paths
        valid_name = self.get_valid_name(name)
        local_path = os.path.join(settings.MEDIA_ROOT, valid_name)
        if os.path.exists(local_path):
            os.remove(local_path)
    
    def exists(self, name):
        """Check if file exists"""
        if name.startswith('https://raw.githubusercontent.com/'):
            return True  # Assume GitHub URLs exist
        # Use get_valid_name to handle absolute paths
        valid_name = self.get_valid_name(name)
        return os.path.exists(os.path.join(settings.MEDIA_ROOT, valid_name))
    
    def url(self, name):
        """Return file URL"""
        if name.startswith('https://raw.githubusercontent.com/'):
            return name  # Already a full URL
        elif name.startswith('media/') or '/' in name:
            # This is a GitHub path, construct the full URL
            # Add 'media/' prefix if not present
            if not name.startswith('media/'):
                name = f"media/{name}"
            return f"https://raw.githubusercontent.com/{self.repo_name}/{self.branch}/{name}"
        else:
            # Local file
            return f"{settings.MEDIA_URL}{name}"
    
    def size(self, name):
        """Get file size"""
        if name.startswith('https://raw.githubusercontent.com/'):
            # For GitHub URLs, we can't easily get size without API call
            return 0
        # Use get_valid_name to handle absolute paths
        valid_name = self.get_valid_name(name)
        local_path = os.path.join(settings.MEDIA_ROOT, valid_name)
        if os.path.exists(local_path):
            return os.path.getsize(local_path)
        return 0
    
    def open(self, name, mode='rb'):
        """Open file for reading"""
        if name.startswith('https://raw.githubusercontent.com/'):
            # For GitHub URLs, we need to download the file
            import requests
            response = requests.get(name)
            return ContentFile(response.content)
        
        # Use get_valid_name to handle absolute paths
        valid_name = self.get_valid_name(name)
        local_path = os.path.join(settings.MEDIA_ROOT, valid_name)
        return open(local_path, mode)
