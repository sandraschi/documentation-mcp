# GitLab CE Local Setup Guide

**Last Updated:** 2025-12-03  
**Status:** CURRENT  
**GitLab Version:** CE (Community Edition) latest

---

## Overview

Set up **free, self-hosted GitLab CE** for private repositories and CI/CD, running locally via Docker.

**Use Case**: Private repos + CI/CD on your own hardware (Goliath)

---

## Prerequisites

- Docker Desktop running
- 4GB+ RAM available
- 10GB+ disk space
- Ports 8080 and 2222 available

---

## Quick Setup

### 1. Create Docker Compose

**File**: `deploy/gitlab/docker-compose.yml`

```yaml
version: '3.8'

services:
  gitlab:
    image: gitlab/gitlab-ce:latest
    container_name: gitlab-ce
    hostname: gitlab.local
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://gitlab.local:8080'
        gitlab_rails['gitlab_shell_ssh_port'] = 2222
        # Reduce memory usage
        puma['worker_processes'] = 2
        sidekiq['max_concurrency'] = 10
    ports:
      - '8080:8080'
      - '2222:22'
    volumes:
      - './config:/etc/gitlab'
      - './logs:/var/log/gitlab'
      - './data:/var/opt/gitlab'
    restart: unless-stopped
    shm_size: '256m'
```

### 2. Start GitLab

```powershell
# Create directories
cd D:\Dev\repos
New-Item -ItemType Directory -Path "gitlab-ce\config","gitlab-ce\logs","gitlab-ce\data" -Force

# Start GitLab
cd gitlab-ce
docker compose up -d

# Wait for GitLab to start (takes 2-5 minutes first time)
Write-Host "Waiting for GitLab to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 120

# Check status
docker compose logs -f
```

### 3. Get Root Password

```powershell
# Get initial root password
docker exec -it gitlab-ce cat /etc/gitlab/initial_root_password

# Or
docker compose exec gitlab cat /etc/gitlab/initial_root_password
```

**Save this password!** You'll need it to login.

### 4. Access GitLab

**URL**: http://localhost:8080

**Login**:
- Username: `root`
- Password: (from step 3)

**Change root password immediately!**

---

## Configuration

### Create User

1. Go to Admin Area → Users
2. Create new user (your account)
3. Set as admin
4. Logout and login as your user

### Create Group

1. Go to Groups → New Group
2. Name: `mcp-servers` (or whatever you want)
3. Visibility: Private

### Create Project

1. Go to Projects → New Project
2. Create blank project
3. Name: `claude-depot`
4. Group: `mcp-servers`
5. Visibility: Private

---

## Push Existing Repo to GitLab

### Add GitLab Remote

```powershell
cd C:\Users\<user>\Documents\claude-depot

# Add GitLab remote
git remote add gitlab http://localhost:8080/mcp-servers/claude-depot.git

# Or if using SSH
git remote add gitlab git@localhost:2222:mcp-servers/claude-depot.git

# View remotes
git remote -v
# origin  https://github.com/sandraschi/claude-depot.git (fetch)
# origin  https://github.com/sandraschi/claude-depot.git (push)
# gitlab  http://localhost:8080/mcp-servers/claude-depot.git (fetch)
# gitlab  http://localhost:8080/mcp-servers/claude-depot.git (push)
```

### Push to GitLab

```powershell
# Push all branches
git push gitlab --all

# Push all tags
git push gitlab --tags

# Or push specific branch
git push gitlab master
```

---

## Dual Remote Strategy

### Push to Both GitHub and GitLab

```powershell
# Push to GitHub (public/backup)
git push origin master

# Push to GitLab (private/CI)
git push gitlab master

# Or push to both at once
git push origin master; git push gitlab master
```

### Set Up Mirror

**Option A: Manual push to both**
```bash
git remote set-url --add --push origin https://github.com/sandraschi/claude-depot.git
git remote set-url --add --push origin http://localhost:8080/mcp-servers/claude-depot.git

# Now 'git push' pushes to both!
```

**Option B: GitLab mirror (automatic)**
1. In GitLab: Settings → Repository → Mirroring repositories
2. Add GitHub URL with token
3. GitLab automatically syncs

---

## GitLab CI/CD

### Basic Pipeline

**File**: `.gitlab-ci.yml`

```yaml
stages:
  - test
  - build

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

test:
  stage: test
  image: python:3.11-slim
  before_script:
    - python -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
  script:
    - pytest tests/
    - ruff check .
  only:
    - master
    - merge_requests

build:
  stage: build
  image: python:3.11-slim
  script:
    - python -m build
  artifacts:
    paths:
      - dist/
  only:
    - tags
```

---

## Backup Strategy

### GitLab Backup

```powershell
# Create backup
docker exec -it gitlab-ce gitlab-rake gitlab:backup:create

# Backups stored in: ./data/backups/

# Copy to safe location
Copy-Item "gitlab-ce\data\backups\*" "\\goliath\backups\gitlab\"
```

### Automated Backup Script

**File**: `scripts/backup-gitlab.ps1`

```powershell
# GitLab Backup Script
$backupDate = Get-Date -Format "yyyy-MM-dd"

Write-Host "Creating GitLab backup..." -ForegroundColor Cyan

# Create backup
docker exec gitlab-ce gitlab-rake gitlab:backup:create

# Copy to off-site
$latestBackup = Get-ChildItem "gitlab-ce\data\backups\" | 
                Sort-Object LastWriteTime -Descending | 
                Select-Object -First 1

Copy-Item $latestBackup.FullName "\\goliath\backups\gitlab\gitlab-backup-$backupDate.tar"

Write-Host "✅ Backup complete: gitlab-backup-$backupDate.tar" -ForegroundColor Green
```

**Schedule**: Run monthly

---

## Restore from Backup

```powershell
# Stop GitLab
docker compose down

# Copy backup to data/backups/
Copy-Item "backup-file.tar" "gitlab-ce\data\backups\"

# Start GitLab
docker compose up -d

# Wait for startup
Start-Sleep -Seconds 120

# Restore
docker exec -it gitlab-ce gitlab-rake gitlab:backup:restore BACKUP=timestamp
```

---

## Tailscale Integration

### Access GitLab from Other Machines

**Option 1: Tailscale Serve** (Simple)
```bash
# On Goliath
tailscale serve http://localhost:8080

# Access from anywhere on Tailscale
https://goliath.tailnet-name.ts.net
```

**Option 2: Tailscale Funnel** (Public)
```bash
# Make publicly accessible (be careful!)
tailscale funnel 8080
```

**Recommended**: Use Serve (Tailscale network only)

---

## GitHub vs GitLab Strategy

### GitHub (Public)
**Use for**:
- ✅ Public MCP servers
- ✅ Open source projects
- ✅ Community collaboration
- ✅ Glama registry submissions

**Examples**:
- `plex-mcp`
- `calibre-mcp`
- `devices-mcp`

### GitLab (Private)
**Use for**:
- ✅ Private notes (claude-depot!)
- ✅ Experimental projects
- ✅ Internal tools
- ✅ Heavy CI/CD on local hardware

**Examples**:
- `claude-depot` (private notes)
- `mcp-experiments`
- Internal automation scripts

### Both (Mirror)
**Use for**:
- ✅ Public repo with private CI
- ✅ Backup redundancy

**Example**: Public GitHub repo mirrored to private GitLab for CI

---

## Pros & Cons

### GitLab CE Pros
✅ **Free** - No cost for unlimited private repos  
✅ **Full control** - Your hardware, your rules  
✅ **Integrated CI/CD** - Built-in pipelines  
✅ **Privacy** - Data never leaves your network  
✅ **Heavy CI** - Use Goliath's 24 cores!  

### GitLab CE Cons
❌ **Maintenance** - You manage updates, backups  
❌ **Resource heavy** - Needs 4GB+ RAM  
❌ **Single point of failure** - Backup critical!  
❌ **No mobile app** - (GitHub has better mobile)  

### GitHub Pros
✅ **Zero maintenance** - GitHub handles everything  
✅ **Mobile apps** - iOS/Android  
✅ **Community** - More discoverable  
✅ **Reliability** - 99.9%+ uptime  

### GitHub Cons
❌ **Cost** - Private repos on free plan limited  
❌ **Less control** - GitHub's rules  
❌ **CI minutes** - Limited on free plan  

---

## Recommendation

### For Claude Depot

**Best approach**: **Use both!**

1. **GitHub** (already done!):
   - Primary remote
   - Backup
   - Easy access from anywhere

2. **GitLab CE** (optional):
   - Secondary remote
   - CI/CD experiments
   - Heavy automation on Goliath

**Command**:
```powershell
# Push to both
git push origin master    # GitHub
git push gitlab master    # GitLab (when set up)
```

---

## Quick Start Commands

### Setup GitLab
```powershell
cd D:\Dev\repos
mkdir gitlab-ce
cd gitlab-ce
# Copy docker-compose.yml from above
docker compose up -d
```

### Add to claude-depot
```powershell
cd C:\Users\<user>\Documents\claude-depot
git remote add gitlab http://localhost:8080/username/claude-depot.git
git push gitlab master
```

---

## Related Documentation

### Git Basics
- `../git/fundamentals.md` - Git basics
- `../git/etiquette.md` - Best practices

### GitHub
- `../github/COMPLETE_SETUP_GUIDE.md` - GitHub setup
- `../github/WORKFLOWS.md` - GitHub Actions

### GitLab
- This file - Setup guide
- `COMPARISON.md` (to be created) - GitHub vs GitLab

---

**Last Updated:** 2025-12-03  
**Freshness:** CURRENT  
**GitLab Version:** CE latest

