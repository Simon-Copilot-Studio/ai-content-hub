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

**版本**：1.2.0  
**作者**：Hermes Agent  
**標籤**：["blog", "ai", "automation", "seo", "tech", "finance"]  
**建立日期**：2026-05-17  
**最後更新**：2026-06-09

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
**策略：多管道搜尋，包含工具可用性檢查**
- **主要來源**：內容分析 + 搜尋工具 (推薦)
  ```bash
  # 檢查 web_search 工具是否可用
  if command -v search > /dev/null; then
      # 使用 search 工具
      search query="AI news LLM chips robotics past 3 hours" engine=web_search
  else
      # 使用 browser 工具直接導航網站
      browser_navigate url="https://techcrunch.com"
      # 手動抓取最新內容
  fi
  
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
  - **注意**：可能遭遇 bot detection，需要備用方案
  - **實際經驗**：Bloomberg 有嚴格 bot 檢測，建議使用 TechCrunch 等替代

**實際執行經驗**：
- **工具檢查**：先檢查工具可用性，再決定採用方法
- **Bot Detection**：Bloomberg 等網站有嚴格 bot 檢測，改用 TechCrunch
- **Browser Navigation**：當 web_search 不可用時，使用 browser_navigate + 手動抓取
- **內容抓取**：使用 browser_snapshot 獲取完整內容，browser_console 獲取純文本

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
**優先順序與實際執行經驗**：
1. **檢查工具可用性** (新增)
   ```bash
   # 先檢查圖片生成工具是否可用
   if skill_exists "stable-diffusion-image-generation"; then
       echo "圖片生成工具可用"
   elif skill_exists "pixel-art"; then
       echo "像素藝術工具可用"
   else
       echo "圖片生成工具不可用，使用 fallback 方案"
   fi
   ```

2. **自動圖片生成工具** (推薦)
   ```python
   # 使用 image_gen 工具自動生成專屬封面圖
   delegate_task goal="生成加密貨幣市場分析文章的封面圖，圖片應專業、現代，包含Bitcoin、Ethereum等加密貨幣元素，適合繁體中文讀者。圖片格式為PNG，尺寸建議1200x600px。" toolsets=["image_gen"]
   
   # 檢查生成結果
   search_files pattern="crypto" target="files" path="/home/simon/blog/static/images" file_glob="*.png"
   ```
   - **實際經驗**：許多圖片生成技能在特定環境中可能不可用
   - 優點：完全自控、符合文章主題、無版權問題
   - 需要：image_gen 工具支援
   - 注意：檢查生成是否成功

3. **使用 skill 工具生成圖片** (備用)
   ```bash
   # 如果 image_gen 失敗，使用其他圖片生成技能
   skill_view name="pixel-art"
   # 檢查其他可用技能
   skills_list category="creative"
   ```

4. **使用 Unsplash API 獲取免費高品質圖片** (實際採用)
   ```python
   # 直接使用 Unsplash URL 作為 fallback
   image_url = "https://source.unsplash.com/random/?crypto,currency,finance"
   
   # 實際執行：建立圖片 URL 檔案
   echo "https://images.unsplash.com/photo-1550745165-9bc0b252726a?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" > image_url.txt
   ```

5. **使用 Unsplash URL 作為最終 fallback** (實際使用)
   ```bash
   # 在圖片生成失敗時使用
   echo "image: \"https://images.unsplash.com/...\"" > fallback_image.yml
   ```

**實際執行經驗**：
- **工具檢查**：技能列表中的圖片生成工具可能實際不可用
- **快速決策**：當自動生成失敗時，立即切換到 Unsplash fallback
- **圖片 URL 管理**：將圖片 URL 直接寫入文章 frontmatter
- **無延誤處理**：圖片處理不應影響整體發布流程

**圖片要求**：
- 寬度 1200px x 高度 630px (Facebook分享最佳比例)
- 相關主題
- 高品質免版權
- 中文標題顯示
- **實際策略**：優保證發布速度，次要考慮圖片完美性

### 6. Git 操作 🚀
```bash
cd ~/blog

# 檢查 git 狀態
git status

# 添加新文章
git add content/tech/YYYY-MM-DD-article-title.md

# 提交變更
git commit -m "auto: [文章標題]"

# 重要：處理可能的遠端衝突 (實際經驗)
echo "檢查遠端變更..."
git fetch origin main

# 檢查是否有衝突
if git diff --quiet origin/main; then
    echo "無遠端變更，直接推送"
    git push origin main
else
    echo "發現遠端變更，進行 rebase..."
    # 使用 rebase 整合遠端變更
    git pull --rebase origin main
    
    # 如果 rebase 成功，再推送
    if [ $? -eq 0 ]; then
        echo "Rebase 成功，推送變更"
        git push origin main
    else
        echo "Rebase 失敗，需要手動解決衝突"
        # 可以嘗試其他策略或標記為需要人工介入
        echo "⚠️  需要人工介入解決 git 衝突"
        exit 1
    fi
fi
```

**實際執行經驗**：
- **衝突處理**：多台設備同時推送時可能發生 `Updates were rejected` 錯誤
- **解決方案**：使用 `git pull --rebase` 整合遠端變更，而非 `merge`
- **錯誤處理**：檢查 rebase 是否成功，失敗時需要人工介入
- **安全機制**：確保 commit 訊息格式一致 (`auto: [標題]`)

**Git 衝突處理進階策略**：
```bash
# 完整的衝突解決流程
cd ~/blog

# 1. 嘗試 rebase
git pull --rebase origin main

# 2. 如果失敗，檢查衝突狀態
if [ $? -ne 0 ]; then
    echo "發生衝突，檢查衝突檔案..."
    git status
    
    # 3. 手動解決衝突（如果需要）
    # git checkout --ours content/tech/YYYY-MM-DD-article-title.md
    # git add content/tech/YYYY-MM-DD-article-title.md
    
    # 4. 繼續 rebase
    # git rebase --continue
    
    # 5. 如果仍無法解決，放棄 rebase 使用 merge
    # git rebase --abort
    # git pull origin main --no-rebase
fi

# 6. 最終推送
git push origin main
```

**最佳實踐**：
- **定期 fetch**：在操作前先 fetch 最新遠端狀態
- **衝突預防**：開發前確認遠端最新狀態
- **錯誤恢復**：準備好 abort 和備用方案
- **日誌記錄**：記錄重要操作步驟和結果

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

**環境限制處理**：
```bash
# 檢查可用通知工具
if command -v telegram-send > /dev/null; then
    # 使用 telegram-send 進行通知
    telegram-send "🚀 新文章發布：[文章標題]"
elif [ -f "$HOME/.hermes/messaging/telegram_available" ]; then
    # 如果有 Telegram 配置檔案
    echo "Telegram 通知可用，但需要正確的 Bot Token 和 Chat ID"
else
    # 僅使用本地通知檔案
    echo "⚠️  通知功能受限，僅建立本地通知檔案"
fi
```

**實際執行經驗**：
- **環境限制**：某些工具（如 Telegram、image_gen）在特定環境中可能不可用
- **處理策略**：檢查工具可用性，提供備用方案
- **通知優先級**：本地檔案 > 服務通知 > 無通知（不影響發布流程）

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
- **實際發現**：TechCrunch 是最穩定的來源，Bloomberg 有嚴格 bot 檢測

### Bot Detection 處理 🤖
- **問題**：Bloomberg、WSJ 等金融網站有嚴格的 bot 檢測
- **解決方案**：
  - 使用 browser 工具而非 curl
  - 添加適當的 User-Agent
  - 避免過於頻繁的請求
- **實際經驗**：
  ```bash
  # Bloomberg 會直接拒絕訪問，返回 "Are you a robot?"
  # 改用 TechCrunch，相對開放且內容豐富
  browser_navigate url="https://techcrunch.com"
  ```

### 工具可用性檢查 🔧
```bash
# 檢查關鍵工具是否可用
check_tool_availability() {
    local tools=("$@")
    for tool in "${tools[@]}"; do
        if command -v "$tool" > /dev/null; then
            echo "✓ $tool 可用"
        else
            echo "✗ $tool 不可用"
        fi
    done
}

# 檢查技能可用性
check_skill_availability() {
    local skills=("$@")
    for skill in "${skills[@]}"; do
        if skill_view "$skill" > /dev/null 2>&1; then
            echo "✓ 技能 $skill 可用"
        else
            echo "✗ 技能 $skill 不可用"
        fi
    done
}

# 使用範例
check_tool_availability "search" "browser" "git"
check_skill_availability "stable-diffusion-image-generation" "web_search"
```

### 環境適應策略 🌍
- **問題**：不同環境中工具可用性不同
- **解決方案**：建立工具檢查機制，動態調整策略
- **實際執行**：
  1. 檢查 web_search → 不可用 → 改用 browser_navigate
  2. 檢查 image_gen → 不可用 → 改用 Unsplash URL
  3. 檢查 Telegram → 不可用 → 改用本地通知檔案
  4. Git 衝突 → 使用 rebase 解決

## 錯誤處理

### 常見錯誤及解決方案
1. **RSS feed 過時**
   - 檢查 feed 最後更新時間
   - 切換到網站直接訪問

2. **Bot detection**
   - 使用 browser 工具而非 curl
   - 添加適當的延遲
   - 更換新聞來源

3. **Git 操作失敗**
   - 檢查 git status
   - 確認遠程倉庫連接
   - 檢查 branch 狀態
   - 使用 rebase 解決衝突

4. **文章格式錯誤**
   - 使用現有文章作為模板
   - 檢查 YAML frontmatter 格式
   - 驗證 FAQ 結構

5. **工具不可用** (新增)
   - 檢查工具和技能可用性
   - 提供備用方案
   - 確保核心流程不中斷

### 錯誤處理流程圖
```
開始 → 檢查工具可用性 → 工具可用？ → 執行主要邏輯
                              ↓ 否
                          使用備用方案 → 備用方案可用？ → 繼續執行
                                                    ↓ 否
                                                  記錄錯誤 → 繼續執行（不中斷）
```

### 錯誤記錄機制
```bash
# 建立錯誤日誌
log_error() {
    local error_message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] ERROR: $error_message" >> ~/blog_publisher_errors.log
    echo "⚠️  錯誤已記錄：$error_message"
}

# 使用範例
log_error "web_search 工具不可用，已切換到 browser_navigate"
log_error "圖片生成失敗，已使用 Unsplash fallback"
```

### 成功案例

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

### 案例 3：微軟安全事件 (最新)
- **主題**：Microsoft 開源工具遭駭客攻擊
- **來源**：TechCrunch 直接導航
- **成果**：10,893 字安全分析文章
- **關鍵因素**：即時性 + 安全深度 + 全球影響
- **技術挑戰**：Bloomberg bot detection → 改用 TechCrunch
- **解決方案**：browser_navigate + 手動內容提取

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