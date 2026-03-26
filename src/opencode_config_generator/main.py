"""Main CLI entry point."""

import click
import sys
from pathlib import Path

from .ui.theme import console
from .ui.display import (
    print_welcome,
    print_step,
    print_done,
    print_info,
    print_success,
    show_generated_files,
)
from .detectors.stack import StackDetector
from .generators import ConfigGenerator
from .generators.skills import SkillGenerator
from .types import (
    ProjectConfig,
    AgentConfig,
    AgentMode,
    Language,
    ProjectType,
    Framework,
    PackageManager,
    PermissionLevel,
    MCPServer,
)


def is_interactive():
    """Check if running in interactive terminal."""
    return sys.stdin.isatty()


def run_interactive(name, output, detect):
    """Run interactive mode with prompts."""
    from .ui.prompts import (
        ask_project_name,
        ask_language,
        ask_project_type,
        ask_framework,
        ask_package_manager,
        confirm_stack,
        ask_num_agents,
        ask_agent_type,
        ask_agent_mode,
        ask_agent_model,
        ask_agent_tools,
        ask_mcp_servers,
        ask_output_directory,
        ask_additional_options,
        ask_permission_level,
        ask_skills_mode,
        ask_skills_auto,
        ask_skills_manual,
        ask_plugins,
    )
    
    print_welcome()
    
    step = 1
    total_steps = 10
    
    # Step 1: Project name
    print_step(step, total_steps, "Nombre del proyecto")
    if not name:
        name = ask_project_name()
    
    if not name:
        console.print("[error]Error: Nombre del proyecto es requerido[/error]")
        sys.exit(1)
    
    # Step 2: Detect stack
    print_step(step := step + 1, total_steps, "Detectando stack")
    
    detected = {}
    if detect:
        detector = StackDetector(".")
        detected = detector.detect()
        if detected:
            print_info("Stack detectado automáticamente")
        else:
            print_info("No se detectó stack automáticamente")
    
    # Step 3: Confirm or select language
    print_step(step := step + 1, total_steps, "Stack del proyecto")
    
    detected_lang = detected.get("language", "").lower() if detected else ""
    language = ask_language(detected_lang)
    
    # Project type
    detected_type = detected.get("project_type", "").lower() if detected else ""
    project_type = ask_project_type(detected_type)
    
    # Framework
    detected_framework = detected.get("framework", "").lower() if detected else ""
    framework = ask_framework(language, detected_framework)
    
    # Package manager
    detected_pm = detected.get("package_manager", "").lower() if detected else ""
    package_manager = ask_package_manager(language, detected_pm)
    
    # Confirm stack
    if not confirm_stack({
        "language": language.value.capitalize(),
        "framework": framework.value if framework and framework.value != "none" else None,
        "package_manager": package_manager.value if package_manager else None,
    }):
        # Re-ask with manual selection
        language = ask_language()
        project_type = ask_project_type()
        framework = ask_framework(language)
        package_manager = ask_package_manager(language)
    
    # Step 4: Skills (awesome-agent-skills)
    print_step(step := step + 1, total_steps, "Skills (awesome-agent-skills)")
    
    skills_mode = ask_skills_mode()
    selected_skills = []
    
    if skills_mode == "auto":
        selected_skills = ask_skills_auto(language.value, project_type.value)
    else:
        selected_skills = ask_skills_manual()
    
    create_skills = len(selected_skills) > 0
    
    # Step 6: Agents
    print_step(step := step + 1, total_steps, "Configuración de Agentes")
    
    num_agents = ask_num_agents()
    agents = []
    
    if num_agents > 0:
        console.print(f"\n[info]Configurando {num_agents} agente(s)...[/info]\n")
        
        for i in range(num_agents):
            agent_type = ask_agent_type()
            
            # Ask for agent details
            agent_name = click.prompt(
                f"Nombre del agente {i+1}",
                type=str,
                default=agent_type.replace("-", "_")
            )
            
            agent_description = click.prompt(
                "Descripción breve",
                type=str,
                default=f"Agente de {agent_type}"
            )
            
            mode_str = ask_agent_mode()
            mode = AgentMode.PRIMARY if mode_str == "primary" else AgentMode.SUBAGENT
            
            model = ask_agent_model()
            tools = ask_agent_tools()
            
            # Permission levels
            perm_edit = ask_permission_level("edit")
            perm_bash = ask_permission_level("bash")
            
            agent_config = AgentConfig(
                name=agent_name,
                description=agent_description,
                mode=mode,
                model=model,
                tools=tools,
                permission_edit=perm_edit,
                permission_bash=perm_bash,
            )
            
            agents.append(agent_config)
    
    # Step 7: MCP Servers
    print_step(step := step + 1, total_steps, "Servidores MCP")
    
    mcp_servers = ask_mcp_servers()
    
    # Step 8: Permissions
    print_step(step := step + 1, total_steps, "Permisos")
    
    perm_edit = ask_permission_level("edit")
    perm_bash = ask_permission_level("bash")
    
    # Step 9: Additional options
    print_step(step := step + 1, total_steps, "Opciones adicionales")
    
    options = ask_additional_options()
    
    # Step 10: Output directory
    print_step(step := step + 1, total_steps, "Directorio de salida")
    
    if not output:
        output = ask_output_directory(name)
    
    return create_config(
        name=name,
        output=output,
        detect=detect,
        language=language,
        project_type=project_type,
        framework=framework,
        package_manager=package_manager,
        detected=detected,
        agents=agents,
        mcp_servers=mcp_servers,
        selected_skills=selected_skills,
        selected_plugins=selected_plugins,
        local_plugins=local_plugins,
        perm_edit=perm_edit,
        perm_bash=perm_bash,
        options={**options, "create_skills": create_skills, "create_plugins": create_plugins},
    )


def create_config(name, output, detect, language=None, project_type=None, framework=None, package_manager=None, detected=None, agents=None, mcp_servers=None, selected_skills=None, selected_plugins=None, local_plugins=None, perm_edit=None, perm_bash=None, options=None):
    """Create ProjectConfig from provided or detected values."""
    
    # Use defaults if not provided
    if language is None:
        language = Language.TYPESCRIPT
    if project_type is None:
        project_type = ProjectType.WEB
    if framework is None:
        framework = Framework.NONE
    if package_manager is None:
        package_manager = PackageManager.NPM
    if detected is None:
        detected = {}
    if agents is None:
        agents = []
    if mcp_servers is None:
        mcp_servers = []
    if selected_skills is None:
        selected_skills = []
    if selected_plugins is None:
        selected_plugins = []
    if local_plugins is None:
        local_plugins = []
    if perm_edit is None:
        perm_edit = PermissionLevel.ALLOW
    if perm_bash is None:
        perm_bash = PermissionLevel.ASK
    if options is None:
        options = {"create_agents": True, "create_commands": True, "create_skills": False, "create_custom_tools": False, "create_plugins": False}
    
    # If auto skills, get them now
    if "__auto__" in selected_skills and language and project_type:
        skill_gen = SkillGenerator()
        selected_skills = skill_gen.get_auto_skills(language.value, project_type.value)
        options["create_skills"] = len(selected_skills) > 0
    
    return ProjectConfig(
        name=name,
        language=language,
        project_type=project_type,
        framework=framework,
        package_manager=package_manager,
        testing_framework=detected.get("testing"),
        formatter=detected.get("formatter"),
        linter=detected.get("linter"),
        agents=agents,
        mcp_servers=mcp_servers,
        selected_skills=selected_skills,
        selected_plugins=selected_plugins,
        local_plugins=local_plugins,
        permission_edit=perm_edit,
        permission_bash=perm_bash,
        output_dir=output,
        **options
    )


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """OpenCode Config Generator - CLI para generar configuraciones de OpenCode.
    
    Genera archivos de configuración completos para usar OpenCode en tu proyecto:
    - opencode.json: Configuración principal
    - AGENTS.md: Reglas del proyecto
    - .opencode/agents/: Agentes personalizados
    - .opencode/commands/: Comandos personalizados
    - .opencode/skills/: Habilidades (skills)
    - .opencode/tools/: Tools personalizadas
    
    \b
    Comandos principales:
    
    \b
    init           - Generar configuración (modo interactivo o CLI)
    list-mcps      - Listar servidores MCP disponibles
    list-agents    - Listar plantillas de agentes
    list-skills    - Listar skills de awesome-agent-skills
    list-plugins   - Listar plugins del ecosistema (33+ npm + 9 templates locales)
    
    \b
    Ejemplos:
    
    \b
    # Generar plantilla de configuración
    opencode-init --generate-template
    
    \b
    # Usar archivo de configuración
    opencode-init --config mi-config.md
    
    \b
    # Configuración básica
    opencode-init -n mi-proyecto -l python -f fastapi
    
    \b
    # Con skills auto
    opencode-init -n mi-proyecto -l python --skill auto --generate-skills
    
    \b
    # Listar recursos disponibles
    opencode-init list-skills
    opencode-init list-mcps
    """
    pass


@cli.command()
@click.option("--name", "-n", help="Nombre del proyecto")
@click.option("--output", "-o", help="Directorio de salida")
@click.option("--preview", is_flag=True, help="Solo mostrar preview sin generar archivos")
@click.option("--detect/--no-detect", default=True, help="Detectar stack automáticamente del directorio actual")
@click.option("--language", "-l", 
              type=click.Choice([l.value for l in Language]), 
              help="Lenguaje de programación (typescript, python, go, rust, java, php, ruby, swift, kotlin, csharp)")
@click.option("--framework", "-f", 
              type=click.Choice([fw.value for fw in Framework if fw.value != 'none']), 
              help="Framework (react, nextjs, vue, fastapi, django, express, nestjs, etc.)")
@click.option("--project-type", "-t", 
              type=click.Choice([pt.value for pt in ProjectType]), 
              help="Tipo de proyecto (web, api, library, monorepo, cli, mobile, fullstack, data, security)")
@click.option("--agents", "-a", type=int, default=0, help="Número de agentes personalizados a crear")
@click.option("--mcps", "-m", multiple=True, 
              help="MCP servers a habilitar (context7, sentry, gh_grep, github)")
@click.option("--skill", "-s", 
              help="Skill específica a generar (use 'auto' para auto-detectar según proyecto, o nombre específico)")
@click.option("--skills-mode", type=click.Choice(["auto", "manual"]), 
              help="Modo de selección de skills: auto (recomendadas) o manual")
@click.option("--perm-edit", type=click.Choice(["allow", "ask", "deny"]), default="allow", 
              help="Permisos para edit/write (allow=permitir siempre, ask=confirmar, deny=denegar)")
@click.option("--perm-bash", type=click.Choice(["allow", "ask", "deny"]), default="ask", 
              help="Permisos para bash (allow=permitir siempre, ask=confirmar, deny=denegar)")
@click.option("--commands/--no-commands", default=True, help="Generar comandos personalizados (/test, /lint)")
@click.option("--generate-skills/--no-generate-skills", default=False, help="Generar skills de awesome-agent-skills")
@click.option("--tools/--no-tools", default=False, help="Generar tools personalizadas (TypeScript)")
@click.option("--plugins", "-p", multiple=True, help="Plugins npm del ecosistema (nombre del package)")
@click.option("--local-plugins", multiple=True, help="Plugins locales a generar (notification, env-protection, inject-env, custom-tool, compaction-hook, session-tracker, command-logger, file-watcher, permission-handler)")
@click.option("--config", "-c", "config_file", type=click.Path(exists=True), 
              help="Archivo de configuración Markdown/YAML con toda la configuración")
@click.option("--generate-template", is_flag=True, help="Generar plantilla de configuración y salir")
@click.option("--interactive", "-i", is_flag=True, help="Forzar modo interactivo (requiere terminal)")
def init(name, output, preview, detect, language, framework, project_type, agents, mcps, skill, skills_mode, perm_edit, perm_bash, commands, generate_skills, tools, plugins, local_plugins, config_file, generate_template, interactive):
    """Iniciar generador de configuración de OpenCode.
    
    Ejemplos de uso:
    
    \b
    # Generar plantilla de configuración
    opencode-init --generate-template
    
    \b
    # Usar archivo de configuración
    opencode-init --config mi-config.md
    
    \b
    # Configuración básica por CLI
    opencode-init --name mi-proyecto --language python --framework fastapi
    
    \b
    # Con skills auto-detectadas
    opencode-init --name mi-proyecto --language python --skill auto --generate-skills
    
    \b
    # Con agentes y MCPs
    opencode-init --name mi-proyecto --agents 2 --mcps context7 --mcps sentry
    
    \b
    # Con plugins npm del ecosistema
    opencode-init --name mi-proyecto --plugins opencode-wakatime --plugins opencode-firecrawl
    
    \b
    # Con plugins locales
    opencode-init --name mi-proyecto --local-plugins notification --local-plugins custom-tool
    
    \b
    # Preview sin generar
    opencode-init --config mi-config.md --preview
    """
    
    from opencode_config_generator.config_parser import ConfigParser
    from pathlib import Path
    
    # Generate template if requested
    if generate_template:
        template_path = Path("./opencode-config-template.md")
        import shutil
        template_source = Path(__file__).parent.parent.parent / "config-template.md"
        if template_source.exists():
            shutil.copy(template_source, template_path)
            console.print(f"[success]✓ Plantilla generada en: {template_path}[/success]")
            console.print("\n[info]Edita el archivo y usa:[/info]")
            console.print(f"  opencode-init --config {template_path}")
            return
        else:
            console.print("[error]No se encontró la plantilla[/error]")
            sys.exit(1)
    
    # Check if config file is provided
    if config_file:
        print_welcome()
        
        console.print(f"\n[info]📄 Leyendo configuración de: {config_file}[/info]\n")
        
        parser = ConfigParser(config_file)
        project_config = parser.parse()
        
        if not project_config:
            console.print("[error]Error al parsear configuración:[/error]")
            for err in parser.get_errors():
                console.print(f"  [error]• {err}[/error]")
            sys.exit(1)
        
        # Show warnings if any
        for warn in parser.get_warnings():
            console.print(f"  [warning]⚠ {warn}[/warning]")
        
        console.print(f"\n[success]✓ Configuración parseada correctamente[/success]")
        console.print(f"  → Proyecto: {project_config.name}")
        console.print(f"  → Lenguaje: {project_config.language.value}")
        console.print(f"  → Agentes: {len(project_config.agents)}")
        console.print(f"  → MCPs: {len(project_config.mcp_servers)}")
        console.print(f"  → Skills: {len(project_config.selected_skills)}")
        
        output_dir = project_config.output_dir
        config = project_config
        
    # Check if interactive mode is needed or requested
    elif interactive or not name:
        if not is_interactive():
            console.print("[warning]No hay terminal interactiva disponible.[/warning]")
            console.print("[info]Usando modo no interactivo. Especifica --name y otras opciones.[/info]")
            if not name:
                console.print("[error]Error: --name es requerido en modo no interactivo[/error]")
                sys.exit(1)
        else:
            config = run_interactive(name, output, detect)
            output_dir = config.output_dir
    else:
        # Non-interactive mode with CLI options
        print_welcome()
        
        if not name:
            console.print("[error]Error: --name es requerido[/error]")
            sys.exit(1)
        
        # Detect stack if enabled
        if detect:
            print_step(1, 4, "Detectando stack")
            detector = StackDetector(".")
            detected = detector.detect()
            if detected:
                print_info("Stack detectado automáticamente")
                console.print(f"  → Lenguaje: {detected.get('language', 'N/A')}")
                console.print(f"  → Framework: {detected.get('framework', 'N/A')}")
                console.print(f"  → Gestor: {detected.get('package_manager', 'N/A')}")
            else:
                print_info("No se detectó stack automáticamente")
                detected = {}
        else:
            detected = {}
        
        # Use CLI options or defaults
        lang_enum = Language(language) if language else Language.TYPESCRIPT
        proj_type_enum = ProjectType(project_type) if project_type else ProjectType.WEB
        fw_enum = Framework(framework) if framework else Framework.NONE
        
        # Try to get from detected if not provided
        if not framework and detected.get("framework"):
            try:
                fw_enum = Framework(detected["framework"].lower())
            except:
                pass
        
        # Create MCP servers list
        mcp_server_list = []
        for mcp_name in mcps:
            if mcp_name == "context7":
                mcp_server_list.append(MCPServer(name="context7", description="Context7", type="remote", url="https://mcp.context7.com/mcp", enabled=True))
            elif mcp_name == "sentry":
                mcp_server_list.append(MCPServer(name="sentry", description="Sentry", type="remote", url="https://mcp.sentry.dev/mcp", enabled=True))
            elif mcp_name == "gh_grep":
                mcp_server_list.append(MCPServer(name="gh_grep", description="Grep by Vercel", type="remote", url="https://mcp.grep.app", enabled=True))
            elif mcp_name == "github":
                mcp_server_list.append(MCPServer(name="github", description="GitHub MCP", type="remote", url="https://github.com/github/copilot-mcp-server", enabled=True))
        
        # Handle skills
        selected_skills = []
        create_skills = generate_skills
        
        if skill:
            if skill == "auto":
                skill_gen = SkillGenerator()
                selected_skills = skill_gen.get_auto_skills(lang_enum.value, proj_type_enum.value)
                create_skills = True
            else:
                selected_skills.append(skill)
        elif skills_mode == "auto":
            skill_gen = SkillGenerator()
            selected_skills = skill_gen.get_auto_skills(lang_enum.value, proj_type_enum.value)
            create_skills = True
        
        # Handle plugins
        selected_plugins = list(plugins) if plugins else []
        local_plugins_list = list(local_plugins) if local_plugins else []
        
        # Create default agents if specified
        agent_configs = []
        if agents > 0:
            console.print(f"\n[info]Creando {agents} agente(s) por defecto...[/info]")
            for i in range(agents):
                agent_configs.append(AgentConfig(
                    name=f"agent_{i+1}",
                    description=f"Agente personalizado {i+1}",
                    mode=AgentMode.SUBAGENT,
                    model="anthropic/claude-sonnet-4-5",
                    tools=["read", "grep", "glob"],
                    permission_edit=PermissionLevel(perm_edit),
                    permission_bash=PermissionLevel(perm_bash),
                ))
        
        # Output directory
        if not output:
            output = f"./{name}/opencode-config"
        
        config = create_config(
            name=name,
            output=output,
            detect=detect,
            language=lang_enum,
            project_type=proj_type_enum,
            framework=fw_enum,
            package_manager=PackageManager.NPM if lang_enum in (Language.TYPESCRIPT, Language.JAVASCRIPT) else None,
            detected=detected,
            agents=agent_configs,
            mcp_servers=mcp_server_list,
            selected_skills=selected_skills,
            selected_plugins=selected_plugins,
            local_plugins=local_plugins_list,
            perm_edit=PermissionLevel(perm_edit),
            perm_bash=PermissionLevel(perm_bash),
            options={
                "create_agents": agents > 0,
                "create_commands": commands,
                "create_skills": create_skills,
                "create_custom_tools": tools,
                "create_plugins": bool(selected_plugins or local_plugins_list),
            }
        )
        
        output_dir = output
    
    # Generate
    if preview:
        console.print("\n[warning]Preview mode - No se generarán archivos[/warning]\n")
        generator = ConfigGenerator(output_dir)
        preview_data = generator.preview(config)
        
        console.print("[bold]opencode.json:[/bold]")
        console.print(preview_data["opencode.json"])
        console.print("\n[bold]AGENTS.md (primeros 50 líneas):[/bold]")
        console.print("\n".join(preview_data["AGENTS.md"].split("\n")[:50]))
        
    else:
        generator = ConfigGenerator(output_dir)
        files = generator.generate(config)
        
        print_done()
        
        show_generated_files(files)
        
        console.print(f"\n[success]Archivos generados en: {output_dir}[/success]")
        if config.selected_skills:
            console.print(f"\n[info]Skills generadas: {', '.join(config.selected_skills)}[/info]")
        console.print("\n[info]Próximos pasos:[/info]")
        console.print(f"  1. Copiar los archivos a tu proyecto: cp -r {output_dir}/* tu-proyecto/")
        console.print("  2. Revisar y personalizar los archivos según tus necesidades")
        console.print("  3. Ejecutar 'opencode' en tu proyecto")


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Mostrar más detalles")
def list_mcps(verbose):
    """Listar servidores MCP disponibles.
    
    Muestra los servidores MCP (Model Context Protocol) que puedes configurar
    en tu proyecto para extender las capacidades de OpenCode.
    
    \b
    Ejemplo:
    opencode-init list-mcps
    opencode-init list-mcps --verbose
    """
    
    available_mcps = [
        ("context7", "Búsqueda en documentación", "https://mcp.context7.com/mcp", "Remote"),
        ("sentry", "Errores y monitoring", "https://mcp.sentry.dev/mcp", "Remote"),
        ("gh_grep", "Búsqueda de código en GitHub (Grep by Vercel)", "https://mcp.grep.app", "Remote"),
        ("github", "Issues, PRs y código", "https://github.com/github/copilot-mcp-server", "Remote"),
    ]
    
    console.print("\n[bold]Servidores MCP disponibles:[/bold]\n")
    
    for name, desc, url, mtype in available_mcps:
        console.print(f"  [cyan]{name}[/cyan] - {desc}")
        if verbose:
            console.print(f"         [dim]URL: {url}[/dim]")
            console.print(f"         [dim]Tipo: {mtype}[/dim]")
        console.print()


@cli.command()
def list_agents():
    """Listar plantillas de agentes disponibles.
    
    Muestra las plantillas de agentes personalizados que puedes crear
    para automatizar tareas específicas en tu proyecto.
    
    \b
    Ejemplo:
    opencode-init list-agents
    """
    
    templates = [
        ("code-reviewer", "Analiza código y sugiere mejoras de calidad", "subagent"),
        ("test-generator", "Genera tests unitarios y de integración", "subagent"),
        ("docs-writer", "Genera documentación técnica", "subagent"),
        ("debugger", "Investiga y resuelve bugs", "subagent"),
        ("security-audit", "Análisis de seguridad", "subagent"),
        ("component-generator", "Genera componentes de UI", "subagent"),
        ("api-handler", "Genera endpoints de API", "subagent"),
    ]
    
    console.print("\n[bold]Plantillas de agentes disponibles:[/bold]\n")
    console.print("[dim]Todas las plantillas se generan como subagent[/dim]\n")
    
    for name, desc, mode in templates:
        console.print(f"  [cyan]{name}[/cyan] - {desc}")
        console.print(f"         [dim]Modo: {mode}[/dim]\n")


@cli.command()
def list_skills():
    """Listar skills disponibles de awesome-agent-skills."""
    
    skill_gen = SkillGenerator()
    categories = skill_gen.list_all_skills()
    
    console.print("\n[bold]Skills disponibles (awesome-agent-skills):[/bold]\n")
    console.print("[dim]Skills locales generadas automáticamente según selección[/dim]\n")
    
    for category, skills in categories.items():
        console.print(f"[bold]{category}:[/bold]")
        for skill in skills:
            langs = ", ".join(skill["languages"])
            console.print(f"  [cyan]{skill['name']}[/cyan] - {skill['description']}")
            console.print(f"         [dim]Lenguajes: {langs}[/dim]")
        console.print()


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Mostrar más detalles")
def list_plugins(verbose):
    """Listar plugins disponibles del ecosistema de OpenCode.
    
    Muestra los plugins npm disponibles en el ecosistema de OpenCode
    y los templates de plugins locales que puedes generar.
    
    \b
    Ejemplo:
    opencode-init list-plugins
    opencode-init list-plugins --verbose
    """
    
    from .types import PLUGIN_CATALOG
    from .generators.plugins import PluginsGenerator
    
    # Group npm plugins by category
    categories = {}
    for plugin in PLUGIN_CATALOG:
        if plugin.category not in categories:
            categories[plugin.category] = []
        categories[plugin.category].append(plugin)
    
    console.print("\n[bold]Plugins npm del ecosistema (33+):[/bold]\n")
    
    for category, plugins in categories.items():
        console.print(f"[bold]{category}:[/bold]")
        for plugin in plugins:
            console.print(f"  [cyan]{plugin.name}[/cyan] - {plugin.description}")
            if verbose:
                console.print(f"         [dim]Package: {plugin.npm_package}[/dim]")
        console.print()
    
    # List local plugin templates
    plugin_gen = PluginsGenerator()
    templates = plugin_gen.get_available_templates()
    
    console.print("\n[bold]Templates de plugins locales:[/bold]\n")
    
    for template in templates:
        desc = plugin_gen.get_template_description(template)
        console.print(f"  [cyan]{template}[/cyan] - {desc}")
    console.print()


if __name__ == "__main__":
    cli()
