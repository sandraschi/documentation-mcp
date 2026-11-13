# DocCraft — Assessment (Retired)

**Status:** Retired / Deleted from `D:\Dev\repos` (2026-11-09) · **Grade:** Retired · **Superseded by:** [bookcraft](bookcraft.md) (`v0.5.0`) + `office-mcp`

## Why it was retired

Code audit on 2026-11-09 showed `sandraschi/doccraft` (`418 LOC` Python) was a thin wrapper around `soffice --headless --convert-to` plus 25 lines of `pypdf` merge/text extraction. E-book/PDF/HTML ingestion, text extraction, and format conversion live in **[bookcraft](bookcraft.md)** (`v0.5.0`, 30 tools), and Office COM/OOXML automation lives in `office-mcp`.
