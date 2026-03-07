# Auto-Publish Skill

## 描述
AI 自動生成並發佈 Hugo 文章到 AI Content Hub。透過 web_search 搜尋最新話題，生成高品質中文 Markdown 文章，並透過 git push 觸發 CI/CD 自動部署。

## 支援分類
- `tech` — 科技新聞與分析
- `economy` — 財經趨勢與市場觀察
- `entertainment` — 娛樂資訊與評論
- `news` — 國際時事與深度報導
- `fiction` — 短篇小說與創意寫作

## 觸發方式
- **手動**：直接呼叫此 skill，指定分類和主題
- **排程**：設定 cron 定時自動發佈

## 流程

### Step 1：選擇分類
```
分類 = tech | economy | entertainment | news | fiction
如果未指定 → 隨機選擇或依最近更新頻率決定
```

### Step 2：搜尋最新話題
使用 `web_search` 搜尋該分類的最新熱門話題：
```
web_search("2026 {分類} 最新 trending 話題")
web_search("{分類} 新聞 本週 重要")
```

### Step 3：生成文章
參考 `scripts/generate-article-prompt.md` 的 prompt 模板，生成：
- 完整 front matter（title, date, description, categories, tags, image, readingTime）
- 300-500 字高品質中文內容
- SEO 優化的標題與描述
- 適當的結構（引言 → 主體 → 結論）

### Step 4：寫入並發佈
```bash
bash scripts/publish-article.sh \
  --category {分類} \
  --title "{文章標題}" \
  --content /tmp/article-content.md
```

### Step 5：驗證部署
- 等待 GitHub Actions 執行完成（約 2-3 分鐘）
- 驗證文章已出現在網站上
- 確認搜尋索引已更新

## 使用範例

### 手動發佈科技文章
```
請幫我發佈一篇關於「AI 代理人最新發展」的科技文章
```

### 手動發佈財經文章
```
搜尋今天的財經新聞，發佈一篇關於台股的分析文章
```

### 批次發佈（每個分類各一篇）
```
請每個分類各發佈一篇最新文章
```

## 注意事項
- 確保在正確的 git repo 目錄下執行：`/home/simon/.openclaw/workspace/projects/ai-content-hub/`
- GitHub repo 必須設定好 secrets：`CLOUDFLARE_API_TOKEN`、`CLOUDFLARE_ACCOUNT_ID`
- 文章 slug 自動從標題生成（中文轉拼音或英文）
- 圖片 URL 使用 Unsplash 或 Pexels 免費圖片

## 依賴
- git（已安裝）
- 正確配置的 GitHub remote
- Cloudflare Pages 專案已建立
- GitHub Actions secrets 已設定
