"""Type definitions for OpenCode Config Generator."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Language(str, Enum):
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    PYTHON = "python"
    GO = "go"
    RUST = "rust"
    JAVA = "java"
    PHP = "php"
    RUBY = "ruby"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    CSHARP = "csharp"


class ProjectType(str, Enum):
    WEB = "web"
    API = "api"
    LIBRARY = "library"
    MONOREPO = "monorepo"
    CLI = "cli"
    MOBILE = "mobile"
    FULLSTACK = "fullstack"
    DATA = "data"
    SECURITY = "security"


class Framework(str, Enum):
    REACT = "react"
    NEXTJS = "nextjs"
    VUE = "vue"
    NUXT = "nuxt"
    SVELTE = "svelte"
    ANGULAR = "angular"
    FASTAPI = "fastapi"
    DJANGO = "django"
    FLASK = "flask"
    EXPRESS = "express"
    NESTJS = "nestjs"
    GIN = "gin"
    FASTIFY = "fastify"
    SPRING = "spring"
    LARAVEL = "laravel"
    RAILS = "rails"
    NONE = "none"


class PackageManager(str, Enum):
    NPM = "npm"
    PNPM = "pnpm"
    YARN = "yarn"
    BUN = "bun"
    POETRY = "poetry"
    PIP = "pip"
    CARGO = "cargo"
    GO_MOD = "go.mod"


class PermissionLevel(str, Enum):
    ALLOW = "allow"
    ASK = "ask"
    DENY = "deny"


class AgentMode(str, Enum):
    PRIMARY = "primary"
    SUBAGENT = "subagent"


@dataclass
class ToolConfig:
    name: str
    enabled: bool = True
    permission: PermissionLevel = PermissionLevel.ALLOW


@dataclass
class AgentConfig:
    name: str
    description: str
    mode: AgentMode = AgentMode.SUBAGENT
    model: str = "anthropic/claude-sonnet-4-5"
    temperature: float = 0.3
    max_steps: Optional[int] = None
    tools: list[str] = field(default_factory=list)
    permission_edit: PermissionLevel = PermissionLevel.ALLOW
    permission_bash: PermissionLevel = PermissionLevel.ALLOW
    hidden: bool = False


@dataclass
class MCPServer:
    name: str
    description: str
    type: str  # "local" or "remote"
    url: Optional[str] = None
    command: Optional[list[str]] = None
    enabled: bool = False


@dataclass
class SkillDefinition:
    """Definition of an Agent Skill from awesome-agent-skills."""
    name: str
    description: str
    category: str
    languages: list[str] = field(default_factory=list)
    project_types: list[str] = field(default_factory=list)
    url: Optional[str] = None


# Complete catalog of skills from awesome-agent-skills
SKILL_CATALOG = [
    # Processing Documents
    SkillDefinition(
        name="docx",
        description="Crear, editar, analizar documentos Word con control de cambios",
        category="Procesamiento de Documentos",
        languages=["python", "typescript"],
        project_types=["general"]
    ),
    SkillDefinition(
        name="xlsx",
        description="Manipulación de hojas de cálculo: fórmulas, gráficos, transformaciones de datos",
        category="Procesamiento de Documentos",
        languages=["python", "typescript"],
        project_types=["data", "api"]
    ),
    SkillDefinition(
        name="pptx",
        description="Leer, generar y ajustar diapositivas, diseños, plantillas",
        category="Procesamiento de Documentos",
        languages=["python", "typescript"],
        project_types=["general"]
    ),
    SkillDefinition(
        name="pdf",
        description="Extraer texto, tablas, metadatos de PDFs",
        category="Procesamiento de Documentos",
        languages=["python", "typescript"],
        project_types=["general", "data"]
    ),
    SkillDefinition(
        name="markdown-to-epub",
        description="Convierte documentos markdown en libros electrónicos EPUB profesionales",
        category="Procesamiento de Documentos",
        languages=["python", "typescript"],
        project_types=["general", "library"]
    ),
    
    # Desarrollo Web
    SkillDefinition(
        name="playwright",
        description="Automatización del navegador para probar aplicaciones web",
        category="Desarrollo Web",
        languages=["typescript", "python"],
        project_types=["web", "fullstack"]
    ),
    SkillDefinition(
        name="d3js",
        description="Gráficos D3 y visualizaciones de datos interactivas",
        category="Desarrollo Web",
        languages=["javascript", "typescript"],
        project_types=["web"]
    ),
    SkillDefinition(
        name="obsidian-plugin",
        description="Desarrollo de plugins para Obsidian.md",
        category="Desarrollo Web",
        languages=["typescript"],
        project_types=["library"]
    ),
    SkillDefinition(
        name="stream-coding",
        description="Metodología de Stream Coding",
        category="Desarrollo Web",
        languages=["general"],
        project_types=["general"]
    ),
    SkillDefinition(
        name="specrate",
        description="Gestiona especificaciones y cambios con un flujo de trabajo estructurado",
        category="Desarrollo Web",
        languages=["general"],
        project_types=["general", "web", "api"]
    ),
    SkillDefinition(
        name="vibe-testing",
        description="Prueba de estrés de documentos de especificación con razonamiento LLM antes de escribir código",
        category="Desarrollo Web",
        languages=["general"],
        project_types=["general", "web", "api"]
    ),
    
    # AWS/Cloud
    SkillDefinition(
        name="aws-skills",
        description="Desarrollo AWS y mejores prácticas CDK",
        category="AWS/Cloud",
        languages=["typescript", "python"],
        project_types=["api", "web", "fullstack"]
    ),
    
    # iOS/macOS
    SkillDefinition(
        name="swiftui",
        description="Guía de plataforma y SwiftUI creada por Apple extraída de Xcode",
        category="iOS/macOS",
        languages=["swift"],
        project_types=["mobile"]
    ),
    SkillDefinition(
        name="ios-simulator",
        description="Interactuar con el Simulador de iOS para pruebas",
        category="iOS/macOS",
        languages=["swift"],
        project_types=["mobile"]
    ),
    SkillDefinition(
        name="swift-concurrency-migration",
        description="Guía de migración de Swift Concurrency",
        category="iOS/macOS",
        languages=["swift"],
        project_types=["mobile"]
    ),
    
    # Data/ML
    SkillDefinition(
        name="kaggle",
        description="Integración completa de Kaggle - configuración de cuenta, informes de competencias, descarga de datasets/modelos, ejecución de notebooks, envíos y colección de insignias",
        category="Data/ML",
        languages=["python"],
        project_types=["data"]
    ),
    SkillDefinition(
        name="csv-summarizer",
        description="Analizar archivos CSV y generar insights con visualizaciones",
        category="Data/ML",
        languages=["python"],
        project_types=["data", "api"]
    ),
    SkillDefinition(
        name="hf-dataset-creator",
        description="Prompts, plantillas y scripts para crear conjuntos de datos de entrenamiento estructurados",
        category="Data/ML",
        languages=["python"],
        project_types=["data", "library"]
    ),
    SkillDefinition(
        name="hf-model-evaluation",
        description="Instrucciones y utilidades para orquestar trabajos de evaluación, generar informes y mapear métricas",
        category="Data/ML",
        languages=["python"],
        project_types=["data"]
    ),
    SkillDefinition(
        name="hf-llm-trainer",
        description="Habilidad de entrenamiento integral con guía, scripts auxiliares, estimadores de costos",
        category="Data/ML",
        languages=["python"],
        project_types=["data"]
    ),
    SkillDefinition(
        name="hf-paper-publisher",
        description="Herramientas para publicar y gestionar artículos de investigación en Hugging Face Hub",
        category="Data/ML",
        languages=["python"],
        project_types=["data", "library"]
    ),
    
    # Colaboración
    SkillDefinition(
        name="git-pushing",
        description="Automatizar operaciones git e interacciones con repositorios",
        category="Colaboración",
        languages=["general"],
        project_types=["general"]
    ),
    SkillDefinition(
        name="review-implementing",
        description="Evaluar planes de implementación de código",
        category="Colaboración",
        languages=["general"],
        project_types=["general"]
    ),
    SkillDefinition(
        name="test-fixing",
        description="Detectar pruebas fallidas y proponer correcciones",
        category="Colaboración",
        languages=["general"],
        project_types=["general", "web", "api"]
    ),
    
    # Seguridad
    SkillDefinition(
        name="computer-forensics",
        description="Análisis e investigación de informática forense digital",
        category="Seguridad",
        languages=["general"],
        project_types=["security"]
    ),
    SkillDefinition(
        name="threat-hunting",
        description="Caza de amenazas usando reglas de detección Sigma",
        category="Seguridad",
        languages=["general"],
        project_types=["security", "api"]
    ),
    SkillDefinition(
        name="safe-encryption",
        description="Alternativa moderna de cifrado a GPG/PGP con soporte post-cuántico",
        category="Seguridad",
        languages=["python", "typescript"],
        project_types=["security", "api"]
    ),
    
    # Integraciones
    SkillDefinition(
        name="dev-browser",
        description="Capacidad de navegador web para agentes",
        category="Integraciones",
        languages=["typescript", "python"],
        project_types=["general"]
    ),
    SkillDefinition(
        name="sheets-cli",
        description="Automatización CLI de Google Sheets",
        category="Integraciones",
        languages=["python", "typescript"],
        project_types=["api", "data"]
    ),
    SkillDefinition(
        name="spotify",
        description="Integración de API de Spotify",
        category="Integraciones",
        languages=["python", "typescript"],
        project_types=["api"]
    ),
    SkillDefinition(
        name="notification",
        description="Enviar notificaciones de mensajes para flujos de trabajo de agentes",
        category="Integraciones",
        languages=["python", "typescript"],
        project_types=["general"]
    ),
    SkillDefinition(
        name="transloadit",
        description="Procesamiento de medios: codificación de video, manipulación de imágenes, OCR",
        category="Integraciones",
        languages=["python", "typescript"],
        project_types=["api"]
    ),
    
    # Avanzado
    SkillDefinition(
        name="context-engineering",
        description="Técnicas de ingeniería de contexto",
        category="Avanzado",
        languages=["general"],
        project_types=["general"]
    ),
    SkillDefinition(
        name="pomodoro-system",
        description="Patrón de Habilidad del Sistema (habilidades que recuerdan y mejoran)",
        category="Avanzado",
        languages=["general"],
        project_types=["general"]
    ),
    SkillDefinition(
        name="mind-cloning",
        description="Clonación mental con habilidades LLM",
        category="Avanzado",
        languages=["general"],
        project_types=["general"]
    ),
]


def get_skills_by_project(language: str, project_type: str) -> list[SkillDefinition]:
    """Get recommended skills based on language and project type."""
    recommended = []
    for skill in SKILL_CATALOG:
        if language.lower() in skill.languages or "general" in skill.languages:
            if project_type.lower() in skill.project_types or "general" in skill.project_types:
                recommended.append(skill)
    return recommended


def get_skills_by_category() -> dict[str, list[SkillDefinition]]:
    """Get all skills grouped by category."""
    categories = {}
    for skill in SKILL_CATALOG:
        if skill.category not in categories:
            categories[skill.category] = []
        categories[skill.category].append(skill)
    return categories


@dataclass
class PluginDefinition:
    """Definition of a Plugin from the OpenCode ecosystem."""
    name: str
    description: str
    category: str
    npm_package: Optional[str] = None
    local_template: Optional[str] = None


PLUGIN_CATALOG = [
    # Auth Plugins
    PluginDefinition(
        name="opencode-openai-codex-auth",
        description="Use your ChatGPT Plus/Pro subscription instead of API credits",
        category="Auth",
        npm_package="opencode-openai-codex-auth"
    ),
    PluginDefinition(
        name="opencode-gemini-auth",
        description="Use your existing Gemini plan instead of API billing",
        category="Auth",
        npm_package="opencode-gemini-auth"
    ),
    PluginDefinition(
        name="opencode-antigravity-auth",
        description="Use Antigravity's free models instead of API billing",
        category="Auth",
        npm_package="opencode-antigravity-auth"
    ),
    PluginDefinition(
        name="opencode-google-antigravity-auth",
        description="Google Antigravity OAuth Plugin with Google Search support",
        category="Auth",
        npm_package="opencode-google-antigravity-auth"
    ),

    # Dev Tools
    PluginDefinition(
        name="opencode-devcontainers",
        description="Multi-branch devcontainer isolation with shallow clones and auto-assigned ports",
        category="Dev Tools",
        npm_package="opencode-devcontainers"
    ),
    PluginDefinition(
        name="opencode-pty",
        description="Enables AI agents to run background processes in a PTY, send interactive input",
        category="Dev Tools",
        npm_package="opencode-pty"
    ),
    PluginDefinition(
        name="opencode-shell-strategy",
        description="Instructions for non-interactive shell commands - prevents hangs from TTY-dependent operations",
        category="Dev Tools",
        npm_package="opencode-shell-strategy"
    ),

    # Monitoring
    PluginDefinition(
        name="opencode-wakatime",
        description="Track OpenCode usage with Wakatime",
        category="Monitoring",
        npm_package="opencode-wakatime"
    ),
    PluginDefinition(
        name="opencode-codetime",
        description="Track your AI coding activity and time spent",
        category="Monitoring",
        npm_package="opencode-codetime"
    ),
    PluginDefinition(
        name="opencode-sentry-monitor",
        description="Trace and debug your AI agents with Sentry AI Monitoring",
        category="Monitoring",
        npm_package="opencode-sentry-monitor"
    ),

    # Utilities
    PluginDefinition(
        name="opencode-md-table-formatter",
        description="Clean up markdown tables produced by LLMs",
        category="Utilities",
        npm_package="opencode-md-table-formatter"
    ),
    PluginDefinition(
        name="opencode-zellij-namer",
        description="AI-powered automatic Zellij session naming based on OpenCode context",
        category="Utilities",
        npm_package="opencode-zellij-namer"
    ),
    PluginDefinition(
        name="opencode-daytona",
        description="Automatically run OpenCode sessions in isolated Daytona sandboxes with git sync and live previews",
        category="Utilities",
        npm_package="opencode-daytona"
    ),

    # AI/ML
    PluginDefinition(
        name="opencode-firecrawl",
        description="Web scraping, crawling, and search via the Firecrawl CLI",
        category="AI/ML",
        npm_package="opencode-firecrawl"
    ),
    PluginDefinition(
        name="opencode-supermemory",
        description="Persistent memory across sessions using Supermemory",
        category="AI/ML",
        npm_package="opencode-supermemory"
    ),
    PluginDefinition(
        name="opencode-skillful",
        description="Allow OpenCode agents to lazy load prompts on demand with skill discovery and injection",
        category="AI/ML",
        npm_package="opencode-skillful"
    ),
    PluginDefinition(
        name="opencode-websearch-cited",
        description="Add native websearch support with Google grounded style citations",
        category="AI/ML",
        npm_package="opencode-websearch-cited"
    ),

    # Security
    PluginDefinition(
        name="opencode-vibeguard",
        description="Redact secrets/PII into VibeGuard-style placeholders before LLM calls; restore locally",
        category="Security",
        npm_package="opencode-vibeguard"
    ),
    PluginDefinition(
        name="opencode-dynamic-context-pruning",
        description="Optimize token usage by pruning obsolete tool outputs",
        category="Security",
        npm_package="opencode-dynamic-context-pruning"
    ),

    # Notifications
    PluginDefinition(
        name="opencode-notificator",
        description="Desktop notifications and sound alerts for OpenCode sessions",
        category="Notifications",
        npm_package="opencode-notificator"
    ),
    PluginDefinition(
        name="opencode-notifier",
        description="Desktop notifications for permission, completion, and error events",
        category="Notifications",
        npm_package="opencode-notifier"
    ),
    PluginDefinition(
        name="opencode-notify",
        description="Native OS notifications for OpenCode - know when tasks complete",
        category="Notifications",
        npm_package="opencode-notify"
    ),

    # Advanced
    PluginDefinition(
        name="oh-my-opencode",
        description="Background agents, pre-built LSP/AST/MCP tools, curated agents, Claude Code compatible",
        category="Advanced",
        npm_package="oh-my-opencode"
    ),
    PluginDefinition(
        name="opencode-background-agents",
        description="Claude Code-style background agents with async delegation and context persistence",
        category="Advanced",
        npm_package="opencode-background-agents"
    ),
    PluginDefinition(
        name="opencode-workspace",
        description="Bundled multi-agent orchestration harness - 16 components, one install",
        category="Advanced",
        npm_package="opencode-workspace"
    ),
    PluginDefinition(
        name="opencode-worktree",
        description="Zero-friction git worktrees for OpenCode",
        category="Advanced",
        npm_package="opencode-worktree"
    ),
    PluginDefinition(
        name="opencode-helicone-session",
        description="Automatically inject Helicone session headers for request grouping",
        category="Advanced",
        npm_package="opencode-helicone-session"
    ),
    PluginDefinition(
        name="opencode-type-inject",
        description="Auto-inject TypeScript/Svelte types into file reads with lookup tools",
        category="Advanced",
        npm_package="opencode-type-inject"
    ),
    PluginDefinition(
        name="opencode-morph-plugin",
        description="Fast Apply editing, WarpGrep codebase search, and context compaction via Morph",
        category="Advanced",
        npm_package="opencode-morph-plugin"
    ),
    PluginDefinition(
        name="opencode-scheduler",
        description="Schedule recurring jobs using launchd (Mac) or systemd (Linux) with cron syntax",
        category="Advanced",
        npm_package="opencode-scheduler"
    ),
    PluginDefinition(
        name="micode",
        description="Structured Brainstorm → Plan → Implement workflow with session continuity",
        category="Advanced",
        npm_package="micode"
    ),
    PluginDefinition(
        name="octto",
        description="Interactive browser UI for AI brainstorming with multi-question forms",
        category="Advanced",
        npm_package="octto"
    ),
]


def get_plugins_by_category() -> dict[str, list[PluginDefinition]]:
    """Get all plugins grouped by category."""
    categories = {}
    for plugin in PLUGIN_CATALOG:
        if plugin.category not in categories:
            categories[plugin.category] = []
        categories[plugin.category].append(plugin)
    return categories


@dataclass
class ProjectConfig:
    name: str
    language: Language = Language.TYPESCRIPT
    project_type: ProjectType = ProjectType.WEB
    framework: Optional[Framework] = None
    package_manager: Optional[PackageManager] = None
    has_testing: bool = True
    has_linting: bool = True
    has_formatting: bool = True
    testing_framework: Optional[str] = None
    linter: Optional[str] = None
    formatter: Optional[str] = None
    agents: list[AgentConfig] = field(default_factory=list)
    mcp_servers: list[MCPServer] = field(default_factory=list)
    selected_skills: list[str] = field(default_factory=list)
    selected_plugins: list[str] = field(default_factory=list)
    local_plugins: list[str] = field(default_factory=list)
    permission_edit: PermissionLevel = PermissionLevel.ALLOW
    permission_bash: PermissionLevel = PermissionLevel.ASK
    output_dir: str = "./opencode-config"
    create_agents: bool = True
    create_commands: bool = True
    create_skills: bool = False
    create_custom_tools: bool = False
    create_plugins: bool = False
    create_vscode: bool = False
    create_github_actions: bool = False
    create_docker: bool = False
    create_precommit: bool = False
    create_release: bool = False
