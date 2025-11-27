# 🚀 快速部署指南

> **重要**: 提供的测试 token 格式不正确。请按照下面的说明获取正确的 API Token。

## 📋 前置条件

### 获取正确的 Cloudflare API Token

提供的 token `21f3fb278a15b732a4f52c95d5042d78d1a21` **不是正确的格式**。

正确的 Cloudflare API Token 格式类似：
```
v1.0-abc123def456...xyz  (通常很长)
```

### 如何获取：

1. **访问**: https://dash.cloudflare.com/profile/api-tokens
2. **点击**: "Create Token"
3. **选择**: "Create Custom Token"
4. **配置权限**:
   ```
   Account Permissions:
   - Cloudflare Pages → Edit
   
   Zone Permissions:
   - DNS → Edit
   - Workers Routes → Edit
   - Zone → Edit
   ```
5. **创建并复制** token（只显示一次！）

### 测试 Token

```bash
# 使用 curl 测试
curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json"

# 或使用我们的测试脚本
python3 test_credentials.py
```

---

## 🎯 三种部署方式

### 方式 1: 使用一键启动脚本（最简单）

```bash
./start.sh
```

选择：
- `1` - Docker Compose（推荐）
- `2` - Docker
- `3` - Python 本地运行

### 方式 2: Docker Compose

```bash
# 1. 创建环境变量文件（可选）
cp .env.example .env
nano .env  # 编辑填入你的凭据

# 2. 启动
docker-compose up -d

# 3. 访问
# http://localhost:7860

# 4. 查看日志
docker-compose logs -f

# 5. 停止
docker-compose down
```

### 方式 3: 纯 Docker

```bash
# 1. 构建镜像
docker build -t cloudflare-manager .

# 2. 运行容器
docker run -d \
  --name cloudflare-manager \
  -p 7860:7860 \
  cloudflare-manager

# 3. 访问
# http://localhost:7860

# 4. 查看日志
docker logs -f cloudflare-manager

# 5. 停止和删除
docker stop cloudflare-manager
docker rm cloudflare-manager
```

### 方式 4: Python 本地运行

```bash
# 1. 安装依赖
pip3 install -r requirements.txt

# 2. 运行 Web 界面
python3 app.py

# 3. 访问
# http://localhost:7860
```

---

## 🌐 Hugging Face Spaces 部署

### 步骤 1: 创建 Space

1. 访问 https://huggingface.co/new-space
2. 填写：
   - **Space name**: cloudflare-manager
   - **License**: MIT
   - **SDK**: Gradio
   - **Python version**: 3.10

### 步骤 2: 准备文件

确保根目录有这个文件（已创建）：

**README.md** (用于 Hugging Face):
```yaml
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
```

### 步骤 3: 上传文件

**方式 A: Web 上传**
1. 在 Space 页面点击 "Files and versions"
2. 拖拽上传所有文件：
   - `app.py` ✅ **必需**
   - `cloudflare_manager.py` ✅ **必需**
   - `requirements.txt` ✅ **必需**
   - 其他文件（可选）

**方式 B: Git 推送**
```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/cloudflare-manager
cd cloudflare-manager

# Copy files
cp /path/to/project/*.py .
cp /path/to/project/requirements.txt .
cp /path/to/project/README_HUGGINGFACE.md README.md

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### 步骤 4: 配置 Secrets（推荐）

在 Space Settings → Repository secrets:

```
CLOUDFLARE_EMAIL=your-email@example.com
CLOUDFLARE_TOKEN=your-correct-api-token
```

这样凭据会自动预填充。

### 步骤 5: 访问

Space 会自动构建，几分钟后访问：
```
https://huggingface.co/spaces/YOUR_USERNAME/cloudflare-manager
```

---

## 📝 使用 Web 界面

### 1. 打开界面

访问 http://localhost:7860 (本地) 或你的 Space URL

### 2. 输入凭据

在顶部输入：
- **Cloudflare Email**: 你的 Cloudflare 邮箱
- **API Token**: 你的 API Token

### 3. 测试连接

点击 "Connection Test" 标签，然后点击 "Test Connection"

应该看到：
```
✓ Connected!

Account: Your Account Name
ID: abc123...
```

### 4. 使用功能

#### 📦 管理 Pages 项目

**列出项目:**
- 进入 "Pages Projects" 标签
- 点击 "List Projects"

**创建项目:**
- 输入项目名称
- 输入分支（默认 main）
- 点击 "Create Project"

#### 🌐 管理域名和 Zones

**列出 Zones:**
- 进入 "Domains & Zones" 标签
- 点击 "List Zones"

**创建 Zone 并获取 Nameservers:**
- 输入域名（如 example.com）
- 点击 "Create Zone"
- 复制显示的 Nameservers
- 添加到你的域名注册商

**示例输出:**
```
✓ Zone created for example.com

Zone ID: abc123...

📋 Add these nameservers to your domain registrar:

   ns1.cloudflare.com
   ns2.cloudflare.com
```

#### 🔗 绑定域名到 Pages

- 进入 "Bind Domain" 标签
- 输入项目名称
- 输入域名
- 点击 "Bind Domain"

#### ⚡ 配置 Worker 路由

- 进入 "Worker Routes" 标签
- 输入 Zone ID
- 输入路由模式（如 `example.com/api/*`）
- 输入 Worker 脚本名称
- 点击 "Create Route"

---

## 🔧 CLI 工具

除了 Web 界面，还可以使用命令行：

### 快速启动向导
```bash
python3 quickstart.py
```

### 交互式菜单
```bash
python3 cloudflare_manager.py
```

### 运行示例
```bash
python3 example_usage.py
```

### 运行测试
```bash
python3 test_manager.py
```

---

## 💻 Python API

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

# 1. 初始化
account = CloudflareAccount(
    email="your-email@example.com",
    token="your-correct-token"  # 正确的格式！
)
cf = CloudflareManager(account)

# 2. 创建 Pages 项目
project = cf.create_pages_project("my-site", "main")
print(f"Created: {project['subdomain']}")

# 3. 创建 Zone 获取 Nameservers
zone = cf.create_zone("example.com")
print("Nameservers:")
for ns in zone["name_servers"]:
    print(f"  {ns}")

# 4. 绑定域名
cf.add_pages_domain("my-site", "example.com")
print("Domain bound!")

# 5. 列出所有项目
projects = cf.list_pages_projects()
for p in projects:
    print(f"- {p['name']}")

# 6. 列出所有 Zones
zones = cf.list_zones()
for z in zones:
    print(f"- {z['name']}")

# 7. 创建 Worker 路由
zone_id = zones[0]['id']
cf.create_worker_route(
    zone_id=zone_id,
    pattern="example.com/api/*",
    script_name="my-worker"
)
```

---

## ⚠️ 常见问题

### Q1: Token 无效

**错误**: "Invalid request headers" 或 "Invalid format for Authorization header"

**原因**: 
- 提供的 token `21f3fb278a15b732a4f52c95d5042d78d1a21` 不是正确格式
- 正确的 token 应该以 `v1.0-` 开头，且很长

**解决**: 按照上面的说明重新创建 token

### Q2: 没有权限

**错误**: "Permission denied"

**解决**: 
确保 token 有以下权限：
- Account > Cloudflare Pages > Edit
- Zone > DNS > Edit
- Zone > Workers Routes > Edit

### Q3: Docker 端口被占用

**错误**: "Port 7860 is already in use"

**解决**:
```bash
# 使用不同端口
docker run -d -p 8080:7860 cloudflare-manager

# 或停止占用进程
lsof -ti:7860 | xargs kill -9
```

### Q4: gradio 模块未找到

**错误**: "No module named 'gradio'"

**解决**:
```bash
pip3 install gradio
# 或
pip3 install -r requirements.txt
```

---

## 📚 完整文档

- **[快速开始](GET_STARTED.md)** - 5分钟入门
- **[使用指南](USAGE_GUIDE.md)** - 完整使用说明
- **[API 参考](API_REFERENCE.md)** - 所有 API 方法
- **[部署指南](DEPLOYMENT.md)** - 详细部署说明
- **[项目总结](PROJECT_SUMMARY.md)** - 技术概览

---

## ✅ 检查清单

部署前检查：

- [ ] 获取了正确格式的 API Token
- [ ] Token 有足够的权限
- [ ] 已安装 Docker 或 Python 3.10+
- [ ] 端口 7860 可用
- [ ] 已阅读文档

---

## 🎉 完成！

现在你可以：

1. ✅ 管理 Pages 项目
2. ✅ 部署静态网站
3. ✅ 绑定自定义域名
4. ✅ 获取 Nameservers
5. ✅ 配置 Worker 路由

**需要帮助？**
查看完整文档或运行测试：
```bash
python3 test_manager.py
```

**享受使用！** 🚀
