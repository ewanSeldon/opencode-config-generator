"""Interactive prompts using Questionary."""

import questionary
from questionary import Choice
from typing import Optional
from ..types import Language, ProjectType, Framework, PackageManager, PermissionLevel, AgentConfig, MCPServer, PLUGIN_CATALOG
from .theme import console


def ask_project_name(default: Optional[str] = None) -> str:
    """Ask for project name."""
    return questionary.text(
        "Nombre del proyecto:",
        default=default or "",
        qmark="📁"
    ).ask()


def ask_language(detected: Optional[str] = None) -> Language:
    """Ask for programming language."""
    choices = [
        Choice("TypeScript", Language.TYPESCRIPT),
        Choice("JavaScript", Language.JAVASCRIPT),
        Choice("Python", Language.PYTHON),
        Choice("Go", Language.GO),
        Choice("Rust", Language.RUST),
        Choice("Java", Language.JAVA),
        Choice("PHP", Language.PHP),
        Choice("Ruby", Language.RUBY),
        Choice("Swift", Language.SWIFT),
        Choice("Kotlin", Language.KOTLIN),
        Choice("C#", Language.CSHARP),
    ]

    default_idx = 0
    if detected:
        for i, choice in enumerate(choices):
            if choice.value.value.lower() == detected.lower():
                default_idx = i
                break

    return questionary.select(
        "Lenguaje de programación:",
        choices=choices,
        default=choices[default_idx],
        qmark="🔤"
    ).ask()


def ask_project_type(detected: Optional[str] = None) -> ProjectType:
    """Ask for project type."""
    choices = [
        Choice("Web (Frontend)", ProjectType.WEB),
        Choice("API / Backend", ProjectType.API),
        Choice("Biblioteca / Paquete", ProjectType.LIBRARY),
        Choice("Monorepo", ProjectType.MONOREPO),
        Choice("CLI (Línea de comandos)", ProjectType.CLI),
        Choice("Móvil", ProjectType.MOBILE),
        Choice("Fullstack (Frontend + Backend)", ProjectType.FULLSTACK),
    ]

    default_idx = 0
    if detected:
        for i, choice in enumerate(choices):
            if choice.value.value.lower() == detected.lower():
                default_idx = i
                break

    return questionary.select(
        "Tipo de proyecto:",
        choices=choices,
        default=choices[default_idx],
        qmark="🌐"
    ).ask()


def ask_framework(language: Language, detected: Optional[str] = None) -> Optional[Framework]:
    """Ask for framework based on language."""
    
    frameworks_map = {
        Language.TYPESCRIPT: [
            Choice("React", Framework.REACT),
            Choice("Next.js", Framework.NEXTJS),
            Choice("Vue.js", Framework.VUE),
            Choice("Nuxt.js", Framework.NUXT),
            Choice("Svelte", Framework.SVELTE),
            Choice("Angular", Framework.ANGULAR),
            Choice("NestJS (Backend)", Framework.NESTJS),
            Choice("Express (Backend)", Framework.EXPRESS),
            Choice("Ninguno / Vanilla", Framework.NONE),
        ],
        Language.JAVASCRIPT: [
            Choice("React", Framework.REACT),
            Choice("Next.js", Framework.NEXTJS),
            Choice("Vue.js", Framework.VUE),
            Choice("Nuxt.js", Framework.NUXT),
            Choice("Svelte", Framework.SVELTE),
            Choice("Angular", Framework.ANGULAR),
            Choice("Express (Backend)", Framework.EXPRESS),
            Choice("Ninguno / Vanilla", Framework.NONE),
        ],
        Language.PYTHON: [
            Choice("FastAPI", Framework.FASTAPI),
            Choice("Django", Framework.DJANGO),
            Choice("Flask", Framework.FLASK),
            Choice("Ninguno", Framework.NONE),
        ],
        Language.GO: [
            Choice("Gin", Framework.GIN),
            Choice("Chi", Framework.GIN),
            Choice("Echo", Framework.FASTIFY),
            Choice("Ninguno", Framework.NONE),
        ],
    }

    choices = frameworks_map.get(language, [Choice("Ninguno", Framework.NONE)])

    default_idx = len(choices) - 1
    if detected:
        for i, choice in enumerate(choices):
            if choice.value.value.lower() == detected.lower():
                default_idx = i
                break

    return questionary.select(
        "Framework:",
        choices=choices,
        default=choices[default_idx],
        qmark="⚡"
    ).ask()


def ask_package_manager(language: Language, detected: Optional[str] = None) -> Optional[PackageManager]:
    """Ask for package manager based on language."""
    
    managers_map = {
        Language.TYPESCRIPT: [
            Choice("npm", PackageManager.NPM),
            Choice("pnpm", PackageManager.PNPM),
            Choice("yarn", PackageManager.YARN),
            Choice("bun", PackageManager.BUN),
        ],
        Language.JAVASCRIPT: [
            Choice("npm", PackageManager.NPM),
            Choice("pnpm", PackageManager.PNPM),
            Choice("yarn", PackageManager.YARN),
            Choice("bun", PackageManager.BUN),
        ],
        Language.PYTHON: [
            Choice("Poetry", PackageManager.POETRY),
            Choice("pip / pipenv", PackageManager.PIP),
        ],
        Language.GO: [
            Choice("Go modules (go.mod)", PackageManager.GO_MOD),
        ],
        Language.RUST: [
            Choice("Cargo", PackageManager.CARGO),
        ],
    }

    choices = managers_map.get(language, [])

    if not choices:
        return None

    default_idx = 0
    if detected:
        for i, choice in enumerate(choices):
            if choice.value.value.lower() == detected.lower():
                default_idx = i
                break

    return questionary.select(
        "Gestor de paquetes:",
        choices=choices,
        default=choices[default_idx],
        qmark="📦"
    ).ask()


def confirm_stack(detected: dict) -> bool:
    """Confirm detected stack."""
    console.print("\n[bold]Stack detectado:[/bold]")
    
    if detected.get("language"):
        console.print(f"  🔤 Lenguaje: {detected['language']}")
    if detected.get("framework"):
        console.print(f"  ⚡ Framework: {detected['framework']}")
    if detected.get("package_manager"):
        console.print(f"  📦 Gestor: {detected['package_manager']}")
    if detected.get("testing"):
        console.print(f"  🧪 Testing: {detected['testing']}")
    if detected.get("formatter"):
        console.print(f"  ✨ Formateador: {detected['formatter']}")
    if detected.get("linter"):
        console.print(f"  🔍 Linter: {detected['linter']}")

    return questionary.confirm(
        "\n¿Confirmas este stack?",
        default=True,
        qmark="❓"
    ).ask()


def ask_permission_level(tool: str) -> PermissionLevel:
    """Ask for permission level for a tool."""
    return questionary.select(
        f"Permisos para [bold]{tool}[/bold]:",
        choices=[
            Choice("✓ Allow - Permitir siempre", PermissionLevel.ALLOW),
            Choice("❓ Ask - Confirmar siempre", PermissionLevel.ASK),
            Choice("✗ Deny - Denegar siempre", PermissionLevel.DENY),
        ],
        default=PermissionLevel.ASK if tool == "bash" else PermissionLevel.ALLOW,
        qmark="🔐"
    ).ask()


def ask_num_agents() -> int:
    """Ask how many custom agents to create."""
    return questionary.select(
        "¿Cuántos agentes personalizados necesitas?",
        choices=[
            Choice("0 - Usar solo los integrados", 0),
            Choice("1 - Un agente específico", 1),
            Choice("2 - Dos agentes", 2),
            Choice("3 - Suite completa", 3),
        ],
        qmark="🤖"
    ).ask()


def ask_agent_type() -> str:
    """Ask for type of agent to create."""
    return questionary.select(
        "Selecciona tipo de agente:",
        choices=[
            Choice("Code Reviewer - Análisis sin modificar", "code-reviewer"),
            Choice("Test Generator - Generar tests", "test-generator"),
            Choice("Docs Writer - Documentación", "docs-writer"),
            Choice("Debugger - Investigación de bugs", "debugger"),
            Choice("Security Audit - Análisis de seguridad", "security-audit"),
            Choice("Component Generator - Generar componentes", "component-generator"),
            Choice("API Handler - Generar endpoints", "api-handler"),
            Choice("Custom - Crear desde cero", "custom"),
        ],
        qmark="🤖"
    ).ask()


def ask_agent_mode() -> str:
    """Ask for agent mode."""
    return questionary.select(
        "Modo del agente:",
        choices=[
            Choice("Subagent - Puede ser invocado por otros agentes", "subagent"),
            Choice("Primary - Agente principal", "primary"),
        ],
        default="subagent",
        qmark="🎯"
    ).ask()


def ask_agent_model() -> str:
    """Ask for model to use in agent."""
    return questionary.select(
        "Modelo a usar:",
        choices=[
            Choice("Claude Sonnet 4.5 (balanceado)", "anthropic/claude-sonnet-4-5"),
            Choice("Claude Haiku 4.5 (rápido)", "anthropic/claude-haiku-4-5"),
            Choice("Claude Opus 4.5 (potente)", "anthropic/claude-opus-4-5"),
            Choice("GPT-4o (OpenAI)", "openai/gpt-4o"),
            Choice("GPT-4o-mini (rápido)", "openai/gpt-4o-mini"),
            Choice("Gemini 1.5 Pro (Google)", "google/gemini-1.5-pro"),
        ],
        default="anthropic/claude-sonnet-4-5",
        qmark="🧠"
    ).ask()


def ask_agent_tools() -> list[str]:
    """Ask for tools to enable for agent."""
    return questionary.checkbox(
        "Herramientas habilitadas:",
        choices=[
            Choice("Read - Leer archivos", "read"),
            Choice("Write - Escribir archivos", "write"),
            Choice("Edit - Editar archivos", "edit"),
            Choice("Bash - Ejecutar comandos", "bash"),
            Choice("Grep - Buscar contenido", "grep"),
            Choice("Glob - Buscar archivos", "glob"),
            Choice("WebFetch - Obtener URLs", "webfetch"),
            Choice("WebSearch - Buscar en web", "websearch"),
            Choice("Skill - Usar habilidades", "skill"),
            Choice("TodoWrite - Crear tareas", "todowrite"),
            Choice("TodoRead - Leer tareas", "todoread"),
            Choice("Question - Hacer preguntas", "question"),
            Choice("Otra / Personalizada", "__custom__"),
        ],
        qmark="🔧"
    ).ask()


def ask_mcp_servers() -> list[MCPServer]:
    """Ask which MCP servers to enable."""
    
    available_mcps = [
        MCPServer(
            name="context7",
            description="Búsqueda en documentación",
            type="remote",
            url="https://mcp.context7.com/mcp"
        ),
        MCPServer(
            name="sentry",
            description="Errores y monitoring",
            type="remote",
            url="https://mcp.sentry.dev/mcp"
        ),
        MCPServer(
            name="gh_grep",
            description="Búsqueda de código en GitHub (Grep by Vercel)",
            type="remote",
            url="https://mcp.grep.app"
        ),
        MCPServer(
            name="github",
            description="Issues, PRs y código",
            type="remote",
            url="https://github.com/github/copilot-mcp-server"
        ),
    ]

    console.print("\n[bold]Servidores MCP disponibles:[/bold]")
    console.print("(Selecciona los que quieres configurar)\n")

    selected = questionary.checkbox(
        "MCP Servers:",
        choices=[
            Choice(f"{server.name} - {server.description}", server)
            for server in available_mcps
        ],
        qmark="🔌"
    ).ask()

    # Ask to enable each selected
    for server in selected:
        server.enabled = questionary.confirm(
            f"¿Habilitar {server.name}?",
            default=True,
            qmark="❓"
        ).ask()

    return selected


def ask_output_directory(project_name: str) -> str:
    """Ask for output directory."""
    return questionary.text(
        f"Directorio de salida (default: ./{project_name}/opencode-config):",
        default=f"./{project_name}/opencode-config",
        qmark="📁"
    ).ask()


def ask_additional_options() -> dict:
    """Ask for additional configuration options."""
    
    console.print("\n[bold]Opciones adicionales:[/bold]")

    create_agents = questionary.confirm(
        "¿Generar agentes personalizados?",
        default=True,
        qmark="🤖"
    ).ask()

    create_commands = questionary.confirm(
        "¿Generar comandos personalizados?",
        default=True,
        qmark="⚡"
    ).ask()

    create_skills = questionary.confirm(
        "¿Generar skills (habilidades)?",
        default=False,
        qmark="💡"
    ).ask()

    create_custom_tools = questionary.confirm(
        "¿Generar tools personalizadas (TypeScript)?",
        default=False,
        qmark="🔧"
    ).ask()

    return {
        "create_agents": create_agents,
        "create_commands": create_commands,
        "create_skills": create_skills,
        "create_custom_tools": create_custom_tools,
    }


def ask_skills_mode() -> str:
    """Ask for skills selection mode."""
    return questionary.select(
        "¿Cómo quieres seleccionar las habilidades (skills)?",
        choices=[
            Choice("Auto - Skills recomendadas según tu proyecto", "auto"),
            Choice("Manual - Seleccionar una por una", "manual"),
        ],
        default="auto",
        qmark="🎯"
    ).ask()


def ask_skills_auto(language: str, project_type: str) -> list[str]:
    """Ask to confirm auto-detected skills."""
    from ..generators.skills import SkillGenerator
    
    skill_gen = SkillGenerator()
    recommended = skill_gen.get_auto_skills(language, project_type)
    
    console.print("\n[bold]Skills recomendadas para tu proyecto:[/bold]\n")
    
    choices = []
    for skill_name in recommended:
        choices.append(Choice(skill_name, skill_name, True))
    
    # Añadir opción de personalizada
    choices.append(Choice("Otra / Personalizada", "__custom__"))
    
    selected = questionary.checkbox(
        "Selecciona las skills a incluir (espacio para seleccionar, enter para continuar):",
        choices=choices,
        qmark="🎯"
    ).ask()
    
    # Si eligió personalizada, pedir el nombre
    if "__custom__" in selected:
        selected.remove("__custom__")
        custom_name = questionary.text(
            "Nombre de la skill personalizada:",
            qmark="✏️"
        ).ask()
        if custom_name:
            selected.append(custom_name)
    
    return selected


def ask_skills_manual() -> list[str]:
    """Ask to select skills manually from all available."""
    from ..generators.skills import SkillGenerator
    from ..types import SKILL_CATALOG
    
    skill_gen = SkillGenerator()
    categories = skill_gen.list_all_skills()
    
    selected = []
    
    for category, skills in categories.items():
        console.print(f"\n[bold]{category}:[/bold]\n")
        
        choices = []
        for skill in skills:
            choices.append(Choice(f"{skill['name']} - {skill['description']}", skill['name']))
        
        # Añadir opción de personalizada
        choices.append(Choice("Otra / Personalizada", "__custom__"))
        
        category_selected = questionary.checkbox(
            f"Selecciona skills de {category} (espacio para seleccionar, enter para continuar):",
            choices=choices,
            qmark="🎯"
        ).ask()
        
        # Si eligió personalizada, pedir el nombre
        if "__custom__" in category_selected:
            category_selected.remove("__custom__")
            custom_name = questionary.text(
                "Nombre de la skill personalizada:",
                qmark="✏️"
            ).ask()
            if custom_name:
                selected.append(custom_name)
        
        selected.extend(category_selected)
    
    return selected


def ask_skills() -> tuple[bool, list[str]]:
    """Main function to ask about skills."""
    from ..generators.skills import SkillGenerator
    
    wants_skills = questionary.confirm(
        "¿Quieres generar habilidades (skills) basadas en awesome-agent-skills?",
        default=False,
        qmark="🎯"
    ).ask()
    
    if not wants_skills:
        return False, []
    
    mode = ask_skills_mode()
    
    selected_skills = []
    
    if mode == "auto":
        return True, ["__auto__"]
    else:
        selected_skills = ask_skills_manual()
    
    return True, selected_skills


def ask_plugins() -> tuple[bool, list[str], list[str]]:
    """Ask about plugins (NPM and local)."""
    wants_plugins = questionary.confirm(
        "¿Quieres configurar plugins de OpenCode?",
        default=False,
        qmark="🔌"
    ).ask()
    
    if not wants_plugins:
        return False, [], []
    
    selected_npm = []
    selected_local = []
    
    # Ask about NPM plugins
    use_npm_plugins = questionary.confirm(
        "¿Añadir plugins npm del ecosistema (33+ disponibles)?",
        default=True,
        qmark="📦"
    ).ask()
    
    if use_npm_plugins:
        # Group plugins by category
        categories = {}
        for plugin in PLUGIN_CATALOG:
            if plugin.category not in categories:
                categories[plugin.category] = []
            categories[plugin.category].append(plugin)
        
        for category, plugins in categories.items():
            console.print(f"\n[bold]{category}:[/bold]")
            
            choices = []
            for plugin in plugins:
                choices.append(Choice(f"{plugin.name} - {plugin.description}", plugin.name))
            
            category_selected = questionary.checkbox(
                f"Selecciona plugins de {category}:",
                choices=choices,
                qmark="🔌"
            ).ask()
            
            selected_npm.extend(category_selected)
    
    # Ask about local plugins
    use_local_plugins = questionary.confirm(
        "¿Crear plugins locales personalizados?",
        default=False,
        qmark="📁"
    ).ask()
    
    if use_local_plugins:
        from ..generators.plugins import PluginsGenerator
        
        plugin_gen = PluginsGenerator()
        templates = plugin_gen.get_available_templates()
        
        console.print("\n[bold]Templates de plugins locales:[/bold]\n")
        
        choices = []
        for template in templates:
            desc = plugin_gen.get_template_description(template)
            choices.append(Choice(f"{template} - {desc}", template))
        
        selected_local = questionary.checkbox(
            "Selecciona plugins a generar:",
            choices=choices,
            qmark="🔧"
        ).ask()
    
    return True, selected_npm, selected_local
