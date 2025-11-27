# Cloudflare Manager - Complete Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Interactive CLI](#interactive-cli)
4. [Python API Examples](#python-api-examples)
5. [Complete Workflows](#complete-workflows)
6. [Equivalent curl Commands](#equivalent-curl-commands)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install requests
```

## Quick Start

### Option 1: Quickstart Script (Recommended for Beginners)

```bash
python3 quickstart.py
```

This will guide you through:
- Creating a Pages project
- Deploying from a directory
- Binding a domain
- Getting nameservers

### Option 2: Interactive CLI

```bash
python3 cloudflare_manager.py
```

This provides a full-featured menu with all operations.

### Option 3: Example Script

```bash
python3 example_usage.py
```

This runs pre-configured examples.

## Interactive CLI

The interactive CLI provides these operations:

```
Operations Menu:
1. List Pages Projects
2. Create Pages Project
3. Deploy Pages Project (from directory)
4. Add Domain to Pages Project
5. List Domains for Pages Project
6. Create Zone and Get Nameservers
7. Get Nameservers for Existing Domain
8. List Zones
9. Create Worker Route
10. List Worker Routes
11. Add Worker Custom Domain
0. Exit
```

## Python API Examples

### 1. Basic Setup

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

# Initialize with your credentials
account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)
```

### 2. Deploy Pages Project

```python
# Create project
project = cf.create_pages_project("my-site", "main")

# Deploy from directory
deployment = cf.deploy_pages_project(
    project_name="my-site",
    directory="./public",  # Your static files directory
    branch="main",
    commit_message="Deploy via API"
)

print(f"Deployed to: {deployment['url']}")
```

### 3. Bind Domain and Get Nameservers

```python
# Create zone (adds domain to Cloudflare)
zone = cf.create_zone("example.com")
nameservers = zone["name_servers"]

print("Add these nameservers to your domain registrar:")
for ns in nameservers:
    print(f"  {ns}")

# Bind domain to Pages project
result = cf.add_pages_domain("my-site", "example.com")
print(f"Domain status: {result['status']}")

# If DNS validation is needed
if result.get("validation_data"):
    val = result["validation_data"]
    print(f"Add DNS record: {val['type']} {val['name']} = {val['value']}")
```

### 4. Configure Worker Routes

```python
# Get zone ID
zone = cf.get_zone_by_name("example.com")
zone_id = zone["id"]

# Create worker route
cf.create_worker_route(
    zone_id=zone_id,
    pattern="example.com/api/*",
    script_name="my-api-worker"
)

# Add custom domain to worker
cf.add_worker_domain(
    hostname="api.example.com",
    service="my-api-worker",
    zone_id=zone_id,
    environment="production"
)
```

## Complete Workflows

### Workflow 1: Deploy Static Website

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

# 1. Setup
account = CloudflareAccount(
    email="exslym@closedbyme.com",
    token="21f3fb278a15b732a4f52c95d5042d78d1a21"
)
cf = CloudflareManager(account)

# 2. Create and deploy
cf.create_pages_project("my-blog", "main")
cf.deploy_pages_project("my-blog", "./public", "main")

# 3. Add custom domain
zone = cf.create_zone("myblog.com")
cf.add_pages_domain("my-blog", "myblog.com")
cf.add_pages_domain("my-blog", "www.myblog.com")

print("✓ Website deployed!")
print(f"Nameservers: {zone['name_servers']}")
```

### Workflow 2: API with Custom Domain

```python
# 1. Setup (same as above)
# ...

# 2. Get zone
zone = cf.get_zone_by_name("example.com")
zone_id = zone["id"]

# 3. Configure routes
cf.create_worker_route(
    zone_id=zone_id,
    pattern="example.com/api/*",
    script_name="api-worker"
)

# 4. Add subdomain
cf.add_worker_domain(
    hostname="api.example.com",
    service="api-worker",
    zone_id=zone_id
)

print("✓ API configured at api.example.com")
```

### Workflow 3: Multiple Domains on One Project

```python
# 1. Deploy project
cf.create_pages_project("multi-domain-site", "main")
cf.deploy_pages_project("multi-domain-site", "./dist", "main")

# 2. Add multiple domains
domains = ["example.com", "www.example.com", "example.org", "www.example.org"]

for domain in domains:
    # Create zone for each root domain
    if not domain.startswith("www."):
        cf.create_zone(domain)
    
    # Bind to Pages
    cf.add_pages_domain("multi-domain-site", domain)

print("✓ All domains configured")
```

## Equivalent curl Commands

For reference, here are the equivalent curl commands for key operations:

### 1. List Accounts

```bash
curl https://api.cloudflare.com/client/v4/accounts \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

### 2. Create Pages Project

```bash
curl https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{
    "name": "my-pages-app",
    "production_branch": "main"
  }'
```

### 3. Deploy Pages Project

```bash
curl https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/deployments \
  -H 'Content-Type: multipart/form-data' \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -F branch=main \
  -F commit_message='Deploy via curl' \
  -F manifest='{"index.html": "abc123"}' \
  -F index.html=@./index.html
```

### 4. Add Domain to Pages

```bash
curl https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/domains \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{"name": "example.com"}'
```

### 5. Create Zone (Get Nameservers)

```bash
curl https://api.cloudflare.com/client/v4/zones \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{
    "account": {"id": "'$ACCOUNT_ID'"},
    "name": "example.com",
    "type": "full"
  }'
```

### 6. Get Zone Details (Including Nameservers)

```bash
curl https://api.cloudflare.com/client/v4/zones/$ZONE_ID \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

### 7. Create Worker Route

```bash
curl https://api.cloudflare.com/client/v4/zones/$ZONE_ID/workers/routes \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{
    "pattern": "example.com/*",
    "script": "my-workers-script"
  }'
```

### 8. Add Worker Custom Domain

```bash
curl https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/workers/domains \
  -X PUT \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -d '{
    "hostname": "api.example.com",
    "service": "my-worker",
    "zone_id": "'$ZONE_ID'",
    "environment": "production"
  }'
```

## Testing with Provided Credentials

Using the provided test account:

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

account = CloudflareAccount(
    email="exslym@closedbyme.com",
    token="21f3fb278a15b732a4f52c95d5042d78d1a21"
)
cf = CloudflareManager(account)

# Test 1: List existing projects
projects = cf.list_pages_projects()
print(f"Found {len(projects)} project(s)")

# Test 2: List zones
zones = cf.list_zones()
for zone in zones:
    print(f"Domain: {zone['name']}")
    print(f"Nameservers: {zone['name_servers']}")

# Test 3: Deploy current directory
cf.create_pages_project("test-deploy", "main")
cf.deploy_pages_project("test-deploy", ".", "main")
```

## Environment Variables (Optional)

You can also use environment variables:

```bash
export CLOUDFLARE_EMAIL="your-email@example.com"
export CLOUDFLARE_API_TOKEN="your-token"
```

Then in Python:

```python
import os
from cloudflare_manager import CloudflareManager, CloudflareAccount

account = CloudflareAccount(
    email=os.getenv("CLOUDFLARE_EMAIL"),
    token=os.getenv("CLOUDFLARE_API_TOKEN")
)
cf = CloudflareManager(account)
```

## Troubleshooting

### Issue: "Invalid request headers" or "Invalid format for Authorization header"

**Solution**: Check that your API token is correct and has the required permissions.

### Issue: "Zone not found"

**Solution**: The domain must first be added to Cloudflare using `create_zone()`.

### Issue: "Failed to deploy"

**Solution**: Ensure:
1. The directory exists and contains files
2. There's an `index.html` file
3. Files are not too large (25MB limit per file)

### Issue: Domain validation required

**Solution**: Add the DNS validation record shown in the response to your DNS settings.

## Advanced Usage

### Using Multiple Accounts

```python
from cloudflare_manager import MultiAccountManager

manager = MultiAccountManager()

# Add multiple accounts
manager.add_account("personal", "personal@example.com", "token1")
manager.add_account("work", "work@example.com", "token2")

# Use specific account
personal_cf = manager.get_account("personal")
work_cf = manager.get_account("work")

# Deploy to both accounts
personal_cf.deploy_pages_project("my-site", "./public", "main")
work_cf.deploy_pages_project("company-site", "./dist", "main")
```

### Batch Operations

```python
# Deploy to multiple projects
projects = ["site1", "site2", "site3"]

for project in projects:
    cf.create_pages_project(project, "main")
    cf.deploy_pages_project(project, f"./projects/{project}", "main")
    print(f"✓ Deployed {project}")
```

## API Rate Limits

Cloudflare has rate limits:
- **Standard**: 1,200 requests per 5 minutes
- **Per endpoint**: Varies

The manager handles errors gracefully, but for bulk operations, consider adding delays:

```python
import time

for project in large_project_list:
    cf.deploy_pages_project(project, f"./{project}", "main")
    time.sleep(1)  # Add 1 second delay
```

## Support

For issues or questions:
1. Check the [Cloudflare API docs](https://developers.cloudflare.com/api/)
2. Review error messages carefully
3. Ensure API token has correct permissions
4. Verify account limits (zones, projects, etc.)

## License

MIT License - Use freely in your projects!
