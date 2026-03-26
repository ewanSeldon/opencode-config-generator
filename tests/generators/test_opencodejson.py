"""Tests for opencode.json generator."""

import pytest
from opencode_config_generator.generators.opencodejson import OpenCodeJSONGenerator
from opencode_config_generator.types import (
    ProjectConfig,
    Language,
    ProjectType,
    PermissionLevel,
)


class TestOpenCodeJSONGenerator:
    """Test cases for OpenCodeJSONGenerator."""

    def test_generate_basic_config(self):
        """Test basic config generation."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
            project_type=ProjectType.WEB,
        )
        
        generator = OpenCodeJSONGenerator()
        result = generator.generate(config)
        
        assert '"$schema"' in result
        assert '"model"' in result
        assert '"permission"' in result

    def test_generate_with_plugins(self):
        """Test config generation with npm plugins."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
            selected_plugins=["opencode-wakatime", "opencode-firecrawl"],
        )
        
        generator = OpenCodeJSONGenerator()
        result = generator.generate(config)
        
        assert '"plugin"' in result
        assert "opencode-wakatime" in result
        assert "opencode-firecrawl" in result

    def test_generate_with_mcp_servers(self):
        """Test config generation with MCP servers."""
        from opencode_config_generator.types import MCPServer
        
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
            mcp_servers=[
                MCPServer(
                    name="context7",
                    description="Context7",
                    type="remote",
                    url="https://mcp.context7.com/mcp",
                    enabled=True,
                ),
            ],
        )
        
        generator = OpenCodeJSONGenerator()
        result = generator.generate(config)
        
        assert '"mcp"' in result
        assert "context7" in result

    def test_generate_ignore_patterns(self):
        """Test that ignore patterns are generated for different languages."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
        )
        
        generator = OpenCodeJSONGenerator()
        result = generator.generate(config)
        
        assert "node_modules" in result
        assert "__pycache__" in result
        assert ".venv" in result

    def test_generate_formatters_python(self):
        """Test formatters for Python."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
        )
        
        generator = OpenCodeJSONGenerator()
        result = generator.generate(config)
        
        assert '"formatter"' in result
        assert "black" in result
        assert "isort" in result

    def test_generate_formatters_typescript(self):
        """Test formatters for TypeScript."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
        )
        
        generator = OpenCodeJSONGenerator()
        result = generator.generate(config)
        
        assert '"formatter"' in result
        assert "prettier" in result

    def test_permissions_edit_allow(self):
        """Test edit permission set to allow."""
        config = ProjectConfig(
            name="test-project",
            permission_edit=PermissionLevel.ALLOW,
        )
        
        generator = OpenCodeJSONGenerator()
        result = generator.generate(config)
        
        assert '"edit": "allow"' in result

    def test_permissions_bash_deny(self):
        """Test bash permission set to deny."""
        config = ProjectConfig(
            name="test-project",
            permission_bash=PermissionLevel.DENY,
        )
        
        generator = OpenCodeJSONGenerator()
        result = generator.generate(config)
        
        assert '"bash": "deny"' in result
