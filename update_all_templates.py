#!/usr/bin/env python3
"""
Comprehensive Template Update Script
Updates all template files to use GitHub image URLs with cache-busting
"""

import os
import re
from pathlib import Path

def update_template_file(file_path):
    """Update a single template file"""
    print(f"Updating: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # Pattern 1: img src="{{ variable }}" -> img src="{{ variable|cache_bust }}"
        pattern1 = r'<img\s+([^>]*?)src="\{\{\s*([^}]+)\s*\}\}"([^>]*?)>'
        def replace_img_src(match):
            before_src = match.group(1)
            variable = match.group(2).strip()
            after_src = match.group(3)
            
            # Skip if already has cache_bust
            if '|cache_bust' in variable:
                return match.group(0)
            
            # Skip static files
            if 'static' in variable or '{% static' in variable:
                return match.group(0)
            
            return f'<img {before_src}src="{{{{ {variable}|cache_bust }}}}"{after_src}>'
        
        new_content = re.sub(pattern1, replace_img_src, content)
        if new_content != content:
            changes_made += 1
            content = new_content
        
        # Pattern 2: background-image: url({{ variable }}) -> background-image: url({{ variable|cache_bust }})
        pattern2 = r'background-image:\s*url\(\{\{\s*([^}]+)\s*\}\}\)'
        def replace_bg_image(match):
            variable = match.group(1).strip()
            if '|cache_bust' in variable:
                return match.group(0)
            if 'static' in variable or '{% static' in variable:
                return match.group(0)
            return f'background-image: url({{{{ {variable}|cache_bust }}}})'
        
        new_content = re.sub(pattern2, replace_bg_image, content)
        if new_content != content:
            changes_made += 1
            content = new_content
        
        # Pattern 3: {{ variable }} in src attributes
        pattern3 = r'src="\{\{\s*([^}]+)\s*\}\}"'
        def replace_src(match):
            variable = match.group(1).strip()
            if '|cache_bust' in variable:
                return match.group(0)
            if 'static' in variable or '{% static' in variable:
                return match.group(0)
            return f'src="{{{{ {variable}|cache_bust }}}}"'
        
        new_content = re.sub(pattern3, replace_src, content)
        if new_content != content:
            changes_made += 1
            content = new_content
        
        # Add media_utils load if not present and we made changes
        if changes_made > 0:
            if '{% load media_utils %}' not in content:
                # Find the first {% load %} statement and add after it
                load_pattern = r'({% load [^%]+%})'
                match = re.search(load_pattern, content)
                if match:
                    content = content.replace(match.group(1), f"{match.group(1)}\n{{% load media_utils %}}")
                else:
                    # Add at the beginning after extends
                    extends_pattern = r'({% extends [^%]+%})'
                    match = re.search(extends_pattern, content)
                    if match:
                        content = content.replace(match.group(1), f"{match.group(1)}\n{{% load media_utils %}}")
                    else:
                        # Add at the very beginning
                        content = "{% load media_utils %}\n" + content
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Updated {changes_made} image references")
            return True
        else:
            print(f"  ⏭️ No changes needed")
            return False
            
    except Exception as e:
        print(f"  ❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to update all templates"""
    print("🔄 Updating all template files for GitHub image support...")
    print("=" * 60)
    
    # Find all template files
    template_dirs = [
        'templates',
        'apps/core/templates',
        'apps/accounts/templates',
        'apps/clients/templates',
        'apps/company_management/templates',
        'apps/inventory/templates',
        'apps/invoices/templates',
        'apps/job_orders/templates',
        'apps/quotations/templates',
        'apps/rbac/templates',
        'apps/receipts/templates',
        'apps/waybills/templates',
    ]
    
    updated_files = 0
    total_files = 0
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            print(f"\n📁 Processing {template_dir}/")
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        total_files += 1
                        if update_template_file(file_path):
                            updated_files += 1
    
    print("\n" + "=" * 60)
    print(f"🎉 Template update completed!")
    print(f"📊 Total files processed: {total_files}")
    print(f"✅ Files updated: {updated_files}")
    print(f"⏭️ Files unchanged: {total_files - updated_files}")
    
    if updated_files > 0:
        print("\n🚀 All templates now support GitHub image URLs with cache-busting!")
        print("📝 Changes include:")
        print("   - Added |cache_bust filter to all image URLs")
        print("   - Added {% load media_utils %} where needed")
        print("   - Updated img src attributes")
        print("   - Updated background-image URLs")
    else:
        print("\n✨ All templates were already up to date!")

if __name__ == "__main__":
    main()
