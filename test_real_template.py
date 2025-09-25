#!/usr/bin/env python3
"""
Test real template rendering to see what's happening
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business_app.settings')
django.setup()

from django.template.loader import render_to_string
from django.template import RequestContext
from django.test import RequestFactory
from apps.core.utils import get_company_context
from apps.accounts.models import User

def test_real_template():
    print("🧪 TESTING REAL TEMPLATE RENDERING")
    print("=" * 60)
    
    try:
        # Get user and context
        user = User.objects.get(email='ubanghasteve@gmail.com')
        company_context = get_company_context(user)
        
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/')
        request.user = user
        
        # Test invoice detail template
        print("Testing invoice detail template...")
        try:
            # Get an invoice if it exists
            from apps.invoices.models import Invoice
            invoice = Invoice.objects.first()
            
            if invoice:
                from apps.invoices.views import get_invoice_context
                context = get_invoice_context(invoice, user)
                context.update(company_context)
                
                # Test rendering
                html = render_to_string('invoices/invoice_detail.html', context, request=request)
                
                # Check if images are in the HTML
                if 'raw.githubusercontent.com' in html:
                    print("✅ GitHub URLs found in rendered HTML")
                    if 'company_logo' in html and 'raw.githubusercontent.com' in html:
                        print("✅ Company logo URLs found")
                    if 'company_signature' in html and 'raw.githubusercontent.com' in html:
                        print("✅ Company signature URLs found")
                else:
                    print("❌ No GitHub URLs found in rendered HTML")
                    print("HTML snippet:", html[:500])
            else:
                print("No invoices found to test")
                
        except Exception as e:
            print(f"Error testing invoice template: {e}")
        
        # Test waybill detail template
        print("\nTesting waybill detail template...")
        try:
            from apps.waybills.models import Waybill
            waybill = Waybill.objects.first()
            
            if waybill:
                from apps.waybills.views import get_waybill_context
                context = get_waybill_context(waybill, user)
                context.update(company_context)
                
                # Test rendering
                html = render_to_string('waybills/waybill_detail.html', context, request=request)
                
                # Check if images are in the HTML
                if 'raw.githubusercontent.com' in html:
                    print("✅ GitHub URLs found in waybill HTML")
                else:
                    print("❌ No GitHub URLs found in waybill HTML")
                    print("HTML snippet:", html[:500])
            else:
                print("No waybills found to test")
                
        except Exception as e:
            print(f"Error testing waybill template: {e}")
        
        # Test a simple template with just the context
        print("\nTesting simple template with company context...")
        simple_template = """
        {% load media_utils %}
        <div>
            <h2>Company Information</h2>
            <p>Company: {{ company_profile.company_name }}</p>
            
            {% if company_logo %}
                <img src="{{ company_logo|cache_bust }}" alt="Logo" style="max-width: 200px;">
                <p>Logo URL: {{ company_logo|cache_bust }}</p>
            {% else %}
                <p>No logo available</p>
            {% endif %}
            
            {% if company_signature %}
                <img src="{{ company_signature|cache_bust }}" alt="Signature" style="max-width: 200px;">
                <p>Signature URL: {{ company_signature|cache_bust }}</p>
            {% else %}
                <p>No signature available</p>
            {% endif %}
        </div>
        """
        
        from django.template import Template, Context
        template = Template(simple_template)
        context_obj = Context(company_context)
        html = template.render(context_obj)
        
        print("Simple template HTML:")
        print(html)
        
        if 'raw.githubusercontent.com' in html:
            print("✅ Simple template is working correctly!")
        else:
            print("❌ Simple template has issues")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_template()
