# Git Etiquette & Best Practices

**Last Updated:** 2025-12-03  
**Status:** CURRENT  
**Git Version:** 2.40+

---

## Overview

Git etiquette and best practices for collaborative development and clean history.

---

## Commit Messages

### The Golden Rules

**DO:**
- âœ… Write clear, descriptive messages
- âœ… Use present tense ("add feature" not "added feature")
- âœ… Use conventional commit format
- âœ… Keep subject line under 50 characters
- âœ… Explain WHY, not just WHAT

**DON'T:**
- âŒ "WIP", "fix", "update" without context
- âŒ Commit messages with no subject
- âŒ Novels in commit messages (use body instead)
- âŒ Profanity or unprofessional language

### Conventional Commits Format

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

**Examples:**

**Good:**
```bash
git commit -m "feat(mcp): add HTTP transport support"
git commit -m "fix(docker): resolve layer caching issue"
git commit -m "docs: update transport guide with stdio examples"
```

**Bad:**
```bash
git commit -m "updates"
git commit -m "WIP"
git commit -m "fixed the thing"
```

---

## Branching Etiquette

### Branch Naming

**Format:** `type/short-description`

**Good:**
```bash
feature/http-transport
bugfix/issue-123
hotfix/security-patch
docs/api-reference
refactor/mcp-client
```

**Bad:**
```bash
test
fix
my-branch
temp123
```

### Branch Lifecycle

**DO:**
- âœ… Create branch from latest main
- âœ… Keep branches short-lived (< 1 week)
- âœ… Delete merged branches
- âœ… Rebase on main regularly

**DON'T:**
- âŒ Long-lived feature branches (> 2 weeks)
- âŒ Leave merged branches around
- âŒ Create branches from other feature branches
- âŒ Force-push to shared branches

---

## Pull Request Etiquette

### Creating PRs

**DO:**
- âœ… Write clear PR title and description
- âœ… Reference related issues (#123)
- âœ… Add screenshots/examples if UI changes
- âœ… Request specific reviewers
- âœ… Mark as draft if not ready

**DON'T:**
- âŒ PRs with 1000+ lines (split them!)
- âŒ No description ("see commits")
- âŒ Mixing unrelated changes
- âŒ Pushing without running tests

### PR Description Template

```markdown
## What

[Brief description of changes]

## Why

[Reason for changes]

## How

[Implementation details]

## Testing

- [ ] Unit tests pass
- [ ] Manual testing done
- [ ] No new linter errors

## Related

Closes #123
Related to #456
```

### Reviewing PRs

**DO:**
- âœ… Review promptly (within 24h)
- âœ… Be constructive and respectful
- âœ… Ask questions if unclear
- âœ… Approve when satisfied
- âœ… Test locally if complex changes

**DON'T:**
- âŒ Nitpick style (use linters!)
- âŒ Approve without reviewing
- âŒ Be dismissive or rude
- âŒ Request changes without explanation

---

## Commit Hygiene

### Atomic Commits

**Good:** One logical change per commit
```bash
git commit -m "feat: add HTTP transport"
git commit -m "test: add HTTP transport tests"
git commit -m "docs: document HTTP transport"
```

**Bad:** Multiple unrelated changes in one commit
```bash
git commit -m "add HTTP, fix Docker, update docs, refactor client"
```

### Amending Commits

**Before pushing:**
```bash
# Forgot to add file
git add missing-file.py
git commit --amend --no-edit

# Fix commit message
git commit --amend -m "Better message"
```

**After pushing:** Don't amend! Create new commit instead.

### Interactive Rebase (Advanced)

**Clean up before PR:**
```bash
# Last 3 commits
git rebase -i HEAD~3

# Options:
# pick - keep commit
# reword - change message
# squash - combine with previous
# drop - remove commit
```

**âš ï¸ Warning:** Only rebase unpushed commits or your own branches!

---

## History Etiquette

### Force Push

**NEVER force-push to:**
- âŒ main/master
- âŒ Shared branches
- âŒ Other people's branches

**OK to force-push:**
- âœ… Your own feature branch (if needed)
- âœ… After explicit team agreement
- âœ… With `--force-with-lease` (safer)

```bash
# Safer force push
git push --force-with-lease
```

### Merge vs Rebase

**Merge:** Keep full history
```bash
git checkout main
git merge feature/branch
```

**Rebase:** Clean linear history
```bash
git checkout feature/branch
git rebase main
```

**Team Agreement:** Decide on strategy and stick to it!

---

## File Management

### .gitignore

**DO:**
- âœ… Ignore generated files (dist/, build/)
- âœ… Ignore dependencies (node_modules/, venv/)
- âœ… Ignore IDE files (.vscode/, .idea/)
- âœ… Ignore secrets (.env with actual secrets)
- âœ… Commit .env.example (without secrets)

**DON'T:**
- âŒ Commit secrets or API keys
- âŒ Commit large binary files (use LFS)
- âŒ Ignore files that should be committed
- âŒ Commit __pycache__, *.pyc, etc.

### Large Files

**Use Git LFS** for:
- Binary assets (images, videos)
- Large datasets
- Compiled binaries

```bash
git lfs track "*.psd"
git lfs track "*.mp4"
```

---

## Collaboration Etiquette

### Communication

**DO:**
- âœ… Notify team before major refactoring
- âœ… Discuss architecture changes
- âœ… Ask questions in PRs
- âœ… Document decisions in commits/PRs

**DON'T:**
- âŒ Surprise team with breaking changes
- âŒ Merge without approval (if required)
- âŒ Ignore PR comments
- âŒ Push directly to main (if protected)

### Merge Conflicts

**DO:**
- âœ… Resolve promptly
- âœ… Test after resolving
- âœ… Ask author if unsure
- âœ… Keep both changes if appropriate

**DON'T:**
- âŒ Blindly accept "theirs" or "ours"
- âŒ Delete others' code without understanding
- âŒ Leave conflict markers in code
- âŒ Merge without testing

---

## Repository Hygiene

### Regular Maintenance

```bash
# Clean up merged branches
git branch --merged | grep -v "main\|master" | xargs git branch -d

# Prune remote branches
git remote prune origin

# Garbage collection
git gc
```

### Tag Management

**DO:**
- âœ… Use semantic versioning (v1.0.0)
- âœ… Annotate tags with messages
- âœ… Tag stable releases
- âœ… Push tags explicitly

**DON'T:**
- âŒ Tag every commit
- âŒ Move existing tags (confusing!)
- âŒ Delete published tags
- âŒ Use non-semantic version numbers

---

## Security Etiquette

### Secrets Management

**NEVER commit:**
- âŒ API keys
- âŒ Passwords
- âŒ Private keys
- âŒ OAuth tokens
- âŒ Database credentials

**If you do accidentally:**
```bash
# Remove from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret" \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner (easier)
bfg --delete-files secret-file.txt
```

**Then:** Rotate the compromised secrets immediately!

### Sensitive Data

**Use:**
- âœ… .env files (gitignored)
- âœ… Environment variables
- âœ… Secret managers (Azure Key Vault, etc.)
- âœ… GitHub Secrets (for CI/CD)

---

## MCP-Specific Etiquette

### FastMCP Version References

**DO:**
- âœ… Always specify version: "FastMCP 3.1.1++"
- âœ… Update when new version releases
- âœ… Archive old version docs

**DON'T:**
- âŒ Say "FastMCP" without version
- âŒ Leave old version references (3.1.1+, 3.1.1+, 3.1.1+)
- âŒ Use deprecated APIs

### Portmanteau Tools

**DO:**
- âœ… Use `Literal` for operation enums
- âœ… Comprehensive docstrings
- âœ… Clear operation documentation

**DON'T:**
- âŒ Generic `str` for operations (breaks discoverability)
- âŒ Split operations into separate tools unnecessarily

### MCP Server Distribution

**DO:**
- âœ… Test locally before pushing
- âœ… Update CHANGELOG.md
- âœ… Version bump following semver
- âœ… Tag releases properly

**DON'T:**
- âŒ Push broken code
- âŒ Forget to update version numbers
- âŒ Skip testing with Claude Desktop

---

## When Things Go Wrong

### Oops, Wrong Branch!

```bash
# Move commits to correct branch
git checkout correct-branch
git cherry-pick commit-hash
git checkout wrong-branch
git reset --hard HEAD~1
```

### Oops, Committed Secret!

```bash
# If NOT pushed yet
git reset --soft HEAD~1
# Remove secret from files
git add .
git commit

# If already pushed
# Use BFG or filter-branch (see Security section)
# Then rotate secrets!
```

### Oops, Force-Pushed to Main!

**Contact team immediately!**
```bash
# If they haven't pulled yet, you might recover
git push origin old-main-commit:main --force

# Otherwise, communicate and coordinate
```

---

## Related Documentation

### Git Basics
- `fundamentals.md` - Git commands
- `worktrees.md` - Multiple working directories
- `history-management.md` - Rewriting history

### GitHub Integration
- `../github/COMPLETE_SETUP_GUIDE.md` - Repository setup
- `../github/WORKFLOWS.md` - CI/CD workflows
- `../github/THE_GITHUB_SAGA.md` - What NOT to do (learn from mistakes!)

### Standards
- `../../STANDARDS.md` - Documentation standards
- `../../CONTRIBUTING.md` - Contribution guidelines

---

**Last Updated:** 2025-12-03  
**Freshness:** CURRENT  
**Git Version:** 2.40+


