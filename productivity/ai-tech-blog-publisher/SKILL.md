---
title: "AI 科技部落格自動發布器"
description: "自動搜尋 AI 科技、經濟財金、科技產業最新熱門話題，撰寫 SEO 優化繁體中文部落格文章並發布"
version: "1.0.0"
author: "Hermes Agent"
tags: ["blog", "ai", "automation", "seo", "tech", "finance"]
created: "2026-05-17"
name: "ai-tech-blog-publisher"
---

# AI 科技部落格自動發布器

**描述**：自動搜尋 AI 科技、經濟財金、科技產業最新熱門話題，撰寫 SEO 優化繁體中文部落格文章並發布

**版本**：1.0.0  
**作者**：Hermes Agent  
**標籤**：["blog", "ai", "automation", "seo", "tech", "finance"]  
**建立日期**：2026-05-17

## 觸發條件
- 需要產生 AI/科技/財金相關的部落格文章
- 要避免與現有內容重複
- 需要自動化發布流程

## 工作流程

### 1. 現有內容檢查 🔍
```bash
# 檢查 ~/blog/content/ 各目錄最近文章，避免重複主題
cd ~/blog/content
ls -la */ | grep "$(date +%Y-%m-%d)"
```

### 2. 熱門話題搜尋 📈
**策略：多管道搜尋**
- **主要來源**：TechNews.tw (台灣科技新聞網站)
  - 直接導航網站獲取最新內容
  - 避免 RSS feed 的延遲和過時問題
- **次要來源**：Bloomberg、The Verge、WSJ
  - 注意：可能遭遇 bot detection，需要備用方案

**搜尋關鍵字**：
- AI/LLM/chips/robotics
- 台股/美股/crypto
- Apple/Google/Meta/TSMC/Nvidia
- 地緣政治對科技影響

### 3. 主題選擇標準 🎯
**價值評估因素**：
- 時效性（過去 24-48 小時內的新聞）
- SEO 潛力（關鍵字密度和搜尋量）
- 讀者關注度（瀏覽量和討論度）
- 專業深度（技術細節和市場分析）
- 獨特性（避免與現有文章重複）

### 4. 文章撰寫格式 📝
**YAML Frontmatter 結構**：
```yaml
---
title: "文章標題"
date: "2026-05-17T09:30:00+08:00"
description: "文章描述"
categories:
  - "科技"
  - "財經"
tags:
  - "AI"
  - "半導體"
  - "KOSPI"
image: "https://images.unsplash.com/...?w=800&q=80"
readingTime: 10
draft: false
faq:
  - q: "問題1"
    a: "答案1"
  - q: "問題2"
    a: "答案2"
---
```

**文章結構範例**：
- 標題和導言
- 背景分析
- 核心內容（3-5 個章節）
- 影響分析
- 未來展望
- FAQ 章節

### 5. 封面圖處理 🖼️
**優先順序**：
1. 使用 AI 生成工具創建專屬圖片
2. 使用 Unsplash API 獲取免費高品質圖片
3. 使用 Unsplash URL 作為 fallback

**圖片要求**：
- 寬度 800px 以上
- 相關主題
- 高品質免版權

### 6. Git 操作 🚀
```bash
cd ~/blog
git add content/tech/YYYY-MM-DD-article-title.md
git commit -m "auto: [文章標題]"
git push origin main
```

### 7. 通知系統 📱
**更新通知檔案**：
```bash
echo "🚀 新文章發布通知：" > ~/blog/telegram_notification.txt
echo "📄 標題：[文章標題]" >> ~/blog/telegram_notification.txt
echo "📅 發布時間：[時間]" >> ~/blog/telegram_notification.txt
echo "🔗 URL：[GitHub 連結]" >> ~/blog/telegram_notification.txt
```

## 實用技巧

### 新聞源處理 📰
- **RSS feed 問題**：很多 RSS feed 已過時或受 bot protection
- **解決方案**：直接導航網站獲取最新內容
- **備用網站**：TechNews.tw、ETtoday、中央社科技版

### Bot Detection 處理 🤖
- **問題**：Bloomberg、WSJ 等金融網站有嚴格的 bot 檢測
- **解決方案**：
  - 使用 browser 工具而非 curl
  - 添加適當的 User-Agent
  - 避免過於頻繁的請求

### 內容避坑指南 ⚠️
- **避免重複**：先檢查現有文章
- **時間戳記**：確認文章發布時間
- **來源驗證**：多來源交叉驗證
- **數據準確性**：確認統計數據和趨勢

## 錯誤處理

### 常見錯誤及解決方案
1. **RSS feed 過時**
   - 檢查 feed 最後更新時間
   - 切換到網站直接訪問

2. **Bot detection**
   - 使用 browser 工具而非 curl
   - 添加適當的延遲

3. **Git 操作失敗**
   - 檢查 git status
   - 確認遠程倉庫連接
   - 檢查 branch 狀態

4. **文章格式錯誤**
   - 使用現有文章作為模板
   - 檢查 YAML frontmatter 格式
   - 驗證 FAQ 結構

## 成功案例

### 案例 1：AI 半導體熱潮
- **主題**：韓股 KOSPI 突破 8,000 點
- **來源**：TechNews.tw 最新報導
- **成果**：189 行深度分析文章
- **關鍵因素**：時效性 + 技術深度 + 投資分析

### 案例 2：ArXiv AI 政策
- **主題**：AI 撰寫論文禁令
- **來源**：學術界最新政策
- **成果**：159 行政策分析文章
- **關鍵因素**：權威性 + 政策深度 + 台灣影響

## 優化建議

### 短期優化
- 建立新聞源監控清單
- 設定內容重複檢查機制
- 優化 SEO 關鍵字選擇

### 長期優化
- 整合 AI 內容生成工具
- 建立多語言發布系統
- 開發內容效果追蹤機制

## 注意事項

1. **版權問題**：確保使用免版權圖片和內容
2. **時效性**：盡量使用 24 小時內的新聞
3. **準確性**：交叉驗證數據和資訊
4. **讀者體驗**：保持內質量和可讀性
5. **SEO 優化**：適當關鍵字密度和結構

---

*此技能基於實際專案經驗開發，持續更新中*
*最後更新：2026-05-17*