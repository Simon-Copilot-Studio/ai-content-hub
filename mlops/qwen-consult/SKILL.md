---
name: "qwen-consult"
category: "mlops"
description: "Provides access to Qwen AI models through the qwen_consult MCP tool for complex code analysis, file-heavy refactors, and multi-step reasoning tasks."

---

# Qwen Consult Tool

## What it does
- Delegates complex tasks to Qwen Code CLI agent
- Provides file-system access and local repository analysis
- Supports multiple Qwen models for different use cases
- Returns structured responses from Qwen models

## Prerequisites
- qwen CLI installed and configured
- Qwen OAuth authentication set up
- Available API quota for Qwen services

## Usage
Use this tool for:
- Deep code analysis and understanding
- File-heavy refactoring operations
- Multi-step reasoning on local repositories
- When you need a second LLM opinion on complex tasks
- Code generation with file access capabilities

## Tool Parameters
- `prompt`: The task description in English (Qwen prefers English)
- `model`: Qwen model to use (default: qwen3-coder-plus)
- `timeout_s`: Max seconds to wait (default: 300)

## Available Models
- qwen3-coder-plus: Default model for coding tasks
- coder-model: Fallback model when specific model unavailable
- Other Qwen models may be available based on your plan

## Configuration
Ensure your Qwen authentication is properly configured:
```bash
# Check qwen CLI status
qwen --version

# Test basic functionality
qwen -y "Hello" --auth-type qwen-oauth
```

## Example Usage
```bash
# Simple code analysis
qwen_consult "Analyze this Python code for performance issues and suggest optimizations"

# File-heavy refactor
qwen_consult "Refactor this monolithic function into smaller, testable components"

# Repository analysis
qwen_consult "Review the entire codebase for security vulnerabilities"
```

## Notes
- Qwen CLI must be installed at `/home/simon/.npm-global/bin/qwen`
- Authentication requires proper OAuth configuration
- API quota limitations may affect availability
- Tool runs non-interactively with file-system access

## Troubleshooting
If you encounter authentication errors:
1. Verify OAuth token is valid in `~/.qwen/oauth_creds.json`
2. Check authentication type in `~/.qwen/settings.json`
3. Ensure API quota is available

## Files Created/Modified
- `/home/simon/qwen-mcp/server.py`: MCP server implementation
- `/home/simon/.qwen/settings.json`: Qwen configuration
- `/home/simon/.qwen/oauth_creds.json`: OAuth credentials

---

**Important**: This skill requires the qwen MCP server to be running. The server is automatically configured in your Hermes config.yaml under the `mcp_servers` section.