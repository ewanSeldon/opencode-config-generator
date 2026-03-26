"""Generator for skills based on awesome-agent-skills and best practices."""

from pathlib import Path
from opencode_config_generator.types import SKILL_CATALOG, SkillDefinition


class SkillGenerator:
    """Generates skill SKILL.md files following Anthropic best practices."""
    
    # Level of detail for skills
    LEVEL_BASIC = "basic"
    LEVEL_STANDARD = "standard"
    LEVEL_FULL = "full"
    
    # Detailed skill templates with best practices
    SKILL_TEMPLATES = {
        "docx": {
            "description": "Crea, edita y analiza documentos Word con control de cambios. Úsalo cuando necesites generar documentación técnica, informes o editar documentos colaborativamente.",
            "name_format": "processing-docx",
            "content": {
                "quickstart": """1. Instala: pip install python-docx
2. Crea documento: Document()
3. Guarda: doc.save('archivo.docx')""",
                "examples": [
                    {"input": "Crear documento con título", "output": "Documento con heading y párrafos"},
                    {"input": "Añadir tabla", "output": "Tabla con datos"},
                    {"input": "Aplicar formato", "output": "Texto con estilos"},
                ]
            }
        },
        "xlsx": {
            "description": "Manipula hojas de cálculo: crea fórmulas, gráficos y transforma datos. Úsalo cuando trabajes con datos tabulares, informes Excel o Necesites generar dashboards.",
            "name_format": "processing-excel",
            "content": {
                "quickstart": """1. Instala: pip install openpyxl
2. Crea workbook: Workbook()
3. Accede a hoja: ws = wb.active
4. Guarda: wb.save('datos.xlsx')""",
                "examples": [
                    {"input": "Crear hoja con datos", "output": "Hoja con celdas vacías"},
                    {"input": "Añadir fórmula", "output": "Celda con =SUM(A1:A10)"},
                    {"input": "Crear gráfico", "output": "Gráfico de barras"},
                ]
            }
        },
        "playwright": {
            "description": "Automatiza pruebas E2E de aplicaciones web, graba flujos de usuario y ejecuta tests en múltiples navegadores. Úsalo para testing automatizado, web scraping o verificación de UI.",
            "name_format": "testing-e2e",
            "content": {
                "quickstart": """1. Instala: npm init playwright@latest
2. Ejecuta tests: npx playwright test
3. Graba flujos: npx playwright codegen""",
                "examples": [
                    {"input": "Test básico de página", "output": "Assertions pasan/fallan"},
                    {"input": "Login automatizado", "output": "Usuario logueado"},
                    {"input": "Screenshot", "output": "Imagen capturada"},
                ]
            }
        },
        "kaggle": {
            "description": "Configura cuenta de Kaggle, descarga datasets, ejecuta notebooks y envía resultados. Úsalo cuando trabajes con competencias de ML, necesites datasets de Kaggle, o quieras ejecutar notebooks en la plataforma.",
            "name_format": "ml-kaggle-integration",
            "content": {
                "quickstart": """1. Instala: pip install kaggle
2. Configura API: ~/.kaggle/kaggle.json
3. Descarga: kaggle datasets download -d dataset/name
4. Ejecuta notebook: kaggle notebooks run notebook_id""",
                "examples": [
                    {"input": "Descargar dataset", "output": "Archivo CSV en directorio"},
                    {"input": "Listar competencias", "output": "Lista de competencias activas"},
                    {"input": "Subir submission", "output": "submission.csv enviado"},
                ]
            }
        },
        "git-pushing": {
            "description": "Automatiza operaciones git: crea commits con mensajes descriptivos, gestiona branches y pull requests. Úsalo para workflow de desarrollo diario, releases o mantenimiento de historial limpio.",
            "name_format": "git-workflow",
            "content": {
                "quickstart": """1. Stage cambios: git add .
2. Commit: git commit -m "tipo: descripción"
3. Push: git push origin main""",
                "examples": [
                    {"input": "Commit convencional", "output": "feat(auth): agregar JWT"},
                    {"input": "Crear branch", "output": "Branch feature/login creada"},
                    {"input": "Merge PR", "output": "Cambios fusionados"},
                ]
            }
        },
        "test-fixing": {
            "description": "Ejecuta suite de tests, analiza fallos y propone correcciones. Úsalo cuando tests fallen en CI, necesitas hacer debug de errores o quieres mejorar coverage.",
            "name_format": "debugging-tests",
            "content": {
                "quickstart": """1. Ejecuta: npm test o pytest
2. Analiza output
3. Identifica causa raíz
4. Propón fix""",
                "examples": [
                    {"input": "Test unitario falla", "output": "Assertion error con mensaje"},
                    {"input": "Integration test falla", "output": "Error de conexión"},
                    {"input": "Coverage bajo", "output": "Porcentaje y líneas no cubiertas"},
                ]
            }
        },
        "csv-summarizer": {
            "description": "Analiza archivos CSV, genera estadísticas descriptivas y crea visualizaciones. Úsalo para exploración de datos, data profiling o generación de insights rápidos.",
            "name_format": "analyzing-csv",
            "content": {
                "quickstart": """1. Carga: pd.read_csv('data.csv')
2. Resume: df.describe()
3. Visualiza: df.plot()""",
                "examples": [
                    {"input": "Resumen estadístico", "output": "Media, mediana, desvío por columna"},
                    {"input": "Valores nulos", "output": "Count de nulls por columna"},
                    {"input": "Distribución", "output": "Histograma de valores"},
                ]
            }
        },
        "aws-skills": {
            "description": "Desarrolla y despliega infraestructura AWS con CDK, configura servicios y aplica mejores prácticas de seguridad. Úsalo para infraestructura como código, despliegues cloud o configuración de servicios AWS.",
            "name_format": "aws-cdk-infrastructure",
            "content": {
                "quickstart": """1. Instala CDK: npm install -g aws-cdk
2. Inicializa: cdk init app --language python
3. Despliega: cdk deploy""",
                "examples": [
                    {"input": "Crear bucket S3", "output": "Bucket creado en AWS"},
                    {"input": "Definir Lambda", "output": "Función desplegada"},
                    {"input": "Configurar VPC", "output": "VPC con subnets"},
                ]
            }
        },
        "safe-encryption": {
            "description": "Implementa cifrado moderno con soporte post-cuántico y autenticación componible. Úsalo cuando necesites cifrado seguro, comunicación agente-a-agente o reemplazo de GPG.",
            "name_format": "security-encryption",
            "content": {
                "quickstart": """1. Instala: pip install cryptography
2. Genera ключ: Fernet.generate_key()
3. Cifra: fernet.encrypt(data)
4. Descifra: fernet.decrypt(data)""",
                "examples": [
                    {"input": "Cifrar mensaje", "output": "Bytes cifrados"},
                    {"input": "Firmar datos", "output": "Signature adjunta"},
                    {"input": "Verificar firma", "output": "True/False"},
                ]
            }
        },
    }

    def generate_all(self, selected_skills: list[str], level: str = "standard") -> dict[str, str]:
        """Generate skill files for selected skills."""
        
        files = {}
        
        for skill_name in selected_skills:
            template = self.SKILL_TEMPLATES.get(skill_name, {})
            
            # Find skill in catalog
            skill_def = None
            for s in SKILL_CATALOG:
                if s.name == skill_name:
                    skill_def = s
                    break
            
            if skill_def:
                # Generate full skill with best practices
                files[f"skills/{skill_name}/SKILL.md"] = self._generate(
                    skill_name, 
                    skill_def.description,
                    template,
                    level
                )
                
                # Generate additional files for full level
                if level == self.LEVEL_FULL:
                    if template:
                        # Generate examples
                        examples_content = self._generate_examples(skill_name, template)
                        files[f"skills/{skill_name}/EXAMPLES.md"] = examples_content
                        
                        # Generate workflow
                        workflow_content = self._generate_workflow(skill_name, template)
                        files[f"skills/{skill_name}/WORKFLOW.md"] = workflow_content
                        
                        # Generate reference
                        reference_content = self._generate_reference(skill_name, template)
                        files[f"skills/{skill_name}/REFERENCE.md"] = reference_content
            else:
                # Custom skill - generate basic template
                files[f"skills/{skill_name}/SKILL.md"] = self._generate_custom(skill_name, level)
        
        return files

    def _generate(self, name: str, description: str, template: dict, level: str) -> str:
        """Generate a skill file following best practices."""
        
        name_format = template.get("name_format", f"{name}-skill")
        content = template.get("content", {})
        quickstart = content.get("quickstart", "Configura y usa esta skill según necesidad")
        
        result = f"""---
name: {name_format}
description: {description}
license: MIT
compatibility: opencode
metadata:
  source: awesome-agent-skills
  category: {template.get('category', 'general')}
  best_practices: true
  level: {level}
---

# {name_format.replace('-', ' ').title()}

## Inicio rápido

```bash
# Instalación/Configuración
{quickstart}
```

## Cuándo usar esta skill

- Cuando trabajes con {name}
- Cuando el usuario mencione {name}
- Para tareas relacionadas con {name}

## Flujo de trabajo básico

1. **Preparar**: Asegúrate de tener las dependencias instaladas
2. **Ejecutar**: Sigue los pasos del inicio rápido
3. **Verificar**: Confirma que el resultado es el esperado
4. **Iterar**: Ajusta según sea necesario

"""
        
        # Add examples for standard/full level
        if level in [self.LEVEL_STANDARD, self.LEVEL_FULL] and content.get("examples"):
            result += self._format_examples_brief(content["examples"])
        
        # Add best practices section
        result += """
## Mejores prácticas

- ✅ Sé conciso: solo incluye información que Claude no tenga
- ✅ Escribe en tercera persona la descripción
- ✅ Usa nombres en forma de gerundio (verb-ing)
- ✅ Incluye ejemplos concretos entrada/salida
- ✅ Proporciona flujos de trabajo claros
- ❌ Evites información sensible al tiempo
- ❌ Evites rutas de estilo Windows (usa / no \\)
- ❌ No asumas que paquetes están instalados

"""
        
        # Add validation workflow for full level
        if level == self.LEVEL_FULL:
            result += """## Patrón de validación

Usa el patrón **plan-validar-ejecutar** para operaciones complejas:

1. **Plan**: Crea un plan estructurado
2. **Valida**: Verifica el plan antes de ejecutar
3. **Ejecuta**: Aplica los cambios
4. **Verifica**: Confirma el resultado

```
Progreso:
- [ ] Paso 1: Analizar
- [ ] Paso 2: Planificar  
- [ ] Paso 3: Validar
- [ ] Paso 4: Ejecutar
- [ ] Paso 5: Verificar
```
"""
        
        # Add customization section
        result += """---

# PERSONALIZAR ESTA SKILL

## Ajustar nombre (forma de gerundio)
# name: {name_format}

## Mejorar descripción (tercera persona + cuándo usar)
# description: Tu descripción personalizada aquí. Úsalo cuando...

## Añadir más ejemplos
# Añade ejemplos concretos en EXAMPLES.md

## Añadir flujos de trabajo detallados
# Documenta en WORKFLOW.md

## Añadir referencia de API
# Incluye en REFERENCE.md
"""
        
        return result

    def _format_examples_brief(self, examples: list) -> str:
        """Format examples in brief format."""
        
        result = "\n## Ejemplos\n\n"
        
        for i, ex in enumerate(examples, 1):
            result += f"**Ejemplo {i}**:\n"
            result += f"- Entrada: {ex.get('input', 'N/A')}\n"
            result += f"- Salida: {ex.get('output', 'N/A')}\n\n"
        
        return result

    def _generate_examples(self, name: str, template: dict) -> str:
        """Generate EXAMPLES.md file."""
        
        content = template.get("content", {})
        examples = content.get("examples", [])
        
        result = f"""# Ejemplos de uso: {name}

## Ejemplos detallados

"""
        
        for i, ex in enumerate(examples, 1):
            result += f"""### Ejemplo {i}

**Entrada**:
```
{ex.get('input', 'N/A')}
```

**Salida esperada**:
```
{ex.get('output', 'N/A')}
```

---
"""
        
        result += """
## Guía de ejemplos

Añade más ejemplos siguiendo este formato.
Cada ejemplo debe incluir:
- Entrada clara y específica
- Salida esperada
- Contexto de uso

## Tips

- Los ejemplos ayudan a Claude a entender el estilo deseado
- Incluye casos edge cuando sea relevante
- Usa ejemplos entrada/salida para mayor claridad
"""
        
        return result

    def _generate_workflow(self, name: str, template: dict) -> str:
        """Generate WORKFLOW.md file."""
        
        result = f"""# Flujos de trabajo: {name}

## Flujo de trabajo principal

Copia esta lista de verificación y rastrea tu progreso:

```
Progreso:
- [ ] Paso 1: Preparar entorno
- [ ] Paso 2: Ejecutar tarea
- [ ] Paso 3: Verificar resultado
- [ ] Paso 4: Documentar cambios
```

### Paso 1: Preparar entorno

1. Verifica dependencias instaladas
2. Configura credenciales si es necesario
3. Prepara archivos de entrada

### Paso 2: Ejecutar tarea

1. Sigue los comandos del inicio rápido
2. Monitorea la ejecución
3. Maneja errores si ocurren

### Paso 3: Verificar resultado

1. Confirma que la salida es correcta
2. Verifica archivos creados
3. Prueba casos edge

### Paso 4: Documentar cambios

1. Registra qué se hizo
2. Guarda configuración si es reusable
3. Comparte con el equipo

---

## Flujos de trabajo adicionales

Añade flujos de trabajo específicos para tu caso de uso.

## Troubleshooting

| Problema | Solución |
|----------|----------|
| Error de dependencias | Verifica instalación: `pip list` o `npm list` |
| Error de permisos | Verifica credenciales y permisos |
| Timeout | Aumenta tiempo de espera o optimiza operación |

## Checklist de calidad

- [ ] Todos los pasos completados
- [ ] Resultado verificado
- [ ] Documentación actualizada
- [ ] Errores documentados para futuro reference
"""
        
        return result

    def _generate_reference(self, name: str, template: dict) -> str:
        """Generate REFERENCE.md file."""
        
        result = f"""# Referencia de API: {name}

## Contenidos

- Configuración
- Métodos principales
- Opciones avanzadas
- Patrones de uso
- Manejo de errores

---

## Configuración

### Instalación

```bash
# Comando de instalación
pip install {name}
# o
npm install {name}
```

### Autenticación

```python
# Ejemplo de autenticación
import {name}
{name}.configure(api_key="tu-api-key")
```

---

## Métodos principales

| Método | Descripción | Ejemplo |
|--------|-------------|---------|
| init | Inicializar | `{name}.init()` |
| run | Ejecutar | `{name}.run(data)` |
| validate | Validar | `{name}.validate(input)` |

---

## Opciones avanzadas

### Configuración avanzada

```python
config = {{
    "timeout": 30,
    "retries": 3,
    "debug": True
}}
```

### Personalización

Documenta opciones de personalización según sea necesario.

---

## Manejo de errores

| Código | Descripción | Acción |
|--------|-------------|--------|
| 400 | Bad Request | Verifica formato de entrada |
| 401 | Unauthorized | Verifica credenciales |
| 500 | Server Error | Reintenta o contacta soporte |

---

## Ver también

- [SKILL.md](../SKILL.md) - Guía principal
- [WORKFLOW.md](../WORKFLOW.md) - Flujos de trabajo
- [EXAMPLES.md](../EXAMPLES.md) - Ejemplos adicionales
"""
        
        return result

    def _generate_custom(self, name: str, level: str) -> str:
        """Generate a custom skill file following best practices."""
        
        name_format = f"custom-{name}"
        
        result = f"""---
name: {name_format}
description: Habilidad personalizada - {name}. Úsalo cuando trabajes con esta tarea personalizada.
license: MIT
compatibility: opencode
metadata:
  source: custom
  category: user-defined
  best_practices: true
  level: {level}
---

# {name}

## Qué hace esta skill

Describe aquí qué hace esta habilidad.

## Cuándo usarla

- Cuando necesites realizar esta tarea
- Para casos de uso específicos de tu proyecto

## Inicio rápido

1. Define el objetivo
2. Prepara los datos de entrada
3. Ejecuta el proceso
4. Verifica el resultado

## Flujo de trabajo

```
Progreso:
- [ ] Paso 1: Analizar
- [ ] Paso 2: Planificar
- [ ] Paso 3: Ejecutar
- [ ] Paso 4: Verificar
```

"""
        
        if level in [self.LEVEL_STANDARD, self.LEVEL_FULL]:
            result += """
## Ejemplos

Añade ejemplos específicos para tu caso de uso.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Error 1 | Causa común | Solución aquí |
"""
        
        result += """
---

# PERSONALIZAR ESTA SKILL

## Ajustar nombre (forma de gerundio)
# name: tu-nombre-skill

## Mejorar descripción (tercera persona + cuándo usar)
# description: Tu descripción. Úsalo cuando...

## Añadir ejemplos
# Edita EXAMPLES.md para añadir casos de uso

## Documentar flujos de trabajo
# Edita WORKFLOW.md para procesos específicos

## Añadir referencia de API
# Edita REFERENCE.md para detalles técnicos
"""
        
        return result

    def get_auto_skills(self, language: str, project_type: str) -> list[str]:
        """Get recommended skills based on language and project type."""
        
        recommended = []
        
        # Default skills for all projects
        default_skills = ["git-pushing", "test-fixing"]
        
        # Skills mapping to language/project
        skills_map = {
            ("python", "data"): ["kaggle", "csv-summarizer", "xlsx"],
            ("python", "api"): ["aws-skills", "safe-encryption"],
            ("python", "web"): ["playwright", "test-fixing"],
            ("python", "security"): ["safe-encryption"],
            ("typescript", "web"): ["playwright"],
            ("typescript", "api"): ["aws-skills"],
            ("swift", "mobile"): [],
        }
        
        # Add specific skills
        key = (language.lower(), project_type.lower())
        if key in skills_map:
            recommended.extend(skills_map[key])
        
        # Add default skills
        recommended.extend(default_skills)
        
        # Remove duplicates
        return list(set(recommended))

    def list_all_skills(self) -> dict[str, list[dict]]:
        """List all available skills by category."""
        
        categories = {}
        
        for skill in SKILL_CATALOG:
            if skill.category not in categories:
                categories[skill.category] = []
            
            categories[skill.category].append({
                "name": skill.name,
                "description": skill.description,
                "languages": skill.languages,
                "project_types": skill.project_types
            })
        
        return categories
