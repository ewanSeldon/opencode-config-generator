"""Parser for Markdown/YAML configuration file."""

import re
import yaml
from pathlib import Path
from typing import Optional
from opencode_config_generator.types import (
    Language, ProjectType, Framework, PackageManager,
    PermissionLevel, AgentMode, AgentConfig, MCPServer, ProjectConfig
)


class ConfigParser:
    """Parse markdown configuration file."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.errors = []
        self.warnings = []
    
    def parse(self) -> Optional[ProjectConfig]:
        """Parse configuration file and return ProjectConfig."""
        
        if not self.file_path.exists():
            self.errors.append(f"Archivo no encontrado: {self.file_path}")
            return None
        
        content = self.file_path.read_text(encoding="utf-8")
        
        # Extract YAML config block
        config_dict = self._extract_yaml(content)
        
        if not config_dict:
            self.errors.append("No se encontró bloque de configuración YAML")
            return None
        
        # Parse each section
        return self._parse_config(config_dict)
    
    def _extract_yaml(self, content: str) -> dict:
        """Extract YAML config from markdown."""
        
        # Look for yaml block between --- markers
        yaml_pattern = r'---\s*\n(.*?)\n---'
        match = re.search(yaml_pattern, content, re.DOTALL)
        
        if match:
            yaml_content = match.group(1)
            try:
                return yaml.safe_load(yaml_content) or {}
            except yaml.YAMLError as e:
                self.errors.append(f"Error parsing YAML: {e}")
                return {}
        
        # Try to parse entire content as yaml (no markdown wrapper)
        try:
            return yaml.safe_load(content) or {}
        except yaml.YAMLError:
            return {}
    
    def _parse_config(self, config: dict) -> Optional[ProjectConfig]:
        """Parse configuration dictionary into ProjectConfig."""
        
        # Section 1: Project basic info
        name = config.get("name", "unnamed-project")
        
        # Language
        lang_str = config.get("language", "typescript").lower()
        try:
            language = Language(lang_str)
        except ValueError:
            language = Language.TYPESCRIPT
            self.warnings.append(f"Lenguaje desconocido '{lang_str}', usando typescript")
        
        # Project type
        type_str = config.get("project_type", "web").lower()
        try:
            project_type = ProjectType(type_str)
        except ValueError:
            project_type = ProjectType.WEB
        
        # Framework
        fw_str = config.get("framework", "").lower()
        framework = None
        if fw_str:
            try:
                framework = Framework(fw_str)
            except ValueError:
                self.warnings.append(f"Framework desconocido '{fw_str}'")
        
        # Package manager
        pm_str = config.get("package_manager", "").lower()
        package_manager = None
        if pm_str:
            try:
                package_manager = PackageManager(pm_str)
            except ValueError:
                pass
        
        # Section 2: Agents
        agents = self._parse_agents(config.get("agents", []))
        
        # Section 3: MCP Servers
        mcp_servers = self._parse_mcps(config.get("mcp", {}))
        
        # Section 4: Skills
        selected_skills = self._parse_skills(config.get("skills", []))
        
        # Section 5: Plugins
        selected_plugins, local_plugins = self._parse_plugins(config.get("plugins", {}))
        
        # Section 6: Permissions
        perm_edit, perm_bash = self._parse_permissions(config.get("permission", {}))
        
        # Section 6: Options
        create_agents = config.get("create_agents", True)
        create_commands = config.get("create_commands", True)
        create_skills = config.get("create_skills", False)
        create_custom_tools = config.get("create_custom_tools", False)
        create_plugins = config.get("create_plugins", False)
        
        # Output directory
        output_dir = config.get("output_dir", f"./{name}/opencode-config")
        
        return ProjectConfig(
            name=name,
            language=language,
            project_type=project_type,
            framework=framework,
            package_manager=package_manager,
            agents=agents,
            mcp_servers=mcp_servers,
            selected_skills=selected_skills,
            selected_plugins=selected_plugins,
            local_plugins=local_plugins,
            permission_edit=perm_edit,
            permission_bash=perm_bash,
            output_dir=output_dir,
            create_agents=create_agents,
            create_commands=create_commands,
            create_skills=create_skills,
            create_custom_tools=create_custom_tools,
            create_plugins=bool(selected_plugins or local_plugins),
        )
    
    def _parse_agents(self, agents_data: list) -> list[AgentConfig]:
        """Parse agents section."""
        agents = []
        
        for agent_data in agents_data:
            if isinstance(agent_data, str):
                # Simple format: just agent name
                name = agent_data
                description = f"Agente {name}"
            elif isinstance(agent_data, dict):
                name = agent_data.get("name", "unnamed-agent")
                description = agent_data.get("description", f"Agente {name}")
            else:
                continue
            
            # Parse mode
            mode_str = agent_data.get("mode", "subagent") if isinstance(agent_data, dict) else "subagent"
            mode = AgentMode.PRIMARY if mode_str == "primary" else AgentMode.SUBAGENT
            
            # Parse model
            model = agent_data.get("model", "anthropic/claude-sonnet-4-5") if isinstance(agent_data, dict) else "anthropic/claude-sonnet-4-5"
            
            # Parse temperature
            try:
                temperature = float(agent_data.get("temperature", 0.3)) if isinstance(agent_data, dict) else 0.3
            except:
                temperature = 0.3
            
            # Parse tools
            tools = []
            if isinstance(agent_data, dict) and "tools" in agent_data:
                tools_str = agent_data["tools"]
                if isinstance(tools_str, list):
                    tools = [str(t) for t in tools_str]
                elif isinstance(tools_str, str):
                    tools = [t.strip() for t in tools_str.split(",")]
            
            # Parse permissions
            perm_edit = PermissionLevel.ALLOW
            perm_bash = PermissionLevel.ALLOW
            if isinstance(agent_data, dict) and "permission" in agent_data:
                perms = agent_data["permission"]
                if isinstance(perms, dict):
                    try:
                        perm_edit = PermissionLevel(perms.get("edit", "allow"))
                    except:
                        perm_edit = PermissionLevel.ALLOW
                    try:
                        perm_bash = PermissionLevel(perms.get("bash", "allow"))
                    except:
                        perm_bash = PermissionLevel.ALLOW
            
            agents.append(AgentConfig(
                name=name,
                description=description,
                mode=mode,
                model=model,
                temperature=temperature,
                tools=tools,
                permission_edit=perm_edit,
                permission_bash=perm_bash,
            ))
        
        return agents
    
    def _parse_mcps(self, mcp_data: dict) -> list[MCPServer]:
        """Parse MCP servers section."""
        servers = []
        
        for name, config in mcp_data.items():
            if isinstance(config, dict):
                server = MCPServer(
                    name=name,
                    description=config.get("description", name),
                    type=config.get("type", "remote"),
                    url=config.get("url"),
                    command=config.get("command"),
                    enabled=True
                )
                servers.append(server)
            elif isinstance(config, str):
                # Just URL
                server = MCPServer(
                    name=name,
                    description=name,
                    type="remote",
                    url=config,
                    enabled=True
                )
                servers.append(server)
        
        return servers
    
    def _parse_skills(self, skills_data) -> list[str]:
        """Parse skills section."""
        skills = []
        
        if isinstance(skills_data, list):
            for s in skills_data:
                if isinstance(s, str):
                    skills.append(s)
                elif isinstance(s, dict):
                    skills.append(s.get("name", ""))
        elif isinstance(skills_data, str):
            skills = [s.strip() for s in skills_data.split(",")]
        
        return [s for s in skills if s]
    
    def _parse_permissions(self, perm_data: dict) -> tuple[PermissionLevel, PermissionLevel]:
        """Parse permissions section."""
        
        try:
            perm_edit = PermissionLevel(perm_data.get("edit", "allow"))
        except:
            perm_edit = PermissionLevel.ALLOW
        
        try:
            perm_bash = PermissionLevel(perm_data.get("bash", "ask"))
        except:
            perm_bash = PermissionLevel.ASK
        
        return perm_edit, perm_bash
    
    def _parse_plugins(self, plugins_data) -> tuple[list[str], list[str]]:
        """Parse plugins section."""
        npm_plugins = []
        local_plugins = []
        
        if isinstance(plugins_data, dict):
            # npm: list of package names
            npm_list = plugins_data.get("npm", [])
            if isinstance(npm_list, list):
                npm_plugins = [str(p) for p in npm_list]
            elif isinstance(npm_list, str):
                npm_plugins = [p.strip() for p in npm_list.split(",")]
            
            # local: list of plugin template names
            local_list = plugins_data.get("local", [])
            if isinstance(local_list, list):
                local_plugins = [str(p) for p in local_list]
            elif isinstance(local_list, str):
                local_plugins = [p.strip() for p in local_list.split(",")]
        elif isinstance(plugins_data, list):
            # Simple format: just plugin names (assumed npm)
            npm_plugins = [str(p) for p in plugins_data]
        
        return npm_plugins, local_plugins
    
    def get_errors(self) -> list[str]:
        """Get parsing errors."""
        return self.errors
    
    def get_warnings(self) -> list[str]:
        """Get parsing warnings."""
        return self.warnings
