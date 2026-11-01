# Git Fundamentals

**Last Updated:** 2025-12-03  
**Status:** CURRENT  
**Git Version:** 2.40+

⚠️ **Freshness**: Git is stable - this doc valid for years unless major Git 3.0 release

---

## Overview

Essential Git concepts and commands for MCP development.

---

## Basic Workflow

### Clone Repository
```bash
git clone https://github.com/username/repo.git
cd repo
```

### Make Changes
```bash
# Check status
git status

# Stage files
git add file.py
git add .  # All files

# Commit
git commit -m "feat: add new feature"
```

### Push Changes
```bash
git push origin main
```

---

## Branching

### Create Branch
```bash
# Create and switch
git checkout -b feature/new-feature

# Or modern syntax
git switch -c feature/new-feature
```

### Switch Branches
```bash
git checkout main
git switch main  # Modern
```

### Merge Branch
```bash
git checkout main
git merge feature/new-feature
```

---

## Commit Message Standards

### Format
```
type(scope): subject

body (optional)

footer (optional)
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Formatting, no code change
- **refactor**: Code restructuring
- **test**: Adding tests
- **chore**: Maintenance

### Examples
```bash
git commit -m "feat(mcp): add dual interface support"
git commit -m "fix(docker): resolve build caching issue"
git commit -m "docs: update transport guide for HTTP"
```

---

## Undoing Changes

### Unstage Files
```bash
git restore --staged file.py
```

### Discard Changes
```bash
git restore file.py
```

### Amend Last Commit
```bash
git commit --amend -m "Updated message"
```

### Reset to Previous Commit
```bash
# Soft (keep changes)
git reset --soft HEAD~1

# Hard (discard changes) ⚠️ DANGEROUS
git reset --hard HEAD~1
```

---

## Viewing History

### Log
```bash
# Standard log
git log

# One line per commit
git log --oneline

# Graph view
git log --graph --oneline --all

# Last 10 commits
git log -10
```

### Show Commit
```bash
git show commit-hash
```

### Blame (Who changed what)
```bash
git blame file.py
```

---

## Working with Remotes

### View Remotes
```bash
git remote -v
```

### Add Remote
```bash
git remote add origin https://github.com/user/repo.git
```

### Fetch Updates
```bash
git fetch origin
```

### Pull Changes
```bash
git pull origin main
```

---

## Stashing

### Save Work in Progress
```bash
# Stash changes
git stash

# Stash with message
git stash save "WIP: feature implementation"
```

### List Stashes
```bash
git stash list
```

### Apply Stash
```bash
# Apply most recent
git stash pop

# Apply specific stash
git stash apply stash@{0}
```

---

## Tags

### Create Tag
```bash
# Lightweight tag
git tag v1.0.0

# Annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0"
```

### Push Tags
```bash
# Push specific tag
git push origin v1.0.0

# Push all tags
git push origin --tags
```

### Delete Tag
```bash
# Local
git tag -d v1.0.0

# Remote
git push origin :refs/tags/v1.0.0
```

---

## Configuration

### User Info
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Editor
```bash
git config --global core.editor "code --wait"
```

### Aliases
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
```

---

## .gitignore

### Common Patterns
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
*.egg-info/

# Testing
.coverage
htmlcov/
.pytest_cache/
```

---

## Related Documentation

### Next Steps
- `../github/COMPLETE_SETUP_GUIDE.md` - GitHub repository setup
- `../github/WORKFLOWS.md` - CI/CD workflows
- `worktrees.md` - Advanced: Git worktrees

### Related Topics
- `../ci-cd/` - Continuous integration
- `../security/` - Security best practices
- `../../docker/` - Docker integration with Git

---

**Last Updated:** 2025-12-03  
**Freshness:** CURRENT (Git is stable, valid for years)  
**Git Version:** 2.40+

