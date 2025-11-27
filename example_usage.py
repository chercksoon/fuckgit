#!/usr/bin/env python3
"""
Example usage of Cloudflare Manager
Demonstrates key features:
1. Deploy Pages project
2. Bind domain
3. Get nameservers
4. Configure worker routes
"""

from cloudflare_manager import CloudflareManager, CloudflareAccount


def example_pages_deployment():
    """Example: Deploy a Pages project and bind a domain"""
    print("\n" + "="*60)
    print("Example 1: Deploy Pages Project with Domain")
    print("="*60)
    
    # Initialize manager
    account = CloudflareAccount(
        email="exslym@closedbyme.com",
        token="21f3fb278a15b732a4f52c95d5042d78d1a21"
    )
    cf = CloudflareManager(account)
    
    # Step 1: Create Pages project
    print("\n📝 Step 1: Creating Pages project...")
    project_name = "my-test-site"
    project = cf.create_pages_project(project_name, "main")
    
    if project:
        print(f"✓ Project URL: https://{project.get('subdomain')}")
    
    # Step 2: Deploy from current directory (with index.html)
    print("\n📦 Step 2: Deploying from directory...")
    deployment = cf.deploy_pages_project(
        project_name=project_name,
        directory=".",  # Current directory with index.html
        branch="main",
        commit_message="Initial deployment via API"
    )
    
    if deployment:
        print(f"✓ Deployment URL: {deployment.get('url')}")
    
    # Step 3: List all projects
    print("\n📋 Step 3: Listing all Pages projects...")
    projects = cf.list_pages_projects()
    for proj in projects:
        print(f"  - {proj['name']}: https://{proj.get('subdomain')}")
    
    return cf, project_name


def example_domain_and_nameservers(cf, project_name=None):
    """Example: Add domain and get nameservers"""
    print("\n" + "="*60)
    print("Example 2: Domain Binding and Nameservers")
    print("="*60)
    
    domain_name = input("\n📝 Enter a domain name to add (e.g., example.com): ").strip()
    
    if not domain_name:
        print("⚠️  Skipping domain example (no domain provided)")
        return
    
    # Step 1: Create zone to get nameservers
    print(f"\n📝 Step 1: Creating zone for {domain_name}...")
    zone = cf.create_zone(domain_name)
    
    if zone:
        nameservers = zone.get("name_servers", [])
        zone_id = zone.get("id")
        
        print(f"\n📋 Nameservers to add to your domain registrar:")
        print("="*60)
        for ns in nameservers:
            print(f"   {ns}")
        print("="*60)
        
        # Step 2: Add domain to Pages project (if project exists)
        if project_name:
            print(f"\n📝 Step 2: Adding domain to Pages project '{project_name}'...")
            result = cf.add_pages_domain(project_name, domain_name)
            
            if result:
                print(f"✓ Domain added: {result.get('name')}")
                print(f"  Status: {result.get('status')}")
                
                # Show validation info if needed
                if result.get('validation_data'):
                    val = result['validation_data']
                    print(f"\n📋 DNS Validation Required:")
                    print(f"  Type: {val.get('type')}")
                    print(f"  Name: {val.get('name')}")
                    print(f"  Value: {val.get('value')}")
        
        return zone_id
    
    return None


def example_worker_upload(cf):
    """Example: Upload a Worker script"""
    print("\n" + "="*60)
    print("Example 3: Upload Worker Script")
    print("="*60)
    
    configure = input("\n📝 Do you want to upload a worker? (y/n): ").strip().lower()
    
    if configure != 'y':
        print("⚠️  Skipping worker upload")
        return None
    
    # Upload example worker
    print("\n📤 Uploading example worker...")
    result = cf.upload_worker(
        script_name="example-worker",
        worker_file="example_worker.js"
    )
    
    if result:
        print(f"✓ Worker uploaded successfully!")
        print(f"  Worker ID: {result.get('id')}")
        return "example-worker"
    else:
        print("✗ Failed to upload worker")
        return None


def example_worker_routes(cf, zone_id=None):
    """Example: Configure worker routes"""
    print("\n" + "="*60)
    print("Example 4: Worker Routes Configuration (Optional)")
    print("="*60)
    
    if not zone_id:
        print("⚠️  No zone_id available. Skipping worker routes example.")
        print("   (You need a zone/domain first)")
        return
    
    configure = input("\n📝 Do you want to configure worker routes? (y/n): ").strip().lower()
    
    if configure != 'y':
        print("⚠️  Skipping worker routes configuration")
        return
    
    # Step 1: Get route details
    pattern = input("Enter route pattern (e.g., example.com/api/*): ").strip()
    script_name = input("Enter worker script name: ").strip()
    
    if pattern and script_name:
        # Create worker route
        print(f"\n📝 Creating worker route...")
        route = cf.create_worker_route(zone_id, pattern, script_name)
        
        if route:
            print(f"✓ Route created: {route.get('id')}")
    
    # Step 2: List all routes
    print(f"\n📋 Listing all worker routes...")
    routes = cf.list_worker_routes(zone_id)
    
    if routes:
        for route in routes:
            print(f"  - {route.get('pattern')} -> {route.get('script', 'N/A')}")
    else:
        print("  No routes found")


def example_list_zones(cf):
    """Example: List all zones"""
    print("\n" + "="*60)
    print("Example 5: List All Zones")
    print("="*60)
    
    zones = cf.list_zones()
    
    if zones:
        print(f"\n📋 Found {len(zones)} zone(s):")
        for zone in zones:
            print(f"\n  Domain: {zone['name']}")
            print(f"  Zone ID: {zone['id']}")
            print(f"  Status: {zone.get('status', 'unknown')}")
            
            nameservers = zone.get("name_servers", [])
            if nameservers:
                print(f"  Nameservers:")
                for ns in nameservers:
                    print(f"    - {ns}")
    else:
        print("  No zones found")


def main():
    """Run all examples"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     Cloudflare Manager - Example Usage                  ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    print("This script demonstrates the key features:")
    print("  1. Deploy Pages project")
    print("  2. Bind domain and get nameservers")
    print("  3. Upload Worker script")
    print("  4. Configure worker routes (optional)")
    print("  5. List all zones")
    
    proceed = input("\nDo you want to proceed? (y/n): ").strip().lower()
    
    if proceed != 'y':
        print("\n👋 Exiting...")
        return
    
    # Example 1: Pages deployment
    cf, project_name = example_pages_deployment()
    
    # Example 2: Domain and nameservers
    zone_id = example_domain_and_nameservers(cf, project_name)
    
    # Example 3: Upload Worker
    worker_name = example_worker_upload(cf)
    
    # Example 4: Worker routes (optional)
    example_worker_routes(cf, zone_id)
    
    # Example 5: List zones
    example_list_zones(cf)
    
    print("\n" + "="*60)
    print("✓ All examples completed!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Update nameservers at your domain registrar")
    print("  2. Wait for DNS propagation (5-30 minutes)")
    print("  3. Your site will be live!")
    if worker_name:
        print(f"  4. Your worker is accessible at: https://{worker_name}.<account>.workers.dev")


if __name__ == "__main__":
    main()
