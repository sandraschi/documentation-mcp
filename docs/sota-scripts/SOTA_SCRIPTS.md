# SOTA Scripts - State of the Art Repository Scripts

**Purpose:** Central repository for battle-tested, production-ready scripts used across all MCP repos

**Location:** `mcp-central-docs/templates/scripts/`

**Last Updated:** 2025-10-24

---

## ðŸŽ¯ Concept

**SOTA (State of the Art):** Best-in-class scripts that should be in ALL repos

**Hub-and-Spoke:**
- **Hub:** Central docs holds the SOTA version
- **Spokes:** All MCP repos get copies
- **Updates:** Improve once, propagate everywhere

**Benefits:**
- âœ… Consistency across all projects
- âœ… Single source of truth
- âœ… Easy to improve and deploy
- âœ… Reduced maintenance burden

---

## ðŸ“¦ Available SOTA Scripts

### 1. `backup-repo.ps1` â­

**Purpose:** Automated dual-location repository backup

**Features:**
- Windows native ZIP (no dependencies)
- Dual locations (Desktop + N:\backup\dev\repos)
- Smart exclusions (venv, IDE cache, large test files)
- Selective database handling (keeps small samples)
- Size analysis and compression stats

**Deployment:** 53/53 MCP repos âœ…

---

### 2. `check-repo-standards.ps1` â­ NEW

**Purpose:** Repository standards checker and auto-fixer generator

**Features:**
- FastMCP 3.1.1++ compliance check (no description= params)
- MCPB packaging verification (manifest, assets, etc.)
- CI/CD workflows detection
- Test scaffold analysis
- Folder structure validation
- Documentation completeness check
- Repo root cleanliness scan
- Modern Python tooling check (ruff, uv)
- Auto-generates detailed report in docs/
- Auto-generates fix script in scripts/

**Deployment:** 53/53 MCP repos âœ…

**Usage:**
```powershell
.\scripts\check-repo-standards.ps1
# Generates: docs/repository-analysis-{date}.md
# Generates: scripts/fix-standards.ps1

.\scripts\fix-standards.ps1 -DryRun  # Preview fixes
.\scripts\fix-standards.ps1          # Apply fixes
```

**Checks 8 Categories:**
1. FastMCP 3.1.1++ (no description= parameters)
2. MCPB Packaging (manifest.json, assets/, etc.)
3. CI/CD (GitHub Actions workflows)
4. Test Scaffold (pytest, coverage)
5. Folder Structure (, src/, tests/, scripts/)
6. Documentation (README, CONTRIBUTING, CHANGELOG, .cursorrules)
7. Repo Cleanliness (no *.log, *.old, test files in root)
8. Modern Tooling (ruff, uv, pyproject.toml)

**Scoring:** 10-point scale per category, overall grade  
**Report:** Markdown with detailed findings  
**Fix Script:** PowerShell script with dry-run mode

**Usage:**
```powershell
.\scripts\backup-repo.ps1
```

**Exclusions:**
- Virtual environments: `.venv/`, `venv/`, `env/`
- IDE caches: `.windsurf/`, `.cursor/`, `__pycache__/`
- Build artifacts: `dist/`, `build/`, `*.whl`, `*.tar.gz`
- Large test DBs: `samples\metadata.db`, `test_data\*.db`
- Old formats: ``

**Smart Feature:** Preserves small sample DBs, excludes only large regenerable files

---

## ðŸ”„ Propagation Workflow

### Step 1: Improve in Central Docs

Edit the SOTA version:
```
templates/scripts/backup-repo.ps1
```

### Step 2: Run Propagation Script

```powershell
cd mcp-central-docs
.\scripts\propagate-backup-script.ps1
```

**Result:** Copies to all 50+ MCP repos automatically!

### Step 3: Test in One Repo

```powershell
cd ../some-mcp-repo
.\scripts\backup-repo.ps1
```

### Step 4: Commit if Satisfied

```powershell
# In each affected repo (or batch commit)
git add scripts/backup-repo.ps1
git commit -m "Update backup script from central docs SOTA"
```

---

## ðŸ“‹ Adding New SOTA Scripts

### Criteria for SOTA Status

âœ… **Must be:**
- Useful across ALL or MOST repos
- Battle-tested and proven
- Well-documented
- PowerShell or cross-platform
- Zero or minimal dependencies

âœ… **Examples:**
- Repository backup
- CI/CD helpers
- Release automation
- Documentation generation
- Quality checks

âŒ **Not SOTA:**
- Repo-specific scripts
- One-off utilities
- Experimental code
- Complex dependencies

### Adding New Script

1. **Create in `templates/scripts/`**
   ```powershell
   # Add your script
   templates/scripts/your-new-script.ps1
   ```

2. **Document in `templates/scripts/README.md`**
   - Purpose
   - Usage
   - Features
   - Requirements

3. **Create Propagation Script**
   ```powershell
   # Copy propagate-backup-script.ps1 as template
   scripts/propagate-your-script.ps1
   ```

4. **Test in One Repo First**
   ```powershell
   # Copy manually to test repo
   # Verify it works
   ```

5. **Propagate to All**
   ```powershell
   .\scripts\propagate-your-script.ps1
   ```

6. **Document in This File**
   - Add to "Available SOTA Scripts" section
   - Document deployment status

---

## ðŸŽ¯ Current SOTA Scripts

| Script | Purpose | Repos | Status |
|--------|---------|-------|--------|
| `backup-repo.ps1` | Dual-location backup | 53/53 | âœ… Deployed |
| `check-repo-standards.ps1` | Standards checker + fixer | 53/53 | âœ… Deployed |
| `new-mcp-server.ps1` | Complete MCP server builder | Central | âœ… Ready |

**Future SOTA Candidates:**
- `run-ci-tests.ps1` - Local CI testing
- `bump-version.ps1` - Semantic versioning
- `generate-docs.ps1` - Auto-documentation
- `check-quality.ps1` - Pre-commit quality checks

---

## ðŸ“Š Deployment Status

### Last Propagation: 2025-10-24

**backup-repo.ps1:**
- Total MCP repos: 53
- Updated: 52
- Already current: 1 (calibremcp - source repo)
- Skipped: 0
- Excluded: Repos with "copy", "backup", "old", "archive", "restored" in name

---

## ðŸ”§ Maintenance

### Regular Updates

**Monthly:**
- Review scripts for improvements
- Check for new features in any repo
- Propagate enhancements to all

**After Major Changes:**
- Test in 2-3 repos first
- Document breaking changes
- Propagate with release notes

**Version Tracking:**
- Add version comments to scripts
- Document changes in script header
- Update this file with deployment dates

---

## ðŸ’¡ Best Practices

### Script Design
1. **Self-contained** - Minimal dependencies
2. **Well-documented** - Clear headers and comments
3. **Error handling** - Graceful failures
4. **Progress reporting** - Show what's happening
5. **Dry-run mode** - Preview before changes

### Propagation
1. **Test first** - Always test in one repo
2. **Document changes** - Update README
3. **Batch propagate** - Use automation scripts
4. **Verify deployment** - Check a few repos
5. **Commit strategically** - Batch or individual based on impact

### Quality
1. **Keep it simple** - Complexity is enemy of reuse
2. **Make it robust** - Handle edge cases
3. **Stay current** - Regular reviews
4. **Get feedback** - Improve from usage

---

## ðŸ“š Related Documentation

- [Templates Overview](templates/README.md) - All templates
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Structure](STRUCTURE.md) - Repository organization

---

## ðŸŽ¯ Vision

**Goal:** Every MCP repo has access to best-in-class scripts

**Impact:**
- Faster development
- Higher quality
- Less duplication
- Easier maintenance
- Consistent experience

**Philosophy:** Build once, benefit everywhere!

---

**Maintained by:** Central Docs Team  
**Last Propagation:** 2025-10-24  
**Scripts Available:** 1  
**Repos Covered:** 52+

---

**Status:** âœ… PRODUCTION - Actively used across all MCP repos  
**Pattern:** Hub-and-spoke with automated propagation



