# translate-mcp ÔÇö Project Page

**Status**: CONCEPT  
**Date**: 2026-05-29  
**Type**: FastMCP 3.2+ server + webapp  
**Repo**: `sandraschi/translate-mcp` (to be created)  
**Port**: TBD ÔÇö assign in WEBAPP_PORTS.md

---

## The Idea

Translation is a single concept with three distinct surfaces that no existing
tool unifies:

| Pillar | What it does |
|--------|-------------|
| **Text translate** | Natural language A ÔåÆ language B (human languages, including Esperanto, Latin) |
| **Spoken translate** | Text ÔåÆ translated text ÔåÆ TTS audio in target language (via speechops) |
| **Formal language translate** | Language A ÔåÆ language B for formal/programming languages ÔÇö code transpilation as translation |

The formal language pillar is the original differentiator. Framing code
transpilation as "translation" ÔÇö with the same interface, the same provider
abstraction, the same tool surface ÔÇö is conceptually clean and has no direct
competitor doing all three in one server.

---

## Pillar 1 ÔÇö Text Translation

Natural language translation with pluggable backends.

**Providers** (configured as a dict, switchable per request):

| Provider | Quality | Languages | Notes |
|----------|---------|-----------|-------|
| DeepL | Best for European languages | 30+ | Free tier available; best FrenchÔåÆEnglish |
| Google Translate | Broadest coverage | 130+ | Good fallback |
| Ollama (local LLM) | Good for common pairs | Model-dependent | Private, offline, no API cost |
| Gemini | Strong prosody-aware output | Major languages | Best for spoken translate pipeline |

**Special language support:**
- **Esperanto** ÔÇö Google + local LLM both handle well; language code `eo`
- **Latin** ÔÇö no commercial provider; local LLM (Mistral/Llama) with classical
  pronunciation prompt; reconstructed classical or ecclesiastical pronunciation
  selectable
- **Old/Middle languages** ÔÇö Middle English, Old French, etc. via local LLM

**MCP tools:**

```
translate(operation="text", text="...", source="fr", target="en", provider="deepl")
translate(operation="detect", text="...")  ÔåÆ detected language + confidence
translate(operation="list_providers")
translate(operation="list_languages", provider="deepl")
```

---

## Pillar 2 ÔÇö Spoken Translation

Pipeline: source text ÔåÆ translate ÔåÆ TTS in target language ÔåÆ audio stream.

Integrates with **speechops** (already on fleet) for the TTS step.
Gemini TTS provider recommended for natural prosody in translated output.

```
translate(operation="spoken", text="...", source="fr", target="de",
          voice="gemini-default", speed=1.0)
  ÔåÆ audio/mpeg stream
```

**CalFolio integration**: "Listen in [language]" button on any book ÔÇö
calibreops extracts chapter ÔåÆ translate-mcp translates ÔåÆ speechops speaks.
Enables reading Halter in English audio, or any book in Esperanto or Latin
for the adventurous.

**Fleet use case**: speechops `text_to_dialogue` + translate-mcp for
multilingual TTS pipelines in any MCP-connected app.

---

## Pillar 3 ÔÇö Formal Language Translation

Code and formal language transpilation as a first-class translation operation.
Same interface, same provider abstraction (LLM backend), same tool surface.

**Why this framing is original**: every existing code converter is a standalone
tool or a raw LLM prompt. Presenting it as "translation" with language pairs,
source/target semantics, and provider selection is new.

**Language pairs (non-exhaustive):**

| Source | Target | Fleet relevance |
|--------|--------|----------------|
| Bash | PowerShell | **High** ÔÇö mixed Linux/Windows fleet daily need |
| PowerShell | Bash | **High** ÔÇö same |
| AutoLISP | ECMAScript | CAD scripting modernisation |
| Python | Rust | Performance migration |
| MySQL SQL | PostgreSQL SQL | DB dialect conversion |
| PostgreSQL SQL | SQLite | Embedded migration |
| Makefile | Justfile | **Fleet** ÔÇö standardising on just |
| Regex | Human description | Universal developer need |
| Human description | Regex | Reverse ÔÇö "give me a regex that matches..." |
| JSON | YAML | Config format normalisation |
| YAML | TOML | Same |
| GLSL | HLSL | Shader language cross-platform |
| Old BASIC | Python | Legacy rescue |
| MCP schema | OpenAPI spec | Fleet tooling |
| JavaScript | TypeScript | Type annotation |
| Python 2 | Python 3 | Legacy migration |

**MCP tools:**

```
translate(operation="formal", source_lang="bash", target_lang="powershell",
          code="for f in *.txt; do echo $f; done")
  ÔåÆ { translated: "Get-ChildItem *.txt | ForEach-Object { $_.Name }", notes: "..." }

translate(operation="list_formal_pairs")  ÔåÆ supported language pairs
translate(operation="explain", lang="regex", code="^[a-z]+$")
  ÔåÆ human description of what the formal expression does

translate(operation="formal", source_lang="human", target_lang="regex",
          code="matches a valid EU IBAN with country-specific length rules")
  ÔåÆ {
      regex: "^([A-Z]{2})(\\d{2})([A-Z0-9]{4})(\\d{7,28})$",  # with per-country validation note
      explanation: "matches country code + check digits + BBAN; length varies by country",
      test_cases: {
          valid: ["DE89370400440532013000", "GB29NWBK60161331926819"],
          invalid: ["DE00370400440532013000", "NOTANIBAN"]
      }
    }

The **human ÔåÆ regex direction is the primary use case** ÔÇö only dedicated
neckbeards can spin up a correct regex from scratch. The response always
includes explanation + test cases so the result can be verified before
it silently eats production data for six months.
```

**Provider**: LLM backend ÔÇö Ollama local model for private/offline use,
Gemini/OpenAI-compatible API for quality. Provider selected per request.

---

## Architecture

```
translate-mcp (FastMCP 3.2+)
    Ôöé
    Ôö£ÔöÇÔöÇ Pillar 1: text_translate
    Ôöé       Ôö£ÔöÇÔöÇ DeepL client
    Ôöé       Ôö£ÔöÇÔöÇ Google Translate client
    Ôöé       ÔööÔöÇÔöÇ Ollama / LLM client (local)
    Ôöé
    Ôö£ÔöÇÔöÇ Pillar 2: spoken_translate
    Ôöé       Ôö£ÔöÇÔöÇ ÔåÆ Pillar 1 (text)
    Ôöé       ÔööÔöÇÔöÇ ÔåÆ speechops MCP (TTS)
    Ôöé
    ÔööÔöÇÔöÇ Pillar 3: formal_translate
            ÔööÔöÇÔöÇ ÔåÆ LLM client (Ollama / Gemini / OpenAI-compatible)

Webapp: translation sandbox UI ÔÇö paste text or code, pick source/target,
        hear result (Pillar 2), see diff (Pillar 3)
```

**Port**: assign in `mcp-central-docs/operations/WEBAPP_PORTS.md`  
**Transport**: stdio (Claude Desktop) + HTTP (webapp, CalFolio)

---

## Portmanteau Tool Design

Single tool `translate` with `operation` enum ÔÇö FastMCP 3.2+ standard:

| operation | Pillar | Description |
|-----------|--------|-------------|
| `text` | 1 | Natural language translation |
| `detect` | 1 | Detect source language |
| `spoken` | 2 | Translate + TTS audio output |
| `formal` | 3 | Code / formal language transpilation |
| `explain` | 3 | Human description of formal expression |
| `list_providers` | ÔÇö | Available backends |
| `list_languages` | 1 | Supported natural languages per provider |
| `list_formal_pairs` | 3 | Supported formal language pairs |

---

## Fleet Integration Points

| Consumer | How it uses translate-mcp |
|----------|--------------------------|
| **CalFolio** | Spoken translate for ad-hoc audiobooks in any language |
| **arxiv-mcp** | Translate Japanese/Chinese papers to English |
| **email-mcp** | Translate incoming/outgoing email |
| **Claude Desktop** | Direct tool use ÔÇö "translate this bash script to PowerShell" |
| **git-github-mcp** | Translate commit messages / PR descriptions |
| Fleet scripts | Bash Ôåö PowerShell conversion for mixed-OS fleet |

---

## Webapp

Translation sandbox page:

```
[ Source language Ôû╝ ] [ paste text or code ]  ÔåÆ  [ Target language Ôû╝ ] [ output ]
                                                  [ Listen (Pillar 2) ]
[ Pillar: Text | Spoken | Formal ]
[ Provider: DeepL | Google | Ollama | Gemini ]
```

The webapp is a useful standalone tool entirely separate from CalFolio ÔÇö
developers use it for the BashÔåÆPowerShell conversion, readers use it for
the Esperanto experiment, everyone uses the regex explainer.

---

## Monetisation / Distribution

Fleet-internal first (no monetisation needed ÔÇö it's a fleet MCP server).  
Could be packaged as a standalone `.mcpb` for Claude Desktop distribution
if the formal language pillar gains traction ÔÇö the BashÔåöPowerShell converter
alone has a real developer audience.

---

## References

- [CALFOLIO.md](../apple/CALFOLIO.md) ÔÇö primary consumer of Pillar 2
- speechops MCP ÔÇö TTS backend for Pillar 2
- `mcp-central-docs/operations/WEBAPP_PORTS.md` ÔÇö assign port
- `mcp-central-docs/standards/AGENT_INSTALL_REFERENCE.md` ÔÇö INSTALL.md standard
- `mcp-central-docs/projects/FLEET_INDEX.md` ÔÇö add entry when repo created
