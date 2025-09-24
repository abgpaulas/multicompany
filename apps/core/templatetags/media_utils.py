from django import template
from django.conf import settings
import os

register = template.Library()

@register.filter
def safe_media_url(media_field):
    """
    Safely get media URL, return None if file doesn't exist
    """
    if not media_field:
        return None
    
    try:
        # Check if file exists
        if hasattr(media_field, 'path') and os.path.exists(media_field.path):
            return media_field.url
        elif hasattr(media_field, 'name') and media_field.name:
            # For production, we can't check file existence easily
            # Just return the URL if the field has a name
            return media_field.url
        else:
            return None
    except Exception:
        return None

@register.filter
def has_media_file(media_field):
    """
    Check if media field has a valid file
    """
    if not media_field:
        return False
    
    try:
        if hasattr(media_field, 'path') and os.path.exists(media_field.path):
            return True
        elif hasattr(media_field, 'name') and media_field.name:
            return True
        else:
            return False
    except Exception:
        return False
