"""Validation utilities for OpenCode configuration."""

import json
from pathlib import Path
from typing import Optional


class ConfigValidator:
    """Validates OpenCode configuration files."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_opencode_json(self, content: str) -> bool:
        """Validate opencode.json content."""
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False
        
        # Check required fields
        if "$schema" not in data:
            self.warnings.append("Missing $schema field")
        
        if "model" not in data:
            self.errors.append("Missing required field: model")
        
        if "permission" not in data:
            self.warnings.append("Missing permission configuration")
        else:
            self._validate_permissions(data["permission"])
        
        # Validate MCP servers
        if "mcp" in data:
            self._validate_mcp_servers(data["mcp"])
        
        # Validate plugins
        if "plugin" in data:
            if not isinstance(data["plugin"], list):
                self.errors.append("plugin must be an array")
        
        return len(self.errors) == 0
    
    def _validate_permissions(self, permissions: dict):
        """Validate permission configuration."""
        valid_levels = {"allow", "ask", "deny"}
        
        for key in ["edit", "bash", "webfetch"]:
            if key in permissions:
                if permissions[key] not in valid_levels:
                    self.errors.append(f"Invalid permission level for {key}: {permissions[key]}")
    
    def _validate_mcp_servers(self, mcp_servers: dict):
        """Validate MCP server configuration."""
        for name, config in mcp_servers.items():
            if isinstance(config, dict):
                if config.get("type") == "remote":
                    if "url" not in config:
                        self.errors.append(f"MCP server {name}: missing url for remote server")
                elif config.get("type") == "local":
                    if "command" not in config:
                        self.errors.append(f"MCP server {name}: missing command for local server")
            elif isinstance(config, str):
                pass  # Just a URL, that's fine
            else:
                self.warnings.append(f"MCP server {name}: unexpected configuration format")
    
    def validate_agents_md(self, content: str) -> bool:
        """Validate AGENTS.md content."""
        if len(content) < 50:
            self.errors.append("AGENTS.md seems too short")
        
        if "#" not in content:
            self.warnings.append("AGENTS.md has no markdown headers")
        
        return len(self.errors) == 0
    
    def validate_project_structure(self, project_dir: Path) -> dict:
        """Validate project directory structure."""
        issues = []
        
        # Check for package manager files
        has_package_json = (project_dir / "package.json").exists()
        has_requirements = (project_dir / "requirements.txt").exists()
        has_pyproject = (project_dir / "pyproject.toml").exists()
        has_go_mod = (project_dir / "go.mod").exists()
        
        if not any([has_package_json, has_requirements, has_pyproject, has_go_mod]):
            issues.append("No package manager configuration found")
        
        # Check for git
        if not (project_dir / ".git").exists():
            issues.append("Not a git repository")
        
        # Check for OpenCode config
        opencode_json = project_dir / "opencode.json"
        if not opencode_json.exists():
            issues.append("opencode.json not found")
        else:
            try:
                content = opencode_json.read_text()
                self.validate_opencode_json(content)
                issues.extend(self.errors)
            except Exception as e:
                issues.append(f"Could not read opencode.json: {e}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }
    
    def get_errors(self) -> list[str]:
        """Get validation errors."""
        return self.errors
    
    def get_warnings(self) -> list[str]:
        """Get validation warnings."""
        return self.warnings
