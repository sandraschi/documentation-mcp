import { type Plugin } from "@opencode-ai/plugin"

// Enforces mcp-central-docs CLAUDE.md hard rules at the runtime level, because
// "the agent knows the rule" is not enforcement - see BUG-029 (opencode fleet
// sweep corrupted native/src/backend.rs in 155 repos with zero .bak backups
// and no file-count check, despite both rules being documented).
//
//   Batch Size Limit: no commit / script invocation may touch more than
//   MAX_FILES files without explicit human approval. (No per-session cap since
//   2026-10-09 - the per-commit and sweep checks are what stop blind sweeps.)
//   Batch Mutation Safety: any change touching 3+ files must .bak each file
//   before writing.
//
// Override for a verified, user-approved exception: set FLEET_ALLOW_BATCH=1
// for that one command only (never globally, never for a whole session).

const MAX_FILES = 10

// --- bash sweep heuristic: command looks like it loops + mutates many files ---
const SWEEP_INDICATORS: RegExp[] = [
  /-Recurse/i,
  /Get-ChildItem[^\n|]*\|\s*ForEach-Object/i,
  /for\s+\S+\s+in\s+.+;\s*do/i, // bash for-loop
  /foreach\s*\(/i, // powershell foreach
  /\bfind\b.+-exec\b/i,
]
const WRITE_INDICATORS: RegExp[] = [
  /Set-Content/i,
  /-replace\s/i,
  /sed\s+-i/i,
  /\.WriteAllText\(/i,
  /open\([^)]*['"]w/i, // python open(..., 'w'/'wb')
  /with open\(/i,
]
const BAK_INDICATORS: RegExp[] = [/\.bak/i, /Copy-Item/i, /shutil\.copy/i]

export const BatchMutationGuard: Plugin = async ({ $, directory }) => {
  return {
    "tool.execute.before": async (input, output) => {
      // Early exit if tool is not bash so MCP servers, edit and read tools are never touched
      if (input.tool !== "bash") return

      const allowBatch =
        (typeof Bun !== "undefined" && Boolean(Bun?.env?.FLEET_ALLOW_BATCH)) ||
        (typeof process !== "undefined" && Boolean(process?.env?.FLEET_ALLOW_BATCH))
      if (allowBatch) return

      const cmd = (output?.args?.command as string) || ""
      if (!cmd) return

      // 1. per-commit hard cap - precise, no heuristics
      if (/\bgit\s+commit\b/i.test(cmd)) {
        try {
          const cwd = (output.args?.cwd as string) || directory
          const result = await $`git diff --cached --name-only`.cwd(cwd).nothrow().quiet()
          const staged = result.text().split("\n").filter(Boolean)
          if (staged.length > MAX_FILES) {
            throw new Error(
              `Batch Size Limit violation: this commit stages ${staged.length} files (max ${MAX_FILES}).\n\n` +
                `  Rule: no commit may touch more than ${MAX_FILES} files (mcp-central-docs CLAUDE.md).\n\n` +
                `  Fix: split into multiple commits (git add/commit per group), or if this is a\n` +
                `  verified, user-approved one-time exception, set FLEET_ALLOW_BATCH=1 for this\n` +
                `  command only.`,
            )
          }
        } catch (e) {
          if (e instanceof Error && e.message.startsWith("Batch Size Limit")) throw e
          // not a git repo / git unavailable: don't block on infra errors
        }
      }

      // 2. multi-file mutating sweep heuristic - per script invocation
      const looksLikeSweep =
        SWEEP_INDICATORS.some((r) => r.test(cmd)) && WRITE_INDICATORS.some((r) => r.test(cmd))
      const hasBackup = BAK_INDICATORS.some((r) => r.test(cmd))
      if (looksLikeSweep && !hasBackup) {
        throw new Error(
          `Batch Mutation Safety violation (heuristic): this command looks like it loops\n` +
            `over files and writes to them, with no visible backup step.\n\n` +
            `  Command: ${cmd.split("\n")[0]}\n\n` +
            `  Rule: any change touching 3+ files must create a timestamped .bak copy of\n` +
            `  each file before writing (mcp-central-docs CLAUDE.md; see BUG-029 for what\n` +
            `  happens without this - 155 repos corrupted, zero backups, uncommitted for days).\n\n` +
            `  Fix: back up each file before writing it (e.g. Copy-Item "$f" "$f.$(Get-Date` +
            ` -Format 'yyyyMMdd_HHmmss').bak" / shutil.copy(f, f + '.' + ts + '.bak')), then\n` +
            `  re-run. If this genuinely touches <=2 files or is a false positive, set\n` +
            `  FLEET_ALLOW_BATCH=1 for this command only.`,
        )
      }
    },
  }
}
