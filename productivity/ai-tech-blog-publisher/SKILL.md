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

**版本**：1.1.0  
**作者**：Hermes Agent  
**標籤**：["blog", "ai", "automation", "seo", "tech", "finance"]  
**建立日期**：2026-05-17  
**最後更新**：2026-06-08

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

# 更精確的方法：檢查當天已發布文章
search_files pattern="$(date +%Y-%m-%d)-" target="files" path="tech"
```

### 2. 避免重複主題檢查 🚫
```python
# 檢查當日是否已有相似主題文章
import os
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
tech_dir = '/home/simon/blog/content/tech'

# 獲取當天所有文章
today_articles = []
for file in os.listdir(tech_dir):
    if file.startswith(today):
        today_articles.append(file)

# 分析已發布主題
published_topics = []
for article in today_articles:
    with open(os.path.join(tech_dir, article), 'r') as f:
        content = f.read()
        if 'AI泡沫' in content or 'ai-bubble' in article:
            published_topics.append('AI泡沫')
        if 'geopolitical' in content or '地緣政治' in content:
            published_topics.append('地緣政治')
        # 添加更多主題檢查...

print(f"已發布主題: {published_topics}")
```

### 3. 熱門話題搜尋 📈
**策略：多管道搜尋**
- **主要來源**：內容分析 + 搜尋工具 (推薦)
  ```bash
  # 使用 search_files 分析現有內容，找出熱門話題
  search_files pattern="AI|artificial intelligence|machine learning|deep learning|大模型|AI芯片|LLM" target="content" path="." limit=20
  search_files pattern="股市|股票|Fed|台股|美股|crypto|bitcoins|加密貨幣|央行" target="content" path="." limit=20
  search_files pattern="Apple|Google|Meta|TSMC|Nvidia|芯片|半導體|科技|technology" target="content" path="." limit=20
  
  # 分析話題頻率，找出最熱門主題
  # 優點：避免重複、即時性、多來源整合
  # 注意：需要過濾已發布內容
  ```

- **次要來源**：TechNews.tw、ETtoday、中央社科技版
  - 直接導航網站獲取最新內容
  - 避免 RSS feed 的延遲和過時問題
- **備用來源**：Bloomberg、The Verge、WSJ
  - 注意：可能遭遇 bot detection，需要備用方案

**搜尋時間範圍**：
- **推薦**：過去 3 小時內 (獲取最新熱門)
- **備用**：過去 24 小時內

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
1. **自動圖片生成工具** (推薦)
   ```python
   # 使用 image_gen 工具自動生成專屬封面圖
   delegate_task goal="生成加密貨幣市場分析文章的封面圖，圖片應專業、現代，包含Bitcoin、Ethereum等加密貨幣元素，適合繁體中文讀者。圖片格式為PNG，尺寸建議1200x600px。" toolsets=["image_gen"]
   
   # 檢查生成結果
   search_files pattern="crypto" target="files" path="/home/simon/blog/static/images" file_glob="*.png"
   ```
   - 優點：完全自控、符合文章主題、無版權問題
   - 需要：image_gen 工具支援
   - 注意：檢查生成是否成功

2. **使用 skill 工具生成圖片** (備用)
   ```bash
   # 如果 image_gen 失敗，使用其他圖片生成技能
   ```

3. **使用 Unsplash API 獲取免費高品質圖片**
   ```python
   # 直接使用 Unsplash URL 作為 fallback
   image_url = "https://source.unsplash.com/random/?crypto,currency,finance"
   ```

4. **使用 Unsplash URL 作為最終 fallback**
   ```bash
   # 在圖片生成失敗時使用
   echo "image: \"/static/images/[article_topic]_chinese.png\"" > fallback_image.yml
   ```

**圖片要求**：
- 寬度 1200px x 高度 630px (Facebook分享最佳比例)
- 相關主題
- 高品質免版權
- 中文標題顯示

### 6. Git 操作 🚀
```bash
cd ~/blog

# 檢查 git 狀態
git status

# 添加新文章
git add content/tech/YYYY-MM-DD-article-title.md

# 提交變更
git commit -m "auto: [文章標題]"

# 重要：處理可能的遠端衝突
git pull --rebase origin main

# 推送到遠端
git push origin main
```

**Git 衝突處理**：
- **問題**：多台設備同時推送時可能發生衝突
- **解決方案**：使用 `git pull --rebase` 整合遠端變更
- **注意**：確保 commit 訊息格式一致 (`auto: [標題]`)

### 7. 通知系統 📱
**本地通知檔案**：
```bash
# 建立通知檔案
echo "🚀 新文章發布通知：" > ~/blog_notification.txt
echo "📄 標題：[文章標題]" >> ~/blog_notification.txt
echo "📅 發布時間：$(date '+%Y-%m-%d %H:%M:%S')" >> ~/blog_notification.txt
echo "🔗 URL：https://simoncopilotstudio.github.io/ai-content-hub/" >> ~/blog_notification.txt
echo "📊 字數：[文章字數]字" >> ~/blog_notification.txt
echo "📝 Commit Hash：$(git rev-parse HEAD)" >> ~/blog_notification.txt
echo "📂 文章路徑：~/blog/content/tech/YYYY-MM-DD-article-title.md" >> ~/blog_notification.txt
```

**通知內容範例**：
```
🚀 新文章發布通知：
📄 標題：AI泡沫破裂警鐘響起：債券巨頭預測100%機率
📅 發布時間：2026-06-08 09:30:00
🔗 URL：https://simoncopilotstudio.github.io/ai-content-hub/
📊 字數：11,883字
📝 Commit Hash：183559e1
📂 文章路徑：~/blog/content/tech/2026-06-08-ai-bubble-burst-warning.md
```

**進階通知選項**：
- **Telegram 通知** (推薦)
  ```python
  import requests
  
  TELEGRAM_BOT_TOKEN = "your_bot_token"
  TELEGRAM_CHAT_ID = "your_chat_id"
  
  message = f"""
  📝 新文章已發布！
  
  標題：{article_title}
  日期：{publish_date}
  類別：{categories}
  標籤：{tags}
  
  文章內容涵蓋：
  • {key_points}
  
  已成功推送到 GitHub 倉庫！
  """
  
  telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": message,
      "parse_mode": "HTML"
  }
  
  response = requests.post(telegram_url, json=payload)
  ```
  
  - **注意**：需要正確的 Bot Token 和 Chat ID
  - **錯誤處理**：如果認證失敗，記錄日誌但不影響發布流程
  
- **本地通知檔案**：
  ```bash
  # 建立通知檔案
  echo "🚀 新文章發布通知：" > ~/blog_notification.txt
  echo "📄 標題：[文章標題]" >> ~/blog_notification.txt
  echo "📅 發布時間：$(date '+%Y-%m-%d %H:%M:%S')" >> ~/blog_notification.txt
  echo "🔗 URL：https://simoncopilotstudio.github.io/ai-content-hub/" >> ~/blog_notification.txt
  echo "📊 字數：[文章字數]字" >> ~/blog_notification.txt
  echo "📝 Commit Hash：$(git rev-parse HEAD)" >> ~/blog_notification.txt
  echo "📂 文章路徑：~/blog/content/tech/YYYY-MM-DD-article-title.md" >> ~/blog_notification.txt
  ```

**通知內容範例**：
```
🚀 新文章發布通知：
📄 標題：加密貨幣市場最新趨勢：市場分析與未來展望
📅 發布時間：2026-06-08 10:00:00
🔗 URL：https://simoncopilotstudio.github.io/ai-content-hub/
📊 字數：9,562字
📝 Commit Hash：2caf13de
📂 文章路徑：~/blog/content/tech/2026-06-08-crypto-market-analysis.md
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