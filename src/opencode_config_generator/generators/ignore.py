"""Generator for .ignore file."""

from ..types import Language


class IgnoreGenerator:
    """Generates .ignore file for ripgrep."""

    def generate(self, language: Language) -> str:
        """Generate .ignore file content."""
        
        content = """# ============================================================
# .ignore - Archivos a incluir en búsquedas
# ============================================================
# Este archivo permite que grep/glob/list encuentren
# archivos normalmente ignorados por .gitignore
# ============================================================

# Añadir archivos normalmente ignorados
# Ejemplos:

# Node.js
# !node_modules/
# !dist/
# !build/

# Python
# !__pycache__/
# !.venv/
# !venv/

# Rust
# !target/

# Go
# !vendor/

# Generales
# !.next/
# !.nuxt/
# !.cache/
"""

        # Add language-specific suggestions
        if language == Language.PYTHON:
            content += """

# Python - Descomenta para incluir:
# !__pycache__/
# !.venv/
# !venv/
# !env/
# !.env.local
"""
        elif language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            content += """

# JavaScript/TypeScript - Descomenta para incluir:
# !node_modules/
# !dist/
# !build/
# !.next/
# !.nuxt/
# !.cache/
"""

        return content
