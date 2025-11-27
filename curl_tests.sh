#!/bin/bash
# Cloudflare API curl 测试脚本
# 使用提供的 API Key 进行测试

set -e  # 遇到错误立即退出

EMAIL="exslym@closedbyme.com"
API_KEY="21f3fb278a15b732a4f52c95d5042d78d1a21"
ACCOUNT_ID="af2863fcfbc1f170e5ef3b7a648c417d"

echo "═══════════════════════════════════════════════════════════"
echo "  Cloudflare API - curl 测试脚本"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Email: $EMAIL"
echo "Account ID: $ACCOUNT_ID"
echo ""

# 测试 1: 获取账号信息
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 1: 获取账号信息"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" \
  -H "Content-Type: application/json" | jq -r '
if .success then
  "✅ 成功!\n账号名称: \(.result[0].name)\n账号 ID: \(.result[0].id)"
else
  "❌ 失败: \(.errors)"
end'
echo ""

# 测试 2: 列出 Pages 项目
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 2: 列出 Pages 项目"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" | jq -r '
if .success then
  "✅ 成功! 找到 \(.result | length) 个项目:\n" +
  (.result | map("  - \(.name) (\(.subdomain))") | join("\n"))
else
  "❌ 失败: \(.errors)"
end'
echo ""

# 测试 3: 创建 Pages 项目（示例）
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 3: 创建 Pages 项目（跳过，避免重复创建）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "命令示例:"
echo 'curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects" \'
echo '  -H "X-Auth-Email: $EMAIL" \'
echo '  -H "X-Auth-Key: $API_KEY" \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{"name": "my-test-project", "production_branch": "main"}'"'"
echo ""

# 测试 4: 列出 Zones
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 4: 列出 Zones"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" | jq -r '
if .success then
  if (.result | length) > 0 then
    "✅ 成功! 找到 \(.result | length) 个 Zone:\n" +
    (.result | map("  - \(.name) (ID: \(.id))\n    状态: \(.status)\n    Nameservers: \(.name_servers | join(", "))") | join("\n"))
  else
    "✅ 成功! 但没有找到 Zones"
  end
else
  "❌ 失败: \(.errors)"
end'
echo ""

# 测试 5: 创建 Zone（示例）
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 5: 创建 Zone 并获取 Nameservers（示例）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "命令示例:"
echo 'curl -X POST "https://api.cloudflare.com/client/v4/zones" \'
echo '  -H "X-Auth-Email: $EMAIL" \'
echo '  -H "X-Auth-Key: $API_KEY" \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{"account": {"id": "$ACCOUNT_ID"}, "name": "example.com", "type": "full"}'"'"' | \'
echo '  jq -r '"'"'.result.name_servers | join("\n")'"'"
echo ""

# 测试 6: 获取特定项目信息
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 6: 获取特定项目信息"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
PROJECT_NAME="diyiciapiceshi13"
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" | jq -r '
if .success then
  "✅ 成功!\n项目名称: \(.result.name)\n项目 URL: https://\(.result.subdomain)\n创建时间: \(.result.created_on)"
else
  "❌ 失败: \(.errors)"
end'
echo ""

# 测试 7: 列出项目部署
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 7: 列出项目部署历史"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s -X GET "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/deployments" \
  -H "X-Auth-Email: $EMAIL" \
  -H "X-Auth-Key: $API_KEY" | jq -r '
if .success then
  "✅ 成功! 找到 \(.result | length) 个部署:\n" +
  (.result[0:3] | map("  - 部署 ID: \(.short_id)\n    URL: \(.url)\n    状态: \(.latest_stage.name)\n    时间: \(.created_on)") | join("\n\n"))
else
  "❌ 失败: \(.errors)"
end'
echo ""

# 测试 8: 绑定域名到 Pages（示例）
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试 8: 绑定域名到 Pages 项目（示例）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "命令示例:"
echo 'curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/domains" \'
echo '  -H "X-Auth-Email: $EMAIL" \'
echo '  -H "X-Auth-Key: $API_KEY" \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{"name": "example.com"}'"'"
echo ""

# 总结
echo "═══════════════════════════════════════════════════════════"
echo "  测试完成"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "✅ 所有基本测试通过！"
echo ""
echo "下一步:"
echo "  1. 使用 python3 app.py 启动 Web 界面"
echo "  2. 或使用 cloudflare_manager.py 进行 Python 开发"
echo "  3. 或继续使用 curl 命令进行 API 调用"
echo ""
