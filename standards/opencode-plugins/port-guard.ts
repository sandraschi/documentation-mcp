import { type Plugin } from "@opencode-ai/plugin"

const FORBIDDEN = new Set([3000, 5000, 5173, 5174, 5175, 8000, 8080])
const PORT_PATTERNS: RegExp[] = [
  /--port[=\s]+(\d+)/gi,
  /-p\s+(\d+)/gi,
  /\$env:(\w*PORT\w*)\s*=\s*['"]?(\d+)['"]?/gi,
  /:\/\/(?:localhost|127\.0\.0\.1|0\.0\.0\.0):(\d+)/gi,
]

export const PortGuard: Plugin = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool !== "bash") return

      const cmd = output.args.command as string
      if (!cmd) return

      for (const pattern of PORT_PATTERNS) {
        for (const m of cmd.matchAll(pattern)) {
          const port = parseInt(m[m.length - 1], 10) // last capture group is the port
          if (FORBIDDEN.has(port)) {
            throw new Error(
              `Forbidden port ${port} in bash call:\n\n` +
                `  Command: ${cmd.split("\n")[0]}\n\n` +
                `Ports 3000, 5000, 5173, 8000, 8080 are prohibited.\n` +
                `Use a fleet port from 10700-11000. Check WEBAPP_PORTS.md\n` +
                `for your project's allocated ports.`
            )
          }
        }
      }
    },
  }
}
