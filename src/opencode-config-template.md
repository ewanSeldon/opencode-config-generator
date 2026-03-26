# OpenCode Config - Plantilla de Configuración
# ============================================
# Este archivo contiene la configuración para generar
# los archivos de OpenCode. Edita los valores según
# tu proyecto.
# ============================================

# ============================================
# SECCIÓN 1: PROYECTO
# ============================================

name: mi-proyecto
language: typescript
project_type: web
framework: nextjs
package_manager: npm

# ============================================
# SECCIÓN 2: AGENTES PERSONALIZADOS
# ============================================

agents:
  # Ejemplo de agente completo
  - name: code-reviewer
    description: Analiza código y sugiere mejoras de calidad
    mode: subagent
    model: anthropic/claude-sonnet-4-5
    temperature: 0.1
    tools:
      - read
      - grep
      - glob
    permission:
      edit: deny
      bash: deny

  # Ejemplo de agente simple
  - name: test-generator
    description: Genera tests unitarios y de integración

  # Puedes añadir más agentes aquí
  # - name: mi-agente
  #   description: Descripción del agente

# ============================================
# SECCIÓN 3: MCP SERVERS
# ============================================

mcp:
  # Context7 - Búsqueda en documentación
  context7:
    type: remote
    url: https://mcp.context7.com/mcp
    description: Búsqueda en documentación

  # Sentry - Errores y monitoring
  # sentry:
  #   type: remote
  #   url: https://mcp.sentry.dev/mcp

  # GitHub - Issues y PRs
  # github:
  #   type: remote
  #   url: https://github.com/github/copilot-mcp-server

  # Grep by Vercel
  # gh_grep:
  #   type: remote
  #   url: https://mcp.grep.app

# ============================================
# SECCIÓN 4: SKILLS (awesome-agent-skills)
# ============================================

skills:
  # Skills de colaboración (útiles para todos los proyectos)
  - git-pushing
  - test-fixing
  - review-implementing

  # Skills específicas por tipo de proyecto:
  # - Web/Frontend: playwright, d3js, vibe-testing
  # - API/Backend: aws-skills, safe-encryption
  # - Data/ML: kaggle, csv-summarizer, hf-dataset-creator
  # - iOS: swiftui, ios-simulator
  # - Seguridad: threat-hunting, computer-forensics

  # Skills personalizadas (no están en el catálogo)
  # - mi-skill-personalizada

# ============================================
# SECCIÓN 5: PERMISOS
# ============================================

permission:
  # Opciones: allow, ask, deny
  edit: allow
  bash: ask
  webfetch: allow
  # websearch: allow  # Requiere OPENCODE_ENABLE_EXA=1
  # lsp: allow        # Experimental

# ============================================
# SECCIÓN 6: OPCIONES GENERALES
# ============================================

# Crear agentes personalizados
create_agents: true

# Crear comandos personalizados (/test, /lint, etc)
create_commands: true

# Crear skills
create_skills: false

# Crear tools personalizadas (TypeScript)
create_custom_tools: false

# Directorio de salida
# output_dir: ./mi-proyecto/opencode-config

# ============================================
# SECCIÓN 7: NIVEL DE DETALLE DE SKILLS
# ============================================

# Nivel de detalle para las skills generadas:
# - basic: Solo SKILL.md conciso (< 100 líneas)
# - standard: SKILL.md con ejemplos y mejores prácticas
# - full: SKILL.md + EXAMPLES.md + WORKFLOW.md + REFERENCE.md
skill_level: standard

# Incluir ejemplos en skills
# include_examples: true

# Incluir flujos de trabajo
# include_workflows: true

# Incluir scripts de validación (para nivel full)
# include_validators: false

# ============================================
# SECCIÓN 8: MEJORES PRÁCTICAS PARA SKILLS
# ============================================

# Configuración de mejores prácticas (se aplica automáticamente)
# Estas opciones siguen las recomendaciones de:
# https://platform.claude.com/docs/es/agents-and-tools/agent-skills/best-practices

SKILL_BEST_PRACTICES:
  # Formato de nombre: forma de gerundio (verb-ing)
  # Ejemplo: processing-pdfs, analyzing-spreadsheets
  name_format: gerundio

  # Estilo de descripción: tercera persona + cuándo usar
  # ✅ Correcto: "Procesa archivos PDF..."
  # ❌ Incorrecto: "Puedo ayudarte a..."
  description_style: tercera_persona

  # Longitud máxima de SKILL.md (líneas)
  # Recomendado: < 500 líneas para rendimiento óptimo
  max_lines: 500

  # Usar divulgación progresiva
  # Crear archivos separados para contenido detallado
  # - REFERENCE.md: Documentación de API
  # - EXAMPLES.md: Casos de uso detallados
  # - WORKFLOW.md: Procesos paso a paso
  use_progressive_disclosure: true

  # Incluir ejemplos entrada/salida
  include_examples: true

  # Incluir flujos de trabajo con checklist
  include_workflows: true

  # Usar patrón plan-validar-ejecutar para operaciones complejas
  use_validation_loops: true

  # Terminología consistente
  # Define términos y úsalos consistentemente
  consistent_terminology: true

  # Evitar información sensible al tiempo
  # En su lugar, usar sección "patrones antiguos"
  avoid_time_sensitive_info: true

# ============================================
# SECCIÓN 9: CONFIGURACIÓN AVANZADA
# ============================================

# Modelo principal
# model: anthropic/claude-sonnet-4-5

# Modelo rápido para tareas simples
# small_model: anthropic/claude-haiku-4-5

# Tema de OpenCode
# theme: opencode

# Actualización automática
# autoupdate: true

# Agente por defecto
# default_agent: build

# ============================================
# SECCIÓN 10: FORMATEADORES
# ============================================

# Formatters (se configuran automáticamente según el lenguaje)
# formatter:
#   prettier:
#   black:
#   isort:

# ============================================
# SECCIÓN 11: WATCHER
# ============================================

# Patrones a ignorar en búsquedas
# watcher:
#   ignore:
#     - node_modules/**
#     - dist/**
#     - .git/**

# ============================================
# SECCIÓN 12: COMPACTACIÓN
# ============================================

# Compactación de contexto
# compaction:
#   auto: true
#   prune: true
