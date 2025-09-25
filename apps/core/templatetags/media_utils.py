from django import template
from django.utils.safestring import mark_safe
import time

register = template.Library()


@register.filter
def cache_bust(url):
    """
    Add cache-busting parameter to any URL
    Usage: {{ image_url|cache_bust }}
    """
    if not url:
        return url
    
    try:
        # Add cache-busting parameter using current timestamp
        cache_bust = int(time.time())
        separator = '&' if '?' in url else '?'
        return f"{url}{separator}v={cache_bust}"
    except Exception:
        return url


@register.filter
def media_url_with_bust(media_field):
    """
    Get media URL with cache-busting parameter
    Usage: {{ company.logo|media_url_with_bust }}
    """
    if not media_field:
        return None
    
    try:
        if hasattr(media_field, 'name') and media_field.name:
            base_url = media_field.url
            # Add cache-busting parameter using current timestamp
            cache_bust = int(time.time())
            separator = '&' if '?' in base_url else '?'
            return f"{base_url}{separator}v={cache_bust}"
        else:
            return None
    except Exception:
        return None


@register.filter
def safe_media_url(media_field):
    """
    Safely get media URL, return None if file doesn't exist
    Usage: {{ company.logo|safe_media_url }}
    """
    if not media_field:
        return None
    
    try:
        if hasattr(media_field, 'name') and media_field.name:
            return media_field.url
        else:
            return None
    except Exception:
        return None