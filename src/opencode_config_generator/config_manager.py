"""Configuration import/export utilities."""

import json
import yaml
from pathlib import Path
from typing import Optional
from ..types import ProjectConfig, Language, ProjectType, Framework, PackageManager


class ConfigManager:
    """Manage configuration import/export."""
    
    @staticmethod
    def export_to_yaml(config: ProjectConfig, output_path: str) -> bool:
        """Export configuration to YAML file."""
        try:
            data = {
                "name": config.name,
                "language": config.language.value,
                "project_type": config.project_type.value,
                "framework": config.framework.value if config.framework else None,
                "package_manager": config.package_manager.value if config.package_manager else None,
                "create_agents": config.create_agents,
                "create_commands": config.create_commands,
                "create_skills": config.create_skills,
                "create_custom_tools": config.create_custom_tools,
                "create_plugins": config.create_plugins,
                "selected_plugins": config.selected_plugins,
                "local_plugins": config.local_plugins,
                "selected_skills": config.selected_skills,
                "permission": {
                    "edit": config.permission_edit.value,
                    "bash": config.permission_bash.value,
                },
                "mcp": {},
                "agents": [],
            }
            
            # Add MCP servers
            for server in config.mcp_servers:
                data["mcp"][server.name] = {
                    "type": server.type,
                    "url": server.url,
                    "enabled": server.enabled,
                }
            
            # Add agents
            for agent in config.agents:
                data["agents"].append({
                    "name": agent.name,
                    "description": agent.description,
                    "mode": agent.mode.value,
                    "model": agent.model,
                    "tools": agent.tools,
                })
            
            with open(output_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            
            return True
        except Exception as e:
            print(f"Error exporting: {e}")
            return False
    
    @staticmethod
    def export_to_json(config: ProjectConfig, output_path: str) -> bool:
        """Export configuration to JSON file."""
        try:
            data = {
                "name": config.name,
                "language": config.language.value,
                "project_type": config.project_type.value,
                "selected_plugins": config.selected_plugins,
                "local_plugins": config.local_plugins,
                "selected_skills": config.selected_skills,
            }
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting: {e}")
            return False
    
    @staticmethod
    def import_from_file(file_path: str) -> Optional[ProjectConfig]:
        """Import configuration from file."""
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        content = path.read_text(encoding="utf-8")
        
        # Try JSON first
        if path.suffix == ".json":
            return ConfigManager._import_json(content)
        
        # Try YAML
        if path.suffix in [".yaml", ".yml"]:
            return ConfigManager._import_yaml(content)
        
        # Try markdown with YAML block
        if path.suffix == ".md":
            return ConfigManager._import_markdown(content)
        
        return None
    
    @staticmethod
    def _import_json(content: str) -> Optional[ProjectConfig]:
        """Import from JSON."""
        try:
            data = json.loads(content)
            return ConfigManager._parse_dict(data)
        except:
            return None
    
    @staticmethod
    def _import_yaml(content: str) -> Optional[ProjectConfig]:
        """Import from YAML."""
        try:
            data = yaml.safe_load(content)
            return ConfigManager._parse_dict(data)
        except:
            return None
    
    @staticmethod
    def _import_markdown(content: str) -> Optional[ProjectConfig]:
        """Import from markdown with YAML block."""
        import re
        
        # Extract YAML block
        pattern = r"---\s*\n(.*?)\n---"
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            yaml_content = match.group(1)
            return ConfigManager._import_yaml(yaml_content)
        
        return None
    
    @staticmethod
    def _parse_dict(data: dict) -> Optional[ProjectConfig]:
        """Parse dictionary into ProjectConfig."""
        try:
            # Parse language
            lang_str = data.get("language", "typescript")
            language = Language(lang_str.lower())
            
            # Parse project type
            type_str = data.get("project_type", "web")
            project_type = ProjectType(type_str.lower())
            
            # Parse framework
            framework = None
            fw_str = data.get("framework")
            if fw_str:
                try:
                    framework = Framework(fw_str.lower())
                except:
                    pass
            
            # Parse package manager
            package_manager = None
            pm_str = data.get("package_manager")
            if pm_str:
                try:
                    package_manager = PackageManager(pm_str.lower())
                except:
                    pass
            
            return ProjectConfig(
                name=data.get("name", "imported-project"),
                language=language,
                project_type=project_type,
                framework=framework,
                package_manager=package_manager,
                selected_plugins=data.get("selected_plugins", []),
                local_plugins=data.get("local_plugins", []),
                selected_skills=data.get("selected_skills", []),
                create_agents=data.get("create_agents", True),
                create_commands=data.get("create_commands", True),
                create_skills=data.get("create_skills", False),
                create_custom_tools=data.get("create_custom_tools", False),
                create_plugins=data.get("create_plugins", False),
            )
        except Exception as e:
            print(f"Error parsing config: {e}")
            return None
    
    @staticmethod
    def generate_shareable_link(config: ProjectConfig) -> str:
        """Generate a shareable configuration snippet."""
        yaml_content = yaml.dump({
            "name": config.name,
            "language": config.language.value,
            "project_type": config.project_type.value,
            "selected_plugins": config.selected_plugins,
            "local_plugins": config.local_plugins,
            "selected_skills": config.selected_skills,
        }, default_flow_style=True)
        
        return f"""```yaml
{yaml_content}
```"""
