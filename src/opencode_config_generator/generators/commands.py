"""Generator for custom commands."""

from pathlib import Path
from ..types import Language, ProjectConfig


class CommandGenerator:
    """Generates custom command markdown files."""

    def generate_all(self, config: ProjectConfig) -> dict[str, str]:
        """Generate all command files based on project config."""
        
        files = {}
        
        # Test command - always
        files["commands/test.md"] = self._generate_test_command(config)
        
        # Lint command
        if config.has_linting:
            files["commands/lint.md"] = self._generate_lint_command(config)
        
        # Language-specific commands
        if config.language == Language.TYPESCRIPT:
            files["commands/type-check.md"] = self._generate_typecheck_command(config)
            
        elif config.language == Language.PYTHON:
            files["commands/type-check.md"] = self._generate_mypy_command(config)
            
        return files

    def _generate_test_command(self, config: ProjectConfig) -> str:
        """Generate test command."""
        
        # Determine test command based on framework
        test_cmd = "npm test"
        coverage_cmd = "npm test -- --coverage"
        
        if config.testing_framework:
            if config.testing_framework.lower() == "pytest":
                test_cmd = "pytest"
                coverage_cmd = "pytest --cov"
            elif config.testing_framework.lower() == "jest":
                test_cmd = "npm test"
                coverage_cmd = "npm test -- --coverage"
            elif config.testing_framework.lower() == "vitest":
                test_cmd = "npx vitest"
                coverage_cmd = "npx vitest --coverage"
            elif config.testing_framework.lower() == "playwright":
                test_cmd = "npx playwright test"
                coverage_cmd = "npx playwright test --reporter=html"
        
        return f"""---
description: Ejecutar tests con coverage
agent: build
model: anthropic/claude-sonnet-4-5
---

Ejecuta la suite de tests completa con reporte de coverage.
Muestra los tests que fallan y sugiere correcciones.

---

# PERSONALIZAR ESTE COMANDO

## Cambiar agente
# agent: build        # Predeterminado, puede hacer cambios
# agent: plan        # Solo análisis, sin modificar archivos

## Cambiar modelo
# model: anthropic/claude-haiku-4-5    # Más rápido
# model: anthropic/claude-opus-4-5     # Más potente
# model: openai/gpt-4o-mini           # Económico

## Añadir argumentos
# usage: /test unit
# template: Ejecuta los tests $ARGUMENTS

## Incluir salida de comandos
# """ + f"""```markdown
# Salida de tests:
# !`{test_cmd}`
# ```
"""

    def _generate_lint_command(self, config: ProjectConfig) -> str:
        """Generate lint command."""
        
        lint_cmd = "npm run lint"
        
        if config.linter:
            if config.linter.lower() in ["eslint", "tslint"]:
                lint_cmd = "npm run lint"
            elif config.linter.lower() == "flake8":
                lint_cmd = "flake8 ."
            elif config.linter.lower() == "ruff":
                lint_cmd = "ruff check ."

        return f"""---
description: Ejecutar linter y formateador
agent: build
model: anthropic/claude-sonnet-4-5
---

Ejecuta el linter y formateador de código.
Muestra errores de estilo y sugiere correcciones automáticas.

---

# PERSONALIZAR ESTE COMANDO

## Cambiar agente
# agent: build        # Puede aplicar cambios
# agent: plan        # Solo mostrar errores

## Añadir comandos específicos
# """ + f"""```markdown
# Ejecuta: !`{lint_cmd}`
# ```
"""

    def _generate_typecheck_command(self, config: ProjectConfig) -> str:
        """Generate type check command for TypeScript."""
        
        return """---
description: Ejecutar TypeScript type checker
agent: build
model: anthropic/claude-haiku-4-5
---

Ejecuta el type checker de TypeScript.
Muestra errores de tipos y sugiere correcciones.

---

# PERSONALIZAR ESTE COMANDO

## Cambiar agente
# agent: build        # Puede aplicar cambios automática

## Añadir más herramientas
# tools:
#   bash: true        # Necesario para ejecutar tsc
#   edit: true        # Para aplicar fix automáticos
"""

    def _generate_mypy_command(self, config: ProjectConfig) -> str:
        """Generate mypy command for Python."""
        
        return """---
description: Ejecutar MyPy type checker
agent: build
model: anthropic/claude-haiku-4-5
---

Ejecuta MyPy para verificación de tipos en Python.
Muestra errores de tipos y sugiere correcciones.

---

# PERSONALIZAR ESTE COMANDO

## Añadir configuración de mypy
# template: |
#   Ejecuta mypy con configuración estricta
#   !`mypy src/ --strict`

## Cambiar agente
# agent: build        # Puede aplicar cambios
"""
