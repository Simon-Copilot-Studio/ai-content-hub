---
title: "Nvidia CEO 稱 OpenClaw 是「下一個 ChatGPT」，但 ClawHub 12% 惡意技能敲響警鐘"
date: 2026-03-27
description: "Nvidia CEO 黃仁勳公開背書 OpenClaw 為下一代 AI 平台，同時 ClawHub 市場被發現 12% 技能為惡意軟體。這場光環與陰影並存的故事，揭示了 AI Agent 生態的機遇與風險。"
categories: ["tech"]
tags: ["OpenClaw", "Nvidia", "黃仁勳", "ClawHub", "AI安全", "惡意軟體", "AI Agent"]
image: "/images/2026-03-27-openclaw-nvidia-clawhub.webp"
readingTime: 4
draft: false
---

一邊是全球最有影響力的科技 CEO 公開背書，另一邊是安全研究人員發現生態系中暗藏惡意軟體。OpenClaw 的 2026 年 3 月，可說是光環與陰影並存。

## 黃仁勳：「我每天早上都在用」

Nvidia CEO 黃仁勳在近日的採訪中明確表示：「**下一個 ChatGPT 毫無疑問就是 OpenClaw**」，並透露自己每天早上都在使用這個開源 AI 代理平台。

這番言論來自一位執掌 3 兆美元市值公司的 CEO，份量不言而喻。Gizmodo Japan 的報導指出，OpenClaw 僅問世數月，就獲得了 AI 晶片界最重要人物的認可。

### 為什麼是 OpenClaw？

OpenClaw 與 ChatGPT 的本質差異在於：

| 特性 | ChatGPT | OpenClaw |
|------|---------|----------|
| 定位 | 對話式 AI | AI 代理平台 |
| 運作方式 | 問答互動 | 自主執行任務 |
| 擴展性 | 官方插件 | 開源技能市場 |
| 工具控制 | 有限 | 可控制瀏覽器、檔案、排程等 |
| 部署方式 | 雲端 | 自託管 |

簡單來說，ChatGPT 是一個聰明的對話夥伴，而 OpenClaw 更像是一個**會自己動手做事的數位同事**。

## ClawHub 安全事件：341 個惡意技能

就在黃仁勳的背書引發關注的同時，安全研究人員對 ClawHub 技能市場進行了全面審計，結果令人震驚：

> **在 2,857 個已發布的技能中，341 個被確認為惡意軟體**，比例高達 12%。

這些惡意技能可能會：
- 竊取使用者的 API 金鑰和憑證
- 存取本地檔案系統中的敏感資料
- 在背景執行未經授權的操作
- 將個人資訊回傳給攻擊者

### OpenClaw 的回應

面對這個嚴重的安全漏洞，OpenClaw 團隊迅速推出了**驗證篩選機制（Verified Skill Screening）**，包含：

1. **自動化安全掃描**：所有新上架技能必須通過靜態分析
2. **驗證標章**：通過審核的技能獲得「✓ Verified」標記
3. **社群舉報系統**：使用者可回報可疑行為
4. **權限沙盒**：限制技能可存取的系統資源

## Bloomberg：創始人加入 OpenAI

同一週，Bloomberg 報導 OpenClaw 創始人**已加入 OpenAI**，並公開表示美國應向中國學習 AI 應用的採納速度。這一人事異動為 OpenClaw 的未來發展增添了不確定性，同時也暗示 OpenAI 可能正在佈局 AI 代理領域。

## 投資人的「大轉向」

有趣的是，Financial Content 同時報導了另一個趨勢：**投資人正從 AI 熱潮轉向「舊經濟」**。這個被稱為「2026 大轉向」的現象，是否會影響 OpenClaw 等 AI 新創的資金來源，值得持續觀察。

## 對使用者的實際建議

如果你正在使用或考慮使用 OpenClaw：

1. ✅ **只安裝有 Verified 標章的技能**
2. ✅ **定期檢查已安裝技能的更新日誌**
3. ✅ **使用 `skill-vetter` 技能在安裝前進行安全審查**
4. ⚠️ **避免從非官方管道安裝技能**
5. ⚠️ **檢查技能要求的權限是否合理**

## 與本月其他大事的關聯

3 月是 AI 產業極度密集的月份：
- [Anthropic 洩漏 Claude Mythos](/tech/2026-03-27-anthropic-claude-mythos-leak-capybara/) 顯示前沿模型競爭白熱化
- [Google Gemini 記憶匯入](/tech/2026-03-27-google-gemini-import-memory-ai-portability/) 凸顯使用者體驗的重要性
- **MCP 安裝量破 9,700 萬**，AI 代理基礎設施進入主流
- OpenClaw 獲 Nvidia CEO 背書的同時面臨生態系安全挑戰

這一切都指向同一個結論：**AI 代理時代已經到來，但伴隨而來的安全和治理問題同樣迫切**。

## FAQ

### Q: OpenClaw 和 ChatGPT 可以同時使用嗎？
A: 可以。OpenClaw 可以連接多個 AI 模型（包括 GPT、Claude、Gemini），ChatGPT 更像是其中一個「大腦」，而 OpenClaw 提供「手和腳」。

### Q: ClawHub 上的惡意技能已經被移除了嗎？
A: 是的。OpenClaw 已推出驗證篩選機制，已識別的 341 個惡意技能已下架，新技能需通過安全審查才能上架。

### Q: 黃仁勳的背書會影響 OpenClaw 的發展嗎？
A: 短期內會顯著提升知名度和使用者增長。但長期發展取決於產品本身的品質和生態系的健康度。

### Q: OpenClaw 創始人離開後，專案還會繼續嗎？
A: OpenClaw 是開源專案，不依賴單一個人。社群和核心團隊的其他成員會持續維護和發展。
