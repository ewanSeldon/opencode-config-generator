"""Generators package."""

from pathlib import Path

from .opencodejson import OpenCodeJSONGenerator
from .agentsmd import AgentsMDGenerator
from .agents import AgentGenerator
from .commands import CommandGenerator
from .skills import SkillGenerator
from .custom_tools import CustomToolGenerator
from .plugins import PluginsGenerator
from .vscode import VSCodeGenerator
from .github import GitHubActionsGenerator
from .docker import DockerGenerator
from .precommit import PreCommitGenerator
from .release import ReleaseGenerator

__all__ = [
    "OpenCodeJSONGenerator",
    "AgentsMDGenerator",
    "AgentGenerator",
    "CommandGenerator",
    "SkillGenerator",
    "CustomToolGenerator",
    "PluginsGenerator",
    "VSCodeGenerator",
    "GitHubActionsGenerator",
    "DockerGenerator",
    "PreCommitGenerator",
    "ReleaseGenerator",
    "ConfigGenerator",
]


class ConfigGenerator:
    """Coordinates all generators."""

    def __init__(self, output_dir: str):
        from pathlib import Path
        self.output_dir = Path(output_dir)
        self.opencodejson_gen = OpenCodeJSONGenerator()
        self.agentsmd_gen = AgentsMDGenerator()
        self.agent_gen = AgentGenerator()
        self.command_gen = CommandGenerator()
        self.skill_gen = SkillGenerator()
        self.tool_gen = CustomToolGenerator()
        self.plugin_gen = PluginsGenerator()
        self.vscode_gen = VSCodeGenerator()
        self.github_gen = GitHubActionsGenerator()
        self.docker_gen = DockerGenerator()
        self.precommit_gen = PreCommitGenerator()
        self.release_gen = ReleaseGenerator()
        from .ignore import IgnoreGenerator
        self.ignore_gen = IgnoreGenerator()

    def generate(self, config):
        """Generate all configuration files."""
        
        generated_files = []

        # Create directory structure
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / ".opencode").mkdir(exist_ok=True)
        (self.output_dir / ".opencode" / "agents").mkdir(exist_ok=True)
        (self.output_dir / ".opencode" / "commands").mkdir(exist_ok=True)
        (self.output_dir / ".opencode" / "skills").mkdir(exist_ok=True)
        (self.output_dir / ".opencode" / "tools").mkdir(exist_ok=True)

        # 1. Generate opencode.json
        opencode_json = self.opencodejson_gen.generate(config)
        opencode_path = self.output_dir / "opencode.json"
        opencode_path.write_text(opencode_json, encoding="utf-8")
        generated_files.append("opencode.json")

        # 2. Generate AGENTS.md
        agents_md = self.agentsmd_gen.generate(config)
        agents_path = self.output_dir / "AGENTS.md"
        agents_path.write_text(agents_md, encoding="utf-8")
        generated_files.append("AGENTS.md")

        # 3. Generate .ignore
        ignore_content = self.ignore_gen.generate(config.language)
        ignore_path = self.output_dir / ".ignore"
        ignore_path.write_text(ignore_content, encoding="utf-8")
        generated_files.append(".ignore")

        # 4. Generate custom agents
        if config.create_agents and config.agents:
            agent_files = self.agent_gen.generate_all(config.agents)
            for file_path, content in agent_files.items():
                full_path = self.output_dir / ".opencode" / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                generated_files.append(f".opencode/{file_path}")

        # 5. Generate commands
        if config.create_commands:
            command_files = self.command_gen.generate_all(config)
            for file_path, content in command_files.items():
                full_path = self.output_dir / ".opencode" / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                generated_files.append(f".opencode/{file_path}")

        # 6. Generate skills
        if config.create_skills and config.selected_skills:
            skill_files = self.skill_gen.generate_all(config.selected_skills)
            for file_path, content in skill_files.items():
                full_path = self.output_dir / ".opencode" / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                generated_files.append(f".opencode/{file_path}")

        # 7. Generate custom tools
        if config.create_custom_tools:
            tool_files = self.tool_gen.generate_all()
            for file_path, content in tool_files.items():
                full_path = self.output_dir / ".opencode" / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                generated_files.append(f".opencode/{file_path}")

        # 8. Generate local plugins
        if config.create_plugins and config.local_plugins:
            (self.output_dir / ".opencode" / "plugins").mkdir(exist_ok=True)
            plugin_files = self.plugin_gen.generate(config, self.output_dir)
            for file_path, content in plugin_files.items():
                full_path = Path(file_path)
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                generated_files.append(str(full_path.relative_to(self.output_dir)))

        # 9. Generate VS Code settings
        if getattr(config, 'create_vscode', False):
            vscode_files = self.vscode_gen.generate(config)
            for file_path, content in vscode_files.items():
                full_path = self.output_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                generated_files.append(file_path)

        # 10. Generate GitHub Actions workflows
        if getattr(config, 'create_github_actions', False):
            github_files = self.github_gen.generate(config)
            for file_path, content in github_files.items():
                full_path = self.output_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                generated_files.append(file_path)

        # 11. Generate Docker files
        if getattr(config, 'create_docker', False):
            docker_files = self.docker_gen.generate(config)
            for file_path, content in docker_files.items():
                full_path = self.output_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                generated_files.append(file_path)

        # 12. Generate pre-commit hooks
        if getattr(config, 'create_precommit', False):
            precommit_files = self.precommit_gen.generate(config)
            for file_path, content in precommit_files.items():
                full_path = self.output_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                generated_files.append(file_path)

        # 13. Generate release automation
        if getattr(config, 'create_release', False):
            release_files = self.release_gen.generate(config)
            for file_path, content in release_files.items():
                full_path = self.output_dir / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content, encoding="utf-8")
                generated_files.append(file_path)

        return generated_files

    def preview(self, config):
        """Preview what would be generated with full details."""
        
        preview = {
            "opencode.json": self.opencodejson_gen.generate(config),
            "AGENTS.md": self.agentsmd_gen.generate(config),
            ".ignore": self.ignore_gen.generate(config.language),
        }
        
        # Add list of all files to be generated
        files_to_generate = []
        
        # Always generated
        files_to_generate.extend(["opencode.json", "AGENTS.md", ".ignore"])
        
        # Conditional files
        if config.create_agents and config.agents:
            files_to_generate.extend([f".opencode/agents/{a.name}.md" for a in config.agents])
        
        if config.create_commands:
            files_to_generate.extend([".opencode/commands/test.md", ".opencode/commands/lint.md"])
        
        if config.create_skills and config.selected_skills:
            for skill in config.selected_skills:
                files_to_generate.append(f".opencode/skills/{skill}/SKILL.md")
        
        if config.create_custom_tools:
            files_to_generate.extend([".opencode/tools/hello.ts", ".opencode/tools/echo.ts"])
        
        if config.create_plugins and config.local_plugins:
            for plugin in config.local_plugins:
                files_to_generate.append(f".opencode/plugins/{plugin}.ts")
        
        if getattr(config, 'create_vscode', False):
            files_to_generate.extend([".vscode/settings.json", ".vscode/extensions.json"])
        
        if getattr(config, 'create_github_actions', False):
            files_to_generate.extend([".github/workflows/ci.yml", ".github/workflows/coverage.yml"])
        
        if getattr(config, 'create_docker', False):
            files_to_generate.extend(["Dockerfile", ".dockerignore"])
        
        if getattr(config, 'create_precommit', False):
            files_to_generate.append(".pre-commit-config.yaml")
        
        if getattr(config, 'create_release', False):
            files_to_generate.extend([".github/workflows/release.yml", ".release-please-config.json"])
        
        preview["files"] = files_to_generate
        preview["config_summary"] = {
            "name": config.name,
            "language": config.language.value,
            "framework": config.framework.value if config.framework else None,
            "agents": len(config.agents),
            "commands": config.create_commands,
            "skills": len(config.selected_skills),
            "plugins": len(config.selected_plugins) + len(config.local_plugins),
        }
        
        return preview
