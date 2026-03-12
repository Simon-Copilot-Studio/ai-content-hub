# Session 結束檢查清單

每次 `/new` 之前，賈維斯自動執行：

## 1. 摘要本次對話（3-5 條重點）
- 完成了什麼
- 未完成的待辦
- 重要決策

## 2. 存入 memory_store
```
memory_store: 關鍵決策、技術發現、偏好設定
category: fact/decision/preference
importance: 0.6-0.9
```

## 3. 更新每日 MD（極簡版）
- `memory/YYYY-MM-DD.md` 只寫摘要（5-10 行）
- 技術細節不寫進 MD，靠 memory_store 索引

## 4. 更新 ACTIVE_TASKS.md
- 未完成的任務寫入，下次啟動接續

## Token 節省效果
- 啟動讀 MD：~200-500 tokens（原本 2000-5000）
- 需要細節時：memory_recall 按需 ~500 tokens/次
- 預估節省：80-90% 啟動成本
