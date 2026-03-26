"""Tests for plugins generator."""

import pytest
from pathlib import Path
from opencode_config_generator.generators.plugins import PluginsGenerator
from opencode_config_generator.types import ProjectConfig, Language, ProjectType


class TestPluginsGenerator:
    """Test cases for PluginsGenerator."""

    def test_generate_notification_plugin(self):
        """Test notification plugin generation."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
            local_plugins=["notification"],
            create_plugins=True,
        )
        
        generator = PluginsGenerator()
        result = generator.generate(config, Path("."))
        
        assert len(result) > 0
        assert any("notification" in k for k in result.keys())
        assert "@opencode-ai/plugin" in list(result.values())[0]

    def test_generate_env_protection_plugin(self):
        """Test env-protection plugin generation."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
            local_plugins=["env-protection"],
            create_plugins=True,
        )
        
        generator = PluginsGenerator()
        result = generator.generate(config, Path("."))
        
        assert len(result) > 0

    def test_generate_env_protection_plugin(self):
        """Test env-protection plugin generation."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
            local_plugins=["env-protection"],
            create_plugins=True,
        )
        
        generator = PluginsGenerator()
        result = generator.generate(config, Path("."))
        
        assert len(result) > 0

    def test_generate_custom_tool_plugin(self):
        """Test custom-tool plugin generation."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
            local_plugins=["custom-tool"],
            create_plugins=True,
        )
        
        generator = PluginsGenerator()
        result = generator.generate(config, Path("."))
        
        assert len(result) > 0
        assert "tool.schema" in list(result.values())[0]

    def test_generate_multiple_plugins(self):
        """Test generating multiple plugins."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
            local_plugins=["notification", "custom-tool", "inject-env"],
            create_plugins=True,
        )
        
        generator = PluginsGenerator()
        result = generator.generate(config, Path("."))
        
        assert len(result) > 0
        assert "tool.schema" in list(result.values())[0]

    def test_generate_multiple_plugins(self):
        """Test generating multiple plugins."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
            local_plugins=["notification", "custom-tool", "inject-env"],
            create_plugins=True,
        )
        
        generator = PluginsGenerator()
        result = generator.generate(config, Path("."))
        
        assert len(result) == 3

    def test_get_available_templates(self):
        """Test getting available templates."""
        generator = PluginsGenerator()
        templates = generator.get_available_templates()
        
        assert "notification" in templates
        assert "env-protection" in templates
        assert "custom-tool" in templates

    def test_get_template_description(self):
        """Test getting template descriptions."""
        generator = PluginsGenerator()
        
        desc = generator.get_template_description("notification")
        assert "notification" in desc.lower() or "notification" in desc

    def test_generate_empty_when_no_plugins(self):
        """Test empty result when no plugins selected."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
            local_plugins=[],
        )
        
        generator = PluginsGenerator()
        result = generator.generate(config, ".")
        
        assert len(result) == 0
