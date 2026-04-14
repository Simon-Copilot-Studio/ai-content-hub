---
name: system-decommissioning-analysis
category: devops
description: 系統停用與移除的全面分析與規劃方法學
tags: [system-analysis, decommissioning, risk-assessment, migration-cleanup]
---

# 系統停用分析技能

## 概述
提供複雜系統停用前的全面分析、風險評估和移除規劃方法學。適用於軟體遷移、系統替換或系統停用前的安全準備工作。

## 使用場景
- 舊系統移除前的分析
- 軟體遷移後的清理工作
- 系統替換前的評估
- 服務停用的安全規劃

## 分析流程

### 1. 系統現狀全面掃描

#### 檔案結構分析
```bash
# 找出所有相關目錄
find /home/$USER -name "*openclaw*" -type d 2>/dev/null
find /home/$USER -name "*openclaw*" -type f 2>/dev/null

# 磁碟使用量分析
du -sh ~/.openclaw/
du -sh ~/.npm-global/lib/node_modules/openclaw/

# 包含 Windows 端的檔案（WSL 環境）
du -sh /mnt/c/Users/$USER/CoWork/openclaw-* 2>/dev/null
```

#### 進程分析
```bash
# 查找相關進程
ps aux | grep -i openclaw | grep -v grep
ps -ef | grep -i openclaw | grep -v grep

# 查看進程詳細資訊
ps -p 491,2846,490 -o pid,ppid,cmd

# 檔案使用分析
lsof | grep -i openclaw
```

#### 系統服務分析
```bash
# systemd 服務
systemctl list-units --type=service | grep -i openclaw
systemctl --user list-unit-files | grep -i openclaw
systemctl --user status openclaw-gateway.service

# npm 全域套件
npm config get prefix
npm list -g --depth=0 | grep -i openclaw
```

#### 定時任務分析
```bash
# 當前 crontab
crontab -l | grep -i openclaw
crontab -l | grep -v "hermes" | grep -v "^#" | grep -v "^$" | grep -i openclaw
```

### 2. 風險評估與分類

#### 🔴 高風險項目
- **數據庫損壞**：正在使用的資料庫檔案（lcm.db, tasks/runs.sqlite）
- **進程衝突**：運行中的進程強制終止可能導致系統不穩定
- **服務殘留**：systemd 服務可能自動重啟已刪除的進程

#### 🟡 中風險項目
- **配置檔案**：包含 API 金鑰和敏感資訊
- **跨平台依賴**：Windows 端的服務可能仍在運行
- **日誌檔案**：包含運行時資訊，刪除前應備份

#### 🟢 低風險項目
- **npm 套件**：標準 npm 套件移除
- **符號連結**：執行檔案的符號連結移除
- **配置檔案**：一般的設定檔案

### 3. 遷移完整性驗證

#### 已遷移項目檢查
```bash
# 腳本檔案
ls -la ~/.hermes/workspace/scripts/

# Cron 任務
crontab -l | grep -i hermes

# API 配置
ls -la ~/.hermes/.env

# Git 配置
cd ~/.hermes/workspace && git status
cd ~/.hermes/skills && git status
```

#### 未遷移項目識別
- 殘留的舊 cron 任務
- Windows 端依賴服務
- 環境變數設定
- 殘留的日誌檔案

### 4. 移除策略規劃

#### 分階段移除計劃
```bash
# 第一階段：停止服務和進程
systemctl --user stop openclaw-gateway.service
systemctl --user disable openclaw-gateway.service
kill -TERM <PID>  # 優雅終止
sleep 5
kill -KILL <PID>  # 強制終止（如果必要）

# 第二階段：清理系統配置
npm uninstall -g openclaw
rm -rf ~/.npm-global/lib/node_modules/openclaw/
rm ~/.npm-global/bin/openclaw

# 第三階段：清理殘留任務
crontab -l | grep -v "openclaw" | crontab -

# 第四階段：刪除檔案
rm -rf ~/.openclaw/
rm -rf /mnt/c/Users/$USER/CoWork/openclaw-*  # WSL 環境

# 第五階段：清理 systemd 服務
rm ~/.config/systemd/user/openclaw-gateway.service
```

### 5. 驗證與確認

#### 移除完整性檢查
```bash
# 驗證進程已停止
ps aux | grep -i openclaw | grep -v grep || echo "✅ 無運行中進程"

# 驗證檔案已移除
which openclaw || echo "✅ 執行檔案已移除"
ls -la ~/.openclaw 2>/dev/null || echo "✅ 配置目錄已移除"

# 驗證服務已清理
systemctl --user list-unit-files | grep -i openclaw || echo "✅ systemd 服務已清理"

# 驗證 cron 任務已清理
crontab -l | grep -i openclaw || echo "✅ cron 任務已清理"
```

## 執行前確認清單

- [ ] 確認所有數據已遷移
- [ ] 確認新系統功能正常
- [ ] 確認依賴服務無衝突
- [ ] 確認備份完整
- [ ] 確認授權和權限
- [ ] 確認回滚計劃

## 最佳實踐

1. **逐步執行**：按照風險等級分階段執行
2. **充分備份**：在移除前建立完整備份
3. **驗證每步**：每個步驟後進行完整性檢查
4. **文檔記錄**：記錄移除過程和結果
5. **監控系統**：移除後監控系統狀態

## 注意事項

- 在生產環境執行前先在測試環境驗證
- 確保有足夠的磁碟空間進行備份
- 考慮執行時間對系統性能的影響
- 準備緊急回滚方案
- 通知相關人員維護時間

## 工具集需求
- terminal: 用於系統命令執行
- file: 用於檔案操作和備份
- search_files: 用於檔案內容搜尋
- todo: 用於任務追蹤和管理