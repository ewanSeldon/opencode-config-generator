# OpenCode Config Generator

CLI tool to generate OpenCode configurations with support for:
- opencode.json
- AGENTS.md
- Custom agents
- Commands (/test, /lint, etc.)
- Skills from awesome-agent-skills
- MCP Servers
- Ecosystem plugins (33+)
- Custom local plugins

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Interactive mode
opencode-init -i

# With arguments
opencode-init -n my-project -l python --framework fastapi

# With plugins
opencode-init -n my-project --plugins opencode-wakatime --local-plugins notification

# List resources
opencode-init list-plugins
opencode-init list-skills
```

## Features

- ✨ Automatic stack detection
- 📦 33+ OpenCode ecosystem plugins
- 🧩 9 local plugin templates
- 🤖 Custom agents
- 💡 Skills from awesome-agent-skills
- 🔌 MCP Servers
- 🎨 Interactive UI with Rich
