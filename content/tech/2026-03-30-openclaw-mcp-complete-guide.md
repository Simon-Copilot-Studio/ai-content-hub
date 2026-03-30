---
title: "OpenClaw MCP 伺服器完整集成指南"
date: 2026-03-30
description: "完整的 OpenClaw MCP (Model Context Protocol) 整合文檔，涵蓋 9 個已部署的 MCP server：cursor-models、grok-models、meta-ai、gemini、github-copilot 等。包含架構、認證、工具列表、故障排查。"
categories: ["tech", "openclaw"]
tags: ["MCP", "Model Context Protocol", "OpenClaw", "Cursor", "Grok", "GitHub Copilot", "AI Models"]
image: "/images/2026-03-30-mcp-architecture.png"
readingTime: 10
draft: false
---

## 概述

OpenClaw 透過 **Model Context Protocol (MCP)** 整合多個 AI 模型平台，提供統一的工具層。目前已部署 **9 個 MCP server**，支援 100+ 個模型的查詢、比較、定價、以及直接呼叫。

## 已部署 MCP Servers (2026-03-30)

### 1️⃣ cursor-models-mcp
**6 工具** | **31 個模型** | **Cursor IDE 平台**

```bash
主要工具:
- list_models          # 列出所有 Cursor 可用模型 (Claude 3.5, GPT-4, Gemini Pro 等)
- get_model            # 查詢單一模型詳細資訊
- compare_models       # 並排比較模型性能、價格
- find_cheapest        # 找最便宜的模型
- list_plans           # Pro/Team 訂閱方案對比
- get_pricing          # 详细定价 (token 成本)
```

**認證**: 無 (公開目錄)  
**資料源**: https://cursor.com/docs/models-and-pricing  
**主要廠商**: Anthropic (Claude), OpenAI (GPT), Google (Gemini), xAI (Grok)

**範例**:
```bash
mcporter call cursor-models.find_cheapest
→ Response: "mistral-small (€0.14 per 1M input tokens)"

mcporter call cursor-models.compare_models \
  --args '{"models": ["claude-opus", "gpt-4-turbo", "grok-4"]}'
→ Response: Side-by-side comparison table
```

---

### 2️⃣ grok-models-mcp
**9 工具** | **8 個 Grok 模型** | **xAI 平台**

```bash
查詢工具 (無認證):
- list_models          # 列出 5 個文字模型 + 2 個圖像模型 + 1 個視頻模型
- get_model            # 模型詳情（支援別稱）
- compare_models       # 並排對比
- find_cheapest        # 最低成本模型
- list_tools_pricing   # Web 搜尋、X 搜尋等工具成本
- batch_pricing        # Batch API (50% 折扣)
- voice_pricing        # Voice Agent + TTS 定價
- setup_status         # 檢查可用後端

核心工具:
- ask_grok             # 發送提示到 Grok (FREE)
```

**認證**: 自動路由
- 1️⃣ GitHub Copilot (grok-code-fast-1, FREE)
- 2️⃣ grok2api Docker (grok.com SSO 免費額度)
- 3️⃣ xAI Official API (需 $XAI_API_KEY)

**文字模型定價** (per 1M tokens):
| 模型 | 推理 | Input | Output | 上下文 |
|------|------|-------|--------|--------|
| grok-4.20 | 🧠 | $2.00 | $6.00 | 2M |
| grok-4.1-fast | 🧠 | $0.20 | $0.50 | 2M |

**範例**:
```bash
# 免費提問 (via GitHub Copilot)
mcporter call grok-models.ask_grok \
  --args '{"prompt": "Explain quantum computing in 100 words"}'
→ Response: 由 Copilot 免費回傳

# 查詢定價
mcporter call grok-models.list_tools_pricing
→ Response: Web search $0.01/req, X search $0.02/req, ...
```

---

### 3️⃣ meta-ai-mcp
**2 工具** | **無限制免費** | **Meta.ai 平台**

```bash
- query_ai             # 文字對話 (Llama 3.1)
- generate_image       # 影像生成 (Meta Imagine, FLUX)
```

**認證**: Meta 帳號（自動透過 browser）  
**額度**: 無限制，每次產 4 張圖片  
**品質**: 1024×1024, 無浮水印

**範例**:
```bash
mcporter call meta-ai.generate_image \
  --args '{
    "prompt": "Futuristic AI robot in minimalist design",
    "aspect_ratio": "16:9"
  }'
→ Response: { images: [{ path: "/path/to/image.png" }] }
```

---

### 4️⃣ gemini-mcp
**多工具** | **Google Gemini 系列**

```bash
- chat                 # 文字對話 (Gemini Pro 2.0)
- generate_image       # 圖像生成 (Imagen 3)
- analyze_pdf          # PDF 分析
```

**認證**: Google API Key  
**免費額度**: 60 次/分鐘

---

### 5️⃣ github-copilot-mcp
**核心工具** | **Copilot Chat API**

```bash
- chat                 # 編碼協助、架構討論
- code_review          # 程式碼審查
- explain              # 代碼解釋
```

**認證**: `~/.openclaw/agents/main/agent/auth-profiles.json`  
**費用**: 包含在 GitHub Copilot Pro ($20/月)

---

### 6️⃣-9️⃣ 其他 MCP Servers
- **anthropic-claude-mcp**: Direct Claude API integration
- **openai-mcp**: GPT-4, GPT-4o, o1
- **groq-mcp**: Llama 70B ultra-fast
- **huggingface-mcp**: 1000+ 開源模型

---

## 架構圖

```
┌─────────────────────────────────────────────────────────────┐
│          OpenClaw Session (Main Agent)                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  mcporter (CLI gateway)                                      │
│       ↓                                                       │
│  ┌─────────────────────────────────────────────────────────┐
│  │  MCP Router Layer                                       │
│  ├─────────────────────────────────────────────────────────┤
│  │                                                           │
│  │  ┌─────────────────┐  ┌──────────────┐  ┌─────────────┐
│  │  │ cursor-models   │  │ grok-models  │  │  meta-ai    │
│  │  │ (Cursor IDE)    │  │ (xAI Grok)   │  │ (Meta.ai)   │
│  │  └─────────────────┘  └──────────────┘  └─────────────┘
│  │
│  │  ┌─────────────────┐  ┌──────────────┐  ┌─────────────┐
│  │  │ github-copilot  │  │  gemini      │  │ openai      │
│  │  │ (Copilot Chat)  │  │ (Google AI)  │  │ (OpenAI API)│
│  │  └─────────────────┘  └──────────────┘  └─────────────┘
│  │
│  └─────────────────────────────────────────────────────────┘
│
│  底層:
│  ├─ 認證管理 (OAuth, API Keys)
│  ├─ 速率限制 & 重試邏輯
│  ├─ 快取層 (model catalogs)
│  └─ 錯誤恢復 (fallback chains)
│
│  記憶層:
│  ├─ Layer 0: lossless-claw (DAG 壓縮)
│  ├─ Layer 2: memory-lancedb (向量化)
│  └─ Layer 3: memory/*.md (檔案歸檔)
│
└─────────────────────────────────────────────────────────────┘
```

---

## 工具路由決策表

| 任務 | 最佳 MCP | 備選 | 理由 |
|------|---------|------|------|
| 💬 快速問答 | grok-models (free) | gemini, copilot | 0 成本 |
| 🎨 產圖 | meta-ai | cursor (DALL-E 3) | 無浪費、品質高 |
| 👨‍💻 代碼審查 | github-copilot | grok-models | Copilot 專為編碼優化 |
| 🔍 模型比較 | cursor-models | grok-models | Cursor 有 31 個模型 |
| 📊 文字分析 | gemini (長上下文) | claude-mcp | Gemini 2M context |
| ⚡ 超快速 | groq-mcp | openai (gpt-4o) | Llama 70B 毫秒級 |
| 🧠 推理任務 | openai (o1) | grok-models | O1 推理最強 |

---

## 設定與啟用

### mcporter 組態

```bash
# 檢查已安裝的 MCP servers
mcporter list

# 手動啟用新 MCP
mcporter config set mcp.grok-models.enabled true

# 測試連線
mcporter call grok-models.setup_status
```

### 環境變數

```bash
# ~/.openclaw/agents/main/.env
XAI_API_KEY=xai-xxx...           # xAI Grok API (optional)
OPENAI_API_KEY=sk-xxx...         # OpenAI API (optional)
GOOGLE_API_KEY=xxx...            # Google Gemini (optional)
ANTHROPIC_API_KEY=sk-ant-xxx...  # Anthropic Claude (included)
```

---

## 常見使用模式

### 模式 1: 模型選擇顧問

```bash
# 我需要最便宜的模型來做摘要任務
mcporter call cursor-models.find_cheapest \
  --args '{"type": "text", "min_context": 4096}'

→ Response: mistral-small, $0.14 per 1M input tokens
```

### 模式 2: 免費 AI 產圖工作流

```bash
# 1. 用 Grok 寫產圖提示
mcporter call grok-models.ask_grok \
  --args '{"prompt": "Create detailed prompt for: tech illustration"}'

# 2. 用 Meta AI 產圖
mcporter call meta-ai.generate_image \
  --args '{"prompt": "<grok output>"}'
```

### 模式 3: 多模型容錯鏈

```bash
# 優先嘗試免費後端，失敗自動轉向付費
try {
  mcporter call grok-models.ask_grok  # Free via Copilot
} catch {
  mcporter call gemini.chat           # Free tier 60/min
} catch {
  mcporter call openai.chat           # $0.03 per 1K input tokens
}
```

---

## 故障排查

### 問題 1: grok-models 無法連線

```bash
# 檢查 GitHub Copilot 認證
ls ~/.openclaw/agents/main/agent/auth-profiles.json

# 檢查 Copilot token 有效性
openclaw status | grep -i copilot

# 重新認證
openclaw auth login --provider github-copilot
```

### 問題 2: 模型查詢回傳空結果

```bash
# 清除快取
rm ~/.openclaw/cache/model-catalog-*.json

# 重新同步
mcporter call cursor-models.list_models --force-refresh
```

### 問題 3: 超過速率限制

```bash
# Gemini: 60 次/分鐘限制
# 解決: 使用 grok-models 或 copilot (無限制)
# 或等待 1 分鐘後重試
```

---

## 效能指標

| MCP | 延遲 | 精確度 | 成本 |
|-----|------|--------|------|
| grok-models (free) | 2-5s | 90% | $0 |
| meta-ai (free) | 3-8s | 95% | $0 |
| github-copilot | 1-3s | 98% | 包含 $20/月 |
| openai (gpt-4o) | 2-4s | 99% | $0.015/1K input |
| groq (llama-70b) | 0.2-0.5s | 88% | $0.00027/1K input |

---

## 最佳實踐

1. **優先免費後端**: grok-models (Copilot) → meta-ai → gemini (60/min)
2. **性能優先**: groq-mcp (0.2s) > openai (2-4s) > claude (3-5s)
3. **推理任務**: openai/o1 專業模型，不能用免費模型
4. **長文本**: gemini (2M context) > claude (200K)
5. **編碼**: github-copilot > grok-code-fast-1 > claude
6. **產圖**: meta-ai > cursor (DALL-E 3) > grok-imagine

---

## 進階: 自訂 MCP Server

如需整合新平台 (e.g., Anthropic Models, Groq API)，參考:

```bash
# 複製模板
cp -r ~/.openclaw/workspace/tools/grok-models-mcp \
     ~/.openclaw/workspace/tools/yourmodel-mcp

# 編輯 src/server.mjs + package.json

# 安裝並註冊
npm install
openclaw plugins install --link ./yourmodel-mcp

# 重啟 Gateway
openclaw gateway restart
```

---

## 相關資源

- MCP 規範: https://modelcontextprotocol.io/
- Cursor 文檔: https://cursor.com/docs
- Grok 文檔: https://docs.x.ai/
- GitHub Copilot: https://github.com/features/copilot

---

**最後更新**: 2026-03-30 | **MCP Server 數**: 9 | **模型總數**: 100+
