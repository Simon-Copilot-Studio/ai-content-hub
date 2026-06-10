---
name: daily-radar-scanner
category: research
description: "執行每日機會雷達掃描，並行搜尋 GitHub Trending、Hacker News、Product Hunt、arXiv CS.AI 平台，生成報告和 Telegram 摘要"
author: "Hermes Agent"
version: "1.0"
tags: ["research", "ai", "automation", "multi-agent", "telegram"]
---

# 每日機會雷達掃描技能

## 技能概述
此技能用於執行完整的每日機會雷達掃描任務，包含並行搜尋多個 AI 相關平台、內容篩選、報告生成和 Telegram 通知。

## 使用情境
- 每日 AI 機會洞察蒐集
- 技術趨勢監控
- 競爭情報收集
- 自動化內容報告生成

## 執行流程

### 1. 初始化與準備
```python
# 建立必要的目錄結構
os.makedirs('/home/simon/research/daily-radar', exist_ok=True)

# 檢查規格文件是否存在
if not os.path.exists('/home/simon/research/daily-radar/README.md'):
    # 建立規格文件
    create_specification_file()
```

### 2. 並行搜尋執行
```python
# 注意：最多只能使用 3 個並行 sub-agent
# 第一次呼叫：GitHub Trending + Hacker News
# 第二次呼叫：Product Hunt + ArXiv CS.AI

delegate_task(tasks=[
    {"goal": "Search GitHub Trending for AI/Agent/LLM related repositories", "toolsets": ["web", "search"]},
    {"goal": "Search Hacker News for AI/Agent/LLM related discussions", "toolsets": ["web", "search"]}
])

delegate_task(tasks=[
    {"goal": "Search Product Hunt for AI/Agent/LLM/Hermes products", "toolsets": ["web", "search"]},
    {"goal": "Search ArXiv CS.AI for AI/Agent/LLM/Hermes papers", "toolsets": ["web", "search"]}
])
```

### 3. API 限制處理
```python
# 如果遇到 API 限制錯誤（如 429），需要：
# 1. 降低並行任務數量
# 2. 增加重試機制
# 3. 使用備用搜尋策略

if "429" in error or "quota" in error:
    # 拆分為單一任務執行
    search_individually()
```

### 4. 內容篩選與整合
```python
# 只保留 AI/Agent/LLM/Hermes 相關內容
# 排除不相關的科技新聞

def filter_ai_content(content):
    ai_keywords = ["AI", "agent", "LLM", "large language model", 
                   "multi-agent", "hermes", "GPT", "Claude", "LangChain"]
    return any(keyword.lower() in content.lower() for keyword in ai_keywords)
```

### 5. 報告生成
```python
# 生成完整的 Markdown 報告
def generate_daily_report(date, github_data, hn_data, producthunt_data, arxiv_data):
    report = f"""# 機會雷達報告 - {date}

## 搜尋概況
本日使用 3 個 sub-agent 並行搜尋了以下平台：
- GitHub Trending（AI/Agent/LLM 相關項目）
- Hacker News（AI 相關討論）
- Product Hunt（AI 產品）
- ArXiv CS.AI（AI 論文）

所有內容均經過 AI/Agent/LLM/Hermes 相關性篩選。

## GitHub Trending AI 項目
{github_data}

## Hacker News AI 討論
{hn_data}

## Product Hunt AI 產品
{producthunt_data}

## ArXiv AI 論文
{arxiv_data}

## 總結與洞察
{generate_insights(github_data, hn_data, producthunt_data, arxiv_data)}
"""
    return report
```

### 6. Telegram 摘要生成
```python
# 從報告中提取 Top 3 最有價值的內容
def generate_telegram_summary(date, report):
    # 分析報告內容，提取最重要的 3 項
    top_items = extract_top_3(report)
    
    summary = f"""🎯 今日 AI 機會雷達 Top 3 - {date}

{top_items}

#AI機會 #技術趨勢
"""
    return summary
```

## 技術細節

### 搜尋策略
1. **GitHub Trending**: 搜尋 AI、Agent、LLM 相關的熱門專案
2. **Hacker News**: 找出 AI 相關討論熱度高的文章
3. **Product Hunt**: 搜尋最新發布的 AI 產品
4. **ArXiv CS.AI**: 找出最新的 AI 相關論文

### 錯誤處理
- API 限制錯誤（429）：降低並行數量，增加重試
- 網站結構複雜：使用多種抓取策略
- 內容解析失敗：使用正則表達式和 HTML 解析器

### 輸出格式
- **主要報告**: `research/daily-radar/年-月-日.md`
- **Telegram 摘要**: 格式化好的文字內容
- **規格文件**: `research/daily-radar/README.md`

## 使用範例

### 執行每日掃描
```bash
# 自動執行
hermes cron create --name "daily-radar" --deliver "origin" "0 9 * * *" "執行每日機會雷達掃描"

# 手動執行
python daily_radar_scanner.py
```

### 自訂搜尋
```python
# 自訂搜尋關鍵字
custom_keywords = ["hermes", "multi-agent", "autonomous ai"]
filter_results_with_keywords(search_results, custom_keywords)
```

## 注意事項

1. **並行限制**: 最多使用 3 個並行 sub-agent
2. **API 配額**: 注意搜尋工具的 API 使用限制
3. **內容篩選**: 確保只保留相關內容
4. **連結驗證**: 確保所有連結有效且可存取
5. **中文輸出**: 所有報告必須使用中文

## 成功指標

- 成功搜尋 4 個平台
- 生成完整的每日報告
- 提供有價值的 Top 3 摘要
- 所有內容均為 AI/Agent/LLM/Hermes 相關

## 優化方向

1. **增加更多平台**: 如 Reddit AI、Twitter AI 等
2. **改進搜尋算法**: 更精準的內容匹配
3. **增加分析深度**: 更多趨勢分析
4. **自動化通知**: 整合更多通知渠道
---