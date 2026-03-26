"""Display utilities for showing information to user."""

from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich.text import Text
from .theme import console, Colors, Icons


def print_header(title: str) -> None:
    """Print a header section."""
    console.print(f"\n[header]{'═' * 50}[/header]")
    console.print(f"[header] {title} [/header]")
    console.print(f"[header]{'═' * 50}[/header]\n")


def print_subheader(title: str) -> None:
    """Print a subheader section."""
    console.print(f"\n[subtitle]{title}[/subtitle]")
    console.print(f"[subtitle]{'─' * 40}[/subtitle]\n")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[success]{Icons.CHECK} {message}[/success]")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[error]{Icons.CROSS} {message}[/error]")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[warning]{Icons.GEAR} {message}[/warning]")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[info]{Icons.ARROW} {message}[/info]")


def print_detected(label: str, value: str, confirmed: bool = True) -> None:
    """Print a detected item."""
    icon = Icons.CHECK if confirmed else Icons.CROSS
    color = Colors.SUCCESS if confirmed else Colors.ERROR
    console.print(f"[{color}]{icon}[/{color}] [bold]{label}:[/bold] {value}")


def show_stack_table(detected: dict) -> None:
    """Display detected stack in a table."""
    table = Table(title="Stack Detectado", show_header=True, header_style="bold magenta")
    table.add_column("Componente", style="cyan", width=20)
    table.add_column("Valor", style="white")

    if detected.get("language"):
        table.add_row("Lenguaje", detected["language"])
    if detected.get("framework"):
        table.add_row("Framework", detected["framework"])
    if detected.get("package_manager"):
        table.add_row("Gestor", detected["package_manager"])
    if detected.get("testing"):
        table.add_row("Testing", detected["testing"])
    if detected.get("formatter"):
        table.add_row("Formateador", detected["formatter"])
    if detected.get("linter"):
        table.add_row("Linter", detected["linter"])

    console.print(table)


def show_agents_summary(agents: list[dict]) -> None:
    """Display agents configuration summary."""
    if not agents:
        return

    table = Table(title="Agentes Configurados", show_header=True)
    table.add_column("Nombre", style="cyan")
    table.add_column("Modo", style="yellow")
    table.add_column("Descripción", style="white")

    for agent in agents:
        table.add_row(
            agent.get("name", ""),
            agent.get("mode", ""),
            agent.get("description", "")[:50]
        )

    console.print(table)


def show_mcp_summary(servers: list[dict]) -> None:
    """Display MCP servers configuration summary."""
    if not servers:
        return

    table = Table(title="Servidores MCP", show_header=True)
    table.add_column("Nombre", style="cyan")
    table.add_column("Tipo", style="yellow")
    table.add_column("Estado", style="white")

    for server in servers:
        enabled = server.get("enabled", False)
        status = f"[success]{Icons.CHECK} Enabled[/success]" if enabled else f"[dim]Disabled[/dim]"
        table.add_row(
            server.get("name", ""),
            server.get("type", ""),
            status
        )

    console.print(table)


def show_generated_files(files: list[str]) -> None:
    """Display list of generated files."""
    tree = Tree(f"[bold]{Icons.FOLDER} Archivos Generados[/bold]")

    for file in files:
        tree.add(f"[cyan]{Icons.FILE} {file}[/cyan]")

    console.print(tree)


def print_welcome() -> None:
    """Print welcome banner."""
    banner = Text()
    banner.append("╔════════════════════════════════════════════════════════╗\n", style="bold cyan")
    banner.append("║           OpenCode Config Generator                    ║\n", style="bold cyan")
    banner.append("║     Generador de configuraciones para OpenCode         ║\n", style="cyan")
    banner.append("╚════════════════════════════════════════════════════════╝\n", style="bold cyan")

    console.print(banner)


def print_step(step: int, total: int, title: str) -> None:
    """Print current step indicator."""
    console.print(f"\n[header]Step {step}/{total}: {Icons.GEAR} {title}[/header]\n")


def print_done() -> None:
    """Print completion message."""
    console.print(f"\n[success]{'═' * 50}[/success]")
    console.print(f"[success]{Icons.CHECK} ¡Configuración completada![/success]")
    console.print(f"[success]{'═' * 50}[/success]\n")
