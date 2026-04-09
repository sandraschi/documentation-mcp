# Developer Lingo (Practical)

**Last updated:** 2026-03-23  
**Purpose:** Shared shorthand for day-to-day engineering communication in this fleet.

## Smoke Test

**Meaning (plain):** a very fast check that tells you whether the target is obviously broken.

**Meme phrasing:** “Is it on fire?” / “Does it boot?” / “Does it die instantly?”

### What a smoke test should do

- Start the app/server/CLI without immediate crash.
- Hit one tiny happy-path action (or one read-only MCP tool).
- Confirm minimal health signal (`--help`, `/health`, status tool).
- Finish quickly (seconds, not minutes).

### What a smoke test is not

- Not full correctness validation.
- Not full integration coverage.
- Not performance, security, or regression certification.

### Recommended MCP smoke pattern

1. **CLI parse/start smoke**  
   `uv --directory <repo> run python -m <module> --help`
2. **stdio smoke**  
   Start MCP stdio mode; verify no immediate traceback.
3. **tool smoke**  
   Call one low-risk read tool (`status`, `help`, `list`).
4. **HTTP smoke** (if applicable)  
   `GET /health` and one read endpoint.

### Naming convention

- `smoke_cli_startup`
- `smoke_mcp_stdio_startup`
- `smoke_health_endpoint`
- `smoke_core_read_tool`

Keep smoke tests tiny, deterministic, and cheap to run repeatedly.
