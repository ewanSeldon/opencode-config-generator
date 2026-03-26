# OpenCode Config Generator

CLI tool to generate OpenCode configurations with support for:
- opencode.json
- AGENTS.md
- Custom agents
- Commands (/test, /lint, etc.)
- Skills from awesome-agent-skills (24+)
- MCP Servers
- Ecosystem plugins (33+)
- Custom local plugins
- Multi-agent coordination (ensemble/MCP/SSH/native)

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

# With all features
opencode-init -n my-project -l python \
  --vscode \
  --github-actions \
  --docker \
  --precommit \
  --release

# With plugins
opencode-init -n my-project --plugins opencode-wakatime --local-plugins notification

# With skills
opencode-init -n my-project --skill auto --generate-skills

# With agents and MCPs
opencode-init -n my-project --agents 2 --mcps context7 --mcps sentry

# Multi-agent setup (ensemble mode with remote agents)
opencode-init -n my-project \
  --agent-arch remote \
  --coordination ensemble \
  --agent-ips 192.168.1.5,192.168.1.6 \
  --ensemble

# Multi-agent setup (hybrid with SSH coordination)
opencode-init -n my-project \
  --agent-arch hybrid \
  --coordination ssh \
  --agent-ips 10.0.0.5,10.0.0.6,10.0.0.7

# Preview without generating
opencode-init --config config.md --preview

# List resources
opencode-init list-plugins
opencode-init list-skills
opencode-init list-mcps
```

## Features

- ✨ Automatic stack detection
- 📦 33+ OpenCode ecosystem plugins
- 🧩 9 local plugin templates
- 🤖 Custom agents (curated by project type)
- 💡 24+ Skills from awesome-agent-skills
- 🔌 MCP Servers (context7, sentry, gh_grep, github)
- 🎨 Interactive UI with Rich
- 👥 Multi-agent coordination (ensemble/MCP/SSH/native)

### Multi-Agent Architecture

| Flag | Description |
|------|-------------|
| `--agent-arch` | Architecture: `local`, `remote`, `hybrid` |
| `--coordination` | Coordination mode: `ensemble`, `mcp`, `ssh`, `native` |
| `--agent-ips` | Comma-separated list of remote agent IP addresses |
| `--ensemble` | Enable ensemble mode (opencode-ensemble plugin) |

**Coordination Modes:**
- **ensemble**: Use opencode-ensemble plugin with git worktrees
- **mcp**: Via MCP server coordinator
- **ssh**: Via SSH commands
- **native**: OpenCode native Task tool for subagent delegation

### Optional Integrations

| Flag | Generates |
|------|-----------|
| `--vscode` | `.vscode/settings.json`, `.vscode/extensions.json` |
| `--github-actions` | `.github/workflows/ci.yml`, `.github/workflows/coverage.yml` |
| `--docker` | `Dockerfile`, `.dockerignore` |
| `--precommit` | `.pre-commit-config.yaml` |
| `--release` | `.github/workflows/release.yml`, `.release-please-config.json` |

### Commands

- `opencode-init init` - Generate configuration
- `opencode-init list-plugins` - List ecosystem plugins
- `opencode-init list-skills` - List available skills
- `opencode-init list-mcps` - List MCP servers
- `opencode-init list-agents` - List agent templates

## Configuration File

You can also use a YAML configuration file:

```yaml
name: my-project
language: python
framework: fastapi
project_type: api
agents:
  - name: code-reviewer
    description: Code review agent
    mode: subagent
skills:
  - docx
  - pdf
plugins:
  npm:
    - opencode-wakatime
  local:
    - notification
create_vscode: true
create_github_actions: true
```

Then generate:
```bash
opencode-init --config config.yaml
```

## License

MIT
