import { type Plugin } from "@opencode-ai/plugin"

const RG = "C:\\Users\\sandr\\AppData\\Local\\Microsoft\\WinGet\\Links\\rg.exe"

const RULES: [RegExp, string][] = [
  [/\&\&/, '&& → use ";" or "if ($?) { ... }"'],
  [/\|\|/, '|| → use "if (-not $?) { ... }"'],
  [/(?:^|[\s;|&])grep\s+/, `grep → Select-String -Pattern "<regex>" or ${RG}`],
  [/(?:^|[\s;|&])tail\s+/, "tail → Get-Content <path> -Tail <n>"],
  [/(?:^|[\s;|&])cat\s+/, "cat → Get-Content"],
  [/(?:^|[\s;|&])ls\s+/, "ls → Get-ChildItem"],
  [/(?:^|[\s;|&])rm\s+-[rf]+/, "rm -rf → Remove-Item -Recurse -Force"],
]

export const PowerShellGuard: Plugin = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool !== "bash") return

      const cmd = output.args.command as string
      if (!cmd) return

      const hits: string[] = []
      for (const [pattern, suggestion] of RULES) {
        if (pattern.test(cmd)) {
          hits.push(suggestion)
        }
      }

      if (hits.length > 0) {
        throw new Error(
          `PowerShell SOTA violation(s) in bash call:\n\n` +
            `  Command: ${cmd.split("\n")[0]}\n\n` +
            `  Fix:\n    ${hits.join("\n    ")}`
        )
      }
    },
  }
}
