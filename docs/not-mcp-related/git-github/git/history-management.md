# Git History Management

**Last Updated:** 2025-12-03  
**Status:** CURRENT  
**Git Version:** 2.40+

⚠️ **Warning:** History rewriting is powerful but dangerous! Use with caution.

---

## Overview

Managing and rewriting Git history for cleaner commits, squashing mistakes, and maintaining professional repositories.

---

## Viewing History

### Log Commands

```bash
# Standard log
git log

# Compact
git log --oneline

# With graph
git log --graph --oneline --all --decorate

# Last N commits
git log -5

# Specific file history
git log -- path/to/file.py

# Who changed what
git blame file.py

# Find when something was added/removed
git log -S "function_name"
```

### Diff Commands

```bash
# Changes since last commit
git diff

# Staged changes
git diff --staged

# Between branches
git diff main..feature/branch

# Specific commit
git show commit-hash
```

---

## Interactive Rebase

### Basic Usage

```bash
# Rebase last 3 commits
git rebase -i HEAD~3
```

**Options:**
- `pick` - Keep commit as-is
- `reword` - Change commit message
- `edit` - Amend commit
- `squash` - Combine with previous commit
- `fixup` - Like squash but discard commit message
- `drop` - Remove commit

### Example: Clean Up Feature Branch

**Before:**
```
abc123 WIP: add feature
def456 fix typo
ghi789 actually fix feature
jkl012 add tests
```

**Rebase:**
```bash
git rebase -i HEAD~4
```

**Change to:**
```
pick abc123 WIP: add feature
fixup def456 fix typo
fixup ghi789 actually fix feature
pick jkl012 add tests
```

**After:**
```
abc123 feat: add HTTP transport
jkl012 test: add HTTP transport tests
```

### Common Rebase Scenarios

**Squash all into one:**
```bash
git rebase -i HEAD~5
# Change all but first to 'squash'
```

**Split a commit:**
```bash
git rebase -i HEAD~3
# Change commit to 'edit'
# When stopped:
git reset HEAD^
git add file1.py
git commit -m "feat: part 1"
git add file2.py
git commit -m "feat: part 2"
git rebase --continue
```

---

## Amending Commits

### Last Commit (Not Pushed)

```bash
# Add forgotten file
git add forgotten-file.py
git commit --amend --no-edit

# Fix commit message
git commit --amend -m "Better message"

# Change both
git add new-file.py
git commit --amend -m "Updated message"
```

### Older Commits (Advanced)

```bash
# Interactive rebase to specific commit
git rebase -i commit-hash^

# Mark commit as 'edit'
# When stopped, make changes
git add changed-file.py
git commit --amend
git rebase --continue
```

---

## Undoing Changes

### Undo Last Commit (Keep Changes)

```bash
git reset --soft HEAD~1
# Changes still staged
```

### Undo Last Commit (Unstage Changes)

```bash
git reset HEAD~1
# Changes unstaged but kept
```

### Undo Last Commit (Discard Everything)

```bash
git reset --hard HEAD~1
# ⚠️ DANGEROUS: Changes lost forever!
```

### Revert a Commit (Safe)

```bash
# Creates new commit that undoes changes
git revert commit-hash

# Revert without committing
git revert --no-commit commit-hash
```

---

## Cleaning History

### Remove Sensitive Files

**Option 1: filter-branch (built-in)**

```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret.key" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (after backup!)
git push origin --force --all
```

**Option 2: BFG Repo-Cleaner (easier, faster)**

```bash
# Install BFG
# Download from: https://rtyley.github.io/bfg-repo-cleaner/

# Remove file
bfg --delete-files secret.key repo.git

# Remove passwords from files
bfg --replace-text passwords.txt repo.git

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

**⚠️ After cleaning:** Rotate compromised secrets immediately!

### Remove Large Files

```bash
# Find large files
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | \
  sort --numeric-sort --key=2 | \
  tail -10

# Remove with BFG
bfg --strip-blobs-bigger-than 50M repo.git
```

---

## Rewriting History Rules

### Safe to Rewrite

✅ **Your unpushed commits**
```bash
git rebase -i HEAD~3  # Not pushed yet - safe!
```

✅ **Your own feature branch**
```bash
git push --force-with-lease feature/my-branch
```

### NEVER Rewrite

❌ **main/master branch**
❌ **Shared branches** (multiple people working)
❌ **Published releases** (tagged)
❌ **Other people's commits** (without permission)

### Force Push Safely

```bash
# Safer force push (checks remote hasn't changed)
git push --force-with-lease

# After team agreement
git push --force  # Only if absolutely necessary!
```

---

## Cherry-Picking

### Apply Specific Commits

```bash
# Apply one commit from another branch
git cherry-pick commit-hash

# Apply multiple commits
git cherry-pick commit1 commit2 commit3

# Cherry-pick without committing
git cherry-pick --no-commit commit-hash
```

### Use Cases

- Backporting fixes to older versions
- Moving commits between branches
- Selective merging

---

## Bisect (Find Bugs)

### Binary Search for Bug Introduction

```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark known good commit
git bisect good commit-hash

# Git checks out middle commit
# Test if bug exists
git bisect good   # If bug not present
git bisect bad    # If bug present

# Repeat until found
# When done
git bisect reset
```

### Automated Bisect

```bash
git bisect start HEAD v1.0.0
git bisect run pytest tests/test_feature.py
```

---

## Reflog (Safety Net)

### View Reflog

```bash
# Show all HEAD movements
git reflog

# Show last 10
git reflog -10
```

### Recover Lost Commits

```bash
# Find lost commit in reflog
git reflog

# Reset to it
git reset --hard commit-hash

# Or create branch from it
git branch recovered-branch commit-hash
```

**Note:** Reflog expires after 90 days (default)

---

## Clean History Workflow

### Before PR

```bash
# 1. Update from main
git checkout main
git pull
git checkout feature/my-feature
git rebase main

# 2. Clean up commits
git rebase -i main
# Squash WIP commits, fix messages

# 3. Run tests
pytest

# 4. Force push to your branch
git push --force-with-lease

# 5. Create PR
gh pr create --title "feat: description" --body "Details"
```

---

## History Anti-Patterns

### ❌ Merge Commits Everywhere

**Problem:**
```
* Merge branch 'feature' into main
* Merge branch 'main' into feature
* Merge branch 'feature' into main
* Merge branch 'main' into feature
```

**Solution:** Use rebase for feature branches

### ❌ Meaningless Commits

**Problem:**
```
* fix
* fix again
* actually fix
* WIP
* cleanup
```

**Solution:** Squash before PR

### ❌ Giant Commits

**Problem:**
```
* Add 50 files, refactor 20 modules, fix 10 bugs
```

**Solution:** Break into logical commits

---

## Related Documentation

### Git Basics
- `fundamentals.md` - Git basics
- `worktrees.md` - Multiple working directories
- `etiquette.md` - Best practices

### GitHub Integration
- `../github/WORKFLOWS.md` - CI/CD workflows
- `../github/THE_GITHUB_SAGA.md` - What went wrong (learn from it!)
- `../github/TROUBLESHOOTING.md` - Common issues

### Standards
- `../../STANDARDS.md` - Documentation standards
- `../../CONTRIBUTING.md` - Contribution guidelines

---

**Last Updated:** 2025-12-03  
**Freshness:** CURRENT  
**Git Version:** 2.40+

