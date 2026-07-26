# songgeneration-mcp

**Version**: v0.2 — 4 backends, Quick Generate page
**Ports**: 10885 (backend), 10884 (frontend)

Unified AI music generation server. Tries 4 backends in order: Lyria 3 Pro (Vertex AI) → Stable Audio Open 1.0 (diffusers) → MusicGen-small (transformers) → Studio SG2 (local API).

## Backends

| Backend | Quality | Local? | First load |
|---------|---------|--------|------------|
| Lyria 3 Pro | Best | No (Vertex AI) | API call |
| Stable Audio Open | Good (instrumentals) | Yes (diffusers) | ~3GB |
| MusicGen-small | Fair | Yes (transformers) | ~2GB |
| Studio SG2 | Variable | Yes (separate repo) | ~5GB |

## Pages

| Page | Route | What |
|------|-------|------|
| Quick Generate | `/quick` | Text prompt → 4 backends → Load to Deck |
| Generate | `/generate` | Studio-specific: lyrics, voices, stems |
| Listen | `/listen` | Browse generated tracks |
| Settings | `/settings` | Backend configuration |

## Install

```powershell
just install-all          # all 4 backends
uv run uvicorn ... :10885 # serve
```

## Links

- GitHub: https://github.com/sandraschi/songgeneration-mcp
- Docs: `docs/INSTALL.md`, `docs/BACKENDS.md`
