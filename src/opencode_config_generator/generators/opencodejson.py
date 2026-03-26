"""Generator for opencode.json configuration file."""

import json
from pathlib import Path
from typing import Optional
from ..types import ProjectConfig, Language, PermissionLevel


class OpenCodeJSONGenerator:
    """Generates opencode.json configuration file."""

    def generate(self, config: ProjectConfig) -> str:
        """Generate opencode.json content."""
        
        data = {
            "$schema": "https://opencode.ai/config.json",
            "model": "anthropic/claude-sonnet-4-5",
            "theme": "opencode",
            "autoupdate": True,
            "instructions": ["AGENTS.md"],
        }

        # Permissions
        data["permission"] = {
            "edit": config.permission_edit.value,
            "bash": config.permission_bash.value,
            "webfetch": "allow",
            # "websearch": "allow",  # Requiere OPENCODE_ENABLE_EXA=1
            # "lsp": "allow",  # Experimental: OPENCODE_EXPERIMENTAL_LSP_TOOL=true
        }

        # Formatters based on language
        formatters = self._get_formatters(config.language)
        if formatters:
            data["formatter"] = formatters

        # MCP servers
        mcp_servers = self._get_mcp_servers(config)
        if mcp_servers:
            data["mcp"] = mcp_servers

        # Watcher ignore patterns
        data["watcher"] = {
            "ignore": self._get_ignore_patterns(config)
        }

        # Compaction settings
        data["compaction"] = {
            "auto": True,
            "prune": True
        }

        # NPM Plugins
        if config.selected_plugins:
            data["plugin"] = config.selected_plugins

        return json.dumps(data, indent=2, ensure_ascii=False)

    def _get_formatters(self, language: Language) -> dict:
        """Get formatters based on language."""
        
        formatters = {
            Language.PYTHON: {
                "black": {},
                "isort": {}
            },
            Language.TYPESCRIPT: {
                "prettier": {}
            },
            Language.JAVASCRIPT: {
                "prettier": {}
            },
            Language.GO: {
                # Go uses gofmt automatically
            },
            Language.RUST: {
                # Rust uses rustfmt automatically
            },
        }

        return formatters.get(language, {})

    def _get_mcp_servers(self, config: ProjectConfig) -> dict:
        """Get MCP servers configuration."""
        
        mcp = {}
        for server in config.mcp_servers:
            if server.enabled:
                if server.type == "remote":
                    mcp[server.name] = {
                        "type": "remote",
                        "url": server.url
                    }
                elif server.type == "local" and server.command:
                    mcp[server.name] = {
                        "type": "local",
                        "command": server.command
                    }

        return mcp

    def _get_ignore_patterns(self, config: ProjectConfig) -> list[str]:
        """Get ignore patterns based on language."""
        
        base_patterns = [
            "node_modules/**",
            "dist/**",
            "build/**",
            ".git/**",
            "__pycache__/**",
            "*.pyc",
        ]

        if config.language == Language.PYTHON:
            base_patterns.extend([
                ".venv/**",
                "venv/**",
                ".env/**",
            ])
        elif config.language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            base_patterns.extend([
                ".next/**",
                ".nuxt/**",
                ".cache/**",
            ])
        elif config.language == Language.GO:
            base_patterns.extend([
                "vendor/**",
            ])
        elif config.language == Language.RUST:
            base_patterns.extend([
                "target/**",
            ])

        return base_patterns
