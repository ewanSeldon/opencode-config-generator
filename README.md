# OpenCode Config Generator

CLI tool para generar configuraciones de OpenCode con soporte para:
- opencode.json
- AGENTS.md
- Agentes personalizados
- Comandos (/test, /lint, etc.)
- Skills de awesome-agent-skills
- MCP Servers
- Plugins del ecosistema (33+)
- Plugins locales personalizados

## Instalación

```bash
pip install -e .
```

## Uso

```bash
# Modo interactivo
opencode-init -i

# Con argumentos
opencode-init -n mi-proyecto -l python --framework fastapi

# Con plugins
opencode-init -n mi-proyecto --plugins opencode-wakatime --local-plugins notification

# Listar recursos
opencode-init list-plugins
opencode-init list-skills
```

## Features

- ✨ Detección automática de stack
- 📦 33+ plugins del ecosistema OpenCode
- 🧩 9 templates de plugins locales
- 🤖 Agentes personalizados
- 💡 Skills de awesome-agent-skills
- 🔌 MCP Servers
- 🎨 UI interactiva con Rich
