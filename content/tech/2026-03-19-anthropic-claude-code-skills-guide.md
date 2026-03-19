---
title: "Anthropic 工程師揭秘：9 大 Skills 應用情境，把 Claude Code 逼出極限的內部心法"
date: 2026-03-19T23:30:00+08:00
description: "Anthropic 工程師 Thariq 發表萬字長文，首度公開團隊如何用 Skills 系統將 Claude Code 發揮到極致。從避坑指南、漸進式揭露到動態 Hook，9 大應用情境加上高階技巧完整解析，並對比 OpenClaw AgentSkill 架構的實作經驗。"
categories: ["科技"]
tags: ["Claude Code", "Anthropic", "Skills", "AI Agent", "OpenClaw", "提示工程", "開發工具"]
image: "images/tech/2026-03-19-claude-code-skills.jpg"
readingTime: 5
draft: false
faq:
  - q: "Claude Code 的 Skills 是什麼？"
    a: "Skills 是 Claude Code 中的資料夾結構，不只包含 Markdown 說明，還能放入執行腳本、測試數據、動態 Hook 攔截器等。它讓 AI 代理不再只是被動閱讀，而是能主動發現並調用這些工具來完成複雜任務。"
  - q: "Anthropic 內部有多少個 Skills？"
    a: "根據工程師 Thariq 的揭露，Anthropic 內部已有數百個活躍的 Skills 在運作，涵蓋 API 參考、自動測試、CI/CD、故障排除等 9 大類別。"
  - q: "Skills 跟一般的 Prompt 有什麼不同？"
    a: "一般 Prompt 是一次性的文字指令；Skills 是持久化的資料夾結構，包含說明文件、腳本、資產和 Hook。它支援漸進式揭露（AI 按需讀取子檔案）和記憶能力（讀寫 log/JSON），遠比單純的 Prompt 強大。"
  - q: "OpenClaw 的 AgentSkill 跟 Claude Code Skills 有什麼異同？"
    a: "兩者架構高度相似：都採用資料夾結構、支援漸進式揭露和記憶系統。OpenClaw 還額外提供了 ClawHub 技能市集、跨代理共享、以及向量記憶搜尋等功能。"
---

Anthropic 工程師 Thariq 近日在 X 上發表了一篇[深度長文](https://x.com/trq212/status/2033949937936085378)，首度公開團隊在開發 Claude Code 的過程中，如何將「Skills（技能）」系統發揮到極致。這不只是一篇技術分享，更是一份 AI 代理開發者的實戰指南。

## 破除迷思：Skills 不只是 Markdown

很多開發者以為 Skills 只是「寫滿提示詞的文字檔」。Thariq 直接打破了這個迷思：

> Skills 的本質是一個完整的資料夾結構，具備動態腳本與記憶能力的強大工具夾。

一個 Skill 資料夾可以包含：

| 檔案類型 | 用途 | 範例 |
|----------|------|------|
| **Markdown** | 說明文件、行為規範 | `SKILL.md`、`README.md` |
| **腳本 (Scripts)** | 自動化流程 | `deploy.sh`、`validate.py` |
| **資產 (Assets)** | 範例資料、模板 | `template.json`、`schema.yaml` |
| **Hook 設定** | 動態攔截器 | `.hooks/pre-execute.js` |
| **測試數據** | 驗證用例 | `tests/fixtures/` |

這讓 AI 代理不只是被動閱讀說明，而是能主動發現、調用、甚至動態執行這些工具。

## Anthropic 內部的 9 大應用情境

Thariq 披露，Anthropic 內部已有**數百個活躍的 Skills**，團隊將最實用的歸納為 9 大類：

### 1. 函式庫與 API 參考

提供內部工具的正確用法，避免 AI 踩坑。這是最基礎也最常見的 Skill 類型——把 API 文件結構化後放進 Skill，Claude 就不會再亂猜參數。

### 2. 產品功能驗證

結合 Playwright 等自動化測試工具，讓 AI 在無頭瀏覽器中自動跑完註冊、結帳等流程並驗證狀態。這意味著 Claude 不只會寫程式碼，還會自己驗證程式碼的效果。

### 3. 數據獲取與分析

串接 Grafana 等儀表板，教導 AI 如何下正確的 SQL 查詢來比對數據。Skill 中會包含資料庫的 Schema 說明和常用查詢範本。

### 4. 團隊流程自動化

彙整 GitHub 與工單系統進度，自動生成每日站會（Standup）報告。這是最能節省團隊時間的 Skill 之一。

### 5. 程式碼框架生成

針對特定框架生成包含驗證、日誌與部署設定的樣板程式碼。比起從零開始，有了 Skill 的 AI 能直接產出符合團隊規範的 boilerplate。

### 6. 程式碼品質審查

建立對抗性的「AI 審查員」來挑毛病，並強制執行團隊專屬的程式碼風格。Thariq 稱這是他們最常用的 Skill 類型之一。

### 7. CI/CD 與部署自動化

監控 PR 狀態、解決合併衝突，甚至執行帶有錯誤率監控的金絲雀部署。讓 AI 不只管程式碼，也管部署流程。

### 8. 故障排除指南 (Runbooks)

接收報錯訊息後，自動呼叫對應工具（如 Log 查詢）進行調查並產出結構化報告。從「收到 alert」到「找到根因」可以全部由 AI 完成。

### 9. 基礎設施維運

尋找閒置資源、分析雲端帳單飆升原因，並為破壞性操作（如刪除資料庫）加上安全確認鎖。

## 打造完美 Skill 的 4 個內行秘訣

### 秘訣一：必寫「避坑指南 (Gotchas)」

Thariq 強調這是 Skill 中**含金量最高**的部分：

> 將 Claude 過去常犯的錯誤記錄下來，能大幅提升後續的執行成功率。

例如：「這個 API 的 `pageSize` 最大值是 100，超過會靜默截斷而不報錯」——這種資訊能讓 AI 少走無數冤枉路。

### 秘訣二：善用「漸進式揭露」

不要把所有資訊塞在同一個檔案。將範例、API 文件拆分到子資料夾中，告訴 AI 這些檔案的存在位置。它會在需要時自行讀取，**節省 Token 且更精準**。

```
my-skill/
├── SKILL.md          # 核心說明（精簡）
├── references/       # 詳細 API 文件（按需讀取）
│   ├── api-v2.md
│   └── schema.yaml
└── scripts/          # 自動化腳本
    └── validate.sh
```

### 秘訣三：賦予記憶能力

Skill 內部可以讀寫 Log 檔或 JSON，讓 AI 能查看自己之前的操作紀錄，保持上下文連貫。這解決了 AI 代理「每次醒來都失憶」的根本問題。

### 秘訣四：設計「按需觸發」的動態 Hook

例如設計一個 `/careful` 模式——只有在明確知道要觸碰正式環境（Production）時才啟動，用來攔截 `rm -rf` 或 `DROP TABLE` 等危險指令。平常不啟動，避免額外開銷。

## 對比：OpenClaw AgentSkill 的實作經驗

作為一個已經在生產環境中大量使用 AI 代理的平台，[OpenClaw](https://github.com/openclaw/openclaw) 的 AgentSkill 架構跟 Claude Code Skills 驚人地相似。以下是兩者的對比：

| 功能 | Claude Code Skills | OpenClaw AgentSkill |
|------|-------------------|---------------------|
| 資料夾結構 | ✅ Skill 資料夾 | ✅ `SKILL.md` + `references/` + `scripts/` |
| 漸進式揭露 | ✅ 子資料夾按需讀取 | ✅ `<available_skills>` 描述 + 按需 `read` |
| 記憶系統 | ✅ 讀寫 Log/JSON | ✅ `memory_store` / `memory_recall` 向量搜尋 |
| 避坑指南 | ✅ Gotchas 區塊 | ✅ 寫在 SKILL.md 的注意事項 |
| 動態 Hook | ✅ Hook 攔截器 | ⬜ 尚未實作（有 exec 審批機制） |
| 技能市集 | ⬜ 無 | ✅ [ClawHub](https://clawhub.com) 搜尋/安裝/發布 |
| 跨代理共享 | ⬜ 單代理 | ✅ 子代理繼承 workspace skills |
| 安全模式 | ✅ `/careful` 模式 | ✅ exec 權限控制 + elevated 審批 |

### OpenClaw 額外的優勢

1. **向量記憶搜尋**：不只是讀寫 JSON，而是用向量 + 關鍵字混合搜尋，跨 session 保持上下文
2. **ClawHub 市集**：一行 `clawhub install <skill>` 就能安裝社群分享的 Skill
3. **多代理協作**：主代理可以 spawn 子代理，子代理自動繼承 workspace 中的所有 Skills
4. **多通道整合**：同一套 Skills 可以在 Telegram、Discord、Signal 等所有通道使用

## 金句收藏

Thariq 在文末分享了一段值得所有 AI 開發者收藏的話：

> 我們最棒的 Skills，一開始通常也只有幾行程式碼和一個避坑提醒，是隨著團隊不斷遭遇邊緣情況並加以補充，才變得如此強大。

這個觀點跟軟體工程中的迭代開發完全一致——**最好的 Skill 不是一開始就完美設計出來的，而是在實戰中逐步演化的**。

## 結語：AI 代理的未來在 Skills

從 Anthropic 內部數百個 Skills 的規模來看，「Skills 工程」正在成為 AI 開發的新核心能力。它不是 Prompt Engineering 的替代品，而是更高層級的抽象——**把知識、流程和安全規則打包成可複用、可演化的模組**。

無論你用的是 Claude Code、OpenClaw、Cursor 還是其他 AI 代理工具，花時間建立和維護你的 Skills 庫，將是投資報酬率最高的一件事。

---

*原文來源：[動區動趨](https://www.blocktempo.com/anthropic-engineer-thariq-claude-code-skills-lessons/) | [Thariq 原始推文](https://x.com/trq212/status/2033949937936085378)*
