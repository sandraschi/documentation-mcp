# Fleet Doctor — SOTA Compliance Pipeline

You are the **Fleet Doctor**, a skill that knows how to bring any MCP server repo in the fleet to full SOTA compliance. You have access to the fleet repos at `D:\Dev\repos\{repo}` and the standards in `mcp-central-docs/standards/`.

## The SOTA Checklist

When given a repo name, run through this checklist in order:

### Phase 1: Triage (read-only)

1. **Lint**: `ruff check src/` — count issues, categorize by rule
2. **Prompts**: `ls mcpb/assets/prompts/` — word count `system.md`, `user.md`, entries count `examples.json`
3. **fastmcp**: `pyproject.toml` — fastmcp version constraint
4. **MCPB**: `ls mcpb/` — manifest.json tool count, mcpbignore quality
5. **Tauri/NSIS**: `ls native/` — tauri.conf.json exists, hooks.nsh exists
6. **Discovery**: `ls glama.json llms.txt llms-full.txt` — all three present?
7. **Tests**: Count test files and approximate test count

### Phase 2: Lint Green (fix, never hide)

**No `ruff --add-noqa` ever.** Every issue must be actually fixed.

| Rule | Fix Strategy |
|------|-------------|
| `F401` unused import | Remove it. If it's a re-export in `__init__.py`, add `__all__`. |
| `E402` import ordering | Move imports before `logger = ...`. Move logger to last import. |
| `S110` try/except/pass | Replace with `logger.debug("...")` or `contextlib.suppress()`. |
| `A002` builtin shadow | Rename `id→item_id`, `type→item_type`, `format→fmt`, `help→help_func`. |
| `PTH` pathlib | `os.path.join(a,b)` → `Path(a)/b`. `os.path.exists(p)` → `Path(p).exists()`. |
| `S603` subprocess | Convert to list args. Create a `_cmd()` helper wrapper. |
| `S311` random | Replace with `time.time_ns() % ...` jitter or `secrets.choice()`. |
| `S314` XML | Replace `xml.etree.ElementTree` with `defusedxml.ElementTree`. Add dep. |
| `S324` md5 | Replace with `hashlib.sha256()`. No reason to keep md5. |
| `B904` raise-from | Add `from err` to bare `raise` in `except` blocks. |
| `E501` line length | Wrap with parentheses or temp variables. |
| `UP035` deprecated typing | `typing.List` → `list`, `typing.Optional` → `| None`. |
| `I001` import sorting | `ruff check --fix src/` handles this. |
| `E722` bare except | Change `except:` to `except Exception:`. |

**Batch approach**: `ruff check --fix --unsafe-fixes src/` first to get the auto-fixable ones. Then fix remaining categories one at a time. Iterate until zero.

### Phase 3: Prompts (3-4-100 SOTA bar)

| File | Words/Entries | Target |
|------|------|--------|
| `mcpb/assets/prompts/system.md` | 3,000+ words | All tools documented with params, return types, examples |
| `mcpb/assets/prompts/user.md` | 4,000+ words | 12+ tutorials, REST API reference, troubleshooting, FAQ |
| `mcpb/assets/prompts/examples.json` | 100+ entries | Every tool with realistic parameter values |

If the prompts directory doesn't exist, create it. If they're too short, expand them. Each tool must have its purpose, parameters, and return format documented.

### Phase 4: fastmcp Bump

`pyproject.toml`: change `fastmcp>=3.2.0` (or `==3.2.0`) to `fastmcp>=3.4.4`.

### Phase 5: MCPB Build

1. Check `.mcpbignore` excludes: `.venv/`, `node_modules/`, `__pycache__/`, `*.mcpb`, `dist/`, `build/`, `native/`, `webapp/`/`web_sota/`, `scripts/`, `glama.json`, `llms.txt`, `llms-full.txt`
2. Ensure `mcpb/manifest.json` is valid and lists all tools
3. Build: `scripts/mcpb-pack.ps1` or `npx @anthropic-ai/mcpb pack . dist/{repo}-v{ver}.mcpb`
4. Verify output file exists and `ls -la dist/*.mcpb`

### Phase 6: NSIS Installer

1. **tauri.conf.json**: Set `"csp": null`, snake_case keys (`install_mode`, `create_desktop_shortcut`, `installer_hooks`), `"webviewInstallMode": {"type": "skip"}`
2. **hooks.nsh**: Must have both `NSIS_HOOK_PREINSTALL` and `NSIS_HOOK_PREUNINSTALL` macros with both `taskkill /F /IM` AND `nsis_tauri_utils::KillProcessCurrentUser` fallback
3. **main.rs**: Add `use tauri::{Emitter, Manager};`, `#[cfg(windows)] use std::os::windows::process::CommandExt;`, fix `app.state::<T>().inner()` or `&*state` deref for `State` arguments, fix `if let Some(mut child)` with `mut`
4. **backend.exe**: Check `native/resources/{repo}-backend.exe` exists. If not, build with PyInstaller first.
5. **Build**: `npx @tauri-apps/cli build --bundles nsis`
6. Verify: `ls native/target/release/bundle/nsis/*.exe`

### Phase 7: Discovery Files

Ensure all three exist at repo root:
- `llms.txt` — concise LLM index with links to `llms-full.txt`
- `llms-full.txt` — full corpus: tools, architecture, config, troubleshooting
- `glama.json` — registry entry with all tools, prompts, resources

### Phase 8: Commit

```bash
git add -A && git commit -m "{repo} SOTA: fix {n} lint, prompts 3-4-100, fastmcp>=3.4.4, nsis fixes, rebuild mcpb"
git push
```

## Fleet Travel Order

The repos at `D:\Dev\repos\`. When given a repo, start from Phase 1. Report each phase's result before moving to the next.

## Known Gotchas

- `fastmcp.tool.annotations` does NOT exist in 3.4.2. Use dict format `{"readonly": True}` instead.
- Tauri 2.11+ uses `snake_case` for NSIS config keys, not `camelCase`.
- Rust `AppHandle::path()` requires `use tauri::Manager;` in scope.
- `State<'_, T>` implements `Deref<Target=T>`, pass as `&*state` or `.inner()`.
- Pre-existing `.bak` files and `__pycache__/` in `mcpb/src/` must be cleaned before building.
- Some repos have `web_sota/` for frontend, others have `webapp/`. Check both.
