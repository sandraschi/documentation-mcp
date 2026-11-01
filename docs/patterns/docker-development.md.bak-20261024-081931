# Docker Development Pattern: Hot-Reload Everything

**Pattern Category:** Development Workflow  
**Last Updated:** 2025-12-04  
**Status:** ✅ Production Ready

---

## Problem Statement

**Traditional Docker development wastes massive amounts of time:**

```bash
# Change 3 lines of code
docker compose build  # ⏳ Wait 5 minutes
docker compose up -d
# Test, find bug
docker compose build  # ⏳ Wait 5 minutes again
# Repeat 20 times = 100 minutes wasted
```

**Per project, you lose 8+ hours waiting for rebuilds.**

---

## Solution: Hot-Reload Development Pattern

**Core Principle:** Code lives on HOST, container reads via volume mount.

```yaml
# docker-compose.yml
services:
  app:
    build: ./app
    volumes:
      - ./app:/app  # 👈 Mount code directory
    command: uvicorn app:app --reload  # 👈 Hot-reload enabled
```

**Result:**
```bash
# Edit code, save
# See changes in 1 second ✅
# No rebuild needed
```

---

## Implementation

### Pattern 1: Volume Mounts + Hot-Reload (Recommended)

**Best for:** Full-stack development with multiple services

**docker-compose.yml:**
```yaml
services:
  frontend:
    build:
      context: ./frontend
      target: dev  # Multi-stage build
    volumes:
      - ./frontend:/app
      - /app/.venv  # Exclude venv from mount
    command: uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    environment:
      - PYTHONUNBUFFERED=1
      - DEBUG=true
    ports:
      - "8000:8000"
```

**Dockerfile (multi-stage):**
```dockerfile
# Development stage
FROM python:3.11-slim as dev
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
# Note: No COPY of code here!

# Production stage
FROM dev as prod
COPY . .
CMD ["uvicorn", "app:app"]
```

**Benefits:**
- ⚡ Code changes reflect in ~1 second
- 🐳 Full Docker environment (networking, services)
- 👥 Team consistency
- 🔧 Only rebuild when dependencies change

---

### Pattern 2: Native Development (Fastest)

**Best for:** Quick iteration, debugging, single service

**Setup Script (run_dev.ps1):**
```powershell
# Check database is running (in Docker)
$dbRunning = docker ps --filter "name=myapp-db" --format "{{.Names}}"
if (-not $dbRunning) {
    docker compose up -d db
    Start-Sleep -Seconds 5
}

# Setup venv if needed
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    & .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
}

# Run with hot-reload
& .\.venv\Scripts\Activate.ps1
$env:DATABASE_URL = "postgresql://user:pass@localhost:5433/db"
uvicorn app:app --reload --port 8000
```

**docker-compose.yml (DB only):**
```yaml
services:
  db:
    image: postgres:15
    ports:
      - "5433:5432"  # Expose to host
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

**Benefits:**
- 🚀 Starts in 5 seconds
- 🐛 Native IDE debugging
- 💻 No Docker overhead
- 🔧 Direct access to Python tools

---

## Advanced Patterns

### BuildKit Cache Mounts

**Speeds up rebuilds when dependencies DO change:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Pip cache persists between builds
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt
```

**Enable BuildKit:**
```powershell
$env:DOCKER_BUILDKIT = "1"
docker compose build
```

---

### Separate Dev/Prod Configs

**docker-compose.yml (base):**
```yaml
services:
  app:
    build: ./app
    environment:
      - DATABASE_URL=${DATABASE_URL}
```

**docker-compose.dev.yml (overrides):**
```yaml
services:
  app:
    volumes:
      - ./app:/app  # Hot-reload
    command: uvicorn app:app --reload --log-level debug
    environment:
      - DEBUG=true
```

**docker-compose.prod.yml:**
```yaml
services:
  app:
    # No volumes (code baked in)
    command: uvicorn app:app --host 0.0.0.0 --workers 4
    restart: always
```

**Usage:**
```bash
# Development
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

### .dockerignore (Essential)

**Create `.dockerignore` in every Docker project:**

```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.venv/
venv/
*.egg-info/

# Development
.git/
.gitignore
.vscode/
.idea/
*.log
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/

# Docker
Dockerfile
docker-compose*.yml
.dockerignore
```

**Impact:**
- Smaller build context
- Faster COPY operations
- Cleaner images

---

## When to Use What

### Use Hot-Reload in Docker When:
- ✅ Full stack with multiple services (DB, Redis, etc.)
- ✅ Team collaboration (consistent environment)
- ✅ Testing inter-service communication
- ✅ Need container-specific features

### Use Native Development When:
- ✅ Quick iteration on single service
- ✅ Debugging in IDE
- ✅ Fastest possible feedback loop
- ✅ Working on business logic (not infra)

### Use Full Rebuild When:
- ✅ `requirements.txt` changed
- ✅ `Dockerfile` changed
- ✅ System dependencies changed
- ✅ Preparing for production
- ✅ Troubleshooting weird issues

---

## Anti-Patterns (Don't Do This!)

### ❌ Anti-Pattern 0: Using --no-cache for Code Changes

**THE MOST EXPENSIVE MISTAKE:**

```bash
# WRONG: Downloads entire internet, takes 15+ minutes
docker compose build --no-cache frontend

# RIGHT: Uses cached layers, takes 30 seconds
docker compose build frontend

# BEST: Hot-reload, takes 1 second
# (No build needed, just save file!)
```

**When --no-cache is appropriate:**
- ✅ `requirements.txt` changed AND regular build failed mysteriously
- ✅ Final production build before deployment
- ✅ Suspected cache corruption (very rare)
- ✅ Dockerfile itself changed significantly

**When --no-cache is WRONG (99% of time):**
- ❌ Changed Python/Node/Go code
- ❌ Changed HTML/CSS/JS files  
- ❌ Changed config files (.env, .yaml, .json)
- ❌ "Just to be safe" (wastes time, not safer)
- ❌ After git pull (code changes don't need cache clear)
- ❌ "It failed once so now I always use it" (fix the real issue!)

**Real Cost Analysis:**

```
Project with 50 dependencies (typical):

Regular build:
- Uses cached pip/npm packages
- Recompiles only changed layers
- Time: 30 seconds - 2 minutes

--no-cache build:
- Downloads 50 packages from internet
- Compiles C extensions from scratch
- Installs system dependencies again
- Time: 10-20 minutes

Wasted per build: 8-19 minutes
Over 20 rebuilds: 160-380 minutes = 2.6-6.3 HOURS
```

**Decision Flowchart:**

```
What changed?
├─ Python/JS/Go code files?
│  └─ Use hot-reload (1 second) ✅
│     or regular build (30 sec) if needed
│
├─ HTML/CSS/static files?
│  └─ Don't rebuild! Hot-reload handles it ✅
│
├─ requirements.txt/package.json?
│  └─ Regular build (2-3 minutes) ✅
│     Use --no-cache only if this fails
│
├─ Dockerfile?
│  └─ Regular build (2-3 minutes) ✅
│
└─ "Just to be safe"?
   └─ STOP! You're wasting time ❌
```

**Why people use --no-cache by mistake:**

1. **"My build failed once, so now I always use it"**
   - Fix: Investigate why build failed, fix root cause
   - Don't use sledgehammer when screwdriver works

2. **"I want to be sure everything is fresh"**
   - Fix: Docker layer caching is reliable
   - Only invalidates cache when files change

3. **"Someone told me to always use it"**
   - Fix: That person was wrong
   - Share this guide with them

4. **"The docs/tutorial used it"**
   - Fix: Many tutorials are poorly written
   - They use --no-cache to avoid caching issues in demos

---

### ❌ Anti-Pattern 1: No Volumes
```yaml
# BAD: Code baked into image
services:
  app:
    build: .
    # No volumes!
```

**Why bad:** Every code change = 5 minute rebuild

---

### ❌ Anti-Pattern 2: Mounting Everything
```yaml
# BAD: Mounts __pycache__, .git, etc.
volumes:
  - .:/app
```

**Better:**
```yaml
# GOOD: Selective mounts
volumes:
  - ./app:/app/app
  - ./static:/app/static
  - /app/.venv  # Exclude venv
```

---

### ❌ Anti-Pattern 3: Forgetting --reload
```yaml
# BAD: Changes require restart
command: uvicorn app:app
```

**Better:**
```yaml
# GOOD: Auto-restart on changes
command: uvicorn app:app --reload
```

---

### ❌ Anti-Pattern 4: No .dockerignore
```dockerfile
# BAD: Copies everything
COPY . .
```

**Result:** Huge build context, slow builds, bloated images

**Fix:** Create `.dockerignore` first!

---

## Time Savings Analysis

**Example: 100 code changes during development**

### Old Way (Rebuild Every Time)
```
100 changes × 5 minutes = 500 minutes
= 8.3 hours wasted
```

### New Way (Hot-Reload)
```
100 changes × 1 second = 100 seconds = 1.7 minutes
2 rebuilds (requirements.txt) × 5 min = 10 minutes
Total = 11.7 minutes
```

**Time Saved: 488 minutes = 8+ hours per project!**

Over 10 projects: **80+ hours saved** 🎉

---

## Framework-Specific Hot-Reload Commands

### Python (FastAPI/Django/Flask)
```yaml
# FastAPI/Flask
command: uvicorn app:app --reload

# Django
command: python manage.py runserver 0.0.0.0:8000
```

### Node.js (Express/Next.js)
```yaml
# Express with nodemon
command: nodemon server.js

# Next.js
command: npm run dev
```

### Go
```yaml
# Air for hot-reload
command: air -c .air.toml
```

### Rust
```yaml
# Cargo watch
command: cargo watch -x run
```

---

## Troubleshooting

### Changes Not Appearing?

**1. Check volume mount:**
```bash
docker inspect mycontainer | grep Mounts
```

**2. Check hot-reload enabled:**
```bash
docker logs mycontainer | grep reload
```

**3. Restart container:**
```bash
docker compose restart app
```

**4. Check file permissions (Linux/Mac):**
```bash
# Fix ownership
docker compose exec app chown -R appuser:appuser /app
```

---

### Port Already in Use?

**Find process:**
```powershell
# Windows
netstat -ano | findstr "8000"

# Linux/Mac
lsof -i :8000
```

**Change port in docker-compose.yml:**
```yaml
ports:
  - "8001:8000"  # Different host port
```

---

### Database Connection Fails (Native Dev)?

**1. Ensure DB container running:**
```bash
docker compose up -d db
```

**2. Check DB port:**
```bash
docker compose ps db
```

**3. Test connection:**
```bash
psql -h localhost -p 5433 -U user -d db
```

---

## Complete Example: FastAPI Project

### Project Structure
```
myproject/
├── .cursorrules              # References this pattern
├── .dockerignore             # Excludes junk
├── DOCKER_DEV_GUIDE.md       # Project-specific guide
├── docker-compose.yml        # Base config
├── docker-compose.dev.yml    # Dev overrides
├── run_dev.ps1               # Native dev script
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   └── ...
└── db/
    └── init-scripts/
        └── 01_init.sql
```

### docker-compose.yml
```yaml
services:
  db:
    image: postgres:15
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init-scripts:/docker-entrypoint-initdb.d
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: myapp
      POSTGRES_PASSWORD: myapp

  frontend:
    build:
      context: ./frontend
      target: dev
    environment:
      - DATABASE_URL=postgresql://myapp:myapp@db:5432/myapp
    depends_on:
      - db

volumes:
  postgres_data:
```

### docker-compose.dev.yml
```yaml
services:
  frontend:
    volumes:
      - ./frontend:/app
      - /app/.venv
    command: uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
```

### frontend/Dockerfile
```dockerfile
FROM python:3.11-slim as dev
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

FROM dev as prod
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

### .dockerignore
```
__pycache__/
*.pyc
.venv/
.git/
.pytest_cache/
*.log
```

### run_dev.ps1
```powershell
# Ensure DB running
docker compose up -d db
Start-Sleep -Seconds 5

# Setup venv
if (-not (Test-Path "frontend\.venv")) {
    cd frontend
    python -m venv .venv
    & .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    cd ..
}

# Run
cd frontend
& .\.venv\Scripts\Activate.ps1
$env:DATABASE_URL = "postgresql://myapp:myapp@localhost:5433/myapp"
uvicorn app:app --reload --port 8000
```

---

## Adoption Checklist

To implement this pattern in your project:

- [ ] Create `.dockerignore` file
- [ ] Add volume mounts to `docker-compose.yml`
- [ ] Add `--reload` flag to service commands
- [ ] Create `docker-compose.dev.yml` for dev overrides
- [ ] Create `run_dev.ps1` for native option
- [ ] Update `Dockerfile` with multi-stage build
- [ ] Enable BuildKit in environment
- [ ] Document in local `DOCKER_DEV_GUIDE.md`
- [ ] Add Docker dev rule to `.cursorrules`
- [ ] Train team on new workflow

---

## Related Patterns

- **[Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)** - Optimize image size
- **[BuildKit Cache](https://docs.docker.com/build/cache/)** - Speed up rebuilds
- **[Compose Override Files](https://docs.docker.com/compose/multiple-compose-files/)** - Separate dev/prod configs

---

## References

- [Docker Compose Best Practices](https://docs.docker.com/compose/production/)
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)
- [Python Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

---

**Last Updated:** 2025-12-04  
**Pattern Status:** Production Ready  
**Adoption:** mywienerlinien, myai, veogen  

**Never waste time on Docker rebuilds again!** 🚀

