"""Project diagnostic utilities."""

import json
from pathlib import Path
from typing import Optional


class ProjectDiagnostic:
    """Diagnose project issues and improvements."""
    
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.issues = []
        self.warnings = []
        self.suggestions = []
    
    def run_diagnosis(self) -> dict:
        """Run full diagnostic."""
        self._check_structure()
        self._check_git()
        self._check_package_manager()
        self._check_opencode_config()
        self._check_security()
        self._check_performance()
        
        return {
            "valid": len(self.issues) == 0,
            "issues": self.issues,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
            "score": self._calculate_score(),
        }
    
    def _check_structure(self):
        """Check project structure."""
        src_dirs = ["src", "lib", "app", "packages"]
        has_src = any((self.project_dir / d).exists() for d in src_dirs)
        
        if not has_src:
            self.warnings.append("No se encontró directorio src/")
        
        # Check for test directories
        test_dirs = ["tests", "test", "__tests__", "spec"]
        has_test = any((self.project_dir / d).exists() for d in test_dirs)
        
        if not has_test:
            self.warnings.append("No se encontró directorio de tests")
    
    def _check_git(self):
        """Check git configuration."""
        if not (self.project_dir / ".git").exists():
            self.issues.append("No es un repositorio git")
            return
        
        # Check for .gitignore
        if not (self.project_dir / ".gitignore").exists():
            self.warnings.append("Falta archivo .gitignore")
    
    def _check_package_manager(self):
        """Check package manager files."""
        has_package_json = (self.project_dir / "package.json").exists()
        has_requirements = (self.project_dir / "requirements.txt").exists()
        has_pyproject = (self.project_dir / "pyproject.toml").exists()
        has_go_mod = (self.project_dir / "go.mod").exists()
        has_cargo = (self.project_dir / "Cargo.toml").exists()
        
        has_any = has_package_json or has_requirements or has_pyproject or has_go_mod or has_cargo
        
        if not has_any:
            self.issues.append("No se encontró archivo de dependencias (package.json, requirements.txt, pyproject.toml, go.mod, Cargo.toml)")
    
    def _check_opencode_config(self):
        """Check OpenCode configuration."""
        config_file = self.project_dir / "opencode.json"
        
        if not config_file.exists():
            self.warnings.append("No se encontró opencode.json")
            return
        
        try:
            content = config_file.read_text()
            config = json.loads(content)
            
            if "mcp" in config and config["mcp"]:
                for name, mcp in config["mcp"].items():
                    if mcp.get("enabled", False):
                        if mcp.get("type") == "remote" and not mcp.get("url"):
                            self.warnings.append(f"MCP {name} no tiene URL configurada")
            
            if "plugin" in config and config["plugin"]:
                self.suggestions.append(f"Tienes {len(config['plugin'])} plugins configurados")
        
        except json.JSONDecodeError:
            self.issues.append("opencode.json tiene formato inválido")
    
    def _check_security(self):
        """Check for security issues."""
        # Check for .env in git
        if (self.project_dir / ".env").exists():
            if not (self.project_dir / ".gitignore").exists():
                self.issues.append("Archivo .env presente sin .gitignore - riesgo de filtrar secrets")
            else:
                gitignore = (self.project_dir / ".gitignore").read_text()
                if ".env" not in gitignore:
                    self.issues.append(".env debería estar en .gitignore")
        
        # Check for exposed secrets patterns
        patterns = ["password=", "api_key=", "secret=", "token="]
        for pattern in patterns:
            if pattern in (self.project_dir / ".env").read_text() if (self.project_dir / ".env").exists() else "":
                self.issues.append("Posible secreto encontrado en .env")
    
    def _check_performance(self):
        """Check for performance issues."""
        # Check for node_modules in git
        if (self.project_dir / ".git").exists():
            git_modules = self.project_dir / ".git" / "modules"
            if git_modules.exists():
                self.warnings.append("node_modules está siendo trackeado por git (considera usar .gitmodules)")
        
        # Check for large files
        large_files = []
        for pattern in ["*.pyc", "*.pyo", "*.class", "*.o"]:
            large_files.extend(self.project_dir.glob(f"**/{pattern}"))
        
        if large_files:
            self.suggestions.append(f"Se encontraron {len(large_files)} archivos compilados - considera agregarlos a .gitignore")
    
    def _calculate_score(self) -> int:
        """Calculate project health score (0-100)."""
        score = 100
        
        # Deduct points for issues
        score -= len(self.issues) * 15
        
        # Deduct points for warnings
        score -= len(self.warnings) * 5
        
        # Add suggestions count as bonus potential
        max_score = 100
        
        return max(0, min(score, max_score))
    
    def print_report(self):
        """Print diagnostic report."""
        result = self.run_diagnosis()
        
        print(f"\n{'='*50}")
        print(f"  DIAGNÓSTICO DEL PROYECTO")
        print(f"{'='*50}")
        print(f"Puntuación: {result['score']}/100")
        
        if result["issues"]:
            print(f"\n❌ ERRORES ({len(result['issues'])}):")
            for issue in result["issues"]:
                print(f"   • {issue}")
        
        if result["warnings"]:
            print(f"\n⚠️  ADVERTENCIAS ({len(result['warnings'])}):")
            for warning in result["warnings"]:
                print(f"   • {warning}")
        
        if result["suggestions"]:
            print(f"\n💡 SUGERENCIAS ({len(result['suggestions'])}):")
            for suggestion in result["suggestions"]:
                print(f"   • {suggestion}")
        
        if not result["issues"] and not result["warnings"]:
            print("\n✅ ¡Proyecto saludable!")
        
        print(f"{'='*50}\n")
        
        return result
