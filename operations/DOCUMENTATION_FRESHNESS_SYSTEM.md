# Documentation Freshness System

**Date**: 2025-12-03  
**Status**: Proposed System  
**Problem**: Docs go stale fast in AI timescales (1 month = EONS!)

---

## The Challenge

### 1. Cross-Cutting Content
Same topic lives in multiple places:
- **Claude** - `anthropic-ecosystem/` AND `agentic-ai-ides/`
- **FastMCP** - `anthropic-ecosystem/fastmcp/` AND `mcp-technical/` AND root
- **Docker** - `docker/`, `monitoring/`, project-specific
- **CI/CD** - `git-github/`, project READMEs, individual repos

### 2. Rapid Version Churn
- **FastMCP**: 3.1.1+ â†’ 3.1.1+ â†’ 3.1.1+ â†’ 3.1.1+ (in months!)
- **Models**: Flux 1 â†’ Flux 2, Llama 3 â†’ Llama 4, etc.
- **AI Tools**: Cursor â†’ Windsurf â†’ Antigravity â†’ ???

### 3. AI Timescale Problem
**1 month old = OBSOLETE!**
- November 2025: Gemini 3, Antigravity IDE, Marble live
- October 2025: Different SOTA models
- September 2025: Ancient history!

---

## Solution: Multi-Layered System

### Layer 1: Document Headers (MANDATORY)

**Every .md file MUST start with:**

```markdown
# Document Title

**Last Updated:** 2025-12-03  
**Status:** CURRENT | OUTDATED | ARCHIVED  
**FastMCP Version:** 3.1.1++  
**Models Referenced:** Flux 2, Llama 3.1, Gemini 3  
**Valid Until:** 2026-01-03 (estimate)

âš ï¸ **Freshness Check**: If reading after Jan 2026, verify info is still current!

---
```

**Status Meanings:**
- **CURRENT** - Actively maintained, < 1 month old
- **OUTDATED** - > 1 month old, may have stale info, use with caution
- **ARCHIVED** - Superseded, kept for historical reference only

### Layer 2: Version Audit Script

**`scripts/audit-doc-freshness.ps1`**

```powershell
# Scan all docs, extract Last Updated dates
# Generate report of stale docs
# Flag docs > 30 days old as OUTDATED
# Flag docs > 90 days old as ARCHIVED

param(
    [int]$WarnDays = 30,
    [int]$ArchiveDays = 90
)

$stale = @()
$archived = @()

Get-ChildItem -Path "docs" -Recurse -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    if ($content -match '\*\*Last Updated:\*\*\s*(\d{4}-\d{2}-\d{2})') {
        $lastUpdated = [datetime]::Parse($Matches[1])
        $age = (Get-Date) - $lastUpdated
        
        if ($age.Days -gt $ArchiveDays) {
            $archived += [PSCustomObject]@{
                File = $_.FullName
                LastUpdated = $lastUpdated
                Age = "$($age.Days) days"
            }
        }
        elseif ($age.Days -gt $WarnDays) {
            $stale += [PSCustomObject]@{
                File = $_.FullName
                LastUpdated = $lastUpdated
                Age = "$($age.Days) days"
            }
        }
    }
}

# Generate report
Write-Host "ðŸ“Š Documentation Freshness Report" -ForegroundColor Cyan
Write-Host "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor Gray
Write-Host ""

if ($archived.Count -gt 0) {
    Write-Host "ðŸ”´ ARCHIVED (>$ArchiveDays days):" -ForegroundColor Red
    $archived | Format-Table -AutoSize
}

if ($stale.Count -gt 0) {
    Write-Host "âš ï¸  OUTDATED (>$WarnDays days):" -ForegroundColor Yellow
    $stale | Format-Table -AutoSize
}

if ($stale.Count -eq 0 -and $archived.Count -eq 0) {
    Write-Host "âœ… All documents are fresh!" -ForegroundColor Green
}
```

### Layer 3: Cross-Reference Index

**`CROSS_REFERENCE_INDEX.md`**

```markdown
# Cross-Reference Index

**Purpose**: Find all places where a topic is discussed

## By Topic

### FastMCP
**Current Version**: 3.1.1++  
**Last Version Update**: 2025-11-24

**Primary Location**: `docs/anthropic-ecosystem/fastmcp/`

**Related Docs**:
- `FASTMCP_3.1.1+_MIGRATION.md` - Migration guide
- `docs/mcp-technical/FASTMCP_3.1.1+_FEATURES_GUIDE.md` - Features
- `fastmcp/persistent-storage.md` - Storage pattern
- `docs/patterns/FASTMCP_DOCSTRING_PROMPT_RESOURCE_STANDARDS.md` - Docstring standards

**Warning**: If any doc references FastMCP < 3.1.1+, it's OUTDATED!

---

### Claude Desktop
**Relevant Versions**: Desktop app Nov 2025+

**Primary Location**: `docs/anthropic-ecosystem/claude-desktop/`

**Related Docs**:
- `docs/agentic-ai-ides/` - IDE comparison (includes Claude Desktop)
- Project-specific Claude configs

**Cross-Reference**: Claude as IDE vs Claude Desktop - see both sections

---

### Docker
**Primary Location**: `docs/docker/`

**Related Docs**:
- `monitoring/configs/` - Docker Compose files
- `docs/projects/*/STRUCTURE.md` - Project-specific setups
- `docs/mcp-technical/` - Old location (redirects)

---

### Git/GitHub/GitLab
**Primary Location**: `docs/git-github/` (TO BE CREATED)

**Currently Scattered In**:
- `advanced-memory-mcp/docs/github/` - 16 comprehensive guides
- `mcp-studio/docs/github/` - 8 guides
- Individual project `docs/` folders
- Advanced Memory notes (ADN)

**Consolidation Needed**: YES - See Git/GitHub Consolidation Plan below

---

### AI Models
**Fast-Changing Content!**

**Primary Location**: `docs/general-ai/models/`

**Current References** (as of Dec 2025):
- Flux 2 (current)
- Llama 3.1, 4 (current)
- Gemini 3 (SOTA Nov 2025)
- GPT-5 (if released)

**Outdated References** (mark as ARCHIVED):
- Flux 1 (superseded)
- Llama 2 (old)
- GPT-4 (superseded by GPT-5)

**Audit Frequency**: Weekly!

---
```

### Layer 4: README Network

**Every directory needs:**

```markdown
# Directory Name

**Last Updated:** 2025-12-03  
**Status:** CURRENT

## Contents
[List of files with one-line descriptions]

## Related Sections
**See Also**:
- `../other-section/` - [Why it's related]
- `../another-section/doc.md` - [Specific cross-reference]

## Maintenance
**Update Frequency**: [Weekly | Monthly | As needed]  
**Next Review**: 2026-01-03  
**Owner**: [Who maintains this section]
```

### Layer 5: Version Tracking

**`VERSION_TRACKER.md`** (at root)

```markdown
# Version Tracker

**Purpose**: Track current versions of key technologies

| Technology | Current Version | Last Updated | Docs to Update |
|------------|----------------|--------------|----------------|
| FastMCP | 3.1.1++ | 2025-11-24 | All MCP guides |
| Python | 3.11-3.12 | 2025-12-01 | Dockerfiles, workflows |
| Flux | 2.0 | 2025-11-xx | Image gen docs |
| Llama | 4.0 | 2025-11-xx | LLM docs |
| Gemini | 3.0 | 2025-11-xx | SOTA comparisons |
| Claude | 4.5 Sonnet | 2025-11-xx | IDE docs |
| Cursor | 0.43.x | 2025-12-xx | IDE docs |

**Update this monthly!**
```

---

## Git/GitHub Consolidation Plan

### Current State (SCATTERED!)

**Advanced Memory MCP** (`advanced-memory-mcp/docs/github/`):
- CI_CD_PRODUCTION_GUIDE.md
- CI_SUCCESS_WORKFLOW_GUIDE.md
- COMPLETE_SETUP_GUIDE.md
- COMPLETE_TYPE_FIX_GUIDE.md
- DEPENDENCY_MANAGEMENT.md
- GITHUB_ADVANCED_SECURITY_GUIDE.md
- GITHUB_CLI_VS_MCP.md
- GITHUB_RATE_LIMITING_GUIDE.md
- PRE_COMMIT_HOOKS_GUIDE.md
- README.md
- RELEASE_CHECKLIST.md
- SECURITY_HARDENING.md
- THE_GITHUB_SAGA.md
- TROUBLESHOOTING.md
- WORKFLOWS.md

**MCP Studio** (`mcp-studio/docs/github/`):
- Similar but less comprehensive

**Individual Projects**:
- Project-specific GitHub workflows
- Scattered setup guides

### Target State (CONSOLIDATED!)

**Create**: `docs/git-github/`

```
docs/git-github/
â”œâ”€â”€ README.md                          # Hub
â”‚
â”œâ”€â”€ 1-fundamentals/
â”‚   â”œâ”€â”€ git-basics.md
â”‚   â”œâ”€â”€ worktrees.md
â”‚   â”œâ”€â”€ history-management.md
â”‚   â””â”€â”€ etiquette.md
â”‚
â”œâ”€â”€ 2-github/
â”‚   â”œâ”€â”€ setup-guide.md                 # â† From ADN
â”‚   â”œâ”€â”€ cli-vs-mcp.md                  # â† From ADN
â”‚   â”œâ”€â”€ rate-limiting.md               # â† From ADN
â”‚   â””â”€â”€ advanced-security.md           # â† From ADN
â”‚
â”œâ”€â”€ 3-gitlab/
â”‚   â”œâ”€â”€ setup-guide.md
â”‚   â”œâ”€â”€ ci-cd.md
â”‚   â””â”€â”€ comparison.md
â”‚
â”œâ”€â”€ 4-ci-cd/
â”‚   â”œâ”€â”€ github-actions/
â”‚   â”‚   â”œâ”€â”€ workflows.md               # â† From ADN
â”‚   â”‚   â”œâ”€â”€ success-workflow.md        # â† From ADN
â”‚   â”‚   â”œâ”€â”€ production-guide.md        # â† From ADN
â”‚   â”‚   â””â”€â”€ optimization.md
â”‚   â”œâ”€â”€ gitlab-ci/
â”‚   â””â”€â”€ best-practices.md
â”‚
â”œâ”€â”€ 5-security/
â”‚   â”œâ”€â”€ hardening.md                   # â† From ADN
â”‚   â”œâ”€â”€ pre-commit-hooks.md            # â† From ADN
â”‚   â””â”€â”€ vulnerability-scanning.md
â”‚
â”œâ”€â”€ 6-release/
â”‚   â”œâ”€â”€ checklist.md                   # â† From ADN
â”‚   â”œâ”€â”€ versioning.md
â”‚   â””â”€â”€ changelog.md
â”‚
â”œâ”€â”€ 7-troubleshooting/
â”‚   â”œâ”€â”€ common-issues.md               # â† From ADN
â”‚   â”œâ”€â”€ github-saga.md                 # â† From ADN (war stories!)
â”‚   â””â”€â”€ type-errors.md                 # â† From ADN
â”‚
â””â”€â”€ 8-advanced/
    â”œâ”€â”€ stats-analytics.md
    â”œâ”€â”€ automation.md
    â””â”€â”€ dependency-management.md       # â† From ADN
```

---

## Freshness Maintenance Strategy

### Monthly Audit (1st of each month)

```powershell
# Run freshness audit
.\scripts\audit-doc-freshness.ps1

# Review report
# Update VERSION_TRACKER.md
# Update outdated docs or mark as ARCHIVED
```

### Version-Specific Markers

**In documents:**

```markdown
<!-- FASTMCP_VERSION: 3.1.1++ -->
<!-- FLUX_VERSION: 2.0 -->
<!-- LLAMA_VERSION: 3.1 -->

âš ï¸ **Version Check**: This doc assumes FastMCP 3.1.1++. 
If using older versions, see `archive/fastmcp-3.1.1+/`
```

### Archive Strategy

```
archive/
â”œâ”€â”€ fastmcp-3.1.1+/          # Old FastMCP 3.1.1+ docs
â”œâ”€â”€ fastmcp-3.1.1+/          # Even older
â”œâ”€â”€ flux-1/                # Old Flux 1 docs
â””â”€â”€ models-oct-2025/       # October 2025 SOTA
```

**With prominent warnings:**

```markdown
# âš ï¸ ARCHIVED CONTENT

This document is from October 2025 and may be OUTDATED.

**See current version**: `../current/equivalent-doc.md`

**Archived because**: FastMCP 3.1.1+ released, syntax changed

---
```

---

## Cross-Link System

### Standard Cross-Reference Format

**At bottom of every doc:**

```markdown
---

## Related Documentation

### Same Topic, Different Context
- `../agentic-ai-ides/claude-desktop.md` - Claude as IDE
- `../anthropic-ecosystem/claude-desktop/` - Claude configuration

### Prerequisites
- `../protocol/OVERVIEW.md` - Must read first
- `../fastmcp/basics.md` - Required knowledge

### Next Steps
- `../deployment/docker.md` - How to deploy
- `../ci-cd/workflows.md` - How to automate

### See Also
- `../patterns/portmanteau.md` - Related pattern
- `../troubleshooting/common-issues.md` - If problems occur

---

**Last Updated:** 2025-12-03  
**Freshness:** CURRENT (valid until 2026-01-03)  
**Versions:** FastMCP 3.1.1++, Python 3.11+
```

### Bi-Directional Links

If `doc-a.md` links to `doc-b.md`, then `doc-b.md` should link back:

```markdown
**Referenced By**:
- `../path/doc-a.md` - Uses this pattern
- `../path/doc-c.md` - Extends this concept
```

---

## README Network

### Hub-and-Spoke Pattern

**Every directory needs README.md:**

```markdown
# Directory Name

**Last Updated:** 2025-12-03  
**Status:** CURRENT  
**Contents:** 12 documents

---

## ðŸ“š Documents in This Section

### Core Guides (Start Here)
1. **[basics.md](basics.md)** - Fundamentals
2. **[getting-started.md](getting-started.md)** - Quick start

### Advanced Topics
3. **[advanced-patterns.md](advanced-patterns.md)** - Expert techniques
4. **[troubleshooting.md](troubleshooting.md)** - Common issues

### Reference
5. **[api-reference.md](api-reference.md)** - Complete API
6. **[changelog.md](changelog.md)** - Version history

---

## ðŸ”— Related Sections

**Prerequisites**:
- `../fundamentals/` - Read this first

**Next Steps**:
- `../deployment/` - After mastering this

**Cross-References**:
- `../patterns/` - Related patterns
- `../troubleshooting/` - If stuck

---

## ðŸ”„ Maintenance

**Update Frequency:** Monthly  
**Last Review:** 2025-12-03  
**Next Review:** 2026-01-03  
**Owner:** Sandra

**Quick Freshness Check:**
- [ ] All docs have Last Updated dates
- [ ] All version references current (FastMCP 3.1.1++, Flux 2, etc.)
- [ ] All cross-links work
- [ ] No broken external links

---

## ðŸ“Š Statistics

- **Total Documents**: 12
- **CURRENT**: 10
- **OUTDATED**: 2 (need review)
- **ARCHIVED**: 0

---
```

---

## Automated Freshness Checks

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check if modified .md files have updated "Last Updated" date
for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.md$'); do
    if ! grep -q "Last Updated.*$(date +%Y-%m-%d)" "$file"; then
        echo "âš ï¸  $file: Please update 'Last Updated' date!"
        exit 1
    fi
done
```

### GitHub Action

```yaml
name: Documentation Freshness Check

on:
  schedule:
    - cron: '0 0 1 * *'  # 1st of each month
  workflow_dispatch:

jobs:
  freshness-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run freshness audit
        run: pwsh scripts/audit-doc-freshness.ps1
      
      - name: Create issue if stale docs found
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'ðŸ“š Stale documentation detected',
              body: 'Monthly freshness audit found outdated documents. See workflow run for details.',
              labels: ['documentation', 'maintenance']
            })
```

---

## Version Migration Strategy

### When FastMCP Updates

**Example**: FastMCP 3.1.1+ releases in January 2026

**Step 1**: Archive old version docs
```bash
mkdir -p archive/fastmcp-3.1.1+
cp -r docs/fastmcp/* archive/fastmcp-3.1.1+/
```

**Step 2**: Update all FastMCP docs
```bash
# Find all files mentioning FastMCP
grep -r "FastMCP 3.1.1+" docs/

# Update to 3.1.1+
# Add migration notes
```

**Step 3**: Update VERSION_TRACKER.md

**Step 4**: Add warning to archived docs

```markdown
# âš ï¸ ARCHIVED: FastMCP 3.1.1+ Documentation

**Current Version**: FastMCP 3.1.1++ (released 2026-01-xx)

**See**: `../docs/fastmcp/` for current documentation

**This archive kept for**: Projects still using FastMCP 3.1.1+

---
```

---

## Model Reference Strategy

### Problem: Models Update Weekly!

**Bad**:
```markdown
Use Flux for image generation.  # â† Which Flux? 1? 2?
```

**Good**:
```markdown
Use Flux 2 for image generation (Nov 2025+).

**Model Evolution**:
- Flux 1 (June 2025) - Superseded
- Flux 2 (Nov 2025) - **CURRENT**

âš ï¸ **Freshness**: If reading after Jan 2026, check for Flux 3 or alternatives!
```

### Model Version File

**`docs/general-ai/CURRENT_MODELS.md`**

```markdown
# Current AI Models

**Last Updated:** 2025-12-03  
**Review Frequency:** Weekly (AI timescale!)

## Image Generation
| Model | Version | Status | Use For |
|-------|---------|--------|---------|
| Flux | 2.0 | âœ… CURRENT | General image gen |
| Flux | 1.0 | ðŸ—„ï¸ ARCHIVED | Legacy only |
| Midjourney | v7 | âœ… CURRENT | Artistic |
| DALL-E | 3 | âœ… CURRENT | OpenAI ecosystem |

## Text Generation
| Model | Version | Status | Use For |
|-------|---------|--------|---------|
| Claude | 4.5 Sonnet | âœ… CURRENT | Coding, analysis |
| GPT | 5 | âœ… CURRENT | General purpose |
| Llama | 4.0 | âœ… CURRENT | Open source |
| Llama | 3.1 | âš ï¸ OUTDATED | Legacy only |
| Gemini | 3.0 | âœ… CURRENT | Google ecosystem |

## Video Generation
| Model | Version | Status | Use For |
|-------|---------|--------|---------|
| Veo | 3 | âœ… CURRENT | Google |
| Sora | 2 | âœ… CURRENT | OpenAI |

---

**Update this WEEKLY or when major models release!**
```

---

## Implementation Plan

### Phase 1: Add Headers to All Docs (Week 1)
- [ ] Script to add standard headers
- [ ] Run on all existing docs
- [ ] Commit with "docs: add freshness headers"

### Phase 2: Create Cross-Reference Index (Week 2)
- [ ] Audit all docs for cross-cutting topics
- [ ] Create CROSS_REFERENCE_INDEX.md
- [ ] Add "Related Documentation" sections to all docs

### Phase 3: Build README Network (Week 3)
- [ ] Update all directory READMEs
- [ ] Add statistics and maintenance info
- [ ] Establish ownership

### Phase 4: Create Audit Tools (Week 4)
- [ ] Write audit-doc-freshness.ps1
- [ ] Add pre-commit hook
- [ ] Add monthly GitHub Action
- [ ] Create VERSION_TRACKER.md

### Phase 5: Establish Process (Ongoing)
- [ ] Monthly freshness audit (1st of month)
- [ ] Weekly model version check
- [ ] Update VERSION_TRACKER on changes
- [ ] Archive superseded content immediately

---

## Git/GitHub Folder Creation

### Consolidate From

**Copy from advanced-memory-mcp/docs/github/**:
- All 16 comprehensive guides (âœ… CURRENT, well-maintained)

**Copy from mcp-studio/docs/github/**:
- 8 guides (check for overlap/newer versions)

**Add New Content**:
- Git fundamentals (worktrees, history, etiquette)
- GitLab guides
- Git statistics and analytics
- Advanced Git patterns

### Structure

```
docs/git-github/
â”œâ”€â”€ README.md                          # Hub with freshness tracker
â”‚
â”œâ”€â”€ git/
â”‚   â”œâ”€â”€ fundamentals.md
â”‚   â”œâ”€â”€ worktrees.md
â”‚   â”œâ”€â”€ history-management.md
â”‚   â”œâ”€â”€ etiquette.md
â”‚   â””â”€â”€ advanced-patterns.md
â”‚
â”œâ”€â”€ github/
â”‚   â”œâ”€â”€ setup-guide.md
â”‚   â”œâ”€â”€ workflows.md
â”‚   â”œâ”€â”€ ci-cd-production.md
â”‚   â”œâ”€â”€ ci-success-workflow.md
â”‚   â”œâ”€â”€ cli-vs-mcp.md
â”‚   â”œâ”€â”€ rate-limiting.md
â”‚   â”œâ”€â”€ advanced-security.md
â”‚   â”œâ”€â”€ pre-commit-hooks.md
â”‚   â”œâ”€â”€ release-checklist.md
â”‚   â”œâ”€â”€ security-hardening.md
â”‚   â”œâ”€â”€ troubleshooting.md
â”‚   â”œâ”€â”€ type-fix-guide.md
â”‚   â”œâ”€â”€ dependency-management.md
â”‚   â””â”€â”€ the-github-saga.md             # War stories!
â”‚
â”œâ”€â”€ gitlab/
â”‚   â”œâ”€â”€ setup-guide.md
â”‚   â”œâ”€â”€ ci-cd.md
â”‚   â”œâ”€â”€ comparison-with-github.md
â”‚   â””â”€â”€ migration-guide.md
â”‚
â””â”€â”€ analytics/
    â”œâ”€â”€ repo-stats.md
    â”œâ”€â”€ contribution-patterns.md
    â””â”€â”€ automation-metrics.md
```

---

## Benefits

### For Developers
âœ… **Always know if doc is current** - Header tells you immediately  
âœ… **Find related content** - Cross-references guide you  
âœ… **Understand context** - Version info prevents confusion  
âœ… **Safe to use old docs** - Archived docs have clear warnings

### For Maintenance
âœ… **Automated audits** - Script finds stale content  
âœ… **Clear ownership** - Know who maintains what  
âœ… **Version tracking** - One source of truth for current versions  
âœ… **Archive strategy** - Old content preserved but marked

### For AI Timescale
âœ… **Month-old = flagged** - Automatic OUTDATED marking  
âœ… **90-day = archived** - Clear preservation  
âœ… **Weekly model checks** - Catch obsolete model references  
âœ… **Freshness estimates** - "Valid until" dates

---

## Success Metrics

After implementation:
- [ ] 100% of docs have freshness headers
- [ ] All cross-cutting topics have index entries
- [ ] Every directory has README with stats
- [ ] Monthly audit runs automatically
- [ ] No FastMCP < 3.1.1+ references in CURRENT docs
- [ ] No Flux 1 references in CURRENT docs
- [ ] VERSION_TRACKER updated monthly

---

**Status**: System designed, ready for implementation  
**Next**: Create git-github folder and start consolidation


