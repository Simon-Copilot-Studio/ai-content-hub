---
name: auto-blog-publisher
description: End-to-end automated blog publishing workflow - from multi-platform content discovery to SEO-optimized article generation and git deployment
author: Hermes Agent
version: 1.0
tags: ["blog", "automation", "content", "publishing", "seo", "git"]
---

# 自動部落格發布系統

## 技能概述
此技能提供完整的自動化部落格發布流程，包含多平台內容搜尋、主題篩選、SEO 優化文章撰寫、圖片生成處理和 Git 推送部署。

## 使用情境
- 定時部落格內容發布
- 熱門話題自動化報導
- SEO 優化的科技新聞文章
- 多平台內容整合與分析

## 執行流程

### 1. 初始化與環境準備
```bash
# 檢查工作目錄
cd ~/blog

# 檢查現有文章避免重複
ls -la ~/blog/content/tech/ | tail -20
```

### 2. 多平台內容搜尋
```python
# 使用 daily-radar-scanner 進行並行搜尋
# GitHub Trending + Hacker News (第一組)
# Product Hunt + ArXiv CS.AI (第二組)

delegate_task(tasks=[
    {"goal": "Search GitHub Trending for AI/Agent/LLM related repositories from the past 3 hours", "toolsets": ["web"]},
    {"goal": "Search Hacker News for AI/Agent/LLM related discussions from the past 3 hours", "toolsets": ["web"]}
])

delegate_task(tasks=[
    {"goal": "Search Product Hunt for AI/Agent/LLM products launched in the past 3 hours", "toolsets": ["web"]},
    {"goal": "Search ArXiv CS.AI for AI/Agent/LLM research papers published in the past 3 hours", "toolsets": ["web"]}
])
```

### 3. 內容分析與主題選擇
```bash
# 讀取搜尋結果
read_file /home/simon/research/daily-radar/年-月-日.md

# 檢查現有文章避免重複
search_files pattern="existing articles" path=~/blog/content/tech/

# 選擇最有價值的主題
# 考慮因素：時效性、新穎性、讀者價值、避免重複
```

### 4. SEO 優化文章撰寫
```markdown
---
title: "吸引人的標題"
date: 2026-06-10T10:00:00+08:00
description: "吸引人的描述，包含關鍵字"
categories:
  - "科技"
tags:
  - "關鍵字1"
  - "關鍵字2"
  - "AI"
  - "科技新聞"
image: "images/tech/年-月-主題.jpg"
readingTime: 5-8
faq:
  - q: "常見問題1"
    a: "答案1"
  - q: "常見問題2"
    a: "答案2"
---

## 引人入勝的開頭
[吸引讀者注意力的開場白]

## 主要內容
[結構化的內容，包含小標題、列表、引用]

## 技術細節
[深入的技術分析]

## 市場影響
[對市場和行業的影響分析]

## 未來展望
[未來發展趨勢預測]

## 結語
[總結和呼籲行動]
```

### 5. 圖片處理策略
```python
# 優先嘗試圖片生成
try:
    # 使用 image_generate 或 creative 技能
    # 例如：baoyu-infographic 生成資訊圖
    skill_view("baoyu-infographic")
    generate_infographic(topic, layout="bento-grid", style="craft-handmade")
except:
    # 失敗時使用 Unsplash URL
    unsplash_url = f"https://images.unsplash.com/photo-...?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80"
    create_placeholder_image(path)
```

### 6. Git 推送部署
```bash
cd ~/blog
git add -A
git commit -m "auto: [文章標題]"
git push origin main
```

### 7. 通知機制
```bash
# Telegram 通知
echo "🎯 Blog 發布完成！
主題：[文章標題]
連結：[GitHub 連結]

#標籤1 #標籤2"
```

## 技術細節

### 搜尋策略
1. **GitHub Trending**: AI/Agent/LLM 相關熱門專案
2. **Hacker News**: AI 相關討論熱度文章
3. **Product Hunt**: 最新發布的 AI 產品
4. **ArXiv CS.AI**: 最新 AI 相關研究論文

### 內容篩選標準
- **時效性**: 選擇過去 3 小時內的最新內容
- **相關性**: AI/LLM/chips/robotics/Fed/台股/美股/crypto/Apple/Google/Meta/TSMC/Nvidia/地緣政治
- **價值性**: 避免重複現有文章，選擇最有新聞價值的主題
- **SEO 優化**: 標題包含關鍵字，描述吸引人，FAQ 提升搜索排名

### 錯誤處理
- **工具不可用**: 使用替代方案或 placeholder
- **搜尋無結果**: 擴大時間範圍或平台
- **圖片生成失敗**: 使用 Unsplash 或 placeholder
- **Git 操作失敗**: 檢查權限和狀態

### 輸出格式
- **主要文章**: `~/blog/content/tech/年-月-日-主題.md`
- **圖片**: `~/blog/static/images/tech/年-月-日-主題.jpg`
- **搜尋報告**: `~/research/daily-radar/年-月-日.md`
- **通知**: 格式化的 Telegram 消息

## 使用範例

### 執行完整流程
```bash
# 自動執行
hermes cron create --name "auto-blog-publisher" --deliver "origin" "0 9 * * *" "執行自動部落格發布流程"

# 手動執行
python auto_blog_publisher.py
```

### 自訂搜尋
```python
# 自訂搜尋關鍵字和時間範圍
custom_keywords = ["hermes", "multi-agent", "explainable ai"]
time_range = "past 6 hours"
```

## 注意事項

1. **工具依賴**: 檢查必要工具是否可用 (daily-radar-scanner, git, image_generate)
2. **重複檢查**: 確保不與現有文章重複
3. **SEO 優化**: 標題和描述需要包含適當關鍵字
4. **圖片質量**: 優先使用高品質圖片，避免 placeholder
5. **Git 狀態**: 確保工作目錄乾淨，沒有未提交的更改

## 成功指標

- 成功搜尋 4 個平台獲取最新內容
- 撰寫 SEO 優化的高品質文章
- 正確配置圖片和 metadata
- 成功推送到 GitHub repository
- 發送格式化的通知消息

## 優化方向

1. **增加更多平台**: Reddit AI, Twitter AI, LinkedIn AI
2. **改進搜算法**: 更精準的內容匹配和去重
3. **自動化圖片生成**: 整合更多圖片生成工具
4. **A/B 測試**: 測試不同標題和描述的效果
5. **性能監控**: 追蹤文章瀏覽量和 SEO 效果
---

## 實際應用案例

### 案例 1: Hermes Analytics 發布報導
**搜尋來源**: Product Hunt + ArXiv CS.AI  
**主題選擇**: 解釋性 AI 的商業應用
**文章特色**: 結合學術研究與商業應用
**圖片處理**: 由於 image_generate 不可用，使用 placeholder + Unsplash URL
**Git 操作**: 成功 commit 和 push

### 案例 2: Claude Fable 5 發布報導  
**搜尋來源**: TechCrunch 新聞
**主題選擇**: Anthropic 最新模型發布
**文章特色**: 技術規格與定價分析
**圖片處理**: 使用現有圖片庫資源

## 經驗教訓

1. **工具備用方案**: 當主要工具不可用時，要有備用方案
2. **並行搜尋效率**: 使用多個 sub-agent 並行搜尋顯著提升效率
3. **重複檢查重要性**: 避免重複報導現有文章
4. **格式一致性**: 保持與現有文章相同的格式和結構
5. **時效性平衡**: 3 小時時間窗口適合熱門話題，但可能需要擴展

此技能提供了完整的自動化部落格發布解決方案，適合定時內容更新和熱門話題報導。