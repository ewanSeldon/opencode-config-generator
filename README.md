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
