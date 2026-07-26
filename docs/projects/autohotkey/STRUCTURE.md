# autohotkey-test - Directory Structure

**Last Updated:** 2025-11-25  
**Source Repo:** `D:\Dev\repos\autohotkey-test`  
**Docs Location:** `D:\Dev\repos\mcp-central-docs\autohotkey\`

---

## Special Case

AutoHotkey documentation is split between:
1. **Source repo** (`autohotkey-test/`) - Actual scripts
2. **Central docs** (`mcp-central-docs/autohotkey/`) - Extensive guides

This is because the migration guides and syntax references are substantial and serve as a reference for multiple projects.

---

## Source Repo Layout (`autohotkey-test/`)

```
autohotkey-test/
├── scripts/                # AHK v2 scripts
├── lib/                    # Shared libraries
├── tests/                  # Test scripts
└── README.md
```

---

## Central Docs Layout (`mcp-central-docs/autohotkey/`)

```
autohotkey/
├── README.md                              # Overview
│
├── Migration Guides
│   ├── Complete_V1_to_V2_Migration_Guide.md
│   ├── AutoHotkey_v2_Syntax_Migration_Guide.md
│   ├── AutoHotkey_v2_Modulo_Migration_Guide.md
│   └── v1_to_v2_conversion_todo.md
│
├── Syntax References
│   ├── AUTO_HOTKEY_V2_CHEAT_SHEET.md
│   ├── AutoHotkey_v2_Syntax_Reference.md
│   ├── AutoHotkey_v2_Common_Incompatibilities.md
│   └── InputBox_v2_Syntax_Rule.md
│
├── Development Guides
│   ├── DEVELOPMENT_GUIDE.md
│   ├── AutoHotkey_v2_Error_Handling_and_Debugging.md
│   ├── AutoHotkey_Debugging_Guide.md
│   ├── AutoHotkey_v2_GUI_Fixes.md
│   └── autohotkey_v2_development.md
│
├── Tools & Reports
│   ├── COMPATIBILITY_SCANNER_README.md
│   ├── comprehensive_lint_report.txt
│   ├── linting_success_report.md
│   ├── remaining_v1_syntax_report.txt
│   └── v1_ui_syntax_issues.txt
│
└── Analysis
    ├── script_assessment.md
    ├── AutoHotkey_Scriptlets_Analysis.md
    ├── Claude_MCP_Scripts_Extended_Analysis.md
    └── Repository_Status_Report.md
```

---

## Why Split?

1. **Volume** - 30+ documentation files
2. **Cross-project reference** - Other repos use AHK
3. **Migration focus** - v1→v2 guides are reference material
4. **Central availability** - Easier to find and maintain

