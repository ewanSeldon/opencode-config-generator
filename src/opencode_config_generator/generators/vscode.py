"""Generator for VS Code settings."""

import json
from pathlib import Path
from ..types import ProjectConfig, Language


class VSCodeGenerator:
    """Generates VS Code settings."""
    
    def generate(self, config: ProjectConfig) -> dict[str, str]:
        """Generate VS Code settings."""
        
        settings = self._get_settings(config)
        
        return {
            ".vscode/settings.json": json.dumps(settings, indent=2),
            ".vscode/extensions.json": json.dumps(self._get_extensions(config), indent=2),
        }
    
    def _get_settings(self, config: ProjectConfig) -> dict:
        """Get settings based on language."""
        
        settings = {
            "files.trimTrailingWhitespace": True,
            "files.insertFinalNewline": True,
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": "explicit",
            },
        }
        
        # Language-specific settings
        if config.language == Language.PYTHON:
            settings.update({
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": False,
                "python.linting.ruffEnabled": True,
                "python.formatting.provider": "black",
                "python.analysis.typeCheckingMode": "basic",
                "[python]": {
                    "editor.defaultFormatter": "ms-python.black",
                },
            })
        elif config.language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            settings.update({
                "typescript.preferences.importModuleSpecifier": "relative",
                "javascript.preferences.importModuleSpecifier": "relative",
                "[typescript]": {
                    "editor.defaultFormatter": "esbenp.prettier-vscode",
                },
                "[javascript]": {
                    "editor.defaultFormatter": "esbenp.prettier-vscode",
                },
            })
        elif config.language == Language.GO:
            settings.update({
                "go.formatTool": "gofmt",
                "go.lintTool": "golangci-lint",
                "go.useLanguageServer": True,
            })
        elif config.language == Language.RUST:
            settings.update({
                "rust-analyzer.checkOnSave.command": "clippy",
            })
        
        return settings
    
    def _get_extensions(self, config: ProjectConfig) -> dict:
        """Get recommended extensions."""
        
        extensions = {
            "recommendations": [],
        }
        
        # Always useful
        extensions["recommendations"].extend([
            "esbenp.prettier-vscode",
            "usernamehw.errorlens",
        ])
        
        # Language-specific
        if config.language == Language.PYTHON:
            extensions["recommendations"].extend([
                "ms-python.python",
                "ms-python.black",
                "charliermarsh.ruff",
            ])
        elif config.language == Language.TYPESCRIPT:
            extensions["recommendations"].extend([
                "dbaeumer.vscode-eslint",
            ])
        elif config.language == Language.GO:
            extensions["recommendations"].extend([
                "golang.go",
            ])
        elif config.language == Language.RUST:
            extensions["recommendations"].extend([
                "rust-lang.rust-analyzer",
            ])
        
        return extensions
