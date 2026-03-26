"""Generator for custom tools (TypeScript)."""

from pathlib import Path


class CustomToolGenerator:
    """Generates custom tool TypeScript files."""

    def generate_all(self) -> dict[str, str]:
        """Generate custom tool files."""
        
        files = {}
        
        # Example: Database tool
        files["tools/database.ts"] = self._generate_database_tool()
        
        # Example: Logger tool
        files["tools/logger.ts"] = self._generate_logger_tool()
        
        return files

    def _generate_database_tool(self) -> str:
        """Generate database tool."""
        
        return '''import { tool } from "@opencode-ai/plugin"

/**
 * Database Query Tool
 * 
 * Execute queries against the project database.
 * 
 * Usage:
 *   - Use for SELECT queries to fetch data
 *   - Use for INSERT/UPDATE/DELETE with care
 *   - Always use parameterized queries
 * 
 * Requirements:
 *   - Set DATABASE_URL environment variable
 *   - Install pg or your preferred DB driver
 */

export default tool({
  description: "Execute a database query",
  args: {
    query: tool.schema.string().describe("SQL query to execute"),
  },
  async execute(args, context) {
    // Your database logic here
    // Example with pg:
    //
    // import pg from 'pg'
    // const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL })
    // const result = await pool.query(args.query)
    // return result.rows
    
    return `Executed: ${args.query}`
  },
})

// ============================================================
// PERSONALIZAR ESTE TOOL
// ============================================================

// Cambiar nombre de la herramienta (nombre del archivo)
// El archivo database.ts crea la herramienta "database"

// Cambiar argumentos
// args: {
//   table: tool.schema.string().describe("Table name"),
//   operation: tool.schema.enum("select", "insert", "update", "delete").describe("Operation"),
//   data: tool.schema.record(tool.schema.string(), tool.schema.any()).describe("Data for insert/update"),
// }

// Cambiar lógica de ejecución
// async execute(args, context) {
//   const { table, operation, data } = args
//   
//   // Validate inputs
//   if (!table) throw new Error("Table name is required")
//   
//   // Execute based on operation
//   switch (operation) {
//     case "select": return await select(table, data)
//     case "insert": return await insert(table, data)
//     // ...
//   }
// }

// Acceder al contexto
// async execute(args, context) {
//   const { directory, worktree, sessionID } = context
//   // Use worktree for project root
//   // Use directory for current working directory
// }

// Usar otras herramientas
// async execute(args, context) {
//   // You can call other tools here if needed
// }

// Añadir validación con Zod
// import { z } from "zod"
// const QuerySchema = z.object({
//   query: z.string().min(1),
//   params: z.array(z.any()).optional(),
// })
'''

    def _generate_logger_tool(self) -> str:
        """Generate logger tool."""
        
        return '''import { tool } from "@opencode-ai/plugin"

/**
 * Logger Tool
 * 
 * Create structured logs for debugging and monitoring.
 * 
 * Usage:
 *   - Log important events
 *   - Track function calls
 *   - Debug issues
 * 
 * Features:
 *   - Multiple log levels
 *   - Structured output
 *   - Timestamp
 */

export default tool({
  description: "Create a structured log entry",
  args: {
    level: tool.schema.enum("debug", "info", "warn", "error").describe("Log level"),
    message: tool.schema.string().describe("Log message"),
    data: tool.schema.record(tool.schema.string(), tool.schema.any()).describe("Additional data"),
  },
  async execute(args, context) {
    const { level, message, data } = args
    const timestamp = new Date().toISOString()
    
    const logEntry = {
      timestamp,
      level,
      message,
      data,
      session: context.sessionID,
    }
    
    // Your logging logic here
    // Example:
    // console.log(JSON.stringify(logEntry))
    // await fetch(process.env.LOG_ENDPOINT, { ... })
    
    return JSON.stringify(logEntry, null, 2)
  },
})

// ============================================================
// PERSONALIZAR ESTE TOOL
// ============================================================

// Cambiar niveles de log
// level: tool.schema.enum("trace", "debug", "info", "warn", "error", "fatal")

// Añadir más argumentos
// args: {
//   source: tool.schema.string().describe("Source of the log"),
//   action: tool.schema.string().describe("Action being logged"),
// }

// Configurar destino del log
// async execute(args, context) {
//   const logEntry = { ...args, timestamp: new Date().toISOString() }
//   
//   // Console
//   console.log(JSON.stringify(logEntry))
//   
//   // File
//   const fs = await import('fs')
//   fs.appendFileSync('logs/app.log', JSON.stringify(logEntry) + '\\n')
//   
//   // HTTP endpoint
//   await fetch('https://your-logging-service.com/logs', {
//     method: 'POST',
//     body: JSON.stringify(logEntry),
//   })
//   
//   return "Logged successfully"
// }

// Integrar con servicios externos
// - Datadog
// - New Relic
// - Loggly
// - Custom HTTP endpoint
'''
