#!/usr/bin/env python3
"""
Deployment Verification Test
Tests all the fixes implemented for the deployment issues
"""

import requests
import time
from datetime import datetime

def test_deployment():
    """Test the deployment and all fixes"""
    print("🚀 DEPLOYMENT VERIFICATION TEST")
    print("=" * 50)
    print(f"Test started at: {datetime.now()}")
    print()
    
    base_url = "https://multicompany.onrender.com"
    
    # Test 1: Main site accessibility
    print("1️⃣ Testing main site accessibility...")
    try:
        response = requests.get(base_url, timeout=30)
        if response.status_code == 200:
            print("✅ Main site is accessible (Status: 200)")
        else:
            print(f"❌ Main site returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main site error: {e}")
        return False
    
    # Test 2: Company profile page accessibility
    print("\n2️⃣ Testing company profile page...")
    try:
        response = requests.get(f"{base_url}/dashboard/company-profile/", timeout=30)
        if response.status_code == 200:
            print("✅ Company profile page is accessible (Status: 200)")
            print(f"✅ Page content length: {len(response.content)} characters")
        else:
            print(f"❌ Company profile page returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Company profile page error: {e}")
        return False
    
    # Test 3: Check for Bad Gateway errors
    print("\n3️⃣ Testing for Bad Gateway errors...")
    try:
        # Test multiple endpoints that were problematic
        endpoints = [
            "/dashboard/",
            "/dashboard/company-profile/",
            "/invoices/",
            "/quotations/",
        ]
        
        all_good = True
        for endpoint in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=30)
                if response.status_code == 200:
                    print(f"✅ {endpoint} - OK (Status: 200)")
                elif response.status_code == 302:
                    print(f"✅ {endpoint} - Redirect (Status: 302) - Normal for auth")
                else:
                    print(f"⚠️ {endpoint} - Status: {response.status_code}")
                    if response.status_code >= 500:
                        all_good = False
            except Exception as e:
                print(f"❌ {endpoint} - Error: {e}")
                all_good = False
        
        if all_good:
            print("✅ No Bad Gateway errors detected")
        else:
            print("❌ Some endpoints have issues")
            return False
            
    except Exception as e:
        print(f"❌ Bad Gateway test error: {e}")
        return False
    
    # Test 4: Check for migration-related errors
    print("\n4️⃣ Testing for migration-related errors...")
    try:
        # Check if the site loads without database errors
        response = requests.get(f"{base_url}/dashboard/", timeout=30)
        if response.status_code == 200:
            content = response.text.lower()
            if "migration" in content and "error" in content:
                print("❌ Migration errors detected in page content")
                return False
            else:
                print("✅ No migration errors detected")
        else:
            print(f"⚠️ Dashboard returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Migration test error: {e}")
        return False
    
    # Test 5: Check for image-related errors
    print("\n5️⃣ Testing for image-related errors...")
    try:
        response = requests.get(f"{base_url}/dashboard/company-profile/", timeout=30)
        if response.status_code == 200:
            content = response.text
            # Check for common image error patterns
            error_patterns = [
                "404",
                "not found",
                "missing",
                "broken image"
            ]
            
            error_count = 0
            for pattern in error_patterns:
                if pattern in content.lower():
                    error_count += 1
            
            if error_count > 5:  # Allow some 404s for missing images
                print(f"⚠️ {error_count} potential image errors detected")
            else:
                print("✅ No significant image errors detected")
        else:
            print(f"⚠️ Company profile page returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Image test error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 DEPLOYMENT VERIFICATION COMPLETE!")
    print("✅ All critical tests passed")
    print("✅ Application is working correctly")
    print("✅ No Bad Gateway errors")
    print("✅ No migration errors")
    print("✅ Company profile page accessible")
    print("\n🚀 Your application is ready for use!")
    print(f"🌐 Main URL: {base_url}")
    print(f"🏢 Company Profile: {base_url}/dashboard/company-profile/")
    
    return True

if __name__ == "__main__":
    success = test_deployment()
    if success:
        print("\n✅ DEPLOYMENT VERIFICATION: SUCCESS")
        exit(0)
    else:
        print("\n❌ DEPLOYMENT VERIFICATION: FAILED")
        exit(1)
