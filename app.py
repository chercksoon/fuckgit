#!/usr/bin/env python3
"""
Cloudflare Manager Web Interface
For deployment on Hugging Face Spaces
"""

import gradio as gr
import os
from cloudflare_manager import CloudflareManager, CloudflareAccount


def test_connection(email, token):
    """Test Cloudflare API connection"""
    try:
        account = CloudflareAccount(email=email, token=token, use_api_key=True)
        cf = CloudflareManager(account)
        
        if cf.account.account_id:
            return f"✓ Connected!\n\nAccount: {cf.account.name}\nID: {cf.account.account_id}"
        else:
            return "✗ Failed to connect. Please check your credentials."
    except Exception as e:
        return f"✗ Error: {str(e)}"


def list_projects(email, token):
    """List all Pages projects"""
    try:
        account = CloudflareAccount(email=email, token=token, use_api_key=True)
        cf = CloudflareManager(account)
        
        projects = cf.list_pages_projects()
        
        if not projects:
            return "No projects found."
        
        result = f"Found {len(projects)} project(s):\n\n"
        for project in projects:
            result += f"📦 {project['name']}\n"
            result += f"   URL: https://{project.get('subdomain', 'N/A')}\n"
            result += f"   Created: {project.get('created_on', 'N/A')}\n\n"
        
        return result
    except Exception as e:
        return f"✗ Error: {str(e)}"


def create_project(email, token, project_name, branch):
    """Create a new Pages project"""
    try:
        account = CloudflareAccount(email=email, token=token, use_api_key=True)
        cf = CloudflareManager(account)
        
        project = cf.create_pages_project(project_name, branch)
        
        if project:
            return f"✓ Project created!\n\nName: {project['name']}\nURL: https://{project.get('subdomain')}\n"
        else:
            return "✗ Failed to create project"
    except Exception as e:
        return f"✗ Error: {str(e)}"


def list_zones(email, token):
    """List all zones"""
    try:
        account = CloudflareAccount(email=email, token=token, use_api_key=True)
        cf = CloudflareManager(account)
        
        zones = cf.list_zones()
        
        if not zones:
            return "No zones found."
        
        result = f"Found {len(zones)} zone(s):\n\n"
        for zone in zones:
            result += f"🌐 {zone['name']}\n"
            result += f"   Zone ID: {zone['id']}\n"
            result += f"   Status: {zone.get('status', 'unknown')}\n"
            
            nameservers = zone.get('name_servers', [])
            if nameservers:
                result += f"   Nameservers:\n"
                for ns in nameservers:
                    result += f"     - {ns}\n"
            result += "\n"
        
        return result
    except Exception as e:
        return f"✗ Error: {str(e)}"


def create_zone_and_get_ns(email, token, domain_name):
    """Create zone and get nameservers"""
    try:
        account = CloudflareAccount(email=email, token=token, use_api_key=True)
        cf = CloudflareManager(account)
        
        zone = cf.create_zone(domain_name)
        
        if zone:
            nameservers = zone.get('name_servers', [])
            result = f"✓ Zone created for {domain_name}\n\n"
            result += f"Zone ID: {zone['id']}\n\n"
            result += "📋 Add these nameservers to your domain registrar:\n\n"
            for ns in nameservers:
                result += f"   {ns}\n"
            return result
        else:
            return "✗ Failed to create zone"
    except Exception as e:
        return f"✗ Error: {str(e)}"


def bind_domain(email, token, project_name, domain_name):
    """Bind domain to Pages project"""
    try:
        account = CloudflareAccount(email=email, token=token, use_api_key=True)
        cf = CloudflareManager(account)
        
        result_data = cf.add_pages_domain(project_name, domain_name)
        
        if result_data:
            result = f"✓ Domain bound to project!\n\n"
            result += f"Domain: {result_data.get('name')}\n"
            result += f"Status: {result_data.get('status')}\n\n"
            
            if result_data.get('validation_data'):
                val = result_data['validation_data']
                result += f"DNS Validation Required:\n"
                result += f"  Type: {val.get('type')}\n"
                result += f"  Name: {val.get('name')}\n"
                result += f"  Value: {val.get('value')}\n"
            
            return result
        else:
            return "✗ Failed to bind domain"
    except Exception as e:
        return f"✗ Error: {str(e)}"


def create_worker_route(email, token, zone_id, pattern, script_name):
    """Create worker route"""
    try:
        account = CloudflareAccount(email=email, token=token, use_api_key=True)
        cf = CloudflareManager(account)
        
        route = cf.create_worker_route(zone_id, pattern, script_name)
        
        if route:
            return f"✓ Worker route created!\n\nRoute ID: {route.get('id')}\nPattern: {pattern}\nScript: {script_name}"
        else:
            return "✗ Failed to create route"
    except Exception as e:
        return f"✗ Error: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="Cloudflare Manager", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🚀 Cloudflare Multi-Account Manager
    
    Manage Cloudflare Pages, Domains, and Workers through a simple web interface.
    
    ## Features
    - ✅ Pages project management
    - ✅ Domain binding
    - ✅ Nameserver lookup
    - ✅ Worker route configuration
    """)
    
    with gr.Row():
        with gr.Column():
            email_input = gr.Textbox(
                label="Cloudflare Email",
                placeholder="your-email@example.com",
                value=os.getenv("CLOUDFLARE_EMAIL", "")
            )
            token_input = gr.Textbox(
                label="API Token",
                type="password",
                placeholder="Your API Token",
                value=os.getenv("CLOUDFLARE_TOKEN", "")
            )
    
    with gr.Tabs():
        # Tab 1: Connection Test
        with gr.Tab("🔌 Connection Test"):
            test_btn = gr.Button("Test Connection", variant="primary")
            test_output = gr.Textbox(label="Result", lines=5)
            test_btn.click(
                test_connection,
                inputs=[email_input, token_input],
                outputs=test_output
            )
        
        # Tab 2: Pages Projects
        with gr.Tab("📦 Pages Projects"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### List Projects")
                    list_projects_btn = gr.Button("List Projects")
                    list_projects_output = gr.Textbox(label="Projects", lines=10)
                    list_projects_btn.click(
                        list_projects,
                        inputs=[email_input, token_input],
                        outputs=list_projects_output
                    )
                
                with gr.Column():
                    gr.Markdown("### Create Project")
                    project_name = gr.Textbox(label="Project Name", placeholder="my-website")
                    project_branch = gr.Textbox(label="Branch", value="main")
                    create_project_btn = gr.Button("Create Project", variant="primary")
                    create_project_output = gr.Textbox(label="Result", lines=10)
                    create_project_btn.click(
                        create_project,
                        inputs=[email_input, token_input, project_name, project_branch],
                        outputs=create_project_output
                    )
        
        # Tab 3: Domains & Zones
        with gr.Tab("🌐 Domains & Zones"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### List Zones")
                    list_zones_btn = gr.Button("List Zones")
                    list_zones_output = gr.Textbox(label="Zones", lines=10)
                    list_zones_btn.click(
                        list_zones,
                        inputs=[email_input, token_input],
                        outputs=list_zones_output
                    )
                
                with gr.Column():
                    gr.Markdown("### Create Zone & Get Nameservers")
                    zone_domain = gr.Textbox(label="Domain Name", placeholder="example.com")
                    create_zone_btn = gr.Button("Create Zone", variant="primary")
                    create_zone_output = gr.Textbox(label="Result", lines=10)
                    create_zone_btn.click(
                        create_zone_and_get_ns,
                        inputs=[email_input, token_input, zone_domain],
                        outputs=create_zone_output
                    )
        
        # Tab 4: Domain Binding
        with gr.Tab("🔗 Bind Domain"):
            gr.Markdown("### Bind Domain to Pages Project")
            with gr.Row():
                bind_project = gr.Textbox(label="Project Name", placeholder="my-website")
                bind_domain_name = gr.Textbox(label="Domain", placeholder="example.com")
            bind_btn = gr.Button("Bind Domain", variant="primary")
            bind_output = gr.Textbox(label="Result", lines=10)
            bind_btn.click(
                bind_domain,
                inputs=[email_input, token_input, bind_project, bind_domain_name],
                outputs=bind_output
            )
        
        # Tab 5: Worker Routes
        with gr.Tab("⚡ Worker Routes"):
            gr.Markdown("### Create Worker Route")
            worker_zone_id = gr.Textbox(label="Zone ID", placeholder="abc123...")
            worker_pattern = gr.Textbox(label="Route Pattern", placeholder="example.com/api/*")
            worker_script = gr.Textbox(label="Script Name", placeholder="my-worker")
            worker_btn = gr.Button("Create Route", variant="primary")
            worker_output = gr.Textbox(label="Result", lines=10)
            worker_btn.click(
                create_worker_route,
                inputs=[email_input, token_input, worker_zone_id, worker_pattern, worker_script],
                outputs=worker_output
            )
    
    gr.Markdown("""
    ---
    ### 📚 Documentation
    
    - [Quick Start Guide](GET_STARTED.md)
    - [Usage Guide](USAGE_GUIDE.md)
    - [API Reference](API_REFERENCE.md)
    
    ### 🔑 API Token Permissions
    
    Your API token needs:
    - Account > Cloudflare Pages > Edit
    - Zone > DNS > Edit
    - Zone > Workers Routes > Edit
    
    ### 💡 Tips
    
    1. Get your API token from: https://dash.cloudflare.com/profile/api-tokens
    2. After creating a zone, add the nameservers to your domain registrar
    3. DNS propagation takes 5-30 minutes
    """)


if __name__ == "__main__":
    # Run with sharing enabled for Hugging Face Spaces
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
