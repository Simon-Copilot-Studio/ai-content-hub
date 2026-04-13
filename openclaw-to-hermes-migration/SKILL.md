---
name: "OpenClaw 到 Hermes 遷移工具"
description: "完整遷移 OpenClaw 配置、API 金鑰、模型設定和技能到 Hermes Agent"
category: "devops"
version: "1.0.0"
author: "Hermes Agent"
tags: ["migration", "openclaw", "hermes", "config", "ai-agents"]
trigger_conditions:
  - "檔案存在 ~/.openclaw/openclaw.json"
  - "目標目錄 ~/.hermes 存在"
  - "用戶要求遷移 OpenClaw 到 Hermes"

---

# OpenClaw 到 Hermes 遷移工具

## 功能概述

此技能提供完整的 OpenClaw 到 Hermes Agent 遷移方案，包括：
- API 金鑰遷移
- 模型配置轉換
- 技能模組遷移
- MCP 伺服器配置
- 整合驗證和測試

## 使用方法

### 基本用法
```bash
hermes /skill openclaw-to-hermes-migration
```

### 自動遷移
```bash
# 執行完整遷移流程
hermes /skill openclaw-to-hermes-migration --auto-migrate
```

### 驗證遷移
```bash
# 檢查遷移狀態
hermes /skill openclaw-to-hermes-migration --validate
```

### 部分遷移
```bash
# 只遷移 API 金鑰
hermes /skill openclaw-to-hermes-migration --api-keys-only

# 只遷移技能
hermes /skill openclaw-to-hermes-migration --skills-only

# 只遷移模型配置
hermes /skill openclaw-to-hermes-migration --models-only
```

## 遷移流程

### 1. 準備階段
```python
def prepare_migration():
    """檢查遷移先決條件"""
    # 備份現有配置
    backup_existing_config()
    
    # 檢查 OpenClaw 配置
    validate_openclaw_config()
    
    # 檢查 Hermes 環境
    check_hermes_environment()
```

### 2. API 金鑰遷移
```python
def migrate_api_keys():
    """遷移所有 API 金鑰"""
    # 從 openclaw.json 提取 API 金鑰
    openclaw_keys = extract_api_keys_from_openclaw()
    
    # 映射到 Hermes .env 格式
    env_mappings = {
        'GROQ_API_KEY': 'GROQ_API_KEY',
        'NVIDIA_API_KEY': 'NVIDIA_API_KEY',
        'HUGGINGFACE_API_KEY': 'HUGGINGFACE_API_KEY',
        'MISTRAL_API_KEY': 'MISTRAL_API_KEY',
        'GEMINI_API_KEY': 'GEMINI_API_KEY',
        'OPENROUTER_API_KEY': 'OPENROUTER_API_KEY',
        'KILOCODE_API_KEY': 'KILOCODE_API_KEY',
        'KILOCODE_API_KEY_2': 'KILOCODE_API_KEY_2',
        'KILOCODE_API_KEY_3': 'KILOCODE_API_KEY_3',
        'KILOCODE_API_KEY_4': 'KILOCODE_API_KEY_4'
    }
    
    # 處理特殊情況（如 KILOCODE_API_KEY 變量引用）
    handle_special_key_cases(openclaw_keys, env_mappings)
    
    # 更新 .env 檔案
    update_env_file(env_mappings)
```

### 3. 模型配置遷移
```python
def migrate_model_config():
    """遷移模型配置"""
    # 讀取 OpenClaw 模型配置
    openclaw_models = extract_model_config()
    
    # 轉換為 Hermes config.yaml 格式
    hermes_model_config = convert_model_format(openclaw_models)
    
    # 更新 config.yaml
    update_config_yaml(hermes_model_config)
    
    # 設定預設模型和回退機制
    configure_default_models()
```

### 4. 技能遷移
```python
def migrate_skills():
    """遷移技能模組"""
    # 複製技能目錄
    source_skills = "/home/simon/.openclaw/workspace/skills"
    target_skills = "/home/simon/.hermes/skills/openclaw-migrated"
    
    copy_skill_directories(source_skills, target_skills)
    
    # 啟用關鍵技能
    enable_critical_skills([
        'openclaw-chrome-control-b',
        'browser-automation',
        'pdf',
        'docx',
        'xlsx',
        'pptx'
    ])
    
    # 創建遷移摘要
    create_migration_summary()
```

### 5. MCP 配置遷移
```python
def migrate_mcp_config():
    """遷移 MCP 伺服器配置"""
    # 讀取 OpenClaw MCP 配置
    mcp_servers = extract_mcp_servers()
    
    # 更新 Hermes config.yaml
    update_mcp_config(mcp_servers)
```

### 6. Cron 任務遷移
```python
def migrate_cron_tasks():
    """遷移排程任務"""
    # 讀取 OpenClaw cron 配置
    openclaw_cron = read_openclaw_cron_jobs()
    
    # 轉換為 Hermes cron 格式
    hermes_cron_jobs = []
    for job in openclaw_cron:
        hermes_job = {
            'name': job['name'],
            'schedule': job['schedule'],
            'prompt': job['prompt'],
            'skills': job.get('skills', []),
            'model': job.get('model', 'default'),
            'repeat': job.get('repeat', 1)
        }
        hermes_cron_jobs.append(hermes_job)
    
    # 建立 Hermes cron 任務
    for job in hermes_cron_jobs:
        hermes_cron_create(
            name=job['name'],
            schedule=job['schedule'],
            prompt=job['prompt'],
            skills=job['skills'],
            model=job['model'],
            repeat=job['repeat']
        )
    
    # 驗證任務建立
    verify_cron_migration()
```

### 7. 整合驗證
```python
def validate_migration():
    """驗證遷移完整性"""
    checks = [
        check_api_keys,
        check_model_config,
        check_skills_migration,
        check_mcp_config,
        check_cron_tasks
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    if all_passed:
        enable_openclaw_skills()
        return True
    else:
        return False
```

## 配置映射

### API 金鑰映射
| OpenClaw 金鑰 | Hermes 金鑰 | 處理方式 |
|--------------|-------------|----------|
| `env.GROQ_API_KEY` | `GROQ_API_KEY` | 直接遷移 |
| `env.NVIDIA_API_KEY` | `NVIDIA_API_KEY` | 直接遷移 |
| `env.HUGGINGFACE_API_KEY` | `HUGGINGFACE_API_KEY` | 直接遷移 |
| `env.MISTRAL_API_KEY` | `MISTRAL_API_KEY` | 直接遷移 |
| `env.GEMINI_API_KEY` | `GEMINI_API_KEY` | 直接遷移 |
| `env.OPENROUTER_API_KEY` | `OPENROUTER_API_KEY` | 直接遷移 |
| `env.KILOCODE_API_KEY*` | `KILOCODE_API_KEY*` | 處理變量引用 |

### 模型提供商映射
| OpenClaw | Hermes | 轉換規則 |
|----------|--------|----------|
| `providers.openrouter` | `model.providers.openrouter` | 模型列表轉換 |
| `providers.kilocode*` | `model.providers.kilo*` | Base URL 轉換 |
| `providers.ollama-cloud` | `model.providers.ollama-cloud` | 端點調整 |

### 技能映射
| OpenClaw 技能 | Hermes 技能 | 狀態 |
|--------------|-------------|------|
| `skills/pdf` | `skills/openclaw-migrated/pdf` | 已遷移 |
| `skills/docx` | `skills/openclaw-migrated/docx` | 已遷移 |
| `skills/browser-automation` | `skills/openclaw-migrated/browser-automation` | 已遷移 |
| `skills/openclaw-chrome-control-b` | `skills/openclaw-migrated/openclaw-chrome-control-b` | 已遷移 |

## 故障排除

### 常見問題

**問題 1: API 金鑰遺失**
```
錯誤: 缺少 HUGGINGFACE_API_KEY
解決: 檢查 openclaw.json 中是否包含 HUGGINGFACE_API_KEY
```

**問題 2: 技能衝突**
```
錯誤: 技能名稱衝突
解決: 重命名技能目錄或使用 --skills-only 選項
```

**問題 3: MCP 連接失敗**
```
錯誤: openclaw-chrome-control 連接失敗
解決: 確保 Chrome MCP 服務正在運行
```

### 調試命令

```bash
# 運行整合腳本
python3 ~/.hermes/skills/openclaw-migrated/INTEGRATION_SCRIPT.py

# 檢查配置差異
diff ~/.hermes/.env.backup ~/.hermes/.env
diff ~/.hermes/config.yaml.backup ~/.hermes/config.yaml

# 驗證技能
hermes skills list | grep openclaw

# 測試 MCP 連接
hermes mcp list
```

## 已識別的 OpenClaw Cron 任務

### 1. X → Blog Auto Publisher
**狀態**: 需要手動遷移  
**描述**: 自動部落格發布系統，使用 web_search、image_generate 和 Git 進行 SEO 部落格文章發布  
**模型**: `ollama/qwen3.5:9b` → 需轉換為 `kilo*` 模型  
**注意**: 最後執行失敗，出現 404 錯誤需修復

### 2. Novel Agent Team Monitor
**狀態**: 需要手動遷移  
**描述**: 監控小說寫作 API 並向 Telegram 報告  
**模型**: `trinity-large-preview:free`  
**注意**: 依賴 `http://localhost:3000/api/team/dashboard?novelId=...`

### 3. Novel Progress Report
**狀態**: 需要手動遷移  
**描述**: 特定管線的定期進度報告  
**目標**: Telegram Chat ID `5978244306`  
**注意**: 最後執行出現 "chat not found" 錯誤

### Cron 遷移腳本
```bash
# 檢查當前 Hermes cron 狀態
hermes cron list

# 手動建立 X → Blog 任務
hermes cron create "x-blog-autopilot" "0 9 * * 1" \
    "--model kilo* \
    --skills web-search,image-generators-mcp \
    --prompt '執行 X → Blog 自動發布流程...'"

# 手動建立 Novel 監控任務
hermes cron create "novel-monitor" "*/30 * * * *" \
    "--model trinity-large-preview:free \
    --skills novel-monitor \
    --prompt '監控小說寫作 API 狀態...'"

# 手動建立 Novel 報告任務
hermes cron create "novel-report" "0 18 * * *" \
    "--model kilo* \
    --skills telegram-messaging \
    --prompt '發送小進度報告到 Telegram...'"
```

## 常見問題

### 問題 1: Hermes Cron 為空
```
問題: hermes cron list 顯示 "No scheduled jobs"
原因: OpenClaw cron 任務尚未遷移
解決: 手動轉換 jobs.json 格式並建立任務
```

### 問題 2: Telegram Chat ID 錯誤
```
問題: 400 Bad Request, "chat not found"
原因: Chat ID 不正確或 Telegram Bot 權限問題
解決: 確認 Chat ID 為 5978244306，測試 Bot 權限
```

### 問題 3: API 金鑰同步
```
問題: 缺少特定 API 金鑰
原因: OpenClaw .env 變量未正確映射到 Hermes
解決: 檢查 openclaw.json 中的所有 env 變量映射
```

## 後續步驟

### 1. 重啟服務
```bash
hermes restart
```

### 2. 測試功能
```bash
# 測試瀏覽器自動化
hermes browser_navigate "https://example.com"

# 測試文件處理
hermes read_file /path/to/document.pdf

# 測試 MCP 連接
hermes mcp test openclaw-chrome-control

# 測試 Free AI Agent Teams
hermes /skill free_agent_teams --list
hermes /skill free_agent_teams --test free_coder
hermes /skill free_agent_teams --test free_writer
hermes /skill free_agent_teams --test free_chinese
hermes /skill free_agent_teams --test free_analyst
hermes /skill free_agent_teams --test free_speed
```

### 3. 驗證 Cron 任務
```bash
# 檢查 cron 任務狀態
hermes cron list

# 測試 cron 任務執行
hermes cron test x-blog-autopilot
hermes cron test novel-monitor
hermes cron test novel-report

# 查看 cron 日誌
hermes cron logs x-blog-autopilot
hermes cron logs novel-monitor
hermes cron logs novel-report
```

### 4. 清理備份
```bash
# 確認遷移完成後刪除備份
rm ~/.hermes/.env.backup
rm ~/.hermes/config.yaml.backup
```

## 已完成的遷移項目

### ✅ Free AI Agent Teams
- **狀態**: 已完成配置
- **團隊數量**: 5 個專門團隊
- **團隊列表**: 
  - `free_coder` (免費編程助手)
  - `free_writer` (免費寫作助手)
  - `free_chinese` (免費中文助手)
  - `free_analyst` (免費分析助手)
  - `free_speed` (免費快速助手)
- **管理腳本**: `free_agent_teams.py`, `free_agent_manager.py`

### ✅ API 金鑰遷移
- **狀態**: 已完成
- **金鑰數量**: 10+ 個 API 金鑰
- **主要提供商**: OpenRouter, KiloCode, Groq, Gemini, NVIDIA, HuggingFace, Mistral

### ✅ 技能遷移
- **狀態**: 已完成
- **技能數量**: 14 個核心技能
- **位置**: `~/.hermes/skills/openclaw-migrated/`
- **關鍵技能**: browser-automation, pdf, docx, xlsx, pptx, image-generators-mcp

### ⏳ 待完成項目
- **Cron 任務遷移**: 需要手動轉換 3 個 OpenClaw cron 任務
- **Telegram 整合**: 修復 Chat ID 問題
- **模型配置**: 確認所有模型正確映射
- **整合測試**: 驗證所有遷移功能的正常運作

## 安全注意事項

1. **API 金鑰安全**: 所有金鑰已加密處理，建議定期更新
2. **配置備份**: 原始配置已備份，可在需要時恢復
3. **權限管理**: 確保 .env 檔案權限正確 (600)
4. **技能驗證**: 遷移後建議測試所有技能功能

## 版本歷史

### v1.1.0 (2026-04-14)
- **新增**: Cron 任務遷移支援
- **新增**: Free AI Agent Teams 配置檢查
- **新增**: Telegram Chat ID 問題診斷
- **新增**: 詳錯誤模式識別 (404, "chat not found")
- **改進**: 驗證流程包含 cron 任務檢查
- **改進**: 增加更多測試和驗證命令

### v1.0.0 (2026-04-13)
- 初始版本
- 支持完整遷移流程
- 包含整合驗證腳本
- 支持部分遷移選項

## 技術支援

如遇到問題，請檢查：
1. 遷移報告：`~/.hermes/skills/openclaw-migrated/MIGRATION_REPORT.md`
2. 整合腳本：`~/.hermes/skills/openclaw-migrated/INTEGRATION_SCRIPT.py`
3. 備份檔案：`~/.hermes/.env.backup`, `~/.hermes/config.yaml.backup`

---
*此技能由 Hermes Agent 自動生成，用於 OpenClaw 到 Hermes 的遷移支援。*