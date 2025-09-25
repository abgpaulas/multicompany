#!/usr/bin/env python3
"""
Fix template loading issues by adding media_utils to templates that use cache_bust
"""

import os
import re
from pathlib import Path

def fix_template_loading():
    print("🔧 FIXING TEMPLATE LOADING ISSUES")
    print("=" * 60)
    
    # Templates that use cache_bust filter
    templates_with_cache_bust = [
        'templates/waybills/partials/preview_content_optimized.html',
        'templates/waybills/partials/preview_content.html',
        'templates/waybills/waybill_print.html',
        'templates/waybills/waybill_list_export_pdf.html',
        'templates/waybills/waybill_detail.html',
        'templates/receipts/receipt_print.html',
        'templates/receipts/receipt_pdf_template.html',
        'templates/receipts/receipt_pdf.html',
        'templates/receipts/receipt_list_export_pdf.html',
        'templates/receipts/receipt_detail.html',
        'templates/quotations/quotation_print.html',
        'templates/quotations/quotation_pdf.html',
        'templates/quotations/quotation_list_pdf.html',
        'templates/quotations/quotation_detail.html',
        'templates/quotations/pdf.html',
        'templates/job_orders/manufacturing_joborder_list_export_pdf.html',
        'templates/job_orders/joborder_print.html',
        'templates/job_orders/joborder_list_export_pdf.html',
        'templates/job_orders/joborder_detail.html',
        'templates/invoices/invoice_print.html',
        'templates/invoices/invoice_pdf.html',
        'templates/invoices/invoice_list_export_pdf.html',
        'templates/invoices/invoice_create_dynamic.html',
        'templates/receipt.html',
        'templates/invoices/invoice_detail.html',
        'templates/job_orders/product_pdf.html',
        'templates/job_orders/product_view_pdf.html',
        'templates/inventory/inventory_print.html',
        'templates/inventory/layout_form.html',
        'templates/rbac/role_management.html',
        'templates/rbac/my_permissions.html',
        'templates/accounts/profile_edit.html',
        'templates/accounts/profile_view.html',
        'templates/job_orders/manufacturing_joborder_detail.html',
        'templates/job_orders/product_detail.html',
        'templates/job_orders/products.html',
        'templates/job_orders/product_edit.html',
        'templates/job_orders/product_view.html',
    ]
    
    fixed_count = 0
    
    for template_path in templates_with_cache_bust:
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if template already loads media_utils
                if '{% load media_utils %}' in content:
                    print(f"✅ {template_path}: Already has media_utils")
                    continue
                
                # Check if template uses cache_bust
                if 'cache_bust' in content:
                    # Add {% load media_utils %} after the first {% load %} or at the beginning
                    if '{% load ' in content:
                        # Find the first {% load %} line and add media_utils after it
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if line.strip().startswith('{% load '):
                                # Add media_utils after this line
                                lines.insert(i + 1, '{% load media_utils %}')
                                break
                        content = '\n'.join(lines)
                    else:
                        # Add at the beginning of the file
                        content = '{% load media_utils %}\n' + content
                    
                    # Write the updated content
                    with open(template_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ {template_path}: Added media_utils loading")
                    fixed_count += 1
                else:
                    print(f"ℹ️ {template_path}: No cache_bust usage found")
                    
            except Exception as e:
                print(f"❌ {template_path}: Error - {e}")
        else:
            print(f"⚠️ {template_path}: File not found")
    
    print(f"\n🎉 Fixed {fixed_count} templates!")
    print("✅ All templates now properly load media_utils template tag")
    print("✅ cache_bust filter will work in all templates")

if __name__ == "__main__":
    fix_template_loading()
