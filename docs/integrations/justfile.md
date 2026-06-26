# Justfile Integration

The `justfile` is the standard task runner for the **MCP Fleet**. It provides a unified interface for developers and agents to interact with servers, webapps, and security tools.

## Integration Checklist

- [ ] **SOTA Help Menu**: Implement the [SOTA Justfile Standard](../standards/JUSTFILE_STANDARDS.md).
- [ ] **Dependencies**: Include `sync`, `install`, and `install-dev` recipes.
- [ ] **Quality**: Add `lint`, `fmt`, and `typecheck`.
- [ ] **Security**: Provide `check-sec` and `audit-deps`.
- [ ] **Start Stack**: Point to `start.ps1` for full fleet-ready startup.

## Customizing the Help Menu

For specific repositories, the help menu header can be customized to include more metadata (e.g., ports used):

```powershell
Write-Host '{{NAME}} v{{VER}} — SOTA Webapp (10932/10933)' -ForegroundColor Yellow;
```

## Recipe Categories (The Fleet Standard)

| Category | Typical Recipes |
| :--- | :--- |
| **Dev** | `install`, `server`, `webapp`, `start` |
| **Quality** | `lint`, `fmt`, `typecheck` |
| **Security** | `check-sec`, `audit-deps` |
| **Testing** | `test`, `smoke`, `test-e2e` |
| **Models** | `pull-models`, `pull-max` (for Ollama) |
| **Packaging** | `mcpb-pack`, `mcpb-validate` |
| **Housekeeping**| `clean`, `clean-all` |

---
*Maintained by: Antigravity AI (SOTA v12.1)*
*Last updated: April 2026*
