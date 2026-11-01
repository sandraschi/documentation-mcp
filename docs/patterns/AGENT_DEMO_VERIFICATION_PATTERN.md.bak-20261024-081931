# Agent Demo Verification Pattern

**Prove agent-built code actually works -- with artifacts, not trust.**

**Source**: Simon Willison, ["Introducing Showboat and Rodney"](https://simonwillison.net/2026/Feb/10/showboat-and-rodney/) (2026-02-10)

**Last Updated**: 2026-02-11

---

## Problem Statement

Coding agents produce code and claim it works. Tests pass, but:

- Tests only cover what the agent decided to test (scope bias)
- Agents can fabricate or hallucinate tool output in their responses
- Manual QA is slow and doesn't scale across 15+ MCP server repos
- Web UI changes are invisible unless someone opens a browser

We need **verifiable artifacts** that prove agent work is correct, not just self-reported success.

---

## The Pattern: Demo Artifacts + Browser Automation

Two tools solve this:

| Tool | Purpose | Install |
|------|---------|---------|
| **[Showboat](https://github.com/simonw/showboat)** | Agent constructs a Markdown document with real command output and screenshots | `uvx showboat` |
| **[Rodney](https://github.com/simonw/rodney)** | CLI browser automation for multi-turn web sessions (start, open, click, screenshot) | `uvx rodney` |

### How Showboat Works

The agent runs a sequence of CLI commands; Showboat captures real output into Markdown:

```powershell
# Agent constructs a demo document step by step
uvx showboat init demo.md "MCP Tool Verification: calibre_ops"
uvx showboat note demo.md "Testing book_ops with operation=search"
uvx showboat exec demo.md python -c "from calibre_mcp.tools.book_tools import ...; print(result)"
uvx showboat note demo.md "Screenshot of webapp search results:"
uvx showboat image demo.md "uvx rodney screenshot search-results.png"
```

Result: a `demo.md` file with **actual** command output embedded -- not agent-reported output.

### How Rodney Works

For web UI verification, Rodney drives a headless Chrome session:

```powershell
uvx rodney start
uvx rodney open http://localhost:3000/books
uvx rodney js "document.querySelectorAll('.book-card').length"
uvx rodney screenshot books-page.png
uvx rodney click "button.search-submit"
uvx rodney screenshot search-results.png
uvx rodney stop
```

The `--help` output of both tools is designed as a self-contained skill -- agents read it and know everything needed.

---

## Application to Our Ecosystem

### 1. MCP Server Tool Verification

After any MCP tool change, the agent creates a Showboat demo proving the tool works:

```
Agent prompt (append to any feature task):

  "Once implementation is complete, run `uvx showboat --help` then use showboat
   to create a demos/[feature-name].md document that exercises the new/changed
   tools with real invocations and captures their output."
```

**Target repos**: All MCP servers (calibre-mcp, blender-mcp, devices-mcp, ring-mcp, etc.)

### 2. Webapp Screenshot Verification

For repos with web frontends, combine Rodney + Showboat:

```
Agent prompt (for webapp changes):

  "After making the changes, run `uvx rodney --help` and `uvx showboat --help`.
   Start the dev server, then use rodney to navigate to the changed pages and
   capture screenshots. Build a showboat demo document at demos/[feature].md
   showing the pages with screenshots."
```

**Target repos**: calibre-mcp/webapp, devices-mcp/webapp, meta_mcp/web, robotics-mcp/web, mywienerlinien/frontend

### 3. Red/Green TDD Agent Session Opener

Standardize this as the **first instruction** in every agent coding session:

```
"Run existing tests with `uv run pytest -v`. Build using red/green TDD."
```

This serves three purposes:
- Tells the agent tests exist and matter
- Agent reads existing test patterns before writing new ones
- "Red/green TDD" is a well-understood shorthand: write test first, watch it fail, write code to pass

### 4. Anti-Cheat Awareness

Agents will sometimes **edit the Markdown file directly** rather than using Showboat, fabricating command output. Mitigations:

- Use `showboat verify` to re-run all commands and diff against recorded output
- Review demos for suspiciously clean output (no warnings, no paths, no timestamps)
- The `showboat extract` command reverse-engineers CLI commands from a demo for manual replay
- Treat demo files as **append-only** in agent instructions

---

## Prompt Templates

### Template A: MCP Tool Demo (CLI-only servers)

```
After implementing the feature:

1. Run `uvx showboat --help` to learn the tool
2. Create demos/{feature-name}.md using showboat
3. Include:
   - init with descriptive title
   - note explaining what changed
   - exec commands that exercise the new tool(s) with real parameters
   - exec commands showing error handling (invalid input)
4. Run `uvx showboat verify demos/{feature-name}.md` to confirm outputs match
```

### Template B: Webapp Feature Demo (browser required)

```
After implementing the feature:

1. Run `uvx showboat --help` and `uvx rodney --help`
2. Start the dev server (e.g., `cd webapp; .\start.ps1`)
3. Use rodney to:
   - start Chrome
   - open the relevant page(s)
   - interact with the new feature (click, type, js assertions)
   - capture screenshots at each step
   - stop Chrome
4. Build demos/{feature-name}.md using showboat with:
   - init with descriptive title
   - notes explaining each step
   - exec commands for any CLI verification
   - image commands referencing rodney screenshots
5. Verify with `uvx showboat verify demos/{feature-name}.md`
```

### Template C: TDD Session Opener (universal)

```
Run the existing tests with "uv run pytest -v". Build using red/green TDD.
```

Append to the start of any coding agent session. Works in Cursor, Claude Code, Windsurf.

---

## Directory Convention

Each repo that adopts this pattern should have:

```
repo-root/
  demos/
    README.md          # Index of demo documents
    feature-xyz.md     # Showboat-generated demo
    feature-xyz/       # Screenshots and artifacts for that demo
      screenshot-1.png
      screenshot-2.png
```

The `demos/` folder is committed to git. Demo documents serve as:
- **Living documentation** of feature behavior
- **Regression baselines** (re-run with `showboat verify`)
- **Code review evidence** (reviewer sees actual output, not agent claims)

---

## Integration with Existing Patterns

| Existing Pattern | How This Complements It |
|-----------------|------------------------|
| [Development Workflow](../../.cursor/skills/mcp-server-developer/modules/development-workflow.md) | Adds demo verification as step between "tests pass" and "commit" |
| [Docker Hot-Reload](docker-development.md) | Rodney can screenshot running Docker containers |
| [Webapp Integration](webapp-integration-pattern.md) | Rodney verifies the frontend actually renders correctly |
| [Tool Exerciser Scripts](../../.cursor/skills/mcp-server-developer/modules/development-workflow.md#5-tool-exerciser-scripts) | Showboat captures exerciser output as permanent artifacts |

---

## Adoption Checklist

- [ ] Install: `uv tool install showboat rodney`
- [ ] Create `demos/` directory in target repos
- [ ] Add Template C (TDD opener) to agent session practices
- [ ] Use Template A or B for the next feature implementation
- [ ] Review generated demo.md for accuracy
- [ ] Add `demos/*.md` to git tracking
- [ ] Run `showboat verify` periodically to catch drift

---

## References

- Simon Willison: [Showboat](https://github.com/simonw/showboat) -- CLI demo document builder
- Simon Willison: [Rodney](https://github.com/simonw/rodney) -- CLI browser automation
- Simon Willison: [Delivering code that works](https://simonwillison.net/2025/Dec/18/code-proven-to-work/)
- Simon Willison: [StrongDM software factory model](https://simonwillison.net/2026/Feb/7/software-factory/)
- Rod library: [go-rod/rod](https://github.com/go-rod/rod) -- Chrome DevTools Protocol for Go
