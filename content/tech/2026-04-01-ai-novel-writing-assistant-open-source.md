---
title: "AI 導演式長篇小說生產系統：AI-Novel-Writing-Assistant 完整實測與架構解析"
date: 2026-04-01T23:30:00+08:00
description: "深入實測開源專案 AI-Novel-Writing-Assistant——一個用 Agent 工作流、世界觀引擎、寫法引擎和 RAG 知識庫，讓完全不懂寫作的新手也能從一句靈感走到完整長篇小說的 AI Native 系統。附完整本地部署教學。"
categories: ["tech"]
tags: ["AI寫作", "LangChain", "LangGraph", "開源", "Agent", "RAG", "小說生成", "AI Native", "Prisma", "React"]
image: "/images/ai-novel-assistant/创作中枢.png"
readingTime: 8
draft: false
---

你有沒有過這種經驗？腦中浮現一個超棒的小說靈感，打開 ChatGPT 想讓它幫你寫，結果寫了兩章就開始「人設崩塌、世界觀矛盾、劇情越寫越散」？

這不是 AI 的問題，是**工具形態**的問題。聊天模式天生不適合長篇創作。

今天要介紹的開源專案 [AI-Novel-Writing-Assistant](https://github.com/ExplosiveCoderflome/AI-Novel-Writing-Assistant)，用了一個完全不同的思路：**AI 不只是寫字的工具，而是參與規劃、判斷、調度、執行和追蹤的導演角色。**

## 這不是又一個 AI 寫作聊天殼子

先看看它跟市面上 AI 寫作工具的根本差異：

| 傳統 AI 寫作工具 | AI-Novel-Writing-Assistant |
|---|---|
| 你輸入 Prompt，AI 回一段文字 | AI 先幫你規劃整本書的結構 |
| 寫短篇還行，長篇越寫越散 | 專為長篇設計，有卷級/章級管理 |
| 每次生成獨立，沒有記憶 | RAG 知識庫 + 世界觀系統持續追蹤 |
| 風格靠 Prompt 描述 | 寫法引擎：可提取、保存、複用寫作風格 |
| 人工把關所有決策 | Agent 自動導演 + 人工審核節點 |

## 架構一覽

```
開書定盤（靈感 → 方向候選 → 項目設定）
    ↓
整本控制層（宏觀規劃 → 卷戰略 → 拆章）
    ↓
單章生成（寫法引擎 + RAG + 世界觀 + 角色資產）
    ↓
回灌循環（章節完成 → 狀態更新 → 影響後續章節）
```

技術棧很硬核：

- **前端**：React + Vite + Plate 編輯器 + Radix UI
- **後端**：Express + Prisma + SQLite（可選 PostgreSQL）
- **AI 層**：LangChain / LangGraph Agent 編排
- **RAG**：Qdrant 向量檢索 + 關鍵字混合搜尋
- **Monorepo**：pnpm workspace，前後端 + shared types

## 核心功能深度解析

### 1. 自動導演開書

不需要你自己規劃世界觀、主線、角色。只需輸入一句靈感，例如：

> 「一個能看見死亡倒計時的少年」

AI 導演會自動產出多套整本方向候選，包含：
- 題材定位與賣點分析
- 目標讀者感受設計
- 前 30 章承諾
- 主副流派模式建議

不滿意？你可以說「太套路了」「主角驅動力不夠」，系統會沿著你的修正方向繼續迭代，**而不是整頁推翻重來**。

![項目設定](/images/ai-novel-assistant/项目设定.jpeg)

### 2. 世界觀管理系統

世界觀不再是一大段文字貼在 Prompt 裡：

- **結構化分層**：地理、政治、魔法體系、科技水平分別管理
- **快照機制**：不同階段的世界觀可以回溯
- **一致性檢查**：AI 自動偵測新章節是否與既有設定矛盾
- **深化問答**：對任何設定追問，系統自動擴展細節

![世界觀管理](/images/ai-novel-assistant/世界观.png)

### 3. 寫法引擎

這是我覺得最驚豔的功能。你可以：

- 從一段你喜歡的文本**提取寫法特徵**
- 原文樣本一起保存，不用靠記憶猜「當時那個味道怎麼來的」
- 特徵沉澱為**可見特徵池**，可逐項啟用/停用/組合
- 寫法規則自動重新編譯，影響後續所有章節生成

![寫法引擎](/images/ai-novel-assistant/写法引擎与反AI规则.jpeg)

### 4. RAG 知識庫

支持拆書功能——把現有小說拆解後發布到知識庫，再回灌到續寫和規劃：

- 文檔管理 + 向量檢索 + 關鍵字檢索
- 重建任務追蹤
- 與世界觀、角色系統整合

![知識庫](/images/ai-novel-assistant/知识库.png)

### 5. 章節執行與整本生產

從結構化規劃出發，啟動整本寫作任務：

- **卷骨架** → **節奏拆章** → **章節執行**
- 每章完成後自動回灌狀態
- 支持審計、修復、再平衡和重規劃
- 整本批量 Pipeline 持續追蹤進度

![章節執行](/images/ai-novel-assistant/章节执行.jpeg)

### 6. 多 LLM 模型支持

已支持的模型提供商：

| 提供商 | 模型 |
|--------|------|
| OpenAI | GPT-5 mini |
| DeepSeek | deepseek-chat |
| Anthropic | Claude 3.5 Sonnet |
| xAI | Grok-4 |
| Kimi | moonshot-v1-32k |
| 智譜 GLM | glm-4.5-air |
| 通義千問 | qwen-plus |
| Google | Gemini 2.5 Flash |
| SiliconFlow | Qwen 72B |

規劃、正文、審閱可以**按路由拆開配不同模型**，省錢又高效。

![模型配置](/images/ai-novel-assistant/模型配置.png)

## 5 分鐘本地部署教學

### 前置需求

- Node.js ≥ 20
- pnpm ≥ 9.7

### 步驟

```bash
# 1. Clone
git clone https://github.com/ExplosiveCoderflome/AI-Novel-Writing-Assistant.git
cd AI-Novel-Writing-Assistant

# 2. 安裝依賴
pnpm install

# 3. 設定環境變數（最少只需一個 LLM API Key）
cp .env.example server/.env
# 編輯 server/.env，填入至少一個 API Key（推薦 DeepSeek，便宜）

# 4. 初始化資料庫（SQLite，零配置）
cd server
npx prisma generate --schema src/prisma/schema.prisma
npx prisma db push --schema src/prisma/schema.prisma
cd ..

# 5. 啟動
pnpm dev
```

打開 `http://localhost:5173` 就能看到完整的 AI 小說創作工作台。

> **Tips**：不需要 Qdrant 也能跑主鏈。RAG 功能需要時再按需接入。

## 適合誰？

- ✅ **想寫長篇小說但不知道怎麼規劃結構的新手**
- ✅ **研究 AI Native Product 如何落地的開發者**
- ✅ **對 LangGraph Agent 編排有興趣的技術人**
- ✅ **想建立可複用寫作風格資產的作者**
- ❌ 只想要「一鍵出書」的人（它還不是全自動的）
- ❌ 不願意學習工作流的人（有學習曲線）

## 我的評價

這是目前我看過**最認真做長篇小說 AI 生產系統**的開源專案。它不是套殼，而是真正在解決「AI 怎麼組織一條完整的創作工作流」這個難題。

幾個讓我印象深刻的設計決策：

1. **先解決「寫完」再解決「寫好」**——務實的優先級
2. **寫法引擎是長期資產**——不是一次性 Prompt
3. **Agent 有明確的 Planner / Runtime / 審批節點**——不是黑箱
4. **SQLite 即可啟動**——降低試用門檻
5. **支持「偏差修正」而非「推翻重來」**——符合真實創作流程

當然它還在積極開發中，但骨架已經立起來了，值得持續關注。

---

## FAQ

### Q: 需要 GPU 嗎？
不需要。所有 AI 推理都通過 API 呼叫外部模型（OpenAI、DeepSeek 等），本地只需跑 Node.js。

### Q: 免費嗎？
專案本身完全開源免費（MIT License 推測）。但你需要自備 LLM API Key，DeepSeek 是最便宜的選擇。

### Q: 能生成整本小說嗎？
可以。系統有整本生產 Pipeline，但建議逐章審核而非完全自動化，品質會更好。

### Q: 支持繁體中文嗎？
介面目前是簡體中文，但生成內容的語言取決於你的 Prompt 和模型，可以產出繁體中文小說。

### Q: 跟 NovelAI、Sudowrite 比如何？
定位不同。那些是商業 SaaS，強調易用性。這個專案強調的是**完整的長篇生產工作流**和**可控性**，更適合想深度參與創作過程的人。
