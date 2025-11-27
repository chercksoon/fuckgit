# 🚀 快速上手指南 (Getting Started)

欢迎使用 Cloudflare 多账号管理器！这个指南将帮助你在 5 分钟内开始使用。

## 📋 前置要求

1. **Python 3.6+** - 检查版本：
   ```bash
   python3 --version
   ```

2. **Cloudflare 账号** - 需要：
   - 邮箱地址
   - API Token（[获取方式](https://dash.cloudflare.com/profile/api-tokens)）

3. **API Token 权限** - 创建 Token 时需要：
   - Account > Cloudflare Pages > Edit
   - Zone > DNS > Edit
   - Zone > Workers Routes > Edit

## 🔧 安装步骤

### 1. 安装依赖

```bash
pip install requests
```

或者：

```bash
pip install -r requirements.txt
```

### 2. 验证安装

```bash
python3 test_manager.py
```

应该看到：
```
🎉 All tests passed!
```

## 🎯 三种使用方式

### 方式 1: 快速启动（最简单）⭐

适合第一次使用，引导式界面：

```bash
python3 quickstart.py
```

按提示输入：
1. Cloudflare Email
2. API Token
3. 项目名称
4. 要部署的目录
5. 域名（可选）

完成后会得到：
- 部署的 URL
- Nameservers（如果提供了域名）

### 方式 2: 交互式菜单（功能最全）

适合需要多次操作：

```bash
python3 cloudflare_manager.py
```

提供 11 个操作选项：
```
1. List Pages Projects
2. Create Pages Project
3. Deploy Pages Project
4. Add Domain to Pages Project
5. List Domains for Pages Project
6. Create Zone and Get Nameservers
7. Get Nameservers for Existing Domain
8. List Zones
9. Create Worker Route
10. List Worker Routes
11. Add Worker Custom Domain
```

### 方式 3: Python API（集成到代码）

适合编程使用：

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

# 1. 初始化
account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)

# 2. 创建并部署
cf.create_pages_project("my-site", "main")
cf.deploy_pages_project("my-site", "./public", "main")

# 3. 绑定域名
zone = cf.create_zone("example.com")
cf.add_pages_domain("my-site", "example.com")

print(f"Nameservers: {zone['name_servers']}")
```

## 📝 使用测试账号

可以使用提供的测试账号试用：

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

account = CloudflareAccount(
    email="exslym@closedbyme.com",
    token="21f3fb278a15b732a4f52c95d5042d78d1a21"
)
cf = CloudflareManager(account)

# 查看现有项目
projects = cf.list_pages_projects()
for project in projects:
    print(project['name'])
```

## 🎬 完整示例：部署静态网站

### 场景：部署一个静态博客到 myblog.com

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

# 1. 初始化管理器
account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)

# 2. 创建 Pages 项目
print("📝 Creating project...")
cf.create_pages_project("my-blog", "main")

# 3. 部署网站（假设静态文件在 ./public 目录）
print("📦 Deploying...")
deployment = cf.deploy_pages_project(
    project_name="my-blog",
    directory="./public",  # 包含 index.html 等文件
    branch="main",
    commit_message="Initial deployment"
)
print(f"✓ Deployed to: {deployment['url']}")

# 4. 创建 Zone 获取 Nameservers
print("\n🌐 Setting up domain...")
zone = cf.create_zone("myblog.com")
nameservers = zone["name_servers"]

print("\n📋 Add these nameservers to your domain registrar:")
for ns in nameservers:
    print(f"   {ns}")

# 5. 绑定域名
cf.add_pages_domain("my-blog", "myblog.com")
cf.add_pages_domain("my-blog", "www.myblog.com")

print("\n✅ Done! Your site will be live at https://myblog.com")
print("   (Wait 5-30 minutes for DNS propagation)")
```

### 运行结果：

```
📝 Creating project...
✓ Created Pages project: my-blog

📦 Deploying...
📄 Found 5 files to deploy
✓ Deployment created: abc123def456
  URL: https://abc123.my-blog.pages.dev

🌐 Setting up domain...
✓ Zone created: myblog.com
  Zone ID: xyz789

📋 Add these nameservers to your domain registrar:
   ns1.cloudflare.com
   ns2.cloudflare.com

✓ Domain added to Pages project: myblog.com
✓ Domain added to Pages project: www.myblog.com

✅ Done! Your site will be live at https://myblog.com
   (Wait 5-30 minutes for DNS propagation)
```

## 🔌 高级用法：Worker API 路由

### 场景：为 example.com 配置 API 子域名

```python
# 1. 获取 Zone
zone = cf.get_zone_by_name("example.com")
zone_id = zone["id"]

# 2. 创建 Worker 路由（匹配 /api/* 路径）
cf.create_worker_route(
    zone_id=zone_id,
    pattern="example.com/api/*",
    script_name="my-api-worker"
)

# 3. 添加专用子域名
cf.add_worker_domain(
    hostname="api.example.com",
    service="my-api-worker",
    zone_id=zone_id,
    environment="production"
)

print("✓ API configured:")
print("  - https://example.com/api/* → my-api-worker")
print("  - https://api.example.com → my-api-worker")
```

## 📚 下一步

### 新手推荐阅读顺序：

1. **GET_STARTED.md** (当前文件) - 快速上手
2. **README.md** - 项目概述和功能介绍
3. **USAGE_GUIDE.md** - 详细使用指南和示例
4. **API_REFERENCE.md** - 完整 API 文档

### 常用命令：

```bash
# 运行演示
python3 demo.py

# 运行测试
python3 test_manager.py

# 快速部署
python3 quickstart.py

# 完整示例
python3 example_usage.py

# 交互菜单
python3 cloudflare_manager.py
```

## ❓ 常见问题

### Q1: 如何获取 API Token?

1. 访问 https://dash.cloudflare.com/profile/api-tokens
2. 点击 "Create Token"
3. 选择 "Create Custom Token"
4. 添加权限：
   - Account > Cloudflare Pages > Edit
   - Zone > DNS > Edit
   - Zone > Workers Routes > Edit
5. 创建并复制 Token

### Q2: 部署失败怎么办？

检查：
- 目录是否存在且包含 index.html
- 文件大小是否超过 25MB
- API Token 是否有 Pages 权限

### Q3: 域名验证失败？

需要：
1. 在域名注册商处设置 Nameservers
2. 等待 DNS 传播（5-30 分钟）
3. 如果使用 DNS 验证，添加指定的 TXT/CNAME 记录

### Q4: 如何管理多个账号？

```python
from cloudflare_manager import MultiAccountManager

manager = MultiAccountManager()

# 添加账号
manager.add_account("personal", "personal@example.com", "token1")
manager.add_account("work", "work@example.com", "token2")

# 使用特定账号
personal = manager.get_account("personal")
work = manager.get_account("work")

# 各自操作
personal.list_pages_projects()
work.list_pages_projects()
```

### Q5: 如何查看详细错误？

所有错误都会打印到控制台，包含：
- 错误代码
- 错误信息
- 建议的解决方案

## 🎯 快速命令参考

### 部署新项目（一键）

```bash
# 1. 创建目录结构
mkdir my-site
cd my-site
echo "<h1>Hello World</h1>" > index.html

# 2. 使用 Python 部署
python3 << EOF
from cloudflare_manager import CloudflareManager, CloudflareAccount

account = CloudflareAccount(email="your@email.com", token="your-token")
cf = CloudflareManager(account)

cf.create_pages_project("my-site", "main")
cf.deploy_pages_project("my-site", ".", "main")
EOF
```

### 查看账号信息

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

account = CloudflareAccount(email="your@email.com", token="your-token")
cf = CloudflareManager(account)

print(f"Account: {cf.account.name}")
print(f"ID: {cf.account.account_id}")

# 列出资源
print(f"Projects: {len(cf.list_pages_projects())}")
print(f"Zones: {len(cf.list_zones())}")
```

### 批量操作

```python
# 部署多个项目
projects = ["site1", "site2", "site3"]

for project in projects:
    cf.create_pages_project(project, "main")
    cf.deploy_pages_project(project, f"./projects/{project}", "main")
    print(f"✓ {project} deployed")
```

## 🛠️ 故障排除

### API Token 错误

```
Error: Invalid request headers
```

**解决**: 检查 Token 是否正确，是否有足够权限

### Zone 不存在

```
Error: Zone not found
```

**解决**: 先创建 Zone：
```python
cf.create_zone("example.com")
```

### 部署超时

**解决**: 
- 检查文件大小
- 减少文件数量
- 检查网络连接

## 📞 获取帮助

1. 查看文档：README.md, USAGE_GUIDE.md, API_REFERENCE.md
2. 运行测试：`python3 test_manager.py`
3. 运行演示：`python3 demo.py`
4. 查看 Cloudflare 文档：https://developers.cloudflare.com/

## ✅ 完成！

现在你已经掌握了 Cloudflare Manager 的基本使用！

**接下来可以：**
- 🚀 部署你的第一个项目
- 🌐 绑定自定义域名
- ⚡ 配置 Worker 路由
- 📚 阅读详细文档了解更多功能

**祝使用愉快！** 🎉
