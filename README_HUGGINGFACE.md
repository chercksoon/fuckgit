---
title: Cloudflare Manager
emoji: ☁️
colorFrom: orange
colorTo: yellow
sdk: gradio
sdk_version: "4.0.0"
app_file: app.py
pinned: false
license: mit
---

# Cloudflare Multi-Account Manager

🚀 A comprehensive web interface for managing Cloudflare Pages, Domains, and Workers.

## Features

✅ **Pages Management**
- Create and deploy Pages projects
- List all projects
- View deployment URLs

✅ **Domain & Nameservers**
- Create DNS zones
- Get nameservers for domain registrars
- Bind custom domains to Pages projects

✅ **Worker Routes**
- Configure worker routes
- Add custom domains to workers
- Manage route patterns

## Quick Start

### Using the Web Interface

1. Enter your Cloudflare Email and API Token
2. Click "Test Connection" to verify
3. Use the tabs to manage your resources

### Getting Your API Token

1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Create a new token with these permissions:
   - Account > Cloudflare Pages > Edit
   - Zone > DNS > Edit
   - Zone > Workers Routes > Edit
3. Copy the token and paste it in the interface

## Docker Deployment

Build and run with Docker:

```bash
# Build the image
docker build -t cloudflare-manager .

# Run the container
docker run -p 7860:7860 cloudflare-manager
```

Access at: http://localhost:7860

### With Environment Variables

```bash
docker run -p 7860:7860 \
  -e CLOUDFLARE_EMAIL="your-email@example.com" \
  -e CLOUDFLARE_TOKEN="your-api-token" \
  cloudflare-manager
```

## Hugging Face Spaces Deployment

This app is designed to run on Hugging Face Spaces:

1. Create a new Space on Hugging Face
2. Select "Gradio" as the SDK
3. Upload all files or connect to Git
4. The app will automatically deploy

### Setting Secrets in Hugging Face

For better security, set your credentials as Secrets:

1. Go to your Space settings
2. Add secrets:
   - `CLOUDFLARE_EMAIL`: Your Cloudflare email
   - `CLOUDFLARE_TOKEN`: Your API token
3. The app will automatically use these credentials

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python3 app.py
```

Access at: http://localhost:7860

## Python API

You can also use the Python API directly:

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

# Initialize
account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)

# Create Pages project
cf.create_pages_project("my-site", "main")

# Get nameservers
zone = cf.create_zone("example.com")
print(zone["name_servers"])

# Bind domain
cf.add_pages_domain("my-site", "example.com")
```

## CLI Tools

Run interactive commands:

```bash
# Quick start wizard
python3 quickstart.py

# Interactive menu
python3 cloudflare_manager.py

# Run examples
python3 example_usage.py

# Run tests
python3 test_manager.py
```

## Project Structure

```
.
├── app.py                   # Gradio web interface
├── cloudflare_manager.py    # Core library
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── quickstart.py           # CLI quick start
├── example_usage.py        # Usage examples
├── test_manager.py         # Test suite
└── docs/                   # Documentation
    ├── README.md
    ├── GET_STARTED.md
    ├── USAGE_GUIDE.md
    └── API_REFERENCE.md
```

## Documentation

- **[Quick Start Guide](GET_STARTED.md)** - Get started in 5 minutes
- **[Usage Guide](USAGE_GUIDE.md)** - Complete usage examples
- **[API Reference](API_REFERENCE.md)** - Full API documentation
- **[Project Summary](PROJECT_SUMMARY.md)** - Technical overview

## Common Use Cases

### 1. Deploy a Static Website

```python
# Create project
cf.create_pages_project("my-blog", "main")

# Deploy files
cf.deploy_pages_project("my-blog", "./public", "main")

# Add custom domain
zone = cf.create_zone("myblog.com")
cf.add_pages_domain("my-blog", "myblog.com")

# Get nameservers to set in registrar
print(zone["name_servers"])
```

### 2. Configure API Subdomain

```python
# Get zone
zone = cf.get_zone_by_name("example.com")

# Create worker route
cf.create_worker_route(
    zone_id=zone["id"],
    pattern="example.com/api/*",
    script_name="api-worker"
)

# Add custom subdomain
cf.add_worker_domain(
    hostname="api.example.com",
    service="api-worker",
    zone_id=zone["id"]
)
```

## Troubleshooting

### API Token Errors

**Error**: "Invalid request headers"

**Solution**: Make sure your API token has the correct permissions:
- Account > Cloudflare Pages > Edit
- Zone > DNS > Edit
- Zone > Workers Routes > Edit

### Zone Not Found

**Error**: "Zone not found"

**Solution**: Create the zone first:
```python
cf.create_zone("example.com")
```

### DNS Propagation

After adding a domain:
1. Update nameservers at your registrar
2. Wait 5-30 minutes for DNS propagation
3. Check status: `cf.get_zone_by_name("example.com")`

## Security

- Never commit API tokens to Git
- Use environment variables or Hugging Face Secrets
- Rotate tokens regularly
- Use least-privilege permissions

## Support

- 📖 Full documentation in the `/docs` folder
- 🐛 Report issues on GitHub
- 💬 Ask questions in Hugging Face Discussions

## License

MIT License - Free to use and modify

## Credits

Built with:
- Python 3.10+
- Gradio for the web interface
- Cloudflare API
- Docker for containerization

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-27  
**Status**: ✅ Production Ready
