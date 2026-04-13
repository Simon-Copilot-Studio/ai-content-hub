---
title: Messaging Platform Troubleshooting
name: messaging-platform-troubleshooting
category: devops
description: Systematic approach to diagnosing and fixing messaging platform integration issues, focusing on API keys, gateway services, and error resolution
tags: [messaging, telegram, gateway, api, troubleshooting]
---

# Messaging Platform Troubleshooting

## Overview
This skill provides a systematic approach to troubleshooting messaging platform integration issues, specifically for Hermes Agent Gateway with Telegram and other platforms.

## Common Issues & Solutions

### 1. 401 Authentication Errors
**Symptoms**: `Error code: 401 - {'error': {'message': 'User not found.', 'code': 401}}`

**Root Causes**:
- Missing or invalid API keys
- Incorrect environment variable configuration
- Expired API tokens

**Solution Process**:
```bash
# Check current environment
echo $OPENROUTER_API_KEY

# Verify API key in configuration
grep OPENROUTER_API_KEY ~/.hermes/.env

# Test API connectivity
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "test"}]}' \
     https://openrouter.ai/api/v1/chat/completions
```

### 2. Gateway Service Issues
**Symptoms**: Service not running, connection failures, high memory usage

**Diagnostics**:
```bash
# Check service status
cd ~/.hermes/hermes-agent && source venv/bin/activate && python -m hermes_cli.main gateway status

# View recent logs
journalctl --user -u hermes-gateway.service --since "1 hour ago"

# Check process details
ps -p $(pgrep -f hermes-gateway)

# Monitor resource usage
top -p $(pgrep -f hermes-gateway)
```

### 3. Platform Connection Problems
**Symptoms**: Telegram not connected, message delivery failures

**Verification Steps**:
```bash
# Check platform status
cd ~/.hermes/hermes-agent && source venv/bin/activate && python -m hermes_cli.main gateway status

# Check configuration
grep -A 5 -B 5 "telegram:" ~/.hermes/config.yaml

# Validate bot token
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
```

## Systematic Troubleshooting Workflow

### Step 1: Initial Assessment
```bash
# Check overall system health
systemctl --user status hermes-gateway.service

# Check recent restarts
journalctl --user -u hermes-gateway.service --since "24 hours ago" | grep -E "(Started|Stopped|Failed)"

# Check memory and CPU usage
top -p $(pgrep -f hermes-gateway)
```

### Step 2: Configuration Verification
```bash
# Check environment variables
env | grep -i "api\|telegram\|openrouter"

# Verify API key formats
echo $OPENROUTER_API_KEY | wc -c  # Should be reasonable length
echo $TELEGRAM_BOT_TOKEN | wc -c  # Should be reasonable length

# Check configuration files
grep -n "api_key\|token" ~/.hermes/.env
grep -n "telegram:" ~/.hermes/config.yaml
```

### Step 3: Service Management
```bash
# Restart service with proper environment
export OPENROUTER_API_KEY="your-api-key-here"
cd ~/.hermes/hermes-agent && source venv/bin/activate && python -m hermes_cli.main gateway restart

# Alternative: Full restart
systemctl --user restart hermes-gateway.service

# Check status after restart
sleep 5 && systemctl --user status hermes-gateway.service
```

### Step 4: Advanced Troubleshooting
```bash
# Check for permission issues
ls -la ~/.hermes/.env
chmod 644 ~/.hermes/.env  # Fix permissions if needed

# Check for process conflicts
ps aux | grep -i hermes

# Monitor real-time logs
journalctl --user -u hermes-gateway.service -f

# Check network connectivity
curl -I https://api.openrouter.ai/
curl -I https://api.telegram.org/
```

## Common Fixes

### API Key Configuration
```bash
# Set environment variable temporarily
export OPENROUTER_API_KEY="sk-or-..."

# Update .env file (if permissions allow)
echo "OPENROUTER_API_KEY=sk-or-..." >> ~/.hermes/.env

# Test the fix
cd ~/.hermes/hermes-agent && source venv/bin/activate && python -m hermes_cli.main gateway status
```

### Service Restart Process
```bash
# Graceful restart
systemctl --user stop hermes-gateway.service
sleep 3
systemctl --user start hermes-gateway.service
systemctl --user status hermes-gateway.service
```

### Permission Fixes
```bash
# Check and fix file permissions
ls -la ~/.hermes/
chmod 644 ~/.hermes/.env
chmod 600 ~/.hermes/.env  # More secure for API keys
```

## Best Practices

### 1. API Key Management
- Store API keys in `~/.hermes/.env` with proper permissions
- Use environment variables for testing
- Never commit API keys to version control
- Regularly rotate API keys

### 2. Service Monitoring
- Regularly check service health
- Monitor resource usage
- Keep an eye on error logs
- Set up alerts for failures

### 3. Configuration Backup
```bash
# Create regular backups
cp ~/.hermes/.env ~/.hermes/.env.backup.$(date +%Y%m%d)
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.backup.$(date +%Y%m%d)
```

### 4. Testing Changes
- Test API connectivity before applying
- Use temporary environment variables for testing
- Verify platform connections after changes
- Monitor logs for any issues

## Error Reference

### Common Error Messages
- `User not found` - API key issue
- `Connection refused` - Service not running
- `Permission denied` - File permission issues
- `Resource temporarily unavailable` - Resource constraints

### Error Resolution Matrix
| Error Code | Possible Cause | Solution |
|------------|----------------|----------|
| 401 | Authentication failed | Verify API keys and tokens |
| 403 | Permission denied | Check user permissions and bot rights |
| 429 | Rate limited | Implement retry with backoff |
| 500 | Server error | Check service logs and restart |
| 502 | Bad gateway | Restart gateway service |

## Related Commands

### Gateway Management
```bash
# Start service
hermes gateway start

# Stop service
hermes gateway stop

# Restart service
hermes gateway restart

# Check status
hermes gateway status

# View logs
journalctl --user -u hermes-gateway.service -f
```

### System Maintenance
```bash
# Clean up old logs
journalctl --user --vacuum-time=7d

# Check disk usage
df -h ~/.hermes/

# Monitor processes
top -p $(pgrep -f hermes)
```

This skill provides a comprehensive framework for troubleshooting messaging platform integration issues, ensuring reliable operation and quick resolution of common problems.