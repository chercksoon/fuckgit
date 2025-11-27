# Cloudflare Multi-Account Manager

一个功能完整的 Cloudflare 多账号管理器，支持 Pages 部署、域名绑定、Nameserver 查询和 Worker 路由配置。

## 功能特性

- ✅ **多账号管理**: 支持管理多个 Cloudflare 账号
- ✅ **Pages 部署**: 从本地目录部署 Pages 项目
- ✅ **域名绑定**: 将自定义域名绑定到 Pages 项目
- ✅ **Nameserver 查询**: 获取域名的 Nameserver 信息
- ✅ **Worker 路由**: 为 Worker 配置自定义域名和路由
- ✅ **Zone 管理**: 创建和管理 DNS Zone

## 安装依赖

```bash
pip install requests
```

或者使用 requirements.txt:

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 交互式命令行界面

```bash
python cloudflare_manager.py
```

运行后会显示一个交互式菜单，支持以下操作：

1. 列出 Pages 项目
2. 创建 Pages 项目
3. 部署 Pages 项目（选择文件夹）
4. 添加域名到 Pages 项目
5. 列出 Pages 项目的域名
6. 创建 Zone 并获取 Nameservers
7. 获取已有域名的 Nameservers
8. 列出所有 Zones
9. 创建 Worker 路由
10. 列出 Worker 路由
11. 添加 Worker 自定义域名

### 2. Python API 使用

#### 基础配置

```python
from cloudflare_manager import MultiAccountManager, CloudflareManager, CloudflareAccount

# 方法1: 使用多账号管理器
manager = MultiAccountManager()
cf = manager.add_account(
    name="primary",
    email="your-email@example.com",
    token="your-api-token"
)

# 方法2: 直接使用单账号管理器
account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)
```

#### 部署 Pages 项目

```python
# 1. 创建项目
cf.create_pages_project("my-website", production_branch="main")

# 2. 部署项目（从本地目录）
cf.deploy_pages_project(
    project_name="my-website",
    directory="./dist",  # 包含静态文件的目录
    branch="main",
    commit_message="Deploy my website"
)

# 3. 查看部署历史
deployments = cf.list_pages_deployments("my-website")
for deployment in deployments:
    print(f"Deployment: {deployment['url']}")
```

#### 绑定域名并获取 Nameservers

```python
# 1. 创建 Zone（如果域名还没有添加到 Cloudflare）
zone = cf.create_zone("example.com")
nameservers = zone.get("name_servers", [])
print("请在域名注册商处设置以下 Nameservers:")
for ns in nameservers:
    print(f"  {ns}")

# 2. 添加域名到 Pages 项目
result = cf.add_pages_domain("my-website", "example.com")
if result.get("validation_data"):
    val = result["validation_data"]
    print(f"DNS 验证记录:")
    print(f"  类型: {val['type']}")
    print(f"  名称: {val['name']}")
    print(f"  值: {val['value']}")

# 3. 查询已有域名的 Nameservers
nameservers = cf.get_nameservers("example.com")
```

#### 配置 Worker 路由

```python
# 1. 获取 Zone ID
zone = cf.get_zone_by_name("example.com")
zone_id = zone["id"]

# 2. 创建 Worker 路由
cf.create_worker_route(
    zone_id=zone_id,
    pattern="example.com/api/*",
    script_name="my-api-worker"
)

# 3. 添加 Worker 自定义域名
cf.add_worker_domain(
    hostname="api.example.com",
    service="my-api-worker",
    zone_id=zone_id,
    environment="production"
)

# 4. 列出所有路由
routes = cf.list_worker_routes(zone_id)
for route in routes:
    print(f"{route['pattern']} -> {route['script']}")
```

## 完整工作流示例

### 示例 1: 部署静态网站并绑定域名

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

# 1. 初始化
account = CloudflareAccount(
    email="exslym@closedbyme.com",
    token="21f3fb278a15b732a4f52c95d5042d78d1a21"
)
cf = CloudflareManager(account)

# 2. 创建 Pages 项目
cf.create_pages_project("my-blog", "main")

# 3. 部署网站（假设有一个包含 index.html 的目录）
cf.deploy_pages_project(
    project_name="my-blog",
    directory="./public",
    branch="main"
)

# 4. 创建 Zone 获取 Nameservers
zone = cf.create_zone("myblog.com")
nameservers = zone["name_servers"]
print("\n请在域名注册商处设置这些 Nameservers:")
for ns in nameservers:
    print(f"  {ns}")

# 5. 添加自定义域名到 Pages
cf.add_pages_domain("my-blog", "myblog.com")
cf.add_pages_domain("my-blog", "www.myblog.com")

print("\n✓ 部署完成! 等待 DNS 传播后即可访问")
```

### 示例 2: 为 Worker 配置自定义域名

```python
# 1. 获取 Zone
zone = cf.get_zone_by_name("example.com")
zone_id = zone["id"]

# 2. 配置 Worker 路由
cf.create_worker_route(
    zone_id=zone_id,
    pattern="example.com/api/*",
    script_name="api-worker"
)

# 3. 添加子域名
cf.add_worker_domain(
    hostname="api.example.com",
    service="api-worker",
    zone_id=zone_id
)

print("✓ Worker 路由已配置")
```

## API 方法参考

### Pages 相关

- `create_pages_project(project_name, production_branch)` - 创建 Pages 项目
- `list_pages_projects()` - 列出所有项目
- `get_pages_project(project_name)` - 获取项目详情
- `deploy_pages_project(project_name, directory, branch, commit_message)` - 部署项目
- `list_pages_deployments(project_name)` - 列出部署历史

### 域名相关

- `add_pages_domain(project_name, domain_name)` - 添加域名到 Pages
- `list_pages_domains(project_name)` - 列出项目的域名
- `get_pages_domain(project_name, domain_name)` - 获取域名详情

### Zone 相关

- `create_zone(domain_name, zone_type)` - 创建 Zone
- `list_zones()` - 列出所有 Zones
- `get_zone(zone_id)` - 获取 Zone 详情
- `get_zone_by_name(domain_name)` - 通过域名获取 Zone
- `get_nameservers(domain_name)` - 获取 Nameservers

### Worker 相关

- `create_worker_route(zone_id, pattern, script_name)` - 创建 Worker 路由
- `list_worker_routes(zone_id)` - 列出 Worker 路由
- `delete_worker_route(zone_id, route_id)` - 删除路由
- `add_worker_domain(hostname, service, zone_id, environment)` - 添加自定义域名
- `list_worker_domains()` - 列出 Worker 域名

## 使用测试账号

提供的测试账号信息：

```python
EMAIL = "exslym@closedbyme.com"
TOKEN = "21f3fb278a15b732a4f52c95d5042d78d1a21"
# PASSWORD = "h2%Ne&@3kv$G"  # 使用 API Token 不需要密码
# 2FA_KEY = "GMLFJQJITQGWCFD67PBWNKSOCRBKZ2NN"  # API 调用不需要 2FA
```

## 注意事项

1. **API Token 权限**: 确保 API Token 有足够的权限：
   - Account > Cloudflare Pages > Edit
   - Zone > DNS > Edit
   - Zone > Workers Routes > Edit
   - Account > Workers Scripts > Edit

2. **DNS 传播**: 添加域名后需要等待 DNS 传播（通常 5-30 分钟）

3. **HTTPS 证书**: Cloudflare 会自动为绑定的域名申请 SSL 证书

4. **Zone 限制**: 免费账号最多可以添加 1-3 个 Zones

5. **文件部署**: 部署目录中的所有文件都会被上传，确保不包含敏感信息

## 故障排除

### 问题: API 返回 401 错误
**解决**: 检查 API Token 是否正确，是否有足够权限

### 问题: 域名验证失败
**解决**: 
1. 确保域名的 Nameservers 已经指向 Cloudflare
2. 等待 DNS 传播完成
3. 如果使用自定义 DNS，添加验证记录

### 问题: 部署失败
**解决**:
1. 检查目录路径是否正确
2. 确保目录中有 index.html
3. 检查文件大小限制（单文件不超过 25MB）

## 开发者信息

- **项目**: Cloudflare Multi-Account Manager
- **语言**: Python 3.6+
- **依赖**: requests
- **License**: MIT

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v1.0.0 (2024-01-27)
- ✅ 实现 Pages 项目创建和部署
- ✅ 实现域名绑定功能
- ✅ 实现 Nameserver 查询
- ✅ 实现 Worker 路由配置
- ✅ 支持多账号管理
- ✅ 交互式命令行界面

## 联系方式

有问题或建议? 请联系开发者或提交 Issue。
