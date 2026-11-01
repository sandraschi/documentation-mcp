# Crossconnect pattern (fleet-wide)

**Read this before writing a new one-off "integrate with sibling MCP server"
template.** One base, many thin adapters — not one full template per peer.

## Why this exists

By 2026-09-15, three independent speech-mcp integration snippets had
accumulated in this fleet without anyone noticing the overlap:
`templates/chat-page/speech.ts` (Web Speech API only), `templates/speech/`
(Tier 1/Tier 2 fallback, hardcoded `provider=windows`), and an early version
of `templates/speech-crossconnect/` (backend-proxied, provider/voice picker,
no fallback). Each was reasonable in isolation. None of them knew about the
others. That's the failure mode this pattern exists to prevent: every new
peer integration (calibre, plex, discord, aiwatcher, ...) written from
scratch re-derives the same handful of decisions — timeout sizing, error
shape, never-hardcode-what-the-peer-can-tell-you-live — and drifts a little
differently each time.

**The fix:** factor out what's actually common (a peer proxy with a
consistent dialogic shape, sane timeout discipline, and a graceful-
degradation contract) into one base, and keep per-peer adapters small enough
that there's nothing left to drift.

## The base

| File | Vendor to | Purpose |
|---|---|---|
| `templates/crossconnect-base/crossconnect_base.py` | `src/<pkg>/services/crossconnect_base.py` | `CrossconnectPeer` — `get_json`, `post_json`, `raw_get` |
| `templates/crossconnect-base/crossconnect.ts` | `webapp/src/lib/crossconnect.ts` | `crossconnectPeer(apiBase, prefix)` — mirrors the Python contract client-side |

Both files are **peer-agnostic** — vendor them once per repo, unchanged, no
matter how many sibling services you integrate with.

## The contract

1. **Proxy through your own backend. Never call a sibling MCP server
   directly from the browser.** One CORS story, one place for graceful
   degradation. `crossconnect.ts`'s `apiBase` + `prefix` point at YOUR
   backend's routes, not the peer's.
2. **Dialogic `{success, message, data}` everywhere** (matches
   [DIALOGIC_RETURNS.md](../standards/DIALOGIC_RETURNS.md)) for JSON.
   `get_json`/`post_json` give you this automatically; an unreachable peer
   is `success: false` with an actionable message naming the peer, its
   base_url, and the real transport error — never a raw exception surfaced
   to a UI.
3. **Binary responses (audio, images, files) don't go through the dialogic
   shape.** Use `raw_get()` server-side and build your own framework
   Response; use `binaryUrl()` client-side for an `<audio>`/`<img>` tag or a
   manual `fetch().blob()`. Forcing a WAV file through a JSON dict is the
   kind of thing that looks fine right up until someone tries it.
4. **Timeout sizing is a measurement, not a default.** 15s is a reasonable
   starting guess for `get_json`/`post_json`, nothing more — measure the
   actual peer call before shipping. `speech-crossconnect` uses 45s because
   Gemini TTS measured 14-22s for a short excerpt; the generic default would
   have silently misreported a slow-but-successful call as "unreachable."
5. **Never hardcode what the peer can tell you live.** Voice lists, library
   contents, model names, provider status — always call the peer for
   current data. It changes independently of your repo.
6. **Verify before assuming a peer's filter param works.** A nonsense query
   returning the same results as a real one is the tell (found this way
   twice building `speech-crossconnect` — see its README). If a filter is
   genuinely broken server-side, filter client-side here to keep YOUR
   contract honest, and flag the bug upstream via a background task —
   don't reach into the peer's repo yourself unless asked.

## Adding a new peer: the actual steps

1. Vendor `crossconnect_base.py` + `crossconnect.ts` if this repo doesn't
   have them yet (peer-agnostic — one copy serves every peer you add).
2. Write `<peer>_crossconnect.py`: construct one `CrossconnectPeer(name=...,
   base_url=os.getenv("<PEER>_MCP_URL", "http://127.0.0.1:PORT"))`, then a
   handful of functions that call `.get_json()`/`.post_json()`/`.raw_get()`
   against that peer's actual REST endpoints. **Read the peer's live
   `/openapi.json` or docs first — don't guess at paths or params.**
3. Write `<peer>_routes.py`: thin FastAPI routes that call the functions
   from step 2 and return their result (or, for `raw_get`, wrap the bytes in
   a `Response` with the right `media_type`).
4. Write a small frontend client on `crossconnectPeer(apiBase, prefix)` —
   see `speech-crossconnect/speech.ts` for the shape.
5. If there's a UI component, keep it as small and single-purpose as the
   use case actually needs — don't build a generic "crossconnect panel";
   `SpeechControls.tsx`'s provider/voice dropdowns look nothing like a
   library search box, and that's fine.
6. Update this repo's own crossconnect documentation (README, `docs/TOOLS.md`
   equivalent) to say what's wired vs. still just planned — see
   japanophile-mcp's README Crossconnects section for the honesty bar.

## Reference implementation

`patterns/templates/speech-crossconnect/` is the first adapter built on this
base (speech-mcp: TTS with a live provider/voice picker). Its README
documents the three real bugs found while building it — read it before
adding a second peer, several of the lessons (timeout sizing, never-
hardcode-a-voice-list, verify-filters-before-trusting-them) generalize
directly.

`japanophile-mcp`'s own `src/japanophile_mcp/services/crossconnects.py` (the
live, unrefactored production code this template was extracted from) also
has `library_search`/`media_search` adapters for calibre-mcp/plex-mcp — not
yet extracted into templates here, but the next natural candidates once
someone needs them in a second repo.

## Related

- [templates/crossconnect-base/](templates/crossconnect-base/) — the two base files
- [templates/speech-crossconnect/](templates/speech-crossconnect/) — reference adapter
- [speech-mcp-ui-hooks.md](speech-mcp-ui-hooks.md) — the speech-specific "when to use" doc (peer-specific, not the general pattern)
- [VENDS_SOP.md](VENDS_SOP.md) — how `vends` wires a crossconnect template into a repo
- [../standards/DIALOGIC_RETURNS.md](../standards/DIALOGIC_RETURNS.md) — the return-shape standard this pattern implements
