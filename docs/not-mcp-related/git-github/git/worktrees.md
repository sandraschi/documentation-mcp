# Git Worktrees

**Last Updated:** 2025-12-03  
**Status:** CURRENT  
**Git Version:** 2.40+

---

## Overview

Git worktrees allow you to have **multiple working directories** from the same repository simultaneously.

**Use Cases:**
- Work on multiple branches at once
- Test different versions side-by-side
- Keep main branch clean while developing
- Review PRs without stashing

---

## Basic Usage

### Create Worktree

```bash
# Create worktree for new branch
git worktree add ../repo-feature feature/new-feature

# Create worktree for existing branch
git worktree add ../repo-bugfix bugfix/issue-123

# Create worktree from specific commit
git worktree add ../repo-v1.0 v1.0.0
```

**Result**: New directory `../repo-feature` with `feature/new-feature` checked out

### List Worktrees

```bash
git worktree list
```

**Output:**
```
/path/to/repo          abc123 [main]
/path/to/repo-feature  def456 [feature/new-feature]
/path/to/repo-bugfix   ghi789 [bugfix/issue-123]
```

### Remove Worktree

```bash
# Remove worktree directory first
rm -rf ../repo-feature

# Then prune from Git
git worktree prune

# Or remove in one command
git worktree remove ../repo-feature
```

---

## Common Workflows

### Workflow 1: Feature Development

```bash
# Main repo - keep on main branch
cd ~/repos/my-project

# Create worktree for feature
git worktree add ../my-project-feature feature/new-api

# Work in feature worktree
cd ../my-project-feature
# ... make changes ...
git add .
git commit -m "feat: implement new API"
git push origin feature/new-api

# Back to main repo - still on main!
cd ~/repos/my-project
# No stashing needed!
```

### Workflow 2: PR Review

```bash
# Create worktree for PR branch
git fetch origin pull/123/head:pr-123
git worktree add ../my-project-pr123 pr-123

# Review in separate directory
cd ../my-project-pr123
# Test the PR...

# Back to main work
cd ~/repos/my-project
# Your work untouched!

# Clean up after review
git worktree remove ../my-project-pr123
```

### Workflow 3: Hotfix While Developing

```bash
# Currently working on feature branch
cd ~/repos/my-project-feature

# Urgent bug in production!
# Create worktree from main
git worktree add ../my-project-hotfix -b hotfix/urgent-bug main

# Fix bug in hotfix worktree
cd ../my-project-hotfix
# ... fix bug ...
git commit -m "fix: urgent production bug"
git push origin hotfix/urgent-bug

# Back to feature work - no interruption!
cd ~/repos/my-project-feature
```

---

## Advanced Usage

### Bare Repository + Worktrees

**Best practice for multiple long-lived worktrees:**

```bash
# Clone as bare repository
git clone --bare https://github.com/user/repo.git repo.git
cd repo.git

# Create worktrees for each branch
git worktree add ../repo-main main
git worktree add ../repo-develop develop
git worktree add ../repo-feature feature/new-feature

# Work in separate directories
cd ../repo-main      # Main branch
cd ../repo-develop   # Develop branch
cd ../repo-feature   # Feature branch
```

**Benefits:**
- Clean separation
- No accidental commits to wrong branch
- Easy to switch contexts

### Worktree with Different Python Versions

```bash
# Worktree for Python 3.11 testing
git worktree add ../repo-py311 main
cd ../repo-py311
python3.11 -m venv venv
source venv/bin/activate
pip install -e .

# Worktree for Python 3.12 testing
git worktree add ../repo-py312 main
cd ../repo-py312
python3.12 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## Best Practices

### Naming Convention

```bash
# Good: Clear, descriptive
git worktree add ../repo-feature-auth feature/authentication
git worktree add ../repo-bugfix-123 bugfix/issue-123
git worktree add ../repo-v1.0 v1.0.0

# Bad: Confusing
git worktree add ../temp feature/new-thing
git worktree add ../test main
```

### Location Strategy

**Option A: Sibling directories**
```
~/repos/
├── my-project/           # Main repo
├── my-project-feature/   # Worktree
└── my-project-bugfix/    # Worktree
```

**Option B: Subdirectory**
```
~/repos/my-project/
├── .git/
├── main/                 # Worktree (main branch)
├── develop/              # Worktree (develop branch)
└── features/
    ├── feature-a/        # Worktree
    └── feature-b/        # Worktree
```

### Cleanup

```bash
# List all worktrees
git worktree list

# Remove unused worktrees
git worktree prune

# Force remove (if directory already deleted)
git worktree remove --force ../repo-feature
```

---

## Common Issues

### "Branch already checked out"

**Problem:**
```bash
git worktree add ../repo-feature feature/branch
# Error: 'feature/branch' is already checked out
```

**Solution**: Can't have same branch in multiple worktrees
```bash
# Create new branch instead
git worktree add ../repo-feature -b feature/branch-copy feature/branch
```

### Worktree Not Deleted Properly

**Problem:** Deleted directory but Git still thinks worktree exists

**Solution:**
```bash
git worktree prune
```

### Locked Worktree

**Problem:** Can't remove worktree - locked

**Solution:**
```bash
git worktree unlock ../repo-feature
git worktree remove ../repo-feature
```

---

## Integration with MCP Development

### Use Case: Testing MCP Server Changes

```bash
# Main repo - stable version
cd ~/repos/plex-mcp

# Worktree for experimental feature
git worktree add ../plex-mcp-experiment feature/new-transport

# Test in experiment worktree
cd ../plex-mcp-experiment
python server.py --http 3055
# Test HTTP transport...

# Main repo still works with stdio
cd ~/repos/plex-mcp
python server.py
# Stable stdio transport
```

### Use Case: Multiple MCP Server Versions

```bash
# Worktree for each version
git worktree add ../plex-mcp-v1.0 v1.0.0
git worktree add ../plex-mcp-v2.0 v2.0.0
git worktree add ../plex-mcp-dev develop

# Test compatibility across versions
# Each has own venv, own config
```

---

## Related Documentation

### Git Basics
- `fundamentals.md` - Git basics
- `history-management.md` - Rewriting history

### GitHub Integration
- `../github/WORKFLOWS.md` - CI/CD with worktrees
- `../github/TROUBLESHOOTING.md` - Common issues

### Advanced Topics
- `etiquette.md` - Git best practices
- `../advanced/` - Advanced Git patterns

---

**Last Updated:** 2025-12-03  
**Freshness:** CURRENT  
**Git Version:** 2.40+

