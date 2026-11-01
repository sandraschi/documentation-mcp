# REA Tools & Automated Binary Decompilation Pipeline

**Source**: [rea.tools](https://rea.tools) · **GitHub**: [github.com/rea-tools](https://github.com/rea-tools) / [reversing-mcp](https://github.com/sandraschi/reversing-mcp)

## Overview
REA (Reverse Engineering Assistant) is an automated binary analysis and decompilation orchestration framework. Instead of requiring a human engineer to manually point IDA Pro or Ghidra at symbols, REA provides headless automation to ingest binaries, run decompilation passes, extract strings and API import tables, and synthesize architectural summaries.

## Fleet Integration (`reversing-mcp`)
In the `sandraschi` fleet, REA tools are encapsulated through `reversing-mcp`:
* **Portmanteau Verbs**: `analyze_binary`, `extract_strings`, `get_hexdump`, `find_functions`, `analyze_pe_file`.
* **Headless Ghidra & Hopper Bridge**: Feeds decompiled C-pseudocode into local models for vulnerability audits and legacy Directmedia file decoding (`decode_dki_file`).
* **Companion Dashboard**: Webapp running on port `10750` for interactive hex inspection, entropy visualization, and decompiled pseudocode exploration.
