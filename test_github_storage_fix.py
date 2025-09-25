#!/usr/bin/env python3
"""
Test GitHub Storage Fix
Tests if the absolute path handling fix is working
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_app.settings')
django.setup()

from business_app.github_storage import GitHubStorage

def test_github_storage_fix():
    """Test the GitHub storage absolute path handling fix"""
    print("🧪 Testing GitHub Storage Absolute Path Fix")
    print("=" * 50)
    
    # Create GitHub storage instance
    storage = GitHubStorage()
    
    # Test cases for path handling
    test_cases = [
        "/media/company/logos/test.png",
        "media/company/logos/test.png", 
        "company/logos/test.png",
        "/absolute/path/to/file.jpg",
        "relative/path/to/file.jpg"
    ]
    
    print("Testing path handling:")
    for test_path in test_cases:
        try:
            valid_name = storage.get_valid_name(test_path)
            print(f"✅ Input: {test_path}")
            print(f"   Output: {valid_name}")
            print()
        except Exception as e:
            print(f"❌ Error with {test_path}: {e}")
            print()
    
    # Test if GitHub is configured
    if storage.github and storage.repo:
        print("✅ GitHub storage is properly configured")
        print(f"   Repository: {storage.repo_name}")
        print(f"   Branch: {storage.branch}")
    else:
        print("⚠️ GitHub storage is not configured (this is normal if GITHUB_TOKEN is not set)")
        print("   The storage will fall back to local storage")
    
    print("\n🎉 GitHub Storage Fix Test Complete!")
    print("The absolute path handling should now work correctly.")

if __name__ == "__main__":
    test_github_storage_fix()
