"""Tests for commands generator."""

import pytest
from opencode_config_generator.generators.commands import CommandGenerator
from opencode_config_generator.types import ProjectConfig, Language, ProjectType


class TestCommandGenerator:
    """Test cases for CommandGenerator."""

    def test_generate_all_commands(self):
        """Test generating all default commands."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
        )
        
        generator = CommandGenerator()
        result = generator.generate_all(config)
        
        assert len(result) > 0
        assert "commands/test.md" in result
        assert "commands/lint.md" in result

    def test_generate_test_command(self):
        """Test test command content."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
        )
        
        generator = CommandGenerator()
        result = generator.generate_all(config)
        
        assert "commands/test.md" in result
        content = result["commands/test.md"]
        assert "pytest" in content or "test" in content.lower()

    def test_generate_lint_command(self):
        """Test lint command content."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
        )
        
        generator = CommandGenerator()
        result = generator.generate_all(config)
        
        assert "commands/lint.md" in result
        content = result["commands/lint.md"]
        assert "lint" in content.lower() or "ruff" in content

    def test_command_has_required_sections(self):
        """Test that commands have required sections."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
        )
        
        generator = CommandGenerator()
        result = generator.generate_all(config)
        
        content = result["commands/test.md"]
        assert "##" in content  # Has markdown headers
        assert "```" in content  # Has code blocks

    def test_generate_for_typescript(self):
        """Test commands for TypeScript."""
        config = ProjectConfig(
            name="test-project",
            language=Language.TYPESCRIPT,
        )
        
        generator = CommandGenerator()
        result = generator.generate_all(config)
        
        assert "commands/test.md" in result
        content = result["commands/test.md"]
        assert "npm" in content

    def test_generate_for_go(self):
        """Test commands for Go."""
        config = ProjectConfig(
            name="test-project",
            language=Language.GO,
        )
        
        generator = CommandGenerator()
        result = generator.generate_all(config)
        
        assert "commands/test.md" in result
