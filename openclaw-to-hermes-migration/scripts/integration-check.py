#!/usr/bin/env python3
"""
OpenClaw 到 Hermes 整合檢查腳本
用於驗證遷移後的配置完整性
"""

import json
import yaml
import os
from pathlib import Path
import subprocess

def check_api_keys():
    """檢查 API 金鑰是否正確遷移"""
    print("🔍 檢查 API 金鑰...")
    
    env_file = Path('/home/simon/.hermes/.env')
    if not env_file.exists():
        print("❌ .env 檔案不存在")
        return False
    
    with open(env_file, 'r') as f:
        env_content = f.read()
    
    expected_keys = [
        'OPENROUTER_API_KEY',
        'GROQ_API_KEY', 
        'NVIDIA_API_KEY',
        'HUGGINGFACE_API_KEY',
        'MISTRAL_API_KEY',
        'GEMINI_API_KEY',
        'KILOCODE_API_KEY'
    ]
    
    missing_keys = []
    for key in expected_keys:
        if key not in env_content:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ 缺少 API 金鑰: {missing_keys}")
        return False
    else:
        print("✅ 所有 API 金鑰已正確遷移")
        return True

def check_model_config():
    """檢查模型配置"""
    print("🔍 檢查模型配置...")
    
    config_file = Path('/home/simon/.hermes/config.yaml')
    if not config_file.exists():
        print("❌ config.yaml 檔案不存在")
        return False
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    if 'model' not in config:
        print("❌ 缺少 model 配置")
        return False
    
    if 'default' not in config['model']:
        print("❌ 缺少 default 模型")
        return False
    
    print(f"✅ 預設模型: {config['model']['default']}")
    return True

def check_skills_migration():
    """檢查技能遷移"""
    print("🔍 檢查技能遷移...")
    
    skills_dir = Path('/home/simon/.hermes/skills/openclaw-migrated')
    if not skills_dir.exists():
        print("❌ 技能目錄不存在")
        return False
    
    skills = [d.name for d in skills_dir.iterdir() if d.is_dir() and d.name != '__pycache__' and d.name != '.git']
    
    if not skills:
        print("❌ 沒有找到技能")
        return False
    
    print(f"✅ 已遷移 {len(skills)} 個技能:")
    for skill in skills:
        print(f"   - {skill}")
    return True

def check_mcp_config():
    """檢查 MCP 配置"""
    print("🔍 檢查 MCP 配置...")
    
    config_file = Path('/home/simon/.hermes/config.yaml')
    if not config_file.exists():
        print("❌ config.yaml 檔案不存在")
        return False
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    if 'mcp' not in config:
        print("❌ 缺少 MCP 配置")
        return False
    
    if 'servers' not in config['mcp']:
        print("❌ 缺少 MCP 伺服器配置")
        return False
    
    servers = config['mcp']['servers']
    print(f"✅ 已配置 {len(servers)} 個 MCP 伺服器:")
    for name in servers.keys():
        print(f"   - {name}")
    return True

def enable_openclaw_skills():
    """啟用 OpenClaw 相關技能"""
    print("🔧 啟用 OpenClaw 技能...")
    
    config_file = Path('/home/simon/.hermes/config.yaml')
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    if 'skills' not in config:
        config['skills'] = {}
    
    if 'enabled' not in config['skills']:
        config['skills']['enabled'] = {}
    
    # 啟用關鍵技能
    critical_skills = [
        'openclaw-chrome-control-b',
        'browser-automation',
        'pdf',
        'docx',
        'xlsx',
        'pptx'
    ]
    
    for skill in critical_skills:
        config['skills']['enabled'][skill] = True
        print(f"✅ 已啟用技能: {skill}")
    
    # 寫回配置
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    return True

def main():
    """主函數"""
    print("🚖 OpenClaw 到 Hermes 整合檢查")
    print("=" * 50)
    
    checks = [
        check_api_keys,
        check_model_config,
        check_skills_migration,
        check_mcp_config
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ 所有檢查通過！")
        enable_openclaw_skills()
        print("\n🎉 OpenClaw 到 Hermes 遷移完成！")
        
        print("\n📋 後續步驟:")
        print("1. 重啟 Hermes 服務以載入新配置")
        print("2. 測試關鍵功能（瀏覽器自動化、文件處理等）")
        print("3. 根據需要調整配置參數")
        
    else:
        print("❌ 部分檢查失敗，請檢查上述錯誤")

if __name__ == "__main__":
    main()