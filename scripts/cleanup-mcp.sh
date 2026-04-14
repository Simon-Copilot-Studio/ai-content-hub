#!/bin/bash
# 清理 meta-ai MCP 殭屍進程
# 保留最新 1 個，殺掉其餘
COUNT=$(ps aux | grep "meta-ai-mcp/server.mjs" | grep -v grep | wc -l)
if [ "$COUNT" -gt 2 ]; then
  # 只保留最新的 2 個進程
  ps aux | grep "meta-ai-mcp/server.mjs" | grep -v grep | sort -k9 | head -n $((COUNT-2)) | awk '{print $2}' | xargs kill -9 2>/dev/null
  echo "CLEANED: killed $((COUNT-2)) zombie MCP processes (kept 2)"
else
  echo "OK: only $COUNT MCP processes running"
fi
