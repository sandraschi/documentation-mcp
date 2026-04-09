# GitHub Workflows & CI/CD Standards

## Overview
Standards for GitHub Actions workflows, CI/CD pipelines, release mechanisms, and repository management for MCP projects.

## CI/CD Pipeline Standards

### Required Workflows
Every MCP repository MUST have these GitHub Actions workflows:

```
.github/workflows/
├── ci.yml                    # Primary CI pipeline
├── release.yml              # Automated releases
├── security.yml             # Security scanning
├── dependency-review.yml    # Dependency checks
└── codeql-analysis.yml      # Code security analysis
```

### CI Pipeline Structure
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Lint with ruff
      run: ruff check .

    - name: Type check with mypy
      run: mypy src/

    - name: Run tests
      run: pytest --cov=src/ --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Build MCPB package
      run: mcpb build

    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: mcpb-package
        path: dist/
```

## Release Management

### Automated Releases
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine

    - name: Build package
      run: python -m build

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        twine upload dist/*

    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body: |
          ## Changes
          - See CHANGELOG.md for details
        draft: false
        prerelease: false
```

### Semantic Versioning
```python
# version management in __init__.py
__version__ = "1.0.0"

# Automated version bumping
# Use: python -m setuptools_scm or uv-dynamic-versioning
```

## Pre-commit Hooks

### Required Pre-commit Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/Lucas-C/pre-commit-hooks
    rev: v1.5.4
    hooks:
      - id: remove-tabs

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### Pre-commit Hook Enforcement
```bash
# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Run on staged files only
pre-commit run
```

## Issue & PR Management

### Issue Templates
```
.github/ISSUE_TEMPLATE/
├── bug_report.md
├── feature_request.md
├── documentation.md
└── security.md
```

### PR Template
```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows standards
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Pre-commit hooks pass

## Related Issues
Closes #123
```

### Branch Protection Rules
```yaml
# Repository settings > Branches > Branch protection rules
# Protect main/master branch
required_status_checks:
  - ci
  - lint
  - test

required_pull_request_reviews:
  required_approving_review_count: 1
  dismiss_stale_reviews: true
  require_code_owner_reviews: true

restrictions:
  - enforce_admins: true
  - allow_force_pushes: false
  - allow_deletions: false
```

## Repository Management

### Repository Standards Checklist
```yaml
# Repository should have:
.github/
├── workflows/          # CI/CD pipelines
├── ISSUE_TEMPLATE/     # Issue templates
├── PULL_REQUEST_TEMPLATE.md
└── dependabot.yml      # Dependency updates

docs/                   # Documentation
src/                    # Source code
tests/                  # Test suite
scripts/                # Utility scripts

.pre-commit-config.yaml
pyproject.toml
README.md
LICENSE
CONTRIBUTING.md
CHANGELOG.md
```

### Automated Repository Maintenance
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Security Standards

### CodeQL Security Scanning
```yaml
# .github/workflows/codeql-analysis.yml
name: "CodeQL"

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Mondays

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    steps:
    - uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: python

    - name: Autobuild
      uses: github/codeql-action/autobuild@v2

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2
      with:
        category: "/language:python"
```

### Secret Scanning
```yaml
# .github/workflows/security.yml
name: Security

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy scan results
      uses: github/codecov/codecov-action@v3
      if: always()
      with:
        file: trivy-results.sarif
```

## Release Automation

### Conventional Commits
```bash
# Commit message format
<type>[optional scope]: <description>

# Types:
# feat: A new feature
# fix: A bug fix
# docs: Documentation only changes
# style: Changes that do not affect the meaning of the code
# refactor: A code change that neither fixes a bug nor adds a feature
# perf: A code change that improves performance
# test: Adding missing tests or correcting existing tests
# build: Changes that affect the build system
# ci: Changes to CI configuration files
# chore: Other changes that don't modify src or test files
```

### Automated Changelog Generation
```yaml
# .github/workflows/changelog.yml
name: Update Changelog

on:
  push:
    tags:
      - 'v*'

jobs:
  changelog:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Generate changelog
      uses: tj-actions/git-cliff@v1
      id: git-cliff
      with:
        configuration: cliff.toml
        args: --verbose --latest --strip header
      env:
        OUTPUT: CHANGELOG.md

    - name: Commit changelog
      run: |
        git add CHANGELOG.md
        git commit -m "docs: update changelog for ${GITHUB_REF#refs/tags/}"
        git push
```

## Next Steps
After GitHub workflows setup, proceed to:
1. [Testing Standards](./testing.md)
2. [Monitoring Standards](./monitoring.md)
3. [Error Handling Standards](./error-handling.md)
