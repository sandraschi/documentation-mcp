# Git, GitHub & GitLab Documentation

**Last Updated:** 2025-12-03  
**Status:** CURRENT  
**Contents:** 16+ comprehensive guides (consolidated from multiple repos)

âš ï¸ **Freshness Check**: If reading after Jan 2026, verify GitHub Actions and workflows are still current!

---

## ðŸ“š Documentation Structure

```
git-github/
â”œâ”€â”€ README.md                      # This file
â”‚
â”œâ”€â”€ git/                          # Git fundamentals (4 guides)
â”‚   â”œâ”€â”€ README.md                 # Git docs hub
â”‚   â”œâ”€â”€ fundamentals.md           # Git basics
â”‚   â”œâ”€â”€ worktrees.md              # Multiple branches simultaneously
â”‚   â”œâ”€â”€ history-management.md     # Rebase, bisect, reflog
â”‚   â””â”€â”€ etiquette.md              # Best practices
â”‚
â”œâ”€â”€ github/                       # GitHub guides (from ADN)
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ CI_CD_PRODUCTION_GUIDE.md
â”‚   â”œâ”€â”€ CI_SUCCESS_WORKFLOW_GUIDE.md
â”‚   â”œâ”€â”€ COMPLETE_SETUP_GUIDE.md
â”‚   â”œâ”€â”€ COMPLETE_TYPE_FIX_GUIDE.md
â”‚   â”œâ”€â”€ DEPENDENCY_MANAGEMENT.md
â”‚   â”œâ”€â”€ DOCUMENT_AUDIT_CHECKLIST.md
â”‚   â”œâ”€â”€ GITHUB_ADVANCED_SECURITY_GUIDE.md
â”‚   â”œâ”€â”€ GITHUB_CLI_VS_MCP.md         # â­ Use CLI, not MCP!
â”‚   â”œâ”€â”€ GITHUB_RATE_LIMITING_GUIDE.md
â”‚   â”œâ”€â”€ PRE_COMMIT_HOOKS_GUIDE.md
â”‚   â”œâ”€â”€ RELEASE_CHECKLIST.md
â”‚   â”œâ”€â”€ SECURITY_HARDENING.md
â”‚   â”œâ”€â”€ THE_GITHUB_SAGA.md           # War stories!
â”‚   â”œâ”€â”€ TROUBLESHOOTING.md
â”‚   â””â”€â”€ WORKFLOWS.md
â”‚
â”œâ”€â”€ gitlab/                       # GitLab (to be added)
â”‚   â””â”€â”€ (Coming soon)
â”‚
â”œâ”€â”€ ci-cd/                        # CI/CD best practices
â”‚   â””â”€â”€ (To be organized)
â”‚
â”œâ”€â”€ security/                     # Security guides
â”‚   â””â”€â”€ (To be organized)
â”‚
â”œâ”€â”€ release/                      # Release management
â”‚   â””â”€â”€ (To be organized)
â”‚
â”œâ”€â”€ troubleshooting/              # Common issues
â”‚   â””â”€â”€ (To be organized)
â”‚
â””â”€â”€ advanced/                     # Advanced topics
    â””â”€â”€ (To be organized)
```

---

## ðŸŽ¯ Quick Start

### New to Git/GitHub?
1. Start: `git/fundamentals.md`
2. Then: `github/COMPLETE_SETUP_GUIDE.md`
3. Practice: `github/WORKFLOWS.md`

### Setting Up CI/CD?
1. Read: `github/CI_SUCCESS_WORKFLOW_GUIDE.md` â­
2. Copy: Workflow templates
3. Test: Run locally first
4. Deploy: Push and monitor

### GitHub CLI vs MCP?
1. **READ THIS FIRST**: `github/GITHUB_CLI_VS_MCP.md`
2. **TL;DR**: Use `gh` CLI (50-70% token reduction!)
3. **Why**: Self-documenting, composable, efficient

### Having Issues?
1. Check: `github/TROUBLESHOOTING.md`
2. Review: `github/THE_GITHUB_SAGA.md` (learn from our 6-hour debugging odyssey!)
3. See: `github/GITHUB_RATE_LIMITING_GUIDE.md` (if rate limited)

---

## â­ Top Recommendations

### 1. GitHub CLI > MCP (IMPORTANT!)
**File**: `github/GITHUB_CLI_VS_MCP.md`

**TL;DR**: Use `gh` CLI instead of GitHub MCP for AI workflows
- âœ… 50-70% token reduction
- âœ… Self-documenting (`gh --help`)
- âœ… Full feature access
- âœ… Composable commands

### 2. CI Success Workflow
**File**: `github/CI_SUCCESS_WORKFLOW_GUIDE.md`

**TL;DR**: Never break CI again!
- Pre-push validation
- Auto-fix on failure
- Success rate tracking
- `just safe-push "message"` - Ultimate automation

### 3. Production CI/CD
**File**: `github/CI_CD_PRODUCTION_GUIDE.md`

**TL;DR**: Production-ready GitHub Actions
- 6 job workflow (lint, test, security, build, MCPB, quality gate)
- GLAMA.ai integration
- Automated releases

---

## ðŸ”— Related Documentation

### Prerequisites
- `../anthropic-ecosystem/` - MCP protocol and FastMCP basics
- `../docker/` - Docker and containerization

### Related Topics
- `../monitoring/` - Monitoring stack (includes GitHub Actions monitoring)
- `../patterns/` - Development patterns
- `../projects/` - Project-specific GitHub setups

### Cross-References
- **Claude Desktop config** - `../anthropic-ecosystem/claude-desktop/`
- **MCPB packaging** - Uses GitHub Actions for builds
- **FastMCP updates** - Affects CI/CD workflows

---

## ðŸ“Š Statistics

**Total Documents**: 16 (from advanced-memory-mcp)  
**Status Breakdown**:
- âœ… CURRENT: 16
- âš ï¸ OUTDATED: 0
- ðŸ—„ï¸ ARCHIVED: 0

**Last Freshness Audit**: 2025-12-03  
**Next Review**: 2026-01-03

---

## ðŸ”„ Maintenance

### Update Frequency
- **Git fundamentals**: Yearly (Git is stable)
- **GitHub Actions**: Monthly (frequent updates)
- **CI/CD workflows**: Monthly (tooling changes)
- **Model references**: Weekly (AI timescale!)

### Freshness Checks
```powershell
# Run audit
cd D:\Dev\repos\mcp-central-docs
.\scripts\audit-doc-freshness.ps1

# Check for outdated GitHub Actions
grep -r "actions/.*@v1" docs/git-github/
```

### Ownership
**Primary Maintainer**: Sandra  
**Contributors**: Claude, AI assistants  
**Source**: Consolidated from advanced-memory-mcp, mcp-studio

---

## âš ï¸ Version-Specific Notes

### GitHub Actions
**Current**: Actions v4 (checkout, upload-artifact)  
**Deprecated**: v1, v2 (migrate immediately!)  
**Warning**: Check action versions monthly - GitHub deprecates regularly

### FastMCP Integration
**Current**: FastMCP 3.1.1++  
**Affects**: CI workflows, dependency management, MCPB builds  
**Warning**: If docs mention FastMCP < 3.1.1+, they're OUTDATED

### Security Tools
**Current Versions**:
- Bandit 1.7+
- Safety 3.0+
- Trivy latest
- CodeQL latest

---

## ðŸš€ Quick Commands

```powershell
# Navigate to git-github docs
cd D:\Dev\repos\mcp-central-docs\docs\git-github

# List all guides
ls -Recurse *.md

# Search for specific topic
grep -r "topic" .

# Check freshness
grep -r "Last Updated" . | Select-String "2025"
```

---

## ðŸŽ“ Learning Path

### Beginner
1. `git/fundamentals.md` - Git basics
2. `github/COMPLETE_SETUP_GUIDE.md` - GitHub setup
3. `github/WORKFLOWS.md` - Basic CI/CD

### Intermediate
4. `github/CI_SUCCESS_WORKFLOW_GUIDE.md` - Advanced automation
5. `github/SECURITY_HARDENING.md` - Security best practices
6. `github/DEPENDENCY_MANAGEMENT.md` - UV and dependencies

### Advanced
7. `github/CI_CD_PRODUCTION_GUIDE.md` - Production workflows
8. `github/GITHUB_ADVANCED_SECURITY_GUIDE.md` - GHAS features
9. `github/THE_GITHUB_SAGA.md` - War stories and lessons

---

**Purpose**: Central hub for all Git, GitHub, and GitLab documentation  
**Source**: Consolidated from multiple repos (advanced-memory-mcp, mcp-studio)  
**Freshness System**: Active - monthly audits, version tracking, clear status markers


