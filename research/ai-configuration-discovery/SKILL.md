---
name: ai-configuration-discovery
description: Systematic approach to discovering and documenting AI agent configuration parameters, migration data, and compatibility settings across different AI agent frameworks.
---

# AI Configuration Discovery Skill

## Overview

This skill provides a systematic methodology for discovering and documenting AI agent configuration parameters, migration data, and compatibility settings across different AI agent frameworks. It's particularly useful when migrating between AI agents, troubleshooting configuration issues, or understanding the setup of existing AI agent installations.

## Discovery Methodology

### Phase 1: Initial Search Strategy

**1. Conversation History Search**
```bash
# Search for references to the target AI agent
session_search query="agent-name"
session_search query="AgentName" 
session_search query="Agent Name"
```

**2. Filesystem Pattern Search**
```bash
# Search for configuration files and directories
find /path/to/search -name "*agent*" -o -name "*Agent*" 2>/dev/null
search_files pattern="agent-name|AgentName" target="files"
search_files pattern="\.json|\.yaml|\.yml|\.toml|\.cfg|\.conf|\.env" target="files"
```

### Phase 2: Configuration File Analysis

**1. Primary Configuration Locations**
- `~/.agent-name/` - Main configuration directory
- `~/.agent_name/` - Alternative naming convention
- `/path/to/install/` - Installation directory
- `~/.config/agent-name/` - System config location
- `~/.local/share/agent-name/` - Local data location

**2. Configuration File Types**
- `.env` files - Environment variables and API keys
- `.json` files - JSON configuration and manifest files
- `config.yaml`/`config.yml` - YAML configuration
- `settings.json`/`settings.py` - Application settings
- `manifest.json` - Extension/manifest files
- `pyproject.toml` - Python project configuration

**3. Content Analysis**
```bash
# Search for specific configuration patterns
search_files pattern="api.*key|API.*KEY|token|TOKEN" target="content"
search_files pattern="models|providers|servers|endpoints" target="content"
search_files pattern="skills|tools|permissions|security" target="content"
```

### Phase 3: Migration and Compatibility Data

**1. Migration Configuration**
- Source locations of data to be migrated
- Target locations after migration
- Compatibility mappings between old and new formats
- Schema differences between versions

**2. API Key Discovery**
- Environment variable locations
- Configuration file locations
- Key rotation and backup locations
- Security and encryption methods

**3. Skill and Tool Discovery**
- Available skill directories
- Tool definitions and schemas
- Permission and security settings
- Integration points with other systems

### Phase 4: Documentation and Analysis

**1. Configuration Mapping**
Create a comprehensive mapping of discovered configurations:

| Configuration Item | Location | Purpose | Migration Status |
|-------------------|----------|---------|-----------------|
| SOUL.md | ~/.agent-name/workspace/SOUL.md | Agent personality | Migrated |
| API Keys | ~/.agent-name/.env | Service authentication | Pending |
| Skills | ~/.agent-name/workspace/skills/ | Custom functionality | Migrated |
| Extensions | ~/.agent-name/extensions/ | Browser extensions | Pending |

**2. Dependency Analysis**
- Required dependencies and versions
- Optional dependencies and their purposes
- Integration dependencies
- Platform-specific requirements

**3. Security Analysis**
- Permission levels and restrictions
- Data storage locations and security
- Network access patterns
- Authentication mechanisms

## Discovery Workflow

### Step-by-Step Process

1. **Initial Assessment**
   ```bash
   # Determine what we're looking for
   - Target agent name and version
   - Purpose of discovery (migration, troubleshooting, documentation)
   - Known installation locations
   - Access permissions
   ```

2. **Systematic Search**
   ```bash
   # Search all possible locations
   session_search for references
   find command for directories
   search_files for content patterns
   ```

3. **Configuration Analysis**
   ```bash
   # Read and analyze configuration files
   - Read all discovered config files
   - Parse and structure the data
   - Identify dependencies and relationships
   - Map configuration hierarchies
   ```

4. **Documentation Creation**
   ```bash
   # Create comprehensive documentation
   - Configuration inventory
   - Migration guide
   - Troubleshooting guide
   - Security assessment
   - Best practices
   ```

### Common AI Agent Configuration Patterns

**1. API Key Storage**
```
Location patterns:
- ~/.agent-name/.env
- ~/.agent-name/config.yaml
- ~/.agent-name/agents/main/agent/auth-profiles.json
- ~/.agent-name/openclaw.json
- Inline in configuration files
```

**2. Skill Organization**
```
Directory patterns:
- ~/.agent-name/workspace/skills/
- ~/.agent-name/skills/
- ~/.agent-name/agents/*/skills/
- ~/.hermes/skills/ (for migrated systems)
```

**3. Migration Data**
```
Common migration items:
- SOUL.md (agent personality)
- MEMORY.md (user memories)
- USER.md (user profile)
- Skills and tool definitions
- API keys and credentials
- Security configurations
```

**4. Browser Integration**
```
Chrome extension patterns:
- Manifest V3 configurations
- Native messaging hosts
- MCP servers
- Service workers and content scripts
```

## Use Cases

### 1. Agent Migration Planning
```bash
# Before migrating between AI agents
- Discover all current configurations
- Map compatibility between old and new systems
- Identify potential conflicts or issues
- Create migration checklist
```

### 2. Troubleshooting Setup Issues
```bash
# When configuration problems occur
- Locate all relevant configuration files
- Check for missing or corrupted settings
- Verify API key and credential validity
- Analyze permission and security settings
```

### 3. System Documentation
```bash
# For documenting existing installations
- Create comprehensive configuration inventory
- Document dependencies and requirements
- Map integration points
- Create troubleshooting guides
```

### 4. Security Assessment
```bash
# For security reviews and audits
- Identify all stored credentials and keys
- Analyze permission levels and access controls
- Review data storage and transmission security
- Check for potential vulnerabilities
```

## Output Templates

### Configuration Inventory Template
```
# AI Agent Configuration Inventory

## Agent: [Agent Name]
## Version: [Version]
## Discovery Date: [Date]

### Primary Configuration Directory
Location: [Path]
Files: [List of files]

### API Keys and Credentials
- [Provider]: [Location] [Status]
- [Provider]: [Location] [Status]

### Skills and Tools
- [Skill Name]: [Location] [Status]
- [Tool Name]: [Location] [Status]

### Migration Information
- Source: [Source location]
- Target: [Target location]
- Status: [Migration status]

### Dependencies
- [Dependency]: [Version] [Status]
- [Dependency]: [Version] [Status]

### Security Configuration
- Permissions: [Description]
- Access Controls: [Description]
- Data Protection: [Description]
```

### Migration Assessment Template
```
# Migration Assessment Report

## From: [Source Agent]
## To: [Target Agent]

### Compatibility Analysis
- Configurations: [Match/Mismatch/Partial]
- Skills: [Compatible/Incompatible/Needs Adaptation]
- API Keys: [Transferable/Needs Reissue]
- Data: [Migratable/Lossy]

### Migration Risk Assessment
- High Risk Items: [List]
- Medium Risk Items: [List]
- Low Risk Items: [List]

### Recommended Actions
- Immediate Actions: [List]
- Medium-term Actions: [List]
- Long-term Actions: [List]
```

## Best Practices

### 1. Systematic Approach
- Always follow the discovery methodology
- Document every step and finding
- Verify information through multiple sources
- Keep track of what was searched and where

### 2. Security Considerations
- Be careful with sensitive configuration data
- Don't expose API keys or credentials in documentation
- Follow security protocols when accessing configuration
- Consider encryption for sensitive documentation

### 3. Documentation Quality
- Use consistent formatting and structure
- Include timestamps and version information
- Cross-reference related configurations
- Update documentation as configurations change

### 4. Verification
- Test discovered configurations
- Verify API keys and credentials
- Check that skills and tools are functional
- Validate migration compatibility

## Troubleshooting

### Common Issues

**1. Missing Configuration Files**
- Check alternative naming conventions
- Look in installation directories
- Search with case-insensitive patterns
- Check system-wide locations

**2. Corrupted Configuration**
- Backup before making changes
- Use validation tools when available
- Check file permissions and ownership
- Look for syntax errors in config files

**3. Permission Issues**
- Verify file access permissions
- Check user and group ownership
- Look for symlink issues
- Verify system-level access controls

### Verification Methods

**1. Configuration Validation**
```bash
# Test configuration files
- Check syntax validity
- Verify required fields are present
- Test API key connectivity
- Validate skill loading
```

**2. Functionality Testing**
```bash
# Test system functionality
- Run basic agent commands
- Test skill execution
- Verify API connectivity
- Check integration points
```

This skill provides a comprehensive framework for discovering and documenting AI agent configurations, making it easier to understand, migrate, and maintain AI agent systems.