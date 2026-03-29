---
title: "ShadowPrompt 零點擊漏洞：Anthropic Claude Chrome 擴充套件險遭全面劫持"
date: 2026-03-28
description: "Anthropic Claude Chrome Extension 爆出 ShadowPrompt 零點擊漏洞，攻擊者僅需讓用戶造訪惡意網頁即可竊取 Gmail Token、Google Drive 檔案與聊天記錄。已修補，但 300 萬用戶曾暴露在風險中。"
categories: ["tech"]
tags: ["Anthropic", "Claude", "Chrome Extension", "零點擊漏洞", "ShadowPrompt", "資安", "Prompt Injection", "AI安全"]
image: "/images/tech/2026-03-28-claude-chrome-extension-shadowprompt-zero-click.png"
readingTime: 5
draft: false
---

一個「零點擊」漏洞差點讓 300 萬 Claude Chrome Extension 用戶的瀏覽器被完全控制——不需要點擊任何東西，只要造訪一個惡意網頁就夠了。

## 漏洞概述

資安研究團隊 KOI Security 發現了一條被命名為「**ShadowPrompt**」的攻擊鏈，串連了 Anthropic Claude Chrome Extension 中的兩個獨立缺陷：

1. **過度寬鬆的 Origin 白名單**：擴充套件的訊息 API 接受來自任何 `*.claude.ai` 子域名的請求
2. **第三方元件 XSS 漏洞**：Anthropic 使用的 Arkose Labs CAPTCHA 元件託管在 `a-cdn.claude.ai`，舊版本存在 DOM-based XSS

## 攻擊鏈如何運作？

攻擊流程極其隱蔽：

```
惡意網頁 → 嵌入舊版 Arkose CAPTCHA iframe
         → postMessage 注入 HTML payload
         → 在 a-cdn.claude.ai 上下文執行 JS
         → chrome.runtime.sendMessage() 發送惡意指令
         → Claude 擴充套件以為是用戶指令，照做不誤
```

因為 `a-cdn.claude.ai` 符合 `*.claude.ai` 萬用字元，擴充套件完全信任該來源。攻擊者可以讓 Claude 執行任何指令，包括：

- 🔑 **竊取 Google OAuth Token**（持久存取權限）
- 📁 **讀取 Google Drive 檔案**
- 📧 **以用戶名義發送 Gmail**
- 💬 **匯出完整聊天記錄**

全程沒有點擊、沒有權限對話框、沒有任何可見提示。

## 時間軸

| 日期 | 事件 |
|------|------|
| 2025 年 12 月 | 透過 HackerOne 揭露漏洞 |
| 2026 年 1 月 15 日 | Anthropic 部署修補：將萬用字元白名單改為嚴格的 `https://claude.ai` 來源檢查 |
| 2026 年 2 月 19 日 | Arkose Labs XSS 漏洞修補完成 |
| 2026 年 3 月 26 日 | 公開披露 |

## 這件事為什麼重要？

這不只是一個 Chrome Extension 的 bug——它揭示了 **AI 瀏覽器代理的根本安全挑戰**：

### 1. AI 代理 = 放大器
傳統 XSS 漏洞的影響範圍有限，但當 XSS 可以操控一個擁有「自主瀏覽、執行 JavaScript、與網路服務互動」能力的 AI 代理時，影響範圍呈指數級擴大。

### 2. 信任邊界模糊
擴充套件將來自子域名的請求等同於用戶指令——這在 AI Agent 時代是致命的設計缺陷。Prompt Injection 的攻擊面比傳統 Web 應用大得多。

### 3. 供應鏈風險
第三方 CAPTCHA 元件的舊版本成為攻擊入口，說明 AI 產品的安全不只取決於自身程式碼，還取決於整個依賴鏈。

## 用戶該怎麼做？

- **立即更新** Claude Chrome Extension 到 v1.0.41 或更新版本
- **檢查 Google 帳戶活動**，確認沒有可疑的第三方存取
- **撤銷不明的 OAuth Token**（Google 帳戶設定 → 安全性 → 第三方存取）

## FAQ

**Q: 我使用 Claude 網頁版而非 Chrome Extension，是否受影響？**
A: 不受影響。此漏洞僅影響 Chrome Extension（v1.0.41 之前的版本）。

**Q: 攻擊者是否已實際利用此漏洞？**
A: 目前沒有證據顯示此漏洞在修補前被大規模利用，但無法完全排除。

**Q: 其他 AI Chrome Extension 是否有類似風險？**
A: 任何使用寬鬆 Origin 檢查且具備自主操作能力的 AI 擴充套件都可能存在類似風險。建議僅安裝來自可信來源的 AI 擴充套件。
