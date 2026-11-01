# Guides

Human-readable guides for getting access to outside services and for understanding the names around
them. They are written in plain language (whole sentences, every term explained) for people who are not
specialists. Everything in this folder is part of the central documentation index, so the guides can also
be found through the documentation search tools.

| Guide | What it is for | How fast it ages |
|---|---|---|
| [onboarding-microsoft.md](onboarding-microsoft.md) | Registering your own Microsoft app so a program can sign in to Microsoft services such as OneNote | months |
| [onboarding-google.md](onboarding-google.md) | Three separate Google routes: Docs and Drive sign-in, Gemini keys, and the Agent Platform (formerly Vertex AI) | months |
| [onboarding-model-hubs.md](onboarding-model-hubs.md) | Hugging Face tokens, gated models and the download cache; a short Civitai section | months |
| [onboarding-ai-providers.md](onboarding-ai-providers.md) | API keys and billing for OpenAI, Anthropic and Meta, without model names or prices | weeks |
| [ai-names-explained.md](ai-names-explained.md) | A decoder for AI product names, plus a dated snapshot of who calls what | days to weeks |
| [daw-plugins.md](daw-plugins.md) | VST/VST3/CLAP/AU/AAX, the 20-year plugin ecosystem, the free set we test, and the SoundCraft-vs-Reaper instrument finding | weeks (versions) / years (formats) |
| [docs-sites-explained.md](docs-sites-explained.md) | What a documentation site actually is, why four of our five have dead menus, and what `mcp-central-docs` can borrow from the pandoc article (the index idea, not the tool) | months |

## Keeping them current

Every guide carries three fields in its header: `last_verified` (the day someone last checked it against
its sources), `review_every_days` (how long that check stays valid) and `sources` (the official pages its
claims come from). Run the checker once a week:

```
uv run --no-project python scripts/guide_freshness.py
```

It reports which guides are past their review date, and which source pages have disappeared, moved to a
different place, or changed noticeably since the last run. It cannot judge what a change means; it only
narrows the weekly review to the guides that need one. It writes `reports/guide-freshness-latest.md`
and keeps its memory in `data/cache/guide-freshness-state.json`. Pages that refuse automated reading
(HTTP 403) are listed separately and have to be checked by hand.

After reviewing a guide, record it with:

```
uv run --no-project python scripts/guide_freshness.py --mark-verified guides/<name>.md
```

To also send a note to the AI news inbox (aiwatcher) when something needs attention, add
`--notify-aiwatcher http://127.0.0.1:10946`. If that service is not running the checker carries on.

New guide? Copy the header of an existing one. A guide without these fields is ignored by the checker.
