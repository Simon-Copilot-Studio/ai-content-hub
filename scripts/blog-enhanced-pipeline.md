# Blog Enhanced Pipeline — 升級版每日內容流程

## 觸發時間
- 每天午夜 00:00（由 daily-ai-news.sh system event 觸發）

## 流程（5 階段）

### Stage 1: 多源新聞蒐集
用 web_search 從以下來源搜尋過去 24 小時 AI/科技新聞：
1. **英文主流媒體**: TechCrunch, The Verge, Ars Technica, Wired
2. **AI 專業**: Hugging Face blog, arXiv CS.AI, OpenAI blog, Anthropic blog
3. **X.com 替代方案**: 搜尋 `site:x.com AI OR LLM OR agent` 透過 Brave（可抓到公開推文摘要）
4. **中文科技媒體**: iThome, 科技新報, 36氪, 機器之心
5. **OpenClaw 生態系**: GitHub releases, ClawHub, Discord announcements

### Stage 2: NotebookLM 深度研究
對 Stage 1 篩選出的 Top 3-5 主題：
1. 建立臨時 NotebookLM notebook
2. 加入相關文章 URL 作為 source
3. 用 NotebookLM 生成深度分析（交叉比對多來源觀點）
4. 提取關鍵 insight 用於撰文
5. 清理 notebook

### Stage 3: 撰寫 SEO 優化文章
每篇文章包含：
- title: 包含主關鍵字，< 60 字元
- description: 150-160 字元，含 CTA
- tags: 5-8 個相關標籤
- categories: ["tech"]
- image: 待 Stage 4 產生
- 正文: 800-1500 字，結構化小標題
- FAQ: 3-5 個常見問題（Schema markup 友善）
- 內部連結: 連結到既有相關文章

### Stage 4: Meta AI 產圖
用 meta-ai-imagine skill 為每篇文章產生配圖：
1. 根據文章內容生成英文 prompt
2. 呼叫 mcporter call meta-ai generate_image
3. 下載圖片到 ~/blog/static/images/
4. 更新文章 frontmatter 的 image 欄位

### Stage 5: 發布
1. cd ~/blog && git add -A && git commit && git push
2. 發送 Telegram 摘要通知 Simon

## X.com 內容策略（Nitter 已死的替代方案）
- **Brave Search**: `site:x.com [topic]` 可搜到公開推文的標題和摘要
- **fxtwitter.com**: 將 x.com 換成 fxtwitter.com 可直接讀推文內容
- **web_fetch**: 部分公開推文頁面可直接擷取
- **Google cache**: `cache:x.com/username/status/xxx` 偶爾可用
- **新聞引用**: 多數重要推文會被科技媒體引用，從新聞文章中提取

## 參考 KOL 帳號（科技/AI）
- @kaborashy (Andrej Karpathy)
- @ylecun (Yann LeCun)
- @sama (Sam Altman)
- @emaboradchi (AI 新聞)
- @_akhaliq (ML 論文)
- @OpenClawAI (OpenClaw 官方)
