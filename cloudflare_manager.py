#!/usr/bin/env python3
"""
Cloudflare Multi-Account Manager
Supports:
- Managing multiple Cloudflare accounts
- Deploying Pages projects
- Binding domains to Pages projects
- Getting nameservers
- Configuring worker routes
"""

import os
import sys
import json
import requests
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class CloudflareAccount:
    """Cloudflare account configuration"""
    email: str
    token: str
    account_id: Optional[str] = None
    name: Optional[str] = None
    use_api_key: bool = True  # True = API Key (X-Auth-Key), False = API Token (Bearer)


class CloudflareManager:
    """Manager for Cloudflare API operations"""
    
    BASE_URL = "https://api.cloudflare.com/client/v4"
    
    def __init__(self, account: CloudflareAccount):
        self.account = account
        self.session = requests.Session()
        
        # Support both API Key and API Token authentication
        if account.use_api_key:
            # API Key authentication (X-Auth-Email + X-Auth-Key)
            self.session.headers.update({
                "X-Auth-Email": account.email,
                "X-Auth-Key": account.token,
                "Content-Type": "application/json"
            })
        else:
            # API Token authentication (Bearer)
            self.session.headers.update({
                "Authorization": f"Bearer {account.token}",
                "Content-Type": "application/json"
            })
        
        # Auto-fetch account_id if not provided
        if not self.account.account_id:
            self._fetch_account_id()
    
    def _fetch_account_id(self):
        """Fetch the account ID for the authenticated user"""
        response = self.session.get(f"{self.BASE_URL}/accounts")
        data = self._handle_response(response)
        
        if data and data.get("result"):
            accounts = data["result"]
            if accounts:
                self.account.account_id = accounts[0]["id"]
                self.account.name = accounts[0].get("name", "Unknown")
                print(f"✓ Auto-detected account: {self.account.name} ({self.account.account_id})")
    
    def _handle_response(self, response: requests.Response) -> Dict:
        """Handle API response and check for errors"""
        try:
            data = response.json()
        except json.JSONDecodeError:
            print(f"✗ Failed to parse response: {response.text}")
            return {}
        
        if not data.get("success", False):
            errors = data.get("errors", [])
            print(f"✗ API Error: {errors}")
            return {}
        
        return data
    
    def list_accounts(self) -> List[Dict]:
        """List all accounts"""
        response = self.session.get(f"{self.BASE_URL}/accounts")
        data = self._handle_response(response)
        return data.get("result", [])
    
    # ==================== Pages Operations ====================
    
    def create_pages_project(self, project_name: str, production_branch: str = "main") -> Optional[Dict]:
        """Create a new Pages project"""
        url = f"{self.BASE_URL}/accounts/{self.account.account_id}/pages/projects"
        payload = {
            "name": project_name,
            "production_branch": production_branch
        }
        
        response = self.session.post(url, json=payload)
        data = self._handle_response(response)
        
        if data and data.get("result"):
            print(f"✓ Created Pages project: {project_name}")
            return data["result"]
        return None
    
    def list_pages_projects(self) -> List[Dict]:
        """List all Pages projects"""
        url = f"{self.BASE_URL}/accounts/{self.account.account_id}/pages/projects"
        response = self.session.get(url)
        data = self._handle_response(response)
        return data.get("result", [])
    
    def get_pages_project(self, project_name: str) -> Optional[Dict]:
        """Get a specific Pages project"""
        url = f"{self.BASE_URL}/accounts/{self.account.account_id}/pages/projects/{project_name}"
        response = self.session.get(url)
        data = self._handle_response(response)
        return data.get("result")
    
    def deploy_pages_project(self, project_name: str, directory: str, 
                            branch: str = "main", commit_message: str = "Deploy via API") -> Optional[Dict]:
        """Deploy a Pages project from a directory"""
        url = f"{self.BASE_URL}/accounts/{self.account.account_id}/pages/projects/{project_name}/deployments"
        
        # Build manifest and upload files
        manifest = {}
        files_to_upload = []
        
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"✗ Directory not found: {directory}")
            return None
        
        print(f"📦 Building deployment from: {directory}")
        
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(dir_path).as_posix()
                
                # Read file and calculate hash
                with open(file_path, "rb") as f:
                    content = f.read()
                    file_hash = hashlib.sha256(content).hexdigest()
                
                manifest[relative_path] = file_hash
                files_to_upload.append((relative_path, content))
        
        print(f"📄 Found {len(files_to_upload)} files to deploy")
        
        # Prepare multipart form data
        files = []
        files.append(("branch", (None, branch)))
        files.append(("commit_message", (None, commit_message)))
        files.append(("manifest", (None, json.dumps(manifest))))
        
        # Add each file
        for file_name, content in files_to_upload:
            mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
            files.append((file_name, (file_name, content, mime_type)))
        
        # Send deployment
        headers = {"Authorization": f"Bearer {self.account.token}"}
        response = requests.post(url, headers=headers, files=files)
        data = self._handle_response(response)
        
        if data and data.get("result"):
            deployment = data["result"]
            print(f"✓ Deployment created: {deployment.get('id')}")
            print(f"  URL: {deployment.get('url')}")
            print(f"  Stage: {deployment.get('stages', [{}])[0].get('name', 'unknown')}")
            return deployment
        return None
    
    def list_pages_deployments(self, project_name: str) -> List[Dict]:
        """List all deployments for a Pages project"""
        url = f"{self.BASE_URL}/accounts/{self.account.account_id}/pages/projects/{project_name}/deployments"
        response = self.session.get(url)
        data = self._handle_response(response)
        return data.get("result", [])
    
    # ==================== Domain Operations ====================
    
    def add_pages_domain(self, project_name: str, domain_name: str) -> Optional[Dict]:
        """Add a custom domain to a Pages project"""
        url = f"{self.BASE_URL}/accounts/{self.account.account_id}/pages/projects/{project_name}/domains"
        payload = {"name": domain_name}
        
        response = self.session.post(url, json=payload)
        data = self._handle_response(response)
        
        if data and data.get("result"):
            print(f"✓ Domain added to Pages project: {domain_name}")
            return data["result"]
        return None
    
    def list_pages_domains(self, project_name: str) -> List[Dict]:
        """List all domains for a Pages project"""
        url = f"{self.BASE_URL}/accounts/{self.account.account_id}/pages/projects/{project_name}/domains"
        response = self.session.get(url)
        data = self._handle_response(response)
        return data.get("result", [])
    
    def get_pages_domain(self, project_name: str, domain_name: str) -> Optional[Dict]:
        """Get details about a Pages domain"""
        url = f"{self.BASE_URL}/accounts/{self.account.account_id}/pages/projects/{project_name}/domains/{domain_name}"
        response = self.session.get(url)
        data = self._handle_response(response)
        return data.get("result")
    
    # ==================== Zone Operations ====================
    
    def create_zone(self, domain_name: str, zone_type: str = "full") -> Optional[Dict]:
        """Create a new zone (domain)"""
        url = f"{self.BASE_URL}/zones"
        payload = {
            "account": {"id": self.account.account_id},
            "name": domain_name,
            "type": zone_type
        }
        
        response = self.session.post(url, json=payload)
        data = self._handle_response(response)
        
        if data and data.get("result"):
            zone = data["result"]
            print(f"✓ Zone created: {domain_name}")
            print(f"  Zone ID: {zone.get('id')}")
            return zone
        return None
    
    def list_zones(self) -> List[Dict]:
        """List all zones"""
        url = f"{self.BASE_URL}/zones"
        response = self.session.get(url)
        data = self._handle_response(response)
        return data.get("result", [])
    
    def get_zone(self, zone_id: str) -> Optional[Dict]:
        """Get zone details"""
        url = f"{self.BASE_URL}/zones/{zone_id}"
        response = self.session.get(url)
        data = self._handle_response(response)
        return data.get("result")
    
    def get_zone_by_name(self, domain_name: str) -> Optional[Dict]:
        """Get zone by domain name"""
        zones = self.list_zones()
        for zone in zones:
            if zone.get("name") == domain_name:
                return zone
        return None
    
    def get_nameservers(self, domain_name: str) -> Optional[List[str]]:
        """Get nameservers for a domain"""
        zone = self.get_zone_by_name(domain_name)
        
        if zone:
            nameservers = zone.get("name_servers", [])
            print(f"\n📋 Nameservers for {domain_name}:")
            for ns in nameservers:
                print(f"   {ns}")
            return nameservers
        else:
            print(f"✗ Zone not found for domain: {domain_name}")
            return None
    
    # ==================== Worker Routes Operations ====================
    
    def create_worker_route(self, zone_id: str, pattern: str, script_name: str) -> Optional[Dict]:
        """Create a worker route"""
        url = f"{self.BASE_URL}/zones/{zone_id}/workers/routes"
        payload = {
            "pattern": pattern,
            "script": script_name
        }
        
        response = self.session.post(url, json=payload)
        data = self._handle_response(response)
        
        if data and data.get("result"):
            print(f"✓ Worker route created: {pattern} -> {script_name}")
            return data["result"]
        return None
    
    def list_worker_routes(self, zone_id: str) -> List[Dict]:
        """List all worker routes for a zone"""
        url = f"{self.BASE_URL}/zones/{zone_id}/workers/routes"
        response = self.session.get(url)
        data = self._handle_response(response)
        return data.get("result", [])
    
    def delete_worker_route(self, zone_id: str, route_id: str) -> bool:
        """Delete a worker route"""
        url = f"{self.BASE_URL}/zones/{zone_id}/workers/routes/{route_id}"
        response = self.session.delete(url)
        data = self._handle_response(response)
        
        if data:
            print(f"✓ Worker route deleted: {route_id}")
            return True
        return False
    
    # ==================== Worker Domains Operations ====================
    
    def add_worker_domain(self, hostname: str, service: str, zone_id: str, 
                         environment: str = "production") -> Optional[Dict]:
        """Add a custom domain to a worker"""
        url = f"{self.BASE_URL}/accounts/{self.account.account_id}/workers/domains"
        payload = {
            "hostname": hostname,
            "service": service,
            "zone_id": zone_id,
            "environment": environment
        }
        
        response = self.session.put(url, json=payload)
        data = self._handle_response(response)
        
        if data and data.get("result"):
            print(f"✓ Worker domain added: {hostname} -> {service}")
            return data["result"]
        return None
    
    def list_worker_domains(self) -> List[Dict]:
        """List all worker domains"""
        url = f"{self.BASE_URL}/accounts/{self.account.account_id}/workers/domains"
        response = self.session.get(url)
        data = self._handle_response(response)
        return data.get("result", [])


class MultiAccountManager:
    """Manager for multiple Cloudflare accounts"""
    
    def __init__(self):
        self.accounts: Dict[str, CloudflareManager] = {}
    
    def add_account(self, name: str, email: str, token: str, account_id: Optional[str] = None):
        """Add a Cloudflare account"""
        account = CloudflareAccount(email=email, token=token, account_id=account_id, name=name)
        manager = CloudflareManager(account)
        self.accounts[name] = manager
        print(f"✓ Added account: {name}")
        return manager
    
    def get_account(self, name: str) -> Optional[CloudflareManager]:
        """Get a specific account manager"""
        return self.accounts.get(name)
    
    def list_accounts(self) -> List[str]:
        """List all configured accounts"""
        return list(self.accounts.keys())


def print_banner():
    """Print application banner"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     Cloudflare Multi-Account Manager                     ║
║     Features: Pages Deploy, Domain Binding, NS Info      ║
╚══════════════════════════════════════════════════════════╝
""")


def main():
    """Main CLI interface"""
    print_banner()
    
    # Example usage
    manager = MultiAccountManager()
    
    # Add account
    print("\n📝 Adding account...")
    account_name = "primary"
    email = "exslym@closedbyme.com"
    token = "21f3fb278a15b732a4f52c95d5042d78d1a21"
    
    cf_manager = manager.add_account(account_name, email, token)
    
    if not cf_manager:
        print("✗ Failed to add account")
        return
    
    print(f"\n✓ Account configured: {account_name}")
    print(f"  Email: {email}")
    print(f"  Account ID: {cf_manager.account.account_id}")
    
    # Interactive menu
    while True:
        print("\n" + "="*60)
        print("Operations Menu:")
        print("="*60)
        print("1. List Pages Projects")
        print("2. Create Pages Project")
        print("3. Deploy Pages Project (from directory)")
        print("4. Add Domain to Pages Project")
        print("5. List Domains for Pages Project")
        print("6. Create Zone and Get Nameservers")
        print("7. Get Nameservers for Existing Domain")
        print("8. List Zones")
        print("9. Create Worker Route")
        print("10. List Worker Routes")
        print("11. Add Worker Custom Domain")
        print("0. Exit")
        print("="*60)
        
        choice = input("\nSelect operation (0-11): ").strip()
        
        if choice == "0":
            print("\n👋 Goodbye!")
            break
        
        elif choice == "1":
            print("\n📋 Listing Pages projects...")
            projects = cf_manager.list_pages_projects()
            if projects:
                for project in projects:
                    print(f"  - {project['name']} (created: {project.get('created_on', 'N/A')})")
                    print(f"    URL: https://{project.get('subdomain', 'N/A')}")
            else:
                print("  No projects found")
        
        elif choice == "2":
            project_name = input("Enter project name: ").strip()
            branch = input("Enter production branch (default: main): ").strip() or "main"
            cf_manager.create_pages_project(project_name, branch)
        
        elif choice == "3":
            project_name = input("Enter project name: ").strip()
            directory = input("Enter directory path: ").strip()
            branch = input("Enter branch (default: main): ").strip() or "main"
            commit_msg = input("Enter commit message (default: Deploy via API): ").strip() or "Deploy via API"
            cf_manager.deploy_pages_project(project_name, directory, branch, commit_msg)
        
        elif choice == "4":
            project_name = input("Enter project name: ").strip()
            domain_name = input("Enter domain name: ").strip()
            result = cf_manager.add_pages_domain(project_name, domain_name)
            if result:
                print(f"\n📋 Domain Details:")
                print(f"  Name: {result.get('name')}")
                print(f"  Status: {result.get('status')}")
                if result.get('validation_data'):
                    val = result['validation_data']
                    print(f"\n  DNS Validation Required:")
                    print(f"    Type: {val.get('type')}")
                    print(f"    Name: {val.get('name')}")
                    print(f"    Value: {val.get('value')}")
        
        elif choice == "5":
            project_name = input("Enter project name: ").strip()
            domains = cf_manager.list_pages_domains(project_name)
            if domains:
                print(f"\n📋 Domains for {project_name}:")
                for domain in domains:
                    print(f"  - {domain['name']} (status: {domain.get('status', 'unknown')})")
            else:
                print("  No domains found")
        
        elif choice == "6":
            domain_name = input("Enter domain name: ").strip()
            zone = cf_manager.create_zone(domain_name)
            if zone:
                nameservers = zone.get("name_servers", [])
                print(f"\n📋 Nameservers (add these to your domain registrar):")
                for ns in nameservers:
                    print(f"   {ns}")
        
        elif choice == "7":
            domain_name = input("Enter domain name: ").strip()
            cf_manager.get_nameservers(domain_name)
        
        elif choice == "8":
            print("\n📋 Listing zones...")
            zones = cf_manager.list_zones()
            if zones:
                for zone in zones:
                    print(f"  - {zone['name']} (ID: {zone['id']})")
                    print(f"    Status: {zone.get('status', 'unknown')}")
                    nameservers = zone.get("name_servers", [])
                    if nameservers:
                        print(f"    Nameservers: {', '.join(nameservers)}")
            else:
                print("  No zones found")
        
        elif choice == "9":
            zone_id = input("Enter zone ID: ").strip()
            pattern = input("Enter route pattern (e.g., example.com/*): ").strip()
            script_name = input("Enter worker script name: ").strip()
            cf_manager.create_worker_route(zone_id, pattern, script_name)
        
        elif choice == "10":
            zone_id = input("Enter zone ID: ").strip()
            routes = cf_manager.list_worker_routes(zone_id)
            if routes:
                print(f"\n📋 Worker routes:")
                for route in routes:
                    print(f"  - {route.get('pattern')} -> {route.get('script', 'N/A')}")
                    print(f"    ID: {route.get('id')}")
            else:
                print("  No routes found")
        
        elif choice == "11":
            hostname = input("Enter hostname (e.g., api.example.com): ").strip()
            service = input("Enter worker/service name: ").strip()
            zone_id = input("Enter zone ID: ").strip()
            environment = input("Enter environment (default: production): ").strip() or "production"
            cf_manager.add_worker_domain(hostname, service, zone_id, environment)
        
        else:
            print("✗ Invalid option")


if __name__ == "__main__":
    main()
