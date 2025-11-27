# Cloudflare Manager - API Reference

Complete reference for all classes and methods in the Cloudflare Manager.

## Table of Contents

1. [Classes](#classes)
   - [CloudflareAccount](#cloudflareaccount)
   - [CloudflareManager](#cloudflaremanager)
   - [MultiAccountManager](#multiaccountmanager)
2. [Methods](#methods)
   - [Pages Operations](#pages-operations)
   - [Domain Operations](#domain-operations)
   - [Zone Operations](#zone-operations)
   - [Worker Operations](#worker-operations)

---

## Classes

### CloudflareAccount

Data class representing a Cloudflare account.

#### Constructor

```python
CloudflareAccount(email: str, token: str, account_id: Optional[str] = None, name: Optional[str] = None)
```

**Parameters:**
- `email` (str): Cloudflare account email
- `token` (str): API token with appropriate permissions
- `account_id` (Optional[str]): Account ID (auto-detected if not provided)
- `name` (Optional[str]): Account name for reference

**Example:**

```python
account = CloudflareAccount(
    email="user@example.com",
    token="your-api-token"
)
```

---

### CloudflareManager

Main class for interacting with Cloudflare API.

#### Constructor

```python
CloudflareManager(account: CloudflareAccount)
```

**Parameters:**
- `account` (CloudflareAccount): Account configuration

**Example:**

```python
account = CloudflareAccount(email="user@example.com", token="token")
cf = CloudflareManager(account)
```

---

### MultiAccountManager

Manager for handling multiple Cloudflare accounts.

#### Constructor

```python
MultiAccountManager()
```

#### Methods

##### add_account()

Add a Cloudflare account to the manager.

```python
add_account(name: str, email: str, token: str, account_id: Optional[str] = None) -> CloudflareManager
```

**Parameters:**
- `name` (str): Unique name for this account
- `email` (str): Cloudflare account email
- `token` (str): API token
- `account_id` (Optional[str]): Account ID

**Returns:** CloudflareManager instance

**Example:**

```python
manager = MultiAccountManager()
cf = manager.add_account("primary", "user@example.com", "token")
```

##### get_account()

Get a specific account manager by name.

```python
get_account(name: str) -> Optional[CloudflareManager]
```

**Parameters:**
- `name` (str): Account name

**Returns:** CloudflareManager instance or None

##### list_accounts()

List all configured account names.

```python
list_accounts() -> List[str]
```

**Returns:** List of account names

---

## Methods

### Pages Operations

#### create_pages_project()

Create a new Pages project.

```python
create_pages_project(project_name: str, production_branch: str = "main") -> Optional[Dict]
```

**Parameters:**
- `project_name` (str): Name of the Pages project
- `production_branch` (str): Git branch for production (default: "main")

**Returns:** Project details dict or None

**Example:**

```python
project = cf.create_pages_project("my-website", "main")
print(f"Project URL: https://{project['subdomain']}")
```

---

#### deploy_pages_project()

Deploy a Pages project from a local directory.

```python
deploy_pages_project(
    project_name: str, 
    directory: str, 
    branch: str = "main",
    commit_message: str = "Deploy via API"
) -> Optional[Dict]
```

**Parameters:**
- `project_name` (str): Name of the Pages project
- `directory` (str): Path to directory containing static files
- `branch` (str): Git branch name (default: "main")
- `commit_message` (str): Commit message for deployment

**Returns:** Deployment details dict or None

**Example:**

```python
deployment = cf.deploy_pages_project(
    project_name="my-website",
    directory="./dist",
    branch="main",
    commit_message="Deploy v1.0"
)
print(f"Deployed to: {deployment['url']}")
```

**Notes:**
- All files in the directory will be uploaded
- Maximum file size: 25MB per file
- Automatically generates manifest with SHA256 hashes

---

#### list_pages_projects()

List all Pages projects.

```python
list_pages_projects() -> List[Dict]
```

**Returns:** List of project dicts

**Example:**

```python
projects = cf.list_pages_projects()
for project in projects:
    print(f"{project['name']}: {project['subdomain']}")
```

---

#### get_pages_project()

Get details of a specific Pages project.

```python
get_pages_project(project_name: str) -> Optional[Dict]
```

**Parameters:**
- `project_name` (str): Name of the project

**Returns:** Project details dict or None

---

#### list_pages_deployments()

List all deployments for a Pages project.

```python
list_pages_deployments(project_name: str) -> List[Dict]
```

**Parameters:**
- `project_name` (str): Name of the project

**Returns:** List of deployment dicts

**Example:**

```python
deployments = cf.list_pages_deployments("my-website")
for deployment in deployments:
    print(f"Deployment: {deployment['id']} - {deployment['url']}")
```

---

### Domain Operations

#### add_pages_domain()

Add a custom domain to a Pages project.

```python
add_pages_domain(project_name: str, domain_name: str) -> Optional[Dict]
```

**Parameters:**
- `project_name` (str): Name of the Pages project
- `domain_name` (str): Domain to add (e.g., "example.com")

**Returns:** Domain details dict or None

**Example:**

```python
result = cf.add_pages_domain("my-website", "example.com")
print(f"Domain status: {result['status']}")

# Check if validation is needed
if result.get('validation_data'):
    val = result['validation_data']
    print(f"Add DNS record: {val['type']} {val['name']} = {val['value']}")
```

**Response Fields:**
- `name`: Domain name
- `status`: Status (e.g., "pending", "active")
- `validation_data`: DNS validation record (if needed)
  - `type`: Record type (e.g., "TXT", "CNAME")
  - `name`: Record name
  - `value`: Record value

---

#### list_pages_domains()

List all domains for a Pages project.

```python
list_pages_domains(project_name: str) -> List[Dict]
```

**Parameters:**
- `project_name` (str): Name of the project

**Returns:** List of domain dicts

---

#### get_pages_domain()

Get details of a specific domain on a Pages project.

```python
get_pages_domain(project_name: str, domain_name: str) -> Optional[Dict]
```

**Parameters:**
- `project_name` (str): Name of the project
- `domain_name` (str): Domain name

**Returns:** Domain details dict or None

---

### Zone Operations

#### create_zone()

Create a new DNS zone (add domain to Cloudflare).

```python
create_zone(domain_name: str, zone_type: str = "full") -> Optional[Dict]
```

**Parameters:**
- `domain_name` (str): Domain name (e.g., "example.com")
- `zone_type` (str): Zone type (default: "full")

**Returns:** Zone details dict or None

**Example:**

```python
zone = cf.create_zone("example.com")
print(f"Zone ID: {zone['id']}")
print("Nameservers:")
for ns in zone['name_servers']:
    print(f"  {ns}")
```

**Response Fields:**
- `id`: Zone ID
- `name`: Domain name
- `status`: Zone status
- `name_servers`: List of Cloudflare nameservers

---

#### list_zones()

List all zones in the account.

```python
list_zones() -> List[Dict]
```

**Returns:** List of zone dicts

**Example:**

```python
zones = cf.list_zones()
for zone in zones:
    print(f"{zone['name']} (ID: {zone['id']})")
```

---

#### get_zone()

Get details of a specific zone by ID.

```python
get_zone(zone_id: str) -> Optional[Dict]
```

**Parameters:**
- `zone_id` (str): Zone ID

**Returns:** Zone details dict or None

---

#### get_zone_by_name()

Get zone details by domain name.

```python
get_zone_by_name(domain_name: str) -> Optional[Dict]
```

**Parameters:**
- `domain_name` (str): Domain name

**Returns:** Zone details dict or None

**Example:**

```python
zone = cf.get_zone_by_name("example.com")
if zone:
    print(f"Zone ID: {zone['id']}")
```

---

#### get_nameservers()

Get nameservers for a domain.

```python
get_nameservers(domain_name: str) -> Optional[List[str]]
```

**Parameters:**
- `domain_name` (str): Domain name

**Returns:** List of nameserver strings or None

**Example:**

```python
nameservers = cf.get_nameservers("example.com")
if nameservers:
    print("Add these nameservers to your domain registrar:")
    for ns in nameservers:
        print(f"  {ns}")
```

---

### Worker Operations

#### create_worker_route()

Create a worker route on a zone.

```python
create_worker_route(zone_id: str, pattern: str, script_name: str) -> Optional[Dict]
```

**Parameters:**
- `zone_id` (str): Zone ID
- `pattern` (str): Route pattern (e.g., "example.com/api/*")
- `script_name` (str): Worker script name

**Returns:** Route details dict or None

**Example:**

```python
route = cf.create_worker_route(
    zone_id="zone-id-here",
    pattern="example.com/api/*",
    script_name="api-worker"
)
print(f"Route created: {route['id']}")
```

---

#### list_worker_routes()

List all worker routes for a zone.

```python
list_worker_routes(zone_id: str) -> List[Dict]
```

**Parameters:**
- `zone_id` (str): Zone ID

**Returns:** List of route dicts

**Example:**

```python
routes = cf.list_worker_routes("zone-id")
for route in routes:
    print(f"{route['pattern']} -> {route['script']}")
```

---

#### delete_worker_route()

Delete a worker route.

```python
delete_worker_route(zone_id: str, route_id: str) -> bool
```

**Parameters:**
- `zone_id` (str): Zone ID
- `route_id` (str): Route ID

**Returns:** True if successful, False otherwise

---

#### add_worker_domain()

Add a custom domain to a worker.

```python
add_worker_domain(
    hostname: str, 
    service: str, 
    zone_id: str,
    environment: str = "production"
) -> Optional[Dict]
```

**Parameters:**
- `hostname` (str): Hostname (e.g., "api.example.com")
- `service` (str): Worker service name
- `zone_id` (str): Zone ID
- `environment` (str): Environment (default: "production")

**Returns:** Domain details dict or None

**Example:**

```python
result = cf.add_worker_domain(
    hostname="api.example.com",
    service="api-worker",
    zone_id="zone-id",
    environment="production"
)
```

---

#### list_worker_domains()

List all worker custom domains.

```python
list_worker_domains() -> List[Dict]
```

**Returns:** List of domain dicts

---

## Error Handling

All methods handle errors gracefully and return `None` or empty lists on failure. Errors are printed to stdout.

**Example:**

```python
project = cf.create_pages_project("test")
if project:
    print("Success!")
else:
    print("Failed - check error messages above")
```

## Response Format

All API methods return data in the format returned by Cloudflare's API. Common fields:

**Success Response:**
```json
{
  "success": true,
  "errors": [],
  "messages": [],
  "result": { ... }
}
```

**Error Response:**
```json
{
  "success": false,
  "errors": [
    {
      "code": 1234,
      "message": "Error description"
    }
  ],
  "messages": [],
  "result": null
}
```

## Rate Limits

Cloudflare API rate limits:
- **Standard**: 1,200 requests per 5 minutes
- **Varies by endpoint**

The manager automatically handles rate limit headers but doesn't implement retry logic.

## Authentication

All methods use Bearer token authentication via the `Authorization` header:

```
Authorization: Bearer YOUR_API_TOKEN
```

Make sure your API token has the necessary permissions for the operations you want to perform.

## Required Permissions

For full functionality, your API token should have:

- **Account Permissions:**
  - Cloudflare Pages: Edit
  - Workers Scripts: Edit

- **Zone Permissions:**
  - DNS: Edit
  - Workers Routes: Edit
  - Zone: Edit

## Additional Resources

- [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
- [Pages Documentation](https://developers.cloudflare.com/pages/)
- [Workers Documentation](https://developers.cloudflare.com/workers/)
- [DNS Documentation](https://developers.cloudflare.com/dns/)

## Version

**Current Version:** 1.0.0

**Python Compatibility:** Python 3.6+

**Dependencies:**
- requests >= 2.28.0
