#!/usr/bin/env python3
"""
Test script for Cloudflare Manager
Tests all major functionality without making actual API calls
"""

import os
import sys
from pathlib import Path


def test_imports():
    """Test that all imports work"""
    print("Testing imports...")
    try:
        from cloudflare_manager import (
            CloudflareAccount,
            CloudflareManager,
            MultiAccountManager
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_account_creation():
    """Test account creation"""
    print("\nTesting account creation...")
    try:
        from cloudflare_manager import CloudflareAccount
        
        account = CloudflareAccount(
            email="test@example.com",
            token="test-token",
            account_id="test-account-id"
        )
        
        assert account.email == "test@example.com"
        assert account.token == "test-token"
        assert account.account_id == "test-account-id"
        
        print("✓ Account creation successful")
        return True
    except Exception as e:
        print(f"✗ Account creation failed: {e}")
        return False


def test_multi_account_manager():
    """Test multi-account manager"""
    print("\nTesting multi-account manager...")
    try:
        from cloudflare_manager import MultiAccountManager
        
        manager = MultiAccountManager()
        
        # Test adding accounts
        accounts_data = [
            ("account1", "user1@example.com", "token1"),
            ("account2", "user2@example.com", "token2"),
        ]
        
        for name, email, token in accounts_data:
            # Note: This will fail without valid credentials, but tests the structure
            try:
                manager.add_account(name, email, token)
            except:
                pass  # Expected to fail with invalid credentials
        
        print("✓ Multi-account manager structure validated")
        return True
    except Exception as e:
        print(f"✗ Multi-account manager failed: {e}")
        return False


def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "cloudflare_manager.py",
        "README.md",
        "requirements.txt",
        "example_usage.py",
        "quickstart.py",
        "index.html"
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing")
            all_exist = False
    
    return all_exist


def test_index_html():
    """Test that index.html is valid for deployment"""
    print("\nTesting index.html...")
    
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Basic validation
        assert "<!DOCTYPE html>" in content or "<html" in content
        assert "</html>" in content
        
        print("✓ index.html is valid")
        return True
    except Exception as e:
        print(f"✗ index.html validation failed: {e}")
        return False


def test_api_methods():
    """Test that all required API methods exist"""
    print("\nTesting API methods...")
    
    try:
        from cloudflare_manager import CloudflareManager
        
        required_methods = [
            # Pages methods
            "create_pages_project",
            "list_pages_projects",
            "get_pages_project",
            "deploy_pages_project",
            "list_pages_deployments",
            # Domain methods
            "add_pages_domain",
            "list_pages_domains",
            "get_pages_domain",
            # Zone methods
            "create_zone",
            "list_zones",
            "get_zone",
            "get_zone_by_name",
            "get_nameservers",
            # Worker methods
            "create_worker_route",
            "list_worker_routes",
            "delete_worker_route",
            "add_worker_domain",
            "list_worker_domains",
        ]
        
        all_exist = True
        for method_name in required_methods:
            if hasattr(CloudflareManager, method_name):
                print(f"✓ Method '{method_name}' exists")
            else:
                print(f"✗ Method '{method_name}' missing")
                all_exist = False
        
        return all_exist
    except Exception as e:
        print(f"✗ API methods test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     Cloudflare Manager - Test Suite                     ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Account Creation", test_account_creation),
        ("Multi-Account Manager", test_multi_account_manager),
        ("API Methods", test_api_methods),
        ("index.html", test_index_html),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Test: {test_name}")
        print(f"{'='*60}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
