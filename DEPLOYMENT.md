# 部署指南 (Deployment Guide)

## 目录

1. [Hugging Face Spaces 部署](#hugging-face-spaces-部署)
2. [Docker 部署](#docker-部署)
3. [本地开发](#本地开发)
4. [获取 API Token](#获取-api-token)

---

## Hugging Face Spaces 部署

### 方法 1: 通过 Web 界面

1. **创建新 Space**
   - 访问 https://huggingface.co/new-space
   - 选择 Space name（例如：cloudflare-manager）
   - 选择 SDK: **Gradio**
   - 选择 License: MIT

2. **上传文件**
   - 上传所有项目文件
   - 或者连接到 Git 仓库

3. **配置（可选）**
   - 进入 Space Settings
   - 添加 Secrets（推荐用于安全）:
     ```
     CLOUDFLARE_EMAIL=your-email@example.com
     CLOUDFLARE_TOKEN=your-api-token
     ```

4. **访问**
   - Space 会自动构建和部署
   - 访问 `https://huggingface.co/spaces/YOUR_USERNAME/cloudflare-manager`

### 方法 2: 通过 Git

```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/cloudflare-manager
cd cloudflare-manager

# Copy all files
cp -r /path/to/project/* .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

### Hugging Face Space 配置文件

确保在根目录有 `README_HUGGINGFACE.md` 文件（已创建），它包含：

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

---

## Docker 部署

### 使用 Docker Compose（推荐）

1. **准备环境变量**（可选）
   ```bash
   cp .env.example .env
   # 编辑 .env 文件填入你的凭据
   nano .env
   ```

2. **启动服务**
   ```bash
   docker-compose up -d
   ```

3. **查看日志**
   ```bash
   docker-compose logs -f
   ```

4. **访问**
   - 打开浏览器访问: http://localhost:7860

5. **停止服务**
   ```bash
   docker-compose down
   ```

### 使用 Docker 命令

1. **构建镜像**
   ```bash
   docker build -t cloudflare-manager .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     --name cloudflare-manager \
     -p 7860:7860 \
     cloudflare-manager
   ```

3. **带环境变量运行**
   ```bash
   docker run -d \
     --name cloudflare-manager \
     -p 7860:7860 \
     -e CLOUDFLARE_EMAIL="your-email@example.com" \
     -e CLOUDFLARE_TOKEN="your-api-token" \
     cloudflare-manager
   ```

4. **查看日志**
   ```bash
   docker logs -f cloudflare-manager
   ```

5. **停止和删除**
   ```bash
   docker stop cloudflare-manager
   docker rm cloudflare-manager
   ```

### Docker Hub 部署

如果你想发布到 Docker Hub：

```bash
# 构建并打标签
docker build -t your-username/cloudflare-manager:latest .

# 推送到 Docker Hub
docker login
docker push your-username/cloudflare-manager:latest

# 其他人可以这样使用
docker pull your-username/cloudflare-manager:latest
docker run -d -p 7860:7860 your-username/cloudflare-manager:latest
```

---

## 本地开发

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行 Web 界面

```bash
python3 app.py
```

访问: http://localhost:7860

### 3. 使用 CLI 工具

```bash
# 快速启动向导
python3 quickstart.py

# 交互式菜单
python3 cloudflare_manager.py

# 运行示例
python3 example_usage.py

# 运行测试
python3 test_manager.py
```

### 4. Python API 使用

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)

# 使用 API
projects = cf.list_pages_projects()
zones = cf.list_zones()
```

---

## 获取 API Token

### 步骤

1. **登录 Cloudflare**
   - 访问 https://dash.cloudflare.com/

2. **进入 API Tokens 页面**
   - 点击右上角头像
   - 选择 "My Profile"
   - 点击左侧 "API Tokens"
   - 或直接访问: https://dash.cloudflare.com/profile/api-tokens

3. **创建新 Token**
   - 点击 "Create Token"
   - 选择 "Create Custom Token"

4. **配置权限**
   
   需要添加以下权限：
   
   **Account 权限:**
   - Cloudflare Pages → Edit
   
   **Zone 权限:**
   - DNS → Edit
   - Workers Routes → Edit
   - Zone → Edit (可选，用于创建 Zone)

5. **设置 Zone Resources**
   - 选择 "All zones" 或特定的 zones
   - 如果只管理特定域名，选择具体的 zone

6. **设置 Client IP Address Filtering**（可选）
   - 可以限制 IP 地址以增加安全性

7. **创建并复制 Token**
   - 点击 "Continue to summary"
   - 点击 "Create Token"
   - **重要**: 立即复制 token，它只显示一次！

### Token 示例格式

正确的 token 格式类似：
```
v1.0-abc123def456789...xyz
```

**注意**: 提供的 token `21f3fb278a15b732a4f52c95d5042d78d1a21` 似乎不是正确的格式。

### 验证 Token

创建 token 后，可以测试：

```bash
python3 test_credentials.py
```

或使用 curl：

```bash
export CLOUDFLARE_API_TOKEN="your-token"

curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
     -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
     -H "Content-Type: application/json"
```

成功的响应：
```json
{
  "success": true,
  "errors": [],
  "messages": [],
  "result": {
    "id": "...",
    "status": "active"
  }
}
```

---

## 环境变量配置

### 方法 1: .env 文件

```bash
# 复制示例文件
cp .env.example .env

# 编辑文件
nano .env
```

内容：
```bash
CLOUDFLARE_EMAIL=your-email@example.com
CLOUDFLARE_TOKEN=v1.0-your-actual-token
```

### 方法 2: 系统环境变量

**Linux/Mac:**
```bash
export CLOUDFLARE_EMAIL="your-email@example.com"
export CLOUDFLARE_TOKEN="v1.0-your-actual-token"
```

**Windows:**
```cmd
set CLOUDFLARE_EMAIL=your-email@example.com
set CLOUDFLARE_TOKEN=v1.0-your-actual-token
```

### 方法 3: 在代码中

```python
import os

# 设置环境变量
os.environ['CLOUDFLARE_EMAIL'] = 'your-email@example.com'
os.environ['CLOUDFLARE_TOKEN'] = 'v1.0-your-actual-token'

# 然后运行应用
from cloudflare_manager import CloudflareManager, CloudflareAccount

account = CloudflareAccount(
    email=os.environ['CLOUDFLARE_EMAIL'],
    token=os.environ['CLOUDFLARE_TOKEN']
)
```

---

## 部署架构

### 架构图

```
┌─────────────────────────────────────────┐
│         用户浏览器                        │
│     (http://localhost:7860)             │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Gradio Web Interface               │
│           (app.py)                      │
│  - Form inputs                          │
│  - Buttons and tabs                     │
│  - Result display                       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    CloudflareManager                    │
│   (cloudflare_manager.py)               │
│  - API calls                            │
│  - Error handling                       │
│  - Data processing                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Cloudflare API                     │
│  https://api.cloudflare.com/client/v4   │
│  - Pages                                │
│  - Zones                                │
│  - Workers                              │
└─────────────────────────────────────────┘
```

---

## 故障排除

### 问题 1: Token 无效

**错误**: "Invalid request headers" 或 "Invalid format for Authorization header"

**解决**:
1. 检查 token 格式是否正确（应以 `v1.0-` 开头）
2. 验证 token 权限
3. 创建新的 token

### 问题 2: Docker 构建失败

**解决**:
```bash
# 清理并重新构建
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### 问题 3: 端口已被占用

**错误**: "Port 7860 is already in use"

**解决**:
```bash
# 使用不同端口
docker run -d -p 8080:7860 cloudflare-manager

# 或停止占用的进程
lsof -ti:7860 | xargs kill -9
```

### 问题 4: Gradio 界面无法访问

**解决**:
1. 检查防火墙设置
2. 确保容器正在运行: `docker ps`
3. 查看日志: `docker logs cloudflare-manager`

---

## 生产环境建议

### 1. 使用 HTTPS

配置反向代理（如 Nginx）:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. 设置认证

添加基本认证或使用 OAuth。

### 3. 监控和日志

```bash
# 查看日志
docker logs -f cloudflare-manager

# 使用日志聚合工具
# 例如: ELK Stack, Loki, etc.
```

### 4. 自动重启

```yaml
# docker-compose.yml
services:
  cloudflare-manager:
    restart: always  # 改为 always
```

---

## 更新和维护

### 更新应用

```bash
# 拉取最新代码
git pull

# 重新构建和部署
docker-compose down
docker-compose build
docker-compose up -d
```

### 备份配置

```bash
# 备份 .env 文件
cp .env .env.backup

# 备份整个配置
tar -czf cloudflare-manager-backup.tar.gz \
  .env docker-compose.yml
```

---

## 支持的平台

- ✅ Hugging Face Spaces
- ✅ Docker / Docker Compose
- ✅ 本地开发环境
- ✅ Linux 服务器
- ✅ macOS
- ✅ Windows (with WSL2)
- ✅ Cloud platforms (AWS, GCP, Azure)
- ✅ Kubernetes (需要创建相应的 manifests)

---

## 下一步

1. ✅ 获取正确的 API Token
2. ✅ 选择部署方式（Hugging Face / Docker / 本地）
3. ✅ 运行应用
4. ✅ 开始管理 Cloudflare 资源！

有问题？查看完整文档：
- [快速开始](GET_STARTED.md)
- [使用指南](USAGE_GUIDE.md)
- [API 参考](API_REFERENCE.md)
