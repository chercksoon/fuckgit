# 文件上传指南 (File Upload Guide)

这份文档详细说明如何上传文件到 Cloudflare Pages 和 Workers。

This guide explains how to upload files to Cloudflare Pages and Workers in detail.

---

## 目录 (Table of Contents)

1. [上传文件到 Pages](#上传文件到-pages)
2. [上传文件到 Worker](#上传文件到-worker)
3. [API 详细说明](#api-详细说明)
4. [完整示例代码](#完整示例代码)

---

## 上传文件到 Pages

### 方法 1: 从本地目录部署 (Deploy from Local Directory)

这是最简单的方法，会自动扫描目录并上传所有文件。

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

# 初始化账户
account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)

# 先创建项目（如果还没有创建）
cf.create_pages_project("my-website", "main")

# 从目录部署（上传所有文件）
cf.deploy_pages_project(
    project_name="my-website",
    directory="./my-site",          # 本地目录路径
    branch="main",                  # 分支名称
    commit_message="Initial deploy"  # 提交信息
)
```

### 工作原理 (How It Works)

`deploy_pages_project` 方法会：

1. 扫描指定目录下的所有文件
2. 计算每个文件的 SHA-256 哈希值
3. 构建 manifest（文件清单）
4. 使用 `multipart/form-data` 格式上传所有文件
5. 返回部署详情

### 上传的数据格式

```python
# 内部实现的数据格式
files = [
    ("branch", (None, "main")),
    ("commit_message", (None, "Deploy via API")),
    ("manifest", (None, '{"index.html": "abc123...", "style.css": "def456..."}')),
    ("index.html", ("index.html", file_content, "text/html")),
    ("style.css", ("style.css", file_content, "text/css")),
    # ... 更多文件
]
```

### 支持的文件类型

所有常见的 Web 文件类型都支持：
- HTML: `.html`, `.htm`
- CSS: `.css`
- JavaScript: `.js`, `.mjs`
- 图片: `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.ico`
- 字体: `.woff`, `.woff2`, `.ttf`, `.otf`
- JSON: `.json`
- 文本: `.txt`, `.md`

---

## 上传文件到 Worker

### 基本用法

上传 Worker 脚本非常简单：

```python
from cloudflare_manager import CloudflareManager, CloudflareAccount

# 初始化账户
account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)

# 上传 Worker 脚本
cf.upload_worker(
    script_name="my-worker",
    worker_file="./worker.js"
)
```

### 带绑定的高级用法 (Advanced Usage with Bindings)

如果你的 Worker 需要绑定 KV、R2 或其他资源：

```python
# KV 命名空间绑定
bindings = [
    {
        "type": "kv_namespace",
        "name": "MY_KV",
        "namespace_id": "your-kv-namespace-id"
    }
]

cf.upload_worker(
    script_name="my-worker",
    worker_file="./worker.js",
    bindings=bindings
)
```

### Worker 文件示例

创建一个简单的 Worker 文件 `worker.js`：

```javascript
// worker.js
export default {
  async fetch(request, env, ctx) {
    return new Response('Hello from Cloudflare Worker!', {
      headers: { 'Content-Type': 'text/plain' }
    });
  }
}
```

### 上传的数据格式

```python
# 内部实现
metadata = {
    "main_module": "_worker.js",
    "compatibility_date": "2023-01-01",
    "bindings": []  # 可选的绑定
}

files = {
    'metadata': (None, json.dumps(metadata), 'application/json'),
    '_worker.js': ('_worker.js', worker_content, 'text/javascript'),
}
```

---

## API 详细说明

### deploy_pages_project()

**功能**: 从本地目录部署 Pages 项目

**参数**:
- `project_name` (str): 项目名称
- `directory` (str): 本地目录路径
- `branch` (str, 默认="main"): 分支名称
- `commit_message` (str, 默认="Deploy via API"): 提交信息

**返回值**: 
- `Dict`: 部署详情（成功时）
- `None`: 失败时

**示例**:
```python
result = cf.deploy_pages_project(
    project_name="my-website",
    directory="./dist",
    branch="main",
    commit_message="Update homepage"
)

if result:
    print(f"部署 ID: {result['id']}")
    print(f"URL: {result['url']}")
    print(f"状态: {result['latest_stage']['status']}")
```

### upload_worker()

**功能**: 上传 Worker 脚本

**参数**:
- `script_name` (str): Worker 脚本名称
- `worker_file` (str): Worker .js 文件路径
- `bindings` (List[Dict], 可选): 资源绑定列表

**返回值**: 
- `Dict`: Worker 详情（成功时）
- `None`: 失败时

**示例**:
```python
result = cf.upload_worker(
    script_name="api-worker",
    worker_file="./api.js",
    bindings=[
        {
            "type": "kv_namespace",
            "name": "CACHE",
            "namespace_id": "abc123..."
        }
    ]
)

if result:
    print(f"Worker ID: {result['id']}")
    print(f"创建时间: {result['created_on']}")
```

### list_workers()

**功能**: 列出所有 Worker 脚本

**参数**: 无

**返回值**: `List[Dict]` - Worker 列表

**示例**:
```python
workers = cf.list_workers()
for worker in workers:
    print(f"- {worker['id']}")
```

### get_worker()

**功能**: 获取指定 Worker 的详细信息

**参数**:
- `script_name` (str): Worker 脚本名称

**返回值**: 
- `Dict`: Worker 详情（成功时）
- `None`: 失败时

**示例**:
```python
worker = cf.get_worker("my-worker")
if worker:
    print(f"脚本名称: {worker['id']}")
    print(f"修改时间: {worker['modified_on']}")
```

### delete_worker()

**功能**: 删除 Worker 脚本

**参数**:
- `script_name` (str): Worker 脚本名称

**返回值**: `bool` - 成功返回 True，失败返回 False

**示例**:
```python
if cf.delete_worker("old-worker"):
    print("Worker 已删除")
```

---

## 完整示例代码

### 示例 1: 部署静态网站到 Pages

```python
#!/usr/bin/env python3
from cloudflare_manager import CloudflareManager, CloudflareAccount
import os

# 配置账户
account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)

# 项目名称
project_name = "my-blog"

# 创建 Pages 项目
print("📝 创建 Pages 项目...")
cf.create_pages_project(project_name, "main")

# 部署网站
print("📦 部署网站...")
result = cf.deploy_pages_project(
    project_name=project_name,
    directory="./public",  # Hugo/Jekyll 等的输出目录
    branch="main",
    commit_message="Deploy blog v1.0"
)

if result:
    print(f"✅ 部署成功！")
    print(f"访问地址: {result['url']}")
else:
    print("❌ 部署失败")
```

### 示例 2: 上传 Worker API

```python
#!/usr/bin/env python3
from cloudflare_manager import CloudflareManager, CloudflareAccount

# 配置账户
account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)

# 创建 Worker 文件
worker_code = '''
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname === '/api/hello') {
      return new Response(JSON.stringify({
        message: 'Hello from Worker!',
        timestamp: new Date().toISOString()
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return new Response('404 Not Found', { status: 404 });
  }
}
'''

# 保存到文件
with open('api-worker.js', 'w', encoding='utf-8') as f:
    f.write(worker_code)

# 上传 Worker
print("📤 上传 Worker...")
result = cf.upload_worker(
    script_name="api-worker",
    worker_file="api-worker.js"
)

if result:
    print("✅ Worker 上传成功！")
    print(f"可以通过 https://api-worker.{account.name}.workers.dev 访问")
else:
    print("❌ Worker 上传失败")
```

### 示例 3: Worker + KV 存储

```python
#!/usr/bin/env python3
from cloudflare_manager import CloudflareManager, CloudflareAccount

account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)

# Worker 代码（使用 KV）
worker_code = '''
export default {
  async fetch(request, env, ctx) {
    const key = new URL(request.url).pathname.slice(1) || 'counter';
    
    // 从 KV 读取
    let count = await env.MY_KV.get(key);
    count = count ? parseInt(count) : 0;
    
    // 增加计数
    count++;
    
    // 写入 KV
    await env.MY_KV.put(key, count.toString());
    
    return new Response(`访问次数: ${count}`, {
      headers: { 'Content-Type': 'text/plain; charset=utf-8' }
    });
  }
}
'''

with open('counter-worker.js', 'w', encoding='utf-8') as f:
    f.write(worker_code)

# 上传带 KV 绑定的 Worker
print("📤 上传 Worker (with KV)...")
result = cf.upload_worker(
    script_name="counter-worker",
    worker_file="counter-worker.js",
    bindings=[
        {
            "type": "kv_namespace",
            "name": "MY_KV",
            "namespace_id": "your-kv-namespace-id"  # 替换为你的 KV ID
        }
    ]
)

if result:
    print("✅ Worker (with KV) 上传成功！")
```

### 示例 4: 批量部署多个 Workers

```python
#!/usr/bin/env python3
from cloudflare_manager import CloudflareManager, CloudflareAccount
import os

account = CloudflareAccount(
    email="your-email@example.com",
    token="your-api-token"
)
cf = CloudflareManager(account)

# Worker 文件列表
workers = [
    ("api-worker", "./workers/api.js"),
    ("auth-worker", "./workers/auth.js"),
    ("cache-worker", "./workers/cache.js"),
]

print("📤 批量上传 Workers...")
for name, filepath in workers:
    if os.path.exists(filepath):
        print(f"\n上传: {name} <- {filepath}")
        result = cf.upload_worker(name, filepath)
        if result:
            print(f"  ✅ {name} 上传成功")
        else:
            print(f"  ❌ {name} 上传失败")
    else:
        print(f"  ⚠️  文件不存在: {filepath}")

print("\n✅ 批量上传完成！")
```

---

## 常见问题 (FAQ)

### Q1: Pages 部署支持哪些文件大小？

A: 单个文件最大 25MB，总部署大小最大 20,000 个文件。

### Q2: Worker 脚本有大小限制吗？

A: 免费计划限制 1MB，付费计划（Workers Bundled）限制 5MB。

### Q3: 如何处理大型项目？

A: 对于大型项目，建议：
1. 使用构建工具（Webpack、Rollup）打包和压缩
2. 排除 `node_modules` 等不必要的目录
3. 使用 `.gitignore` 风格的过滤

### Q4: 上传失败怎么办？

A: 检查：
1. API Token 权限是否正确
2. 文件路径是否存在
3. 文件格式是否正确
4. 网络连接是否正常

### Q5: 如何查看上传进度？

A: 目前库会在上传时打印文件数量。对于大型部署，建议使用 `tqdm` 等进度条库。

---

## 技术细节 (Technical Details)

### Pages 部署 API

**端点**: `POST /accounts/{account_id}/pages/projects/{project_name}/deployments`

**请求格式**: `multipart/form-data`

**必需字段**:
- `manifest`: JSON 字符串，包含文件名到哈希的映射
- `branch`: 分支名称
- 各个文件字段

**示例请求**:
```python
files = [
    ("manifest", (None, '{"index.html": "sha256-hash..."}')),
    ("branch", (None, "main")),
    ("index.html", ("index.html", file_content, "text/html")),
]
```

### Worker 上传 API

**端点**: `PUT /accounts/{account_id}/workers/scripts/{script_name}`

**请求格式**: `multipart/form-data`

**必需字段**:
- `metadata`: JSON 字符串，包含元数据和绑定
- `_worker.js`: Worker 脚本内容

**示例请求**:
```python
files = {
    'metadata': (None, json.dumps({
        "main_module": "_worker.js",
        "compatibility_date": "2023-01-01"
    }), 'application/json'),
    '_worker.js': ('_worker.js', worker_content, 'text/javascript'),
}
```

---

## 相关文档

- [API 参考手册](./API_REFERENCE.md)
- [使用指南](./USAGE_GUIDE.md)
- [快速开始](./GET_STARTED.md)
- [项目概述](./README.md)

---

## 总结

这份指南覆盖了：

✅ Pages 文件部署（从目录上传）  
✅ Worker 脚本上传  
✅ Worker 资源绑定（KV、R2 等）  
✅ 完整的示例代码  
✅ API 详细说明  
✅ 常见问题解答  

如有其他问题，请查看 [API_REFERENCE.md](./API_REFERENCE.md) 或提交 Issue。
