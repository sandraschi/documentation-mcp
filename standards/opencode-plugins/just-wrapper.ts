import { type Plugin, tool } from "@opencode-ai/plugin"

const JUST = "C:/Users/sandr/scoop/shims/just.exe"

export const JustWrapper: Plugin = async ({ $ }) => {
  return {
    tool: {
      just: tool({
        description: "Run just recipes from the fleet justfile. Use 'list' to discover available recipes, 'run' to execute one. Runs in the current git worktree root.",
        args: {
          operation: tool.schema
            .enum(["list", "run"])
            .describe("'list' shows available recipes, 'run' executes a recipe"),
          recipe: tool.schema
            .string()
            .optional()
            .describe("Recipe name (required for 'run' operation)"),
          extra_args: tool.schema
            .string()
            .optional()
            .describe("Additional key=value arguments for the recipe (e.g. 'port=10967 mode=dual')"),
        },
        async execute(args, context) {
          const cwd = context.worktree || context.directory

          if (args.operation === "list") {
            try {
              const result = await $`${JUST} --list`.cwd(cwd).nothrow().quiet()
              return result.text() || "(no recipes found or no justfile in this directory)"
            } catch (err: any) {
              return `just --list failed: ${err?.message || err}`
            }
          }

          if (!args.recipe) {
            return "Error: recipe name is required for 'run' operation"
          }

          const extra = args.extra_args ? args.extra_args.split(/\s+/).filter(Boolean) : []

          try {
            const result = await $`${JUST} ${args.recipe} ${extra}`.cwd(cwd).nothrow()
            let output = result.text() || "(no output)"

            if (result.stderr && result.stderr.length > 0) {
              const stderrText = new TextDecoder().decode(result.stderr)
              if (stderrText.trim()) {
                output += `\n[stderr]\n${stderrText.trim()}`
              }
            }
            if (result.exitCode !== 0) {
              output += `\n[exit code: ${result.exitCode}]`
            }
            return output
          } catch (err: any) {
            return `just ${args.recipe} failed: ${err?.message || err}`
          }
        },
      }),
    },
  }
}
