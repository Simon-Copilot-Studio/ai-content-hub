---
title: "Google Cloud 全面押注 Agentic AI 資安：收購 Wiz、MCP 整合、自主安全代理一次看懂"
date: 2026-04-02
description: "Google Cloud 在 RSAC 2026 大會上揭示 Agentic AI 資安戰略：完成 Wiz 收購強化多雲安全、推出自主調查代理、支援 MCP 協議讓企業自建安全 Agent，並整合暗網威脅情報。這是雲端資安進入 AI Agent 時代的里程碑。"
categories: ["tech"]
tags: ["Google Cloud", "Agentic AI", "資安", "Wiz", "MCP", "Cybersecurity", "RSAC", "AI Agent", "Vertex AI", "威脅情報", "多雲安全"]
image: "https://images.unsplash.com/photo-1563986768609-322da13575f2?w=1200"
readingTime: 7
draft: false
---

2026 年 4 月，資安產業正在經歷一場典範轉移。Google Cloud 在剛落幕的 **RSAC 2026** 大會上，一口氣丟出多項重磅發表——從完成對 **Wiz** 的收購整合，到推出可自主調查威脅的 **Agentic AI 安全代理**，再到支援 **Model Context Protocol（MCP）** 讓企業自建安全 Agent。

這不只是產品更新，而是宣告：**雲端資安正式進入 AI Agent 時代。**

## Wiz 收購完成：多雲安全的最後一塊拼圖

Google Cloud 在今年 3 月正式完成對資安新創 Wiz 的收購。Wiz 以其出色的雲端原生安全能力聞名，特別擅長：

- **多雲環境**的統一安全視圖
- 針對 **AI 工作負載**的專用防護
- 可擴展的 **AI 安全代理**架構

收購完成後，Wiz 的能力將深度整合進 Google Cloud 生態系，與既有的 **Mandiant** 威脅情報形成互補——Mandiant 負責攻擊面洞察，Wiz 負責雲端內部防護，兩者加在一起構成完整的縱深防禦。

對企業用戶來說，這意味著不再需要拼湊多家資安工具，Google Cloud 正朝著「**一站式 AI 資安平台**」邁進。

## Agentic AI 安全代理：讓 AI 自主調查威脅

最令人興奮的發表是 **Google Security Operations** 中的 Agentic AI 自動化功能（目前為預覽版）。核心亮點包括：

### 🔍 Triage & Investigation Agent

這個自主代理可以：

1. **自動調查安全警報** — 不再需要 SOC 分析師逐一手動審查
2. **收集證據並建立分析鏈** — 為後續的人工決策提供完整脈絡
3. **提供處置建議** — 加速決策流程

Google 內部測試顯示，整合 Google Threat Intelligence 後，系統可以分析每日**數百萬筆外部事件**，準確率達 **98%**。

### 🌐 支援 MCP 自建安全 Agent

從 2026 年 4 月起，Google Security Operations 客戶可以透過 **遠端 MCP 伺服器**開發自己的安全代理。

這一點意義重大。MCP（Model Context Protocol）是近期 AI Agent 生態中最重要的標準協議之一，它讓不同的 AI 模型能夠安全地存取外部工具和資料來源。Google 率先在資安領域支援 MCP，等於是為企業打開了**自定義 AI 資安工作流**的大門。

想像一下：

- 你可以建立一個專門監控 Kubernetes 叢集的安全 Agent
- 或是一個自動分析釣魚郵件的 Agent
- 甚至是跨多個雲端供應商統一回應事件的 Agent

這不再是概念驗證，而是 **production-ready** 的能力。

## 暗網威脅情報：主動追蹤最難纏的威脅

Google Cloud 還在 Threat Intelligence 中推出了**暗網情報功能**，能為每個組織建立獨特的威脅檔案。

傳統的威脅情報多半聚焦在公開來源（OSINT），但真正的高價值攻擊情報——像是被竊取的企業憑證、內部資料洩漏、針對性攻擊的討論——往往藏在暗網深處。Google 利用 AI Agent 來自動化這些情報的蒐集、篩選與關聯分析，讓企業能夠在攻擊發生**之前**就掌握威脅態勢。

## Vertex AI Agent Engine 也獲得安全升級

除了 Security Operations，Google Cloud 還在更廣泛的 AI 產品線中強化安全：

| 功能 | 說明 |
|------|------|
| **AI Protection in Security Command Center** | 延伸至 Vertex AI Agent Engine，攔截代理傳遞的威脅 |
| **Model Armor + MCP** | 整合 Google MCP 伺服器，擴大模型防護覆蓋範圍 |
| **敏感資料保護** | 新增 AI 驅動的上下文分類功能 |
| **外部暴露面管理** | 從外部視角觀察組織的攻擊面 |

這些更新共同指向一個方向：**AI Agent 本身也需要被保護**。當企業部署越來越多的 AI 代理，這些代理就成了新的攻擊面。Google 顯然已經在超前部署這個問題。

## 對產業的影響：三個關鍵觀察

### 1. 資安人力短缺問題有了新解法

全球資安人才缺口估計超過 **350 萬人**。Agentic AI 不是要取代資安分析師，而是讓每個分析師都有一支 AI 團隊協助處理例行調查，專注在真正需要人類判斷的高風險決策。

### 2. MCP 正在成為 AI Agent 的「USB 標準」

Google 在資安領域率先支援 MCP，加上 Anthropic、Microsoft 等也在積極推進，MCP 作為 AI Agent 互通標準的地位正在快速鞏固。對開發者來說，現在學習 MCP 的投資報酬率極高。

### 3. 雲端巨頭的資安軍備競賽加劇

微軟有 Security Copilot，AWS 有 GuardDuty + Bedrock，現在 Google Cloud 用 Wiz + Agentic AI + MCP 打出組合拳。企業在選擇雲端供應商時，**AI 資安能力**正在成為與算力、價格同等重要的決策因素。

## 結語

Google Cloud 在 RSAC 2026 的表現，不只是發佈了幾個新功能。它展示了一個清晰的願景：**未來的資安防禦將由 AI Agent 驅動，人類負責監督和決策，而 MCP 是連接一切的標準。**

這對正在評估雲端資安策略的企業來說，是時候認真看待 Agentic AI 了——不是明年，是現在。

---

## FAQ

### Google Cloud 收購 Wiz 對用戶有什麼影響？

Wiz 的多雲安全能力將整合進 Google Cloud 生態系，與 Mandiant 威脅情報互補，用戶可以獲得更完整的一站式 AI 資安防護，不需要額外拼湊第三方工具。

### 什麼是 Agentic AI 安全代理？

這是一種可以自主調查安全警報、收集證據、提供處置建議的 AI 代理。它內建於 Google Security Operations，能處理每日數百萬筆事件，準確率達 98%，大幅減輕 SOC 分析師的工作負擔。

### MCP 在資安領域的應用是什麼？

MCP（Model Context Protocol）讓企業可以自建安全 Agent，透過標準協議安全地存取外部工具和資料來源。Google 從 2026 年 4 月起在 Security Operations 中支援遠端 MCP 伺服器，企業可以打造針對特定需求的自定義 AI 資安工作流。

### 企業現在應該如何準備？

建議從三個方向著手：(1) 評估現有資安工具是否支援 AI Agent 整合、(2) 開始培養團隊的 MCP 開發能力、(3) 在非關鍵環境中試用 Agentic AI 安全代理，逐步建立信心和最佳實踐。
