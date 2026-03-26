"""UI Theme and Display utilities using Rich."""

from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "title": "bold cyan",
    "subtitle": "cyan",
    "header": "bold magenta",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "info": "blue",
    "question": "bold white",
    "option": "dim",
    "selected": "green",
    "code": "dim cyan",
})

console = Console(theme=custom_theme)


class Colors:
    """Color constants for consistent styling."""

    PRIMARY = "cyan"
    SECONDARY = "magenta"
    SUCCESS = "green"
    WARNING = "yellow"
    ERROR = "red"
    INFO = "blue"
    DIM = "dim"

    # Special
    BOLD = "bold"
    ITALIC = "italic"


class Icons:
    """Unicode icons for visual elements."""

    CHECK = "✓"
    CROSS = "✗"
    ARROW = "→"
    BULLET = "•"
    STAR = "★"
    GEAR = "⚙"
    GLOBE = "🌐"
    ROBOT = "🤖"
    TOOLS = "🔧"
    KEY = "🔑"
    FOLDER = "📁"
    FILE = "📄"
    MAGNIFY = "🔍"
    PACKAGE = "📦"
    CLOUD = "☁"
    SHIELD = "🛡"
    LIGHTNING = "⚡"
