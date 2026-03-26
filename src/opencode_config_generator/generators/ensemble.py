"""Generator for multi-agent coordination (opencode-ensemble)."""

import json
from pathlib import Path
from ..types import ProjectConfig, MultiAgentConfig, RemoteAgentConfig, AgentArchitecture, CoordinationMode


class EnsembleGenerator:
    """Generates multi-agent coordination configuration."""
    
    def generate(self, config: ProjectConfig) -> dict[str, str]:
        """Generate multi-agent configuration files."""
        
        generated = {}
        
        if not config.multi_agent or config.multi_agent.architecture == AgentArchitecture.LOCAL:
            return generated
        
        multi_agent = config.multi_agent
        
        # Generate ensemble config
        if multi_agent.coordination == CoordinationMode.ENSEMBLE or multi_agent.ensemble_enabled:
            generated.update(self._generate_ensemble_config(config))
        
        # Generate MCP coordinator config
        if multi_agent.coordination == CoordinationMode.MCP and multi_agent.mcp_coordinator_url:
            generated.update(self._generate_mcp_config(config))
        
        # Generate SSH config
        if multi_agent.coordination == CoordinationMode.SSH:
            generated.update(self._generate_ssh_config(config))
        
        # Generate agent configs
        if multi_agent.remote_agents:
            generated.update(self._generate_remote_agent_configs(config))
        
        # Generate orchestration skill
        generated["skills/orchestration/SKILL.md"] = self._generate_orchestration_skill(config)
        
        return generated
    
    def _generate_ensemble_config(self, config: ProjectConfig) -> dict[str, str]:
        """Generate opencode-ensemble configuration."""
        
        ensemble_config = {
            "team": config.name,
            "members": [],
            "worktree": True,
            "worktreeBase": "main",
            "planApproval": False,
            "timeout": 300,
        }
        
        for i, remote in enumerate(config.multi_agent.remote_agents):
            role = remote.role or "teammate"
            ensemble_config["members"].append({
                "name": remote.name,
                "role": role,
                "systemPrompt": self._get_role_prompt(role),
                "worktree": remote.worktree_branch or f"agent-{i+1}",
                "model": "anthropic/claude-sonnet-4-5",
            })
        
        return {
            ".opencode/ensemble.json": json.dumps(ensemble_config, indent=2),
        }
    
    def _get_role_prompt(self, role: str) -> str:
        """Get system prompt for agent role."""
        
        prompts = {
            "documentation": "You are a documentation specialist. Focus on writing clear, comprehensive documentation. Always use markdown format.",
            "testing": "You are a testing specialist. Focus on writing comprehensive tests, improving coverage, and ensuring code quality.",
            "review": "You are a code review specialist. Focus on code quality, best practices, security, and performance improvements.",
            "code": "You are a coding specialist. Focus on implementing features correctly and efficiently.",
            "general": "You are a general purpose coding assistant.",
        }
        
        return prompts.get(role, prompts["general"])
    
    def _generate_mcp_config(self, config: ProjectConfig) -> dict[str, str]:
        """Generate MCP coordinator configuration."""
        
        mcp_config = {
            "mcp": {
                "coordinator": {
                    "type": "remote",
                    "url": config.multi_agent.mcp_coordinator_url,
                    "enabled": True,
                }
            }
        }
        
        # Add remote agents as MCP tools
        for remote in config.multi_agent.remote_agents:
            mcp_config["mcp"][f"agent-{remote.name}"] = {
                "type": "remote",
                "url": f"http://{remote.ip}:{remote.port}/mcp",
                "enabled": True,
            }
        
        return {
            "opencode-multi-agent.json": json.dumps(mcp_config, indent=2),
        }
    
    def _generate_ssh_config(self, config: ProjectConfig) -> dict[str, str]:
        """Generate SSH configuration for remote agents."""
        
        ssh_config = f"""# SSH Config for multi-agent setup
# Add to ~/.ssh/config

"""
        
        for remote in config.multi_agent.remote_agents:
            ssh_config += f"""Host {remote.name}
    HostName {remote.ip}
    User {remote.username or 'ubuntu'}
    Port {remote.port}
    IdentityFile ~/.ssh/{remote.name}_key
    
"""
        
        return {
            "ssh-config": ssh_config,
        }
    
    def _generate_remote_agent_configs(self, config: ProjectConfig) -> dict[str, str]:
        """Generate individual agent configurations."""
        
        configs = {}
        
        for remote in config.multi_agent.remote_agents:
            agent_config = {
                "name": remote.name,
                "description": f"Remote agent for {remote.role}",
                "mode": "subagent",
                "model": "anthropic/claude-sonnet-4-5",
                "remote": {
                    "ip": remote.ip,
                    "port": remote.port,
                    "enabled": remote.enabled,
                },
                "tools": {
                    "read": True,
                    "write": True,
                    "bash": True,
                },
                "permission": {
                    "edit": "ask",
                    "bash": "ask",
                },
            }
            
            configs[f"agents/{remote.name}.md"] = self._generate_agent_md(remote)
        
        return configs
    
    def _generate_agent_md(self, remote: RemoteAgentConfig) -> str:
        """Generate agent markdown file."""
        
        return f"""---
name: {remote.name}
description: Remote agent for {remote.role}
mode: subagent
model: anthropic/claude-sonnet-4-5
remote:
  ip: {remote.ip}
  port: {remote.port}
tools:
  read: true
  write: true
  bash: true
---

# {remote.name}

Remote agent running on {remote.ip} for {remote.role} tasks.

## Responsibilities
- Execute {remote.role} tasks as delegated
- Report status to coordinating agent
- Use git worktree for isolation

## Connection
- IP: {remote.ip}
- Port: {remote.port}
- Worktree branch: {remote.worktree_branch}

---
# PERSONALIZAR ESTE AGENTE

## Cambiar modelo
# model: anthropic/claude-opus-4-5
# model: openai/gpt-4o

## Ajustar herramientas
# tools:
#   read: true
#   write: true
#   bash: true
#   grep: true
#   glob: true
"""
    
    def _generate_orchestration_skill(self, config: ProjectConfig) -> str:
        """Generate orchestration skill documentation."""
        
        num_agents = len(config.multi_agent.remote_agents)
        coordination_mode = config.multi_agent.coordination.value
        
        check_ensemble = "✓" if coordination_mode == "ensemble" else "✗"
        check_mcp = "✓" if coordination_mode == "mcp" else "✗"
        check_ssh = "✓" if coordination_mode == "ssh" else "✗"
        check_native = "✓" if coordination_mode == "native" else "✗"
        
        agents_list = "\n".join([
            f"- **{a.name}** ({a.ip}) - Rol: {a.role}"
            for a in config.multi_agent.remote_agents
        ])
        
        content = f"""# Orchestration - Multi-Agent Coordination

Úsalo cuando necesites coordinar múltiples agentes IA que trabajan en paralelo en distintas máquinas.

## Quickstart

```bash
# Install ensemble plugin (if using ensemble mode)
npm install opencode-ensemble

# Start coordination
opencode --ensemble
```

## Modo de Coordinación

- **Ensemble** ({check_ensemble}): opencode-ensemble con git worktrees
- **MCP** ({check_mcp}): Via MCP server coordinator
- **SSH** ({check_ssh}): Via SSH commands
- **Native** ({check_native}): OpenCode Task tool

## Agentes Configurados

{num_agents} agente(s) remoto(s) configurado(s):

{agents_list}

## Ejemplos de Uso

### Delegar tarea a agente específico
```
Ask the docs-agent to write API documentation for the auth module.
```

### Delegar a todos los agentes
```
Run tests in parallel: test-agent on unit tests, review-agent on integration tests.
```

### Coordinar flujo de trabajo
```
1. First, have explore-agent analyze the codebase structure
2. Then, spawn build agents to implement the feature
3. Finally, have review-agent verify the implementation
```

## Workflow Recomendado

1. **Exploración** - Un agente analiza el codebase
2. **Implementación** - Múltiples agentes implementan en paralelo
3. **Revisión** - Agente de review verifica
4. **Testing** - Agente de tests ejecuta suite completa

## Configuración de Red

### Puertos requeridos
- OpenCode: 8765 (default)
- Ensemble: 8766

### Variables de entorno
```
OPENCODE_HOST=0.0.0.0
OPENCODE_PORT=8765
ENSEMBLE_ENABLED=1
```

## Notas

- Cada agente opera en su propio worktree/git branch
- El agente principal coordina y agrega resultados
- Comunicación via mensajes o tareas delegadas
"""
        return content
    
    def validate_connectivity(self, remote_agents: list[RemoteAgentConfig]) -> dict[str, bool]:
        """Validate connectivity to remote agents."""
        
        import socket
        
        results = {}
        for agent in remote_agents:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((agent.ip, agent.port))
                sock.close()
                results[agent.name] = result == 0
            except:
                results[agent.name] = False
        
        return results
