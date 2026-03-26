"""Generator for local OpenCode plugins."""

import os
from pathlib import Path
from typing import Optional
from ..types import ProjectConfig


PLUGIN_TEMPLATES = {
    "notification": """import type { Plugin } from "@opencode-ai/plugin"

export const NotificationPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        await $`osascript -e 'display notification "Session completed!" with title "OpenCode"'`
      }
    },
  }
}
""",
    
    "env-protection": """import type { Plugin } from "@opencode-ai/plugin"

export const EnvProtection: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool === "read" && output.args.filePath.includes(".env")) {
        throw new Error("Do not read .env files - use environment variables instead")
      }
    },
  }
}
""",
    
    "inject-env": """import type { Plugin } from "@opencode-ai/plugin"

export const InjectEnvPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    "shell.env": async (input, output) => {
      // Inject environment variables for all shell executions
      output.env.PROJECT_ROOT = input.cwd
      
      // Example: Load from .env.local if exists
      // output.env.NODE_ENV = process.env.NODE_ENV || "development"
    },
  }
}
""",
    
    "custom-tool": """import { type Plugin, tool } from "@opencode-ai/plugin"

export const CustomToolsPlugin: Plugin = async ({ directory, worktree }) => {
  return {
    tool: {
      greet: tool({
        description: "Greets a user by name",
        args: {
          name: tool.schema.string(),
        },
        async execute(args, context) {
          const { directory, worktree } = context
          return `Hello, ${args.name}! Welcome to ${directory}`
        },
      }),
    },
  }
}
""",
    
    "compaction-hook": """import type { Plugin } from "@opencode-ai/plugin"

export const CompactionPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    "experimental.session.compacting": async (input, output) => {
      // Inject custom context into the compaction summary
      output.context.push(`
## Custom Context

Include any state that should persist:
- Current task status
- Important decisions made
- Files being actively worked on
- Blockers or dependencies
`)
    },
  }
}
""",
    
    "session-tracker": """import type { Plugin } from "@opencode-ai/plugin"

interface SessionState {
  filesModified: string[]
  commandsExecuted: number
  startTime: number
}

const sessions = new Map<string, SessionState>()

export const SessionTracker: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    event: async ({ event }) => {
      const sessionId = (event as any).session_id
      
      if (event.type === "session.created" && sessionId) {
        sessions.set(sessionId, {
          filesModified: [],
          commandsExecuted: 0,
          startTime: Date.now(),
        })
      }
      
      if (event.type === "session.deleted" && sessionId) {
        const state = sessions.get(sessionId)
        if (state) {
          const duration = Math.round((Date.now() - state.startTime) / 1000)
          console.log(`Session ${sessionId}: ${state.commandsExecuted} commands, ${state.filesModified.length} files, ${duration}s`)
          sessions.delete(sessionId)
        }
      }
    },
    
    "tool.execute.after": async (input) => {
      if (sessionId) {
        const state = sessions.get(sessionId)
        if (state) {
          state.commandsExecuted++
          if (input.tool === "edit" || input.tool === "write") {
            state.filesModified.push((input.args as any).filePath)
          }
        }
      }
    },
  }
}
""",
    
    "command-logger": """import type { Plugin } from "@opencode-ai/plugin"

export const CommandLogger: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    "tool.execute.after": async (input, output) => {
      // Log all tool executions
      await client.app.log({
        body: {
          service: "command-logger",
          level: "info",
          message: `Tool executed: ${input.tool}`,
          extra: {
            tool: input.tool,
            args: input.args,
            success: !output.error,
          },
        },
      })
    },
  }
}
""",
    
    "file-watcher": """import type { Plugin } from "@opencode-ai/plugin"

export const FileWatcher: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    "file.watcher.updated": async (input) => {
      console.log(`File changed: ${input.path}`)
      
      // Example: Auto-run tests on file changes
      // if (input.path.endsWith('.test.ts')) {
      //   await $`npm test -- --watch`
      // }
    },
  }
}
""",
    
    "permission-handler": """import type { Plugin } from "@opencode-ai/plugin"

export const PermissionHandler: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    "permission.asked": async (input) => {
      // Log permission requests
      console.log(`Permission requested: ${input.permission} for ${input.tool}`)
      
      // Auto-deny dangerous operations
      if (input.tool === "bash" && (input.args.command as string).includes("rm -rf")) {
        return { action: "deny" }
      }
      
      // Auto-allow safe read operations
      if (input.tool === "read" && !input.args.filePath.includes(".")) {
        return { action: "allow" }
      }
      
      // Let user decide for others
      return { action: "ask" }
    },
  }
}
""",
}


class PluginsGenerator:
    """Generates local OpenCode plugins."""

    def generate(self, config: ProjectConfig, output_dir: Path) -> dict[str, str]:
        """Generate plugin files.
        
        Returns dict mapping filename to content.
        """
        generated = {}
        
        if not config.local_plugins:
            return generated
        
        plugins_dir = output_dir / ".opencode" / "plugins"
        plugins_dir.mkdir(parents=True, exist_ok=True)
        
        for plugin_name in config.local_plugins:
            template = PLUGIN_TEMPLATES.get(plugin_name)
            if template:
                filename = f"{plugin_name.replace('-', '_')}.ts"
                generated[str(plugins_dir / filename)] = template
                
                # Create package.json if needed for dependencies
                # This would be handled by a separate generator
        
        return generated

    def get_available_templates(self) -> list[str]:
        """Get list of available plugin templates."""
        return list(PLUGIN_TEMPLATES.keys())

    def get_template_description(self, name: str) -> str:
        """Get description of a template."""
        descriptions = {
            "notification": "Send desktop notifications on session events",
            "env-protection": "Prevent reading .env files for security",
            "inject-env": "Inject environment variables into shell executions",
            "custom-tool": "Create custom tools that OpenCode can use",
            "compaction-hook": "Customize context preservation during compaction",
            "session-tracker": "Track session statistics and commands",
            "command-logger": "Log all tool executions",
            "file-watcher": "React to file changes in the project",
            "permission-handler": "Handle permission requests automatically",
        }
        return descriptions.get(name, "")