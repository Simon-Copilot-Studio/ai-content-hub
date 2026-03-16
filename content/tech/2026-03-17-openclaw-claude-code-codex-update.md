---
title: "OpenClaw 下週重大更新：支援 Claude Code 與 OpenAI Codex，開源 AI 代理引擎的野心"
date: 2026-03-17T07:00:00+08:00
description: "OpenClaw 創辦人 Peter Steinberger 宣布下週將支援 Claude Code 外掛、OpenAI Codex CLI 整合、ACP 協議相容，並拆分核心引擎為獨立套件。分析其市場定位與面臨的挑戰。"
categories: ["科技"]
tags: ["OpenClaw", "Claude Code", "Codex", "AI編程", "開源", "ACP"]
image: "images/tech/2026-03-17-openclaw-update.jpg"
readingTime: 3
draft: false
faq:
  - q: "OpenClaw 是什麼？"
    a: "OpenClaw 是由前 PSPDFKit 創辦人 Peter Steinberger 打造的開源 AI 編碼代理引擎，定位為輕量、可嵌入的代理運行時（agent runtime），而非完整 IDE。"
  - q: "OpenClaw 下週更新有哪些新功能？"
    a: "主要包含五項：Claude Code 外掛支援、OpenAI Codex CLI 整合、ACP（Agent Communication Protocol）相容、代理中斷機制修復、核心引擎拆分為獨立套件。"
  - q: "OpenClaw 和 Cursor、Claude Code 有什麼不同？"
    a: "Cursor 和 Windsurf 是完整 IDE，Claude Code 和 Codex 是 CLI 代理，而 OpenClaw 定位為可嵌入的底層引擎，讓其他工具能夠使用它的代理能力。三者處於不同層級。"
---

OpenClaw 創辦人 Peter Steinberger 在 X 上宣布了下週即將推出的更新清單，涵蓋多項重大功能整合。這次更新將讓 OpenClaw 同時打通 Anthropic 和 OpenAI 兩大生態系，進一步鞏固其作為開源代理引擎的定位。

## 五大更新內容

### 1. Claude Code 外掛支援

OpenClaw 將能作為 Anthropic 生態系的延伸工具運作。這意味著使用者可以在 OpenClaw 的框架內，直接調用 Claude Code 的程式開發能力，實現更深度的自動化工作流程。

### 2. OpenAI Codex CLI 整合

同時相容 OpenAI 的命令列開發工具 Codex CLI。雙平台支援讓使用者不必在 Anthropic 和 OpenAI 之間二選一，根據任務特性選擇最適合的模型。

### 3. ACP 協議相容

ACP（Agent Communication Protocol）是目前多代理架構的基礎設施標準。支援 ACP 意味著 OpenClaw 的代理可以與其他遵循同一協議的代理系統互通，為跨平台協作開啟大門。

### 4. 代理中斷機制修復

解決了代理執行中途無法優雅停止的問題。這聽起來是小事，但在生產環境中，能否安全中斷一個正在執行的 AI 代理，是可靠性的關鍵指標。

### 5. 核心引擎拆分

將核心引擎拆分為獨立套件，降低安裝體積並改善模組化程度。這對於只需要 OpenClaw 部分功能的開發者來說，是一個實用的改進。

## 市場定位：第三層的生存空間

目前 AI 編碼工具市場大致分三層：

- **完整 IDE**：Cursor、Windsurf、GitHub Copilot Workspace
- **CLI 代理**：Claude Code、OpenAI Codex CLI、Aider
- **可嵌入引擎**：OpenClaw 試圖佔據的位置

OpenClaw 的策略是「讓別人的工具用我的引擎」，這需要生態系的網路效應來支撐。開源是它的護城河之一，特別是對資料敏感的企業用戶有吸引力。

## 值得觀察的風險

動區動趨的分析指出一個值得關注的風險：Steinberger 目前仍同時經營 PSPDFKit（現更名為 Nutrient，100+ 員工）。在 AI 工具以「週」為單位高速迭代的環境下，一位兼職創辦人的投入度是否足夠，是個合理的擔憂。

不過，Steinberger 在開發者工具領域的技術信譽毋庸置疑，PSPDFKit 是少數能在 B2B SDK 市場存活超過十年的獨立公司。技術能力不是問題，時間和頻寬才是。

## 對開發者的建議

如果你正在使用 OpenClaw 或考慮導入，下週的更新值得第一時間升級測試。Claude Code + Codex 雙支援加上 ACP 協議，讓 OpenClaw 成為目前市場上整合度最高的開源代理引擎之一。
