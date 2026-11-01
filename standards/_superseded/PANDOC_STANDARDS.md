---
title: "Pandoc Standards (SOTA 2026)"
category: standards
status: active
audience: mcp-dev
last_updated: 2026-04-20
---

# Pandoc Standards

**Version**: 1.0  
**Status**: MANDATORY (Ingest Ecosystem)  
**Substrate**: Windows (Antigravity Fleet)

## 1. Overview
Pandoc is the mandatory engine for markdown conversion and document ingestion within the Advanced Memory (`adn_inbox`) and documentation pipeline.

## 2. Canonical Configuration
- **Absolute Path**: `C:\Program Files\Pandoc\pandoc.exe`

## 3. Ingest Workflow
The `adn_inbox` tool leverages Pandoc to convert external formats (`.docx`, `.html`, `.pdf`) into high-fidelity Markdown.

### 3.1. Conversion Standards
- **Format**: Always target GitHub Flavored Markdown (`gfm`).
- **Extensions**: Preserve math (`tex_math_dollars`) and tables where possible.

## 4. Usage in Fleet
Scripts and agents MUST use the absolute path to ensure conversion stability:
```powershell
& "C:\Program Files\Pandoc\pandoc.exe" -f docx -t gfm -o report.md original.docx
```

---
👉 [Advanced Memory (ADN)](../integrations/advanced-memory/) | [Documentation Standards](./DOCUMENTATION_STANDARDS.md)
