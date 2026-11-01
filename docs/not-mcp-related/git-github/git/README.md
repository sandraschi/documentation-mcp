# Git Fundamentals

**Last Updated:** 2025-12-03  
**Status:** CURRENT  
**Contents:** 4 comprehensive Git guides

---

## 📚 Git Documentation

### Core Guides

**[fundamentals.md](fundamentals.md)** - Git Basics
- Basic workflow (clone, commit, push)
- Branching and merging
- Commit message standards
- Undoing changes
- Viewing history
- Working with remotes
- Stashing
- Tags
- Configuration

**[worktrees.md](worktrees.md)** - Git Worktrees
- Work on multiple branches simultaneously
- Basic usage (add, list, remove)
- Common workflows (feature dev, PR review, hotfixes)
- Advanced: Bare repos + worktrees
- Best practices and naming conventions
- MCP development use cases

**[etiquette.md](etiquette.md)** - Git Etiquette & Best Practices
- Commit message etiquette
- Branch naming conventions
- Pull request etiquette
- Commit hygiene (atomic commits)
- History rewriting rules
- File management (.gitignore)
- Collaboration best practices
- Security etiquette (never commit secrets!)
- MCP-specific etiquette

**[history-management.md](history-management.md)** - Git History Management
- Interactive rebase
- Amending commits
- Cherry-picking
- Bisect (find bugs)
- Reflog (recover lost commits)
- Clean history workflow
- History anti-patterns
- Sensitive data removal

---

## 🎯 Quick Start

### Never Used Git?
1. Start with `fundamentals.md`
2. Practice basic workflow
3. Then read `etiquette.md`

### Know Git Basics?
1. Skip to `worktrees.md` - Level up your workflow!
2. Read `etiquette.md` - Professional practices
3. Learn `history-management.md` - Advanced techniques

### Setting Up MCP Project?
1. `fundamentals.md` - Refresh basics
2. `../github/COMPLETE_SETUP_GUIDE.md` - GitHub setup
3. `../github/WORKFLOWS.md` - CI/CD automation

---

## 🔗 Related Documentation

### Next Steps
- `../github/` - GitHub-specific guides (16 comprehensive docs)
- `../gitlab/` - GitLab guides (coming soon)
- `../ci-cd/` - CI/CD best practices

### Related Topics
- `../../docker/` - Docker integration with Git
- `../../patterns/` - Development patterns
- `../../CONTRIBUTING.md` - How to contribute to repos

---

## 💡 Pro Tips

### Worktrees
Work on multiple branches without stashing:
```bash
git worktree add ../repo-feature feature/new-feature
cd ../repo-feature
# Work independently from main repo!
```

### Interactive Rebase
Clean up commits before PR:
```bash
git rebase -i HEAD~5
# Squash WIP commits, fix messages
```

### Reflog
Safety net when things go wrong:
```bash
git reflog  # Find lost commits
git reset --hard commit-hash  # Recover
```

---

## 📊 Statistics

- **Total Guides**: 4
- **Status**: All CURRENT
- **Last Review**: 2025-12-03
- **Next Review**: 2026-03-03 (Git is stable)

---

## 🔄 Maintenance

**Update Frequency**: Yearly (Git is stable)  
**Owner**: Sandra  
**Contributors**: Claude, AI assistants

**Quick Freshness Check**:
- [ ] All docs have Last Updated dates
- [ ] Git version references current (2.40+)
- [ ] Commands tested and working
- [ ] Cross-links valid

---

**Last Updated:** 2025-12-03  
**Freshness:** CURRENT  
**Git Version:** 2.40+

