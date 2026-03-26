"""Generator for AGENTS.md file."""

from pathlib import Path
from typing import Optional
from ..types import ProjectConfig, Language, Framework


class AgentsMDGenerator:
    """Generates AGENTS.md configuration file."""

    def generate(self, config: ProjectConfig) -> str:
        """Generate AGENTS.md content."""
        
        content = f"""# {config.name} - Configuración de OpenCode

## Estructura del Proyecto

- `src/` - Código fuente principal
- `tests/` - Tests unitarios
- `docs/` - Documentación
- `scripts/` - Scripts de utilidad

## Stack Tecnológico

- **Lenguaje**: {config.language.value.capitalize()}
{f'- **Framework**: {config.framework.value.capitalize()}' if config.framework and config.framework.value != 'none' else ''}
{f'- **Gestor de paquetes**: {config.package_manager.value}' if config.package_manager else ''}
{f'- **Testing**: {config.testing_framework}' if config.testing_framework else ''}
{f'- **Formateador**: {config.formatter}' if config.formatter else ''}
{f'- **Linter**: {config.linter}' if config.linter else ''}

## Convenciones de Código

{self._get_conventions(config)}

## Comandos Disponibles

{self._get_available_commands(config)}

## Notas Adicionales

{self._get_additional_notes(config)}

---

## PERSONALIZAR ESTE ARCHIVO

Este archivo contiene las reglas específicas del proyecto para OpenCode.
Puedes añadir más secciones según tus necesidades:

### Añadir más instrucciones

```markdown
## Instrucciones Adicionales

- Usar TypeScript con strict mode
- Prefijar componentes con el nombre del módulo
```

### Referenciar archivos externos

```markdown
Para código estilo: ver @docs/coding-style.md
Para tests: ver @test/guidelines.md
```

### Configurar comportamiento

```markdown
## Comportamiento del Agente

- Siempre ejecutar tests antes de commit
- Usar conventional commits
- Revisar PRs antes de merge
```
"""

        return content

    def _get_conventions(self, config: ProjectConfig) -> str:
        """Get code conventions based on language and framework."""
        
        conventions = []

        if config.language == Language.TYPESCRIPT:
            conventions.extend([
                "- Usar TypeScript con strict mode",
                "- Tipado explícito siempre que sea posible",
                "- Interfaces para tipos compartidos",
                "- PascalCase para componentes, camelCase para variables",
            ])
            
            if config.framework in (Framework.REACT, Framework.NEXTJS):
                conventions.extend([
                    "- Componentes funcionales con hooks",
                    "- Props con tipado usando interfaces",
                    "- Usar componentes de Next.js App Router",
                ])
                
        elif config.language == Language.PYTHON:
            conventions.extend([
                "- PEP 8 para estilo de código",
                "- Tipado con type hints",
                "- Docstrings para funciones y clases",
                "- snake_case para funciones y variables",
            ])
            
            if config.framework == Framework.FASTAPI:
                conventions.extend([
                    "- Usar Pydantic para validación de datos",
                    "- Endpoints REST con async/await",
                ])
                
        elif config.language == Language.GO:
            conventions.extend([
                "- Usar go modules",
                "- snake_case para variables (evitar PascalCase excepto exportables)",
                "- Error handling explícito",
                "- Context como primer argumento en funciones",
            ])

        elif config.language == Language.RUST:
            conventions.extend([
                "- Usar cargo para gestión de dependencias",
                "- Follow Rust idioms",
                "- Documentar con doc comments",
                "- Manejo de errores con Result",
            ])

        return "\n".join(conventions) if conventions else "- Seguir mejores prácticas del lenguaje"

    def _get_available_commands(self, config: ProjectConfig) -> str:
        """Get available commands based on project config."""
        
        commands = [
            "`/test` - Ejecutar suite de tests",
            "`/lint` - Ejecutar linter y formateador",
        ]

        if config.framework in (Framework.REACT, Framework.NEXTJS, Framework.VUE):
            commands.append("`/component` - Generar componente nuevo")
            commands.append("`/page` - Generar página nueva")
            
        elif config.framework == Framework.FASTAPI:
            commands.append("`/endpoint` - Generar nuevo endpoint")
            commands.append("`/model` - Generar modelo de datos")

        if config.language == Language.PYTHON:
            commands.append("`/migration` - Generar migración de BD")

        return "\n".join(commands)

    def _get_additional_notes(self, config: ProjectConfig) -> str:
        """Get additional notes based on project type."""
        
        notes = []

        if config.testing_framework:
            notes.append(f"- Tests: {config.testing_framework}")
            
        if config.linter:
            notes.append(f"- Linter: {config.linter}")
            
        notes.extend([
            "- Versionar AGENTS.md en Git",
            "- Compartir configuración con el equipo",
        ])

        return "\n".join(notes)
