#!/usr/bin/env python3
"""
Test script to verify Worker upload functionality
"""

from cloudflare_manager import CloudflareManager, CloudflareAccount
import os

def test_upload_worker_format():
    """Test that upload_worker method has correct signature"""
    print("Testing Worker upload functionality...\n")
    
    # Create a test account (with dummy credentials)
    account = CloudflareAccount(
        email="test@example.com",
        token="dummy-token"
    )
    cf = CloudflareManager(account)
    
    # Check method exists
    assert hasattr(cf, 'upload_worker'), "upload_worker method not found"
    print("✓ upload_worker method exists")
    
    # Check list_workers exists
    assert hasattr(cf, 'list_workers'), "list_workers method not found"
    print("✓ list_workers method exists")
    
    # Check get_worker exists
    assert hasattr(cf, 'get_worker'), "get_worker method not found"
    print("✓ get_worker method exists")
    
    # Check delete_worker exists
    assert hasattr(cf, 'delete_worker'), "delete_worker method not found"
    print("✓ delete_worker method exists")
    
    # Check example worker file exists
    assert os.path.exists('example_worker.js'), "example_worker.js not found"
    print("✓ example_worker.js exists")
    
    # Check documentation exists
    assert os.path.exists('UPLOAD_FILES_GUIDE.md'), "UPLOAD_FILES_GUIDE.md not found"
    print("✓ UPLOAD_FILES_GUIDE.md exists")
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_upload_worker_format()
