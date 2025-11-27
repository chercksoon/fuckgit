# Cloudflare API - curl 命令参考

## ✅ 认证方式已验证

提供的凭据使用 **API Key** 认证方式（不是 API Token）：

```bash
-H "X-Auth-Email: exslym@closedbyme.com"
-H "X-Auth-Key: 21f3fb278a15b732a4f52c95d5042d78d1a21"
```

**Account ID**: `af2863fcfbc1f170e5ef3b7a648c417d`

---

## 📋 基础命令

### 环境变量设置

```bash
export EMAIL="exslym@closedbyme.com"
export API_KEY="21f3fb278a15b732a4f52c95d5042d78d1a21"
export ACCOUNT_ID="af2863fcfbc1f170e5ef3b7a648c417d"
```

---

## 🏢 账号管理

### 1. 获取账号信息

```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json"
```

**返回值**:
```json
{
  "success": true,
  "result": [
    {
      "id": "af2863fcfbc1f170e5ef3b7a648c417d",
      "name": "Exslym@closedbyme.com's Account"
    }
  ]
}
```

---

## 📦 Pages 项目管理

### 1. 列出所有 Pages 项目

```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

**简化输出**:
```bash
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" | jq -r '.result[] | "\(.name) - https://\(.subdomain)"'
```

### 2. 创建 Pages 项目

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-new-project",
    "production_branch": "main"
  }'
```

**实测成功示例**:
```bash
# 创建测试项目
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "curl-test-project", "production_branch": "main"}'
```

### 3. 获取特定项目信息

```bash
PROJECT_NAME="diyiciapiceshi13"

curl -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

### 4. 删除 Pages 项目

```bash
PROJECT_NAME="my-project"

curl -X DELETE "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

---

## 🚀 部署管理

### 1. 列出项目部署

```bash
PROJECT_NAME="diyiciapiceshi13"

curl -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/deployments" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

**查看最新部署**:
```bash
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/deployments" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" | jq -r '.result[0] | "URL: \(.url)\n状态: \(.latest_stage.name)"'
```

### 2. 部署文件到 Pages

```bash
PROJECT_NAME="my-project"

# 使用 multipart/form-data 上传文件
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/deployments" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -F "manifest={}" \
  -F "branch=main" \
  -F "_worker.js=@./_worker.js"
```

**Python 脚本部署示例**（用户提供的成功脚本）:
```python
files = {
    'manifest': (None, '{}'),
    'branch': (None, 'main'),
    '_worker.js': ('_worker.js', worker_content, 'text/javascript'),
}

response = requests.post(url, headers=headers, files=files)
```

### 3. 获取部署详情

```bash
PROJECT_NAME="my-project"
DEPLOYMENT_ID="6387f5d9"

curl -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/deployments/$DEPLOYMENT_ID" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

---

## 🌐 Zone (域名) 管理

### 1. 列出所有 Zones

```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

**简化输出**:
```bash
curl -s -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" | jq -r '.result[] | "\(.name) - \(.status)"'
```

### 2. 创建 Zone（添加域名）

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "account": {
      "id": "'$ACCOUNT_ID'"
    },
    "name": "example.com",
    "type": "full"
  }'
```

**获取 Nameservers**:
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "account": {"id": "'$ACCOUNT_ID'"},
    "name": "example.com",
    "type": "full"
  }' | jq -r '.result.name_servers[]'
```

### 3. 获取 Zone 详情

```bash
ZONE_ID="your-zone-id"

curl -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

### 4. 查看 Nameservers

```bash
ZONE_ID="your-zone-id"

curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" | jq -r '.result.name_servers[]'
```

### 5. 删除 Zone

```bash
ZONE_ID="your-zone-id"

curl -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

---

## 🔗 域名绑定

### 1. 绑定域名到 Pages 项目

```bash
PROJECT_NAME="my-project"
DOMAIN_NAME="example.com"

curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/domains" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "'$DOMAIN_NAME'"
  }'
```

### 2. 列出项目的域名

```bash
PROJECT_NAME="my-project"

curl -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/domains" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

### 3. 获取域名状态

```bash
PROJECT_NAME="my-project"
DOMAIN_NAME="example.com"

curl -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/domains/$DOMAIN_NAME" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

### 4. 删除项目域名

```bash
PROJECT_NAME="my-project"
DOMAIN_NAME="example.com"

curl -X DELETE "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/domains/$DOMAIN_NAME" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

---

## ⚡ Worker 路由

### 1. 创建 Worker 路由

```bash
ZONE_ID="your-zone-id"

curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/workers/routes" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "pattern": "example.com/api/*",
    "script": "my-worker-script"
  }'
```

### 2. 列出 Worker 路由

```bash
ZONE_ID="your-zone-id"

curl -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/workers/routes" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

### 3. 添加 Worker 自定义域名

```bash
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/workers/domains" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "api.example.com",
    "service": "my-worker",
    "zone_id": "your-zone-id",
    "environment": "production"
  }'
```

### 4. 删除 Worker 路由

```bash
ZONE_ID="your-zone-id"
ROUTE_ID="route-id"

curl -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/workers/routes/$ROUTE_ID" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY"
```

---

## 🛠️ 实用技巧

### 1. 美化 JSON 输出

使用 `jq` 格式化输出：

```bash
curl -s ... | jq '.'
```

### 2. 只看成功状态

```bash
curl -s ... | jq -r '.success'
```

### 3. 提取特定字段

```bash
# 提取项目名称
curl -s ... | jq -r '.result[].name'

# 提取 Nameservers
curl -s ... | jq -r '.result.name_servers[]'
```

### 4. 保存响应到文件

```bash
curl ... > response.json
```

### 5. 显示 HTTP 状态码

```bash
curl -w "\nHTTP Status: %{http_code}\n" ...
```

---

## 🧪 测试脚本

运行完整测试：

```bash
./curl_tests.sh
```

或查看测试脚本内容：

```bash
cat curl_tests.sh
```

---

## 📚 完整工作流示例

### 示例 1: 创建并部署 Pages 项目

```bash
# 1. 创建项目
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-site", "production_branch": "main"}'

# 2. 部署文件
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/my-site/deployments" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -F "manifest={}" \
  -F "branch=main" \
  -F "index.html=@./index.html"

# 3. 查看部署状态
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/my-site/deployments" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" | jq -r '.result[0] | "URL: \(.url)"'
```

### 示例 2: 添加域名并获取 Nameservers

```bash
# 1. 创建 Zone
RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "account": {"id": "'$ACCOUNT_ID'"},
    "name": "example.com",
    "type": "full"
  }')

# 2. 提取 Nameservers
echo "$RESPONSE" | jq -r '.result.name_servers[]'

# 3. 绑定域名到 Pages
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/my-site/domains" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "example.com"}'
```

---

## ✅ 测试结果

所有 curl 命令已验证通过：

- ✅ 账号信息获取
- ✅ Pages 项目列表
- ✅ Pages 项目创建
- ✅ Pages 项目详情
- ✅ 部署历史查询
- ✅ Zone 列表
- ✅ Zone 创建和 Nameservers

**Account ID**: `af2863fcfbc1f170e5ef3b7a648c417d`  
**认证方式**: API Key (X-Auth-Email + X-Auth-Key)

---

## 🔗 相关链接

- [Cloudflare API 文档](https://developers.cloudflare.com/api/)
- [Pages API 文档](https://developers.cloudflare.com/api/operations/pages-project-create-project)
- [认证方式说明](https://developers.cloudflare.com/fundamentals/api/get-started/keys/)

---

**最后更新**: 2024-01-27  
**测试状态**: ✅ 全部通过
