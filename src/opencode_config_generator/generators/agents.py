"""Generator for custom agents."""

from pathlib import Path
from ..types import AgentConfig, AgentMode


class AgentGenerator:
    """Generates custom agent markdown files."""
    
    CURATED_AGENTS = {
        "web": ["security-audit", "test-generator", "component-generator"],
        "api": ["security-audit", "test-generator", "api-handler"],
        "data": ["test-generator", "docs-writer"],
        "library": ["test-generator", "docs-writer", "code-reviewer"],
        "fullstack": ["security-audit", "test-generator", "component-generator", "api-handler"],
        "mobile": ["test-generator", "docs-writer"],
        "security": ["security-audit", "debugger"],
    }
    
    TEMPLATES = {
        "code-reviewer": {
            "description": "Analiza código y sugiere mejoras de calidad",
            "mode": AgentMode.SUBAGENT,
            "tools": ["read", "grep", "glob"],
            "temperature": 0.1,
            "prompt": """Eres un revisor de código experto. Analiza el código y proporciona sugerencias constructivas.

## Enfoque
- Calidad del código y mejores prácticas
- Potenciales bugs y casos edge
- Implicaciones de rendimiento
- Consideraciones de seguridad

## Restricciones
- NO realices cambios directos
- Sugiere mejoras con código de ejemplo
- Prioriza issues por severidad"""
        },
        "test-generator": {
            "description": "Genera tests unitarios y de integración",
            "mode": AgentMode.SUBAGENT,
            "tools": ["read", "write", "bash"],
            "temperature": 0.3,
            "prompt": """Eres un experto en testing. Genera tests exhaustivos para el código proporcionado.

## Enfoque
- Cubrir casos edge y boundary conditions
- Tests unitarios y de integración
- Usar mocking cuando sea necesario
- Asegurar coverage significativo

## Restricciones
- Seguir las convenciones de testing del proyecto
- No modificar código existente sin aprobación"""
        },
        "docs-writer": {
            "description": "Genera documentación técnica",
            "mode": AgentMode.SUBAGENT,
            "tools": ["read", "write", "glob"],
            "temperature": 0.2,
            "prompt": """Eres un escritor técnico. Genera documentación clara y completa.

## Enfoque
- Documentación clara y concisa
- Ejemplos de código cuando sea relevante
- Explicar el "por qué" además del "qué"
- Mantener consistencia con documentación existente"""
        },
        "debugger": {
            "description": "Investiga y resuelve bugs",
            "mode": AgentMode.SUBAGENT,
            "tools": ["read", "bash", "grep"],
            "temperature": 0.1,
            "prompt": """Eres un experto en debugging. Investiga y resuelve problemas en el código.

## Enfoque
- Analizar stack traces y errores
- Reproducir el problema
- Identificar causa raíz
- Proponer soluciones viables

## Restricciones
- No modificar código sin aprobación explícita
- Documentar findings y soluciones"""
        },
        "security-audit": {
            "description": "Análisis de seguridad",
            "mode": AgentMode.SUBAGENT,
            "tools": ["read", "grep"],
            "temperature": 0.1,
            "prompt": """Eres un experto en seguridad. Analiza el código para identificar vulnerabilidades.

## Enfoque
- OWASP Top 10
- Validación de inputs
- Autenticación y autorización
- Exposición de datos sensibles
- Dependencias con vulnerabilidades

## Restricciones
- Reportar sin modificar código
- Priorizar por severidad"""
        },
        "component-generator": {
            "description": "Genera componentes de UI",
            "mode": AgentMode.SUBAGENT,
            "tools": ["read", "write"],
            "temperature": 0.4,
            "prompt": """Eres un experto en componentes de UI. Genera código limpio y mantenible.

## Enfoque
- Componentes pequeños y reutilizables
- Props tipadas
- Estilos encapsulados
- Accesibilidad

## Restricciones
- Seguir patrones existentes del proyecto
- Usar componentes base cuando existan"""
        },
        "api-handler": {
            "description": "Genera endpoints de API",
            "mode": AgentMode.SUBAGENT,
            "tools": ["read", "write"],
            "temperature": 0.3,
            "prompt": """Eres un experto en APIs REST. Genera endpoints siguiendo mejores prácticas.

## Enfoque
- RESTful design
- Validación de inputs
- Manejo de errores consistente
- Documentación básica

## Restricciones
- Seguir convenciones del framework
- Usar middlewares existentes"""
        },
    }

    def generate(self, agent_type: str, config: AgentConfig) -> str:
        """Generate agent markdown file."""
        
        template = self.TEMPLATES.get(agent_type, {})
        
        content = f"""---
name: {config.name}
description: {config.description}
mode: {config.mode.value}
model: {config.model}
temperature: {config.temperature}
tools:
{self._format_tools(config.tools)}
---

# {config.name.capitalize()}

{template.get('prompt', config.description)}

---

# PERSONALIZAR ESTE AGENTE

## Cambiar modelo
# model: anthropic/claude-opus-4-5
# model: openai/gpt-4o
# model: google/gemini-1.5-pro

## Ajustar temperatura
# temperature: 0.0   # Más determinista, para análisis preciso
# temperature: 0.5   # Balanceado
# temperature: 0.8   # Más creativo, para brainstorming

## Modificar herramientas
# tools:
#   read: true      # Leer archivos
#   write: true     # Crear/sobrescribir archivos
#   edit: true      # Editar archivos existentes
#   bash: true      # Ejecutar comandos shell
#   grep: true      # Buscar en archivos
#   glob: true      # Buscar archivos por patrón
#   webfetch: true  # Obtener contenido de URLs
#   skill: true     # Usar habilidades

## Configurar permisos
# permission:
#   edit: deny      # Solo lectura
#   edit: ask       # Confirmar antes de editar
#   edit: allow     # Permitir siempre
#   bash: ask       # Confirmar comandos bash

## Ajustar pasos máximos
# steps: 50         # Límite de iteraciones
# steps: 100        # Más iteraciones para tareas complejas

## Ocultar del menú @
# hidden: true      # No aparece en autocompletado

## Añadir instrucciones adicionales
# prompt: |
#   Instrucciones adicionales...
#   - Siempre usar TypeScript strict
# - Verificar tests antes de finalizar
"""

        return content

    def _format_tools(self, tools: list[str]) -> str:
        """Format tools list for YAML."""
        lines = []
        for tool in tools:
            lines.append(f"  {tool}: true")
        return "\n".join(lines)

    def generate_all(self, agent_configs: list[AgentConfig]) -> dict[str, str]:
        """Generate all agent files."""
        
        files = {}
        
        for agent in agent_configs:
            # Map agent type from name
            agent_type = self._get_agent_type(agent.name)
            files[f"agents/{agent.name}.md"] = self.generate(agent_type, agent)
        
        return files

    def _get_agent_type(self, agent_name: str) -> str:
        """Get agent type from name."""
        
        name_lower = agent_name.lower()
        
        if "review" in name_lower:
            return "code-reviewer"
        elif "test" in name_lower:
            return "test-generator"
        elif "doc" in name_lower:
            return "docs-writer"
        elif "debug" in name_lower:
            return "debugger"
        elif "security" in name_lower:
            return "security-audit"
        elif "component" in name_lower:
            return "component-generator"
        elif "api" in name_lower or "endpoint" in name_lower:
            return "api-handler"
        
        return "code-reviewer"  # Default
    
    def get_curated_agents(self, project_type: str) -> list[str]:
        """Get curated agents for a project type."""
        return self.CURATED_AGENTS.get(project_type.lower(), [])
