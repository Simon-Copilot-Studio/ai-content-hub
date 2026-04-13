# Blog 自動產圖任務說明

## 執行時間
每天 00:00 啟動，06:00 前結束

## 流程

### Agent 1: 文章盤點員
1. 掃描 ~/blog/content/ 所有 .md 文件
2. 找出 frontmatter 中 image 欄位缺失、為空、或引用 unsplash 外連的文章
3. 排除 _index.md、about、contact、privacy、search 等頁面
4. 為每篇文章根據標題和內容摘要，產生一個英文圖片 prompt
5. 將結果寫入 /tmp/blog-image-queue.json，格式：
```json
[
  {
    "file": "content/tech/2026-03-20-example.md",
    "title": "文章標題",
    "category": "tech",
    "prompt": "English prompt for Meta AI Imagine",
    "status": "pending"
  }
]
```

### Agent 2: 產圖員
1. 讀取 /tmp/blog-image-queue.json
2. 逐筆使用 Meta AI Imagine 產圖（mcporter call meta-ai.generate_image）
3. 選擇最佳的一張，複製到 ~/blog/static/images/{category}/{filename}.png
4. 更新對應 .md 文件的 image 欄位為 "images/{category}/{filename}.png"
5. 更新 /tmp/blog-image-queue.json 狀態為 done
6. 每處理 5 張圖後暫停 30 秒（避免 Meta AI 限流）

### Agent 3: 記錄與同步員
1. 監控 /tmp/blog-image-queue.json 的進度
2. 每完成一批（10篇），執行 git add + commit + push
3. 將進度記錄到 /tmp/blog-image-log.md
4. 完成後發送 Telegram 通知摘要給 Simon (5978244306)

## 注意事項
- Meta AI 每次產 4 張圖，選最好的 1 張
- 圖片 prompt 用英文，加上 "professional blog header, clean design, 4K quality"
- 食譜類用 "photorealistic food photography, warm lighting, wooden table"
- 科技類用 "modern tech concept, blue tones, futuristic, clean"
- 小說類用 "dramatic cinematic scene, atmospheric lighting, storytelling"
- 財經類用 "business finance concept, professional, data visualization"
