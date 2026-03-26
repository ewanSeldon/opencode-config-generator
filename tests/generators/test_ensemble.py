"""Tests for multi-agent ensemble generator."""

import pytest
from pathlib import Path
from opencode_config_generator.generators.ensemble import EnsembleGenerator
from opencode_config_generator.types import (
    ProjectConfig, Language, ProjectType,
    MultiAgentConfig, RemoteAgentConfig,
    AgentArchitecture, CoordinationMode
)


class TestEnsembleGenerator:
    """Test cases for EnsembleGenerator."""

    def test_generate_empty_for_local(self):
        """Test that no files are generated for local architecture."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
            multi_agent=MultiAgentConfig(
                architecture=AgentArchitecture.LOCAL
            )
        )
        
        generator = EnsembleGenerator()
        result = generator.generate(config)
        
        assert len(result) == 0

    def test_generate_ensemble_config(self):
        """Test ensemble configuration generation."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
            multi_agent=MultiAgentConfig(
                architecture=AgentArchitecture.REMOTE,
                coordination=CoordinationMode.ENSEMBLE,
                remote_agents=[
                    RemoteAgentConfig(
                        name="docs-agent",
                        ip="192.168.1.5",
                        role="documentation",
                        worktree_branch="docs-agent"
                    ),
                    RemoteAgentConfig(
                        name="test-agent",
                        ip="192.168.1.6",
                        role="testing",
                        worktree_branch="test-agent"
                    ),
                ]
            )
        )
        
        generator = EnsembleGenerator()
        result = generator.generate(config)
        
        assert ".opencode/ensemble.json" in result
        assert "skills/orchestration/SKILL.md" in result
        
        ensemble_config = result[".opencode/ensemble.json"]
        assert "test-project" in ensemble_config
        assert "docs-agent" in ensemble_config
        assert "test-agent" in ensemble_config

    def test_generate_remote_agent_configs(self):
        """Test remote agent configuration generation."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
            multi_agent=MultiAgentConfig(
                architecture=AgentArchitecture.REMOTE,
                remote_agents=[
                    RemoteAgentConfig(
                        name="review-agent",
                        ip="192.168.1.7",
                        role="review",
                        port=8765
                    )
                ]
            )
        )
        
        generator = EnsembleGenerator()
        result = generator.generate(config)
        
        assert "agents/review-agent.md" in result
        assert "192.168.1.7" in result["agents/review-agent.md"]
        assert "review" in result["agents/review-agent.md"]

    def test_generate_orchestration_skill(self):
        """Test orchestration skill generation."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
            multi_agent=MultiAgentConfig(
                architecture=AgentArchitecture.HYBRID,
                coordination=CoordinationMode.ENSEMBLE,
                remote_agents=[
                    RemoteAgentConfig(
                        name="docs-agent",
                        ip="192.168.1.5",
                        role="documentation"
                    ),
                    RemoteAgentConfig(
                        name="test-agent",
                        ip="192.168.1.6",
                        role="testing"
                    ),
                ]
            )
        )
        
        generator = EnsembleGenerator()
        result = generator.generate(config)
        
        skill_content = result["skills/orchestration/SKILL.md"]
        assert "Orchestration" in skill_content
        assert "docs-agent" in skill_content
        assert "test-agent" in skill_content
        assert "192.168.1.5" in skill_content
        assert "Ensemble" in skill_content

    def test_generate_mcp_config(self):
        """Test MCP coordinator configuration."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
            multi_agent=MultiAgentConfig(
                architecture=AgentArchitecture.REMOTE,
                coordination=CoordinationMode.MCP,
                mcp_coordinator_url="http://192.168.1.10:8765/mcp",
                remote_agents=[
                    RemoteAgentConfig(
                        name="worker-agent",
                        ip="192.168.1.11",
                        role="general"
                    )
                ]
            )
        )
        
        generator = EnsembleGenerator()
        result = generator.generate(config)
        
        assert "opencode-multi-agent.json" in result
        assert "coordinator" in result["opencode-multi-agent.json"]
        assert "worker-agent" in result["opencode-multi-agent.json"]

    def test_generate_ssh_config(self):
        """Test SSH configuration generation."""
        config = ProjectConfig(
            name="test-project",
            language=Language.PYTHON,
            multi_agent=MultiAgentConfig(
                architecture=AgentArchitecture.REMOTE,
                coordination=CoordinationMode.SSH,
                remote_agents=[
                    RemoteAgentConfig(
                        name="remote-agent",
                        ip="192.168.1.100",
                        username="ubuntu",
                        role="general"
                    )
                ]
            )
        )
        
        generator = EnsembleGenerator()
        result = generator.generate(config)
        
        assert "ssh-config" in result
        assert "192.168.1.100" in result["ssh-config"]
        assert "ubuntu" in result["ssh-config"]

    def test_validate_connectivity(self):
        """Test connectivity validation."""
        config = ProjectConfig(
            name="test-project",
            multi_agent=MultiAgentConfig(
                remote_agents=[
                    RemoteAgentConfig(
                        name="test-agent",
                        ip="127.0.0.1",
                        port=9999
                    )
                ]
            )
        )
        
        generator = EnsembleGenerator()
        results = generator.validate_connectivity(config.multi_agent.remote_agents)
        
        assert "test-agent" in results
        assert results["test-agent"] == False  # Port not open

    def test_role_prompts(self):
        """Test role-specific prompts are generated correctly."""
        generator = EnsembleGenerator()
        
        docs_prompt = generator._get_role_prompt("documentation")
        assert "documentation" in docs_prompt.lower()
        
        test_prompt = generator._get_role_prompt("testing")
        assert "testing" in test_prompt.lower() or "test" in test_prompt.lower()
        
        review_prompt = generator._get_role_prompt("review")
        assert "review" in review_prompt.lower()
        
        general_prompt = generator._get_role_prompt("general")
        assert "general" in general_prompt.lower()
