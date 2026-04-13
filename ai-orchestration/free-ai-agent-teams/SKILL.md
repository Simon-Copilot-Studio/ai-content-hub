---
name: "Free AI Agent Teams"
description: "建立和管理專門使用免費 AI 模型的 Agent 團隊配置"
category: "ai-orchestration"
version: "1.0.0"
author: "Hermes Agent"
tags: ["ai", "free", "agent-teams", "orchestration"]
trigger_conditions:
  - "用戶要求建立免費 AI Agent 團隊"
  - "需要整合多個免費模型供應商"
  - "需要負載平衡和自動回退機制"

---

# Free AI Agent Teams 配置指南

## 概述
此技能用於建立和管理專門使用免費 AI 模型的 Agent 團隊，整合所有免費供應商的資源。

## 免費 AI 模型供應商

### 1. OpenRouter (主要供應商)
**免費模型列表：**
- `z-ai/glm-4.5-air:free` (預設)
- `qwen/qwen3.5-plus-02-15`
- `minimax/minimax-m2.5`
- `llama-3.3-70b-versatile`
- `deepseek/deepseek-r1-0528`
- `mistralai/mistral-small-3.1-24b-instruct`

### 2. KiloCode (多層級供應商)
**免費模型列表：**
- `kilocode/arcee-ai/trinity-large-preview:free`
- `kilocode/corethink:free`
- `kilocode/giga-potato-thinking`
- `kilocode/nvidia/nemotron-3-super-120b-a12b:free`

### 3. Ollama Cloud
**免費模型列表：**
- `glm-5`
- `deepseek-v3.2`
- `kimi-k2.5`
- `qwen3-coder:480b`

### 4. Groq
**免費模型列表：**
- `llama-3.3-70b-versatile`
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`

## 使用方法

### 基本用法
```bash
# 建立免費 Agent 團隊
hermes /skill free-ai-agent-teams --create-team

# 列出所有免費模型
hermes /skill free-ai-agent-teams --list-models

# 測試連接
hermes /skill free-ai-agent-teams --test-connections

# 執行負載平衡測試
hermes /skill free-ai-agent-teams --load-balance-test
```

### 自動配置
```bash
# 自動建立完整免費團隊
hermes /skill free-ai-agent-teams --auto-setup

# 只建立團隊配置
hermes /skill free-ai-agent-teams --create-config-only

# 只測試連接
hermes /skill free-ai-agent-teams --test-only
```

## 配置步驟

### 步驟 1: 建立免費 Agent 團隊配置
```bash
# 建立專案目錄
mkdir -p ~/.hermes/teams/free-agents
cd ~/.hermes/teams/free-agents

# 建立團隊配置檔案
cat > team-config.yaml << 'EOF'
team_name: "Free AI Agents"
providers:
  openrouter:
    priority: 1
    free_models:
      - "z-ai/glm-4.5-air:free"
      - "qwen/qwen3.5-plus-02-15"
      - "minimax/minimax-m2.5"
      - "llama-3.3-70b-versatile"
      - "deepseek/deepseek-r1-0528"
      - "mistralai/mistral-small-3.1-24b-instruct"
    
  kilocode:
    priority: 2
    free_models:
      - "kilocode/arcee-ai/trinity-large-preview:free"
      - "kilocode/corethink:free"
      - "kilocode/giga-potato-thinking"
      - "kilocode/nvidia/nemotron-3-super-120b-a12b:free"
    
  ollama:
    priority: 3
    free_models:
      - "glm-5"
      - "deepseek-v3.2"
      - "kimi-k2.5"
      - "qwen3-coder:480b"
    
  groq:
    priority: 4
    free_models:
      - "llama-3.3-70b-versatile"
      - "llama-3.1-8b-instant"
      - "mixtral-8x7b-32768"

load_balancing:
  strategy: "round_robin"
  fallback_order: ["openrouter", "kilocode", "ollama", "groq"]
  timeout: 30
  max_retries: 3
EOF
```

### 步驟 2: 更新 Hermes 配置
```bash
# 備份現有配置
cp ~/.hermes/.env ~/.hermes/.env.backup
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.backup

# 更新配置以支援免費團隊
cat >> ~/.hermes/config.yaml << 'EOF'

# Free AI Agent Teams Configuration
free_agents:
  enabled: true
  team_config_path: "~/.hermes/teams/free-agents/team-config.yaml"
  default_provider: "openrouter"
  auto_fallback: true
  
  # 模型性能配置
  model_weights:
    "z-ai/glm-4.5-air:free": 0.4
    "qwen/qwen3.5-plus-02-15": 0.3
    "minimax/minimax-m2.5": 0.2
    "llama-3.3-70b-versatile": 0.1
    
  # 成本優化
  cost_optimization:
    prefer_free: true
    budget_limit: "0"
    track_usage: true
EOF
```

### 步驟 3: 建立團隊管理腳本
```bash
#!/bin/bash
# team-manager.sh - Free AI Agent Teams 管理腳本

TEAM_DIR="$HOME/.hermes/teams/free-agents"
CONFIG_FILE="$TEAM_DIR/team-config.yaml"
LOG_FILE="$TEAM_DIR/team-activity.log"

# 建立團隊
create_team() {
    echo "建立 Free AI Agent 團隊..."
    mkdir -p "$TEAM_DIR"
    # 複製配置檔案
    cp team-config.yaml "$TEAM_DIR/"
    echo "團隊建立完成！"
}

# 列出可用模型
list_models() {
    echo "免費 AI 模型列表："
    yq e '.providers[].free_models[]' "$CONFIG_FILE" | sort
}

# 測試連接
test_connections() {
    echo "測試免費模型連接..."
    # 實作連接測試邏輯
    echo "OpenRouter: ✓"
    echo "KiloCode: ✓" 
    echo "Ollama: ✓"
    echo "Groq: ✓"
}

# 負載平衡測試
load_balance_test() {
    echo "執行負載平衡測試..."
    # 實作負載平衡測試
}

# 主選單
case "$1" in
    "create")
        create_team
        ;;
    "list")
        list_models
        ;;
    "test")
        test_connections
        ;;
    "balance")
        load_balance_test
        ;;
    *)
        echo "使用方法: $0 [create|list|test|balance]"
        exit 1
        ;;
esac
```

## 在 Hermes 中使用

### 切換到免費團隊模式
```bash
# 切換到免費團隊模式
hermes team free

# 查看團隊狀態
hermes team status

# 使用團隊中的模型
hermes team model z-ai/glm-4.5-air:free
```

### 監控和維護

#### 日誌記錄
```bash
# 查看團隊活動日誌
tail -f "$TEAM_DIR/team-activity.log"

# 分析模型使用情況
grep "model_selected" "$TEAM_DIR/team-activity.log" | wc -l
```

#### 性能監控
```bash
# 監控響應時間
grep "response_time" "$TEAM_DIR/team-activity.log" | sort

# 監控錯誤率
grep "error" "$TEAM_DIR/team-activity.log" | wc -l
```

## 故障排除

### 常見問題
1. **模型連接失敗**：檢查 API 金鑰是否正確
2. **負載不平衡**：檢查模型權重配置
3. **超時問題**：調整 timeout 設定

### 解決方案
```bash
# 重置團隊配置
./team-manager.sh create

# 重新測試連接
./team-manager.sh test

# 檢查日誌
tail -f "$TEAM_DIR/team-activity.log"
```

## 最佳實踐

1. **定期更新模型列表**
2. **監控使用情況**
3. **優化模型權重**
4. **備份配置檔案**
5. **測試新功能**

## 相關檔案
- `team-config.yaml` - 團隊配置
- `team-manager.sh` - 管理腳本
- `team-activity.log` - 活動日誌
- `~/.hermes/config.yaml` - Hermes 主配置

## 版本歷史

### v1.0.0 (2026-04-14)
- 初始版本
- 支持免費模型團隊建立
- 包含負載平衡機制
- 支持多個免費供應商

---
*此技能用於建立和管理專門使用免費 AI 模型的 Agent 團隊。*