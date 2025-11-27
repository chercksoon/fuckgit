#!/usr/bin/env python3
"""
Quick Start Script for Cloudflare Manager
This script provides the fastest way to:
1. Deploy a Pages project
2. Bind a domain
3. Get nameservers
"""

import sys
from cloudflare_manager import CloudflareManager, CloudflareAccount


def quickstart():
    """Quick start deployment"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     Cloudflare Manager - Quick Start                    ║
║     Deploy Pages + Bind Domain + Get Nameservers        ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Configuration
    print("\n📝 Configuration")
    print("="*60)
    
    email = input("Cloudflare Email: ").strip()
    token = input("Cloudflare API Token: ").strip()
    
    if not email or not token:
        print("✗ Email and Token are required!")
        return
    
    print("\n📝 Project Information")
    print("="*60)
    
    project_name = input("Pages Project Name: ").strip()
    directory = input("Directory to deploy (default: .): ").strip() or "."
    domain = input("Domain to bind (optional): ").strip()
    
    if not project_name:
        print("✗ Project name is required!")
        return
    
    # Initialize
    print("\n🔧 Initializing Cloudflare Manager...")
    account = CloudflareAccount(email=email, token=token)
    cf = CloudflareManager(account)
    
    # Step 1: Create project
    print(f"\n📝 Step 1/4: Creating Pages project '{project_name}'...")
    project = cf.create_pages_project(project_name, "main")
    
    if not project:
        print("✗ Failed to create project")
        return
    
    print(f"✓ Project created: https://{project.get('subdomain')}")
    
    # Step 2: Deploy
    print(f"\n📦 Step 2/4: Deploying from '{directory}'...")
    deployment = cf.deploy_pages_project(
        project_name=project_name,
        directory=directory,
        branch="main",
        commit_message="Quickstart deployment"
    )
    
    if not deployment:
        print("✗ Failed to deploy")
        return
    
    print(f"✓ Deployed: {deployment.get('url')}")
    
    # Step 3: Domain (if provided)
    zone_id = None
    if domain:
        print(f"\n🌐 Step 3/4: Setting up domain '{domain}'...")
        
        # Create zone
        zone = cf.create_zone(domain)
        if zone:
            zone_id = zone.get("id")
            nameservers = zone.get("name_servers", [])
            
            print(f"\n📋 Nameservers (add these to your domain registrar):")
            print("="*60)
            for ns in nameservers:
                print(f"   {ns}")
            print("="*60)
            
            # Bind to Pages
            result = cf.add_pages_domain(project_name, domain)
            if result:
                print(f"✓ Domain bound to Pages project")
                
                if result.get('validation_data'):
                    val = result['validation_data']
                    print(f"\n📋 DNS Validation Record:")
                    print(f"  Type: {val.get('type')}")
                    print(f"  Name: {val.get('name')}")
                    print(f"  Value: {val.get('value')}")
    else:
        print("\n⏭️  Step 3/4: Skipping domain setup (no domain provided)")
    
    # Step 4: Summary
    print(f"\n✅ Step 4/4: Summary")
    print("="*60)
    print(f"✓ Project: {project_name}")
    print(f"✓ URL: {deployment.get('url')}")
    
    if domain:
        print(f"✓ Domain: {domain}")
        print(f"\n📝 Next steps:")
        print(f"  1. Update nameservers at your domain registrar")
        print(f"  2. Wait for DNS propagation (5-30 minutes)")
        print(f"  3. Visit https://{domain}")
    else:
        print(f"\n📝 Next steps:")
        print(f"  1. Visit {deployment.get('url')}")
        print(f"  2. (Optional) Add a custom domain later")
    
    print("="*60)
    print("\n🎉 Quickstart completed successfully!")


if __name__ == "__main__":
    try:
        quickstart()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
