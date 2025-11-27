#!/usr/bin/env python3
"""
Test script to verify Cloudflare credentials
Tests the provided account credentials
"""

import sys
from cloudflare_manager import CloudflareManager, CloudflareAccount


def test_provided_credentials():
    """Test the provided Cloudflare credentials"""
    
    print("="*60)
    print("Cloudflare Credentials Test")
    print("="*60)
    
    # Provided credentials (API Key format)
    email = "exslym@closedbyme.com"
    token = "21f3fb278a15b732a4f52c95d5042d78d1a21"
    
    print(f"\nEmail: {email}")
    print(f"Token (API Key): {token[:10]}...{token[-10:]}")
    print(f"Auth Method: X-Auth-Email + X-Auth-Key")
    
    print("\n" + "-"*60)
    print("Test 1: Initialize Manager")
    print("-"*60)
    
    try:
        account = CloudflareAccount(email=email, token=token, use_api_key=True)
        cf = CloudflareManager(account)
        
        if cf.account.account_id:
            print(f"✓ PASS - Account initialized")
            print(f"  Account ID: {cf.account.account_id}")
            print(f"  Account Name: {cf.account.name}")
        else:
            print(f"✗ FAIL - Could not get account ID")
            print(f"  This usually means:")
            print(f"  1. The token is invalid or expired")
            print(f"  2. The token doesn't have proper permissions")
            print(f"  3. The API format has changed")
            return False
    except Exception as e:
        print(f"✗ FAIL - Exception: {e}")
        return False
    
    print("\n" + "-"*60)
    print("Test 2: List Pages Projects")
    print("-"*60)
    
    try:
        projects = cf.list_pages_projects()
        print(f"✓ PASS - Retrieved {len(projects)} project(s)")
        
        if projects:
            print(f"\nFirst 3 projects:")
            for i, project in enumerate(projects[:3], 1):
                print(f"  {i}. {project['name']}")
                print(f"     URL: https://{project.get('subdomain', 'N/A')}")
    except Exception as e:
        print(f"✗ FAIL - Exception: {e}")
    
    print("\n" + "-"*60)
    print("Test 3: List Zones")
    print("-"*60)
    
    try:
        zones = cf.list_zones()
        print(f"✓ PASS - Retrieved {len(zones)} zone(s)")
        
        if zones:
            print(f"\nFirst 3 zones:")
            for i, zone in enumerate(zones[:3], 1):
                print(f"  {i}. {zone['name']}")
                print(f"     Zone ID: {zone['id']}")
                print(f"     Status: {zone.get('status', 'unknown')}")
                
                nameservers = zone.get('name_servers', [])
                if nameservers:
                    print(f"     Nameservers: {', '.join(nameservers[:2])}")
    except Exception as e:
        print(f"✗ FAIL - Exception: {e}")
    
    print("\n" + "-"*60)
    print("Test 4: Account Capabilities")
    print("-"*60)
    
    try:
        # List accounts to verify permissions
        accounts = cf.list_accounts()
        print(f"✓ PASS - Can list accounts ({len(accounts)} found)")
        
        if accounts:
            print(f"\nAccounts accessible with this token:")
            for i, acc in enumerate(accounts[:3], 1):
                print(f"  {i}. {acc.get('name', 'N/A')}")
                print(f"     ID: {acc['id']}")
    except Exception as e:
        print(f"✗ FAIL - Exception: {e}")
    
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    if cf.account.account_id:
        print("\n✓ Credentials are working!")
        print(f"\nYou can use these credentials for:")
        print(f"  - Creating and deploying Pages projects")
        print(f"  - Managing domains and zones")
        print(f"  - Configuring worker routes")
        print(f"\nTo use in the web interface:")
        print(f"  1. Run: python3 app.py")
        print(f"  2. Open: http://localhost:7860")
        print(f"  3. Enter credentials and start managing!")
        return True
    else:
        print("\n✗ Credentials test failed")
        print(f"\nPossible issues:")
        print(f"  1. Token might be invalid or expired")
        print(f"  2. Token needs these permissions:")
        print(f"     - Account > Cloudflare Pages > Edit")
        print(f"     - Zone > DNS > Edit")
        print(f"     - Zone > Workers Routes > Edit")
        print(f"  3. Get a new token from:")
        print(f"     https://dash.cloudflare.com/profile/api-tokens")
        return False


if __name__ == "__main__":
    success = test_provided_credentials()
    sys.exit(0 if success else 1)
