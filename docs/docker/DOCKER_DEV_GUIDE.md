# Docker Development Guide: Stop Wasting Time on Rebuilds

**TL;DR:** Never wait 5 minutes for a Docker rebuild again. Use hot-reload + volume mounts. And **NEVER use `--no-cache` for code changes!**

---

## 🚨 CRITICAL: Stop Using --no-cache!

**Most common Docker mistake that wastes HOURS:**

```powershell
# ❌ WRONG: Takes 15 minutes, downloads entire internet
docker compose build --no-cache frontend

# ✅ RIGHT: Takes 30 seconds, uses cached dependencies
docker compose build frontend

# ✅ BEST: Takes 1 second, hot-reload handles it
# (Just save your .py file, no build needed!)
```

**When to use --no-cache:**
- ✅ `requirements.txt` changed AND regular build failed
- ✅ Final production build (once per deploy)
- ✅ Suspected cache corruption (rare)

**When NOT to use --no-cache (99% of the time):**
- ❌ Changed Python code (.py files)
- ❌ Changed HTML/CSS/JS files
- ❌ Changed config files (.env, .yaml)
- ❌ "Just to be safe" (it's not safer, just slower)

**Real cost:**
- Regular build: 30 seconds
- `--no-cache` build: 15 minutes
- **You waste 14.5 minutes every time!**

Over 20 rebuilds = **290 minutes = 4.8 hours wasted on nothing.**

---

## The Problem

**Before:**
```bash
# Change 3 lines of code
# Wait 5 minutes for rebuild
# Test
# Find bug
# Wait 5 minutes for rebuild
# Repeat 20 times = 100 minutes wasted
```

**After (with this guide):**
```bash
# Change 3 lines of code
# Save file
# See changes in 1 second
# Test
# Find bug
# Save file
# See changes in 1 second
# Repeat 20 times = 20 seconds total
```

---

## The Solution: Hot-Reload Development

### 1. Volume Mounts (Code Lives Outside Container)

**docker-compose.yml:**
```yaml
services:
  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app  # 👈 Mount code directory
    command: uvicorn app:app --reload  # 👈 Enable hot-reload
```

**What this does:**
- Code files live on your HOST machine
- Container reads from mounted volume
- Changes to host files = instant updates in container
- **No rebuild needed for code changes!**

**When you STILL need to rebuild:**
- ✅ Only when `requirements.txt` changes
- ✅ Only when `Dockerfile` changes
- ✅ Only when system dependencies change

**You DON'T need to rebuild for:**
- ❌ Python code changes (.py files)
- ❌ HTML/CSS/JS changes (static files)
- ❌ Config file changes (.env, .yaml)
- ❌ SQL files (if mounted)

---

### 2. Native Development (No Docker for Dev)

**Run outside Docker entirely:**

**Setup script (run_dev.ps1):**
```powershell
# One-time setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Set environment
$env:DATABASE_URL = "postgresql://user:pass@localhost:5433/db"

# Run with hot-reload
uvicorn app:app --reload --port 3080
```

**Benefits:**
- ⚡ Starts in 5 seconds (vs 5 minutes)
- 🔥 Native Python debugging
- 📊 Use database from Docker (port 5433)
- 🚀 Full IDE integration

**docker-compose.yml for database only:**
```yaml
services:
  db:
    image: postgres:15
    ports:
      - "5433:5432"  # 👈 Expose to host
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

---

## Advanced Tricks

### 3. Multi-Stage Builds (When You Do Rebuild)

**Dockerfile:**
```dockerfile
# Development stage (cached dependencies)
FROM python:3.11-slim as dev
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
# Note: No COPY of code here!

# Production stage (includes code)
FROM dev as prod
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

**Target dev stage in docker-compose.yml:**
```yaml
services:
  frontend:
    build:
      target: dev  # 👈 Stop at dev stage
    volumes:
      - ./frontend:/app  # 👈 Mount code
```

**Benefits:**
- Dependencies cached in `dev` stage
- Code mounted via volume
- Rebuilds only reinstall dependencies if `requirements.txt` changes

---

### 4. .dockerignore (Faster Builds)

**Create `.dockerignore`:**
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.venv/
venv/
ENV/

# Development
.git/
.gitignore
.vscode/
.idea/
*.log

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Docker
Dockerfile
docker-compose.yml
```

**Benefits:**
- Smaller build context
- Faster COPY operations
- Cleaner images

---

### 5. BuildKit Cache Mounts

**Enable BuildKit:**
```powershell
# PowerShell
$env:DOCKER_BUILDKIT = "1"

# Or in docker-compose.yml
services:
  frontend:
    build:
      context: .
      cache_from:
        - myapp:latest
```

**Dockerfile with cache mounts:**
```dockerfile
# Pip cache persists between builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Apt cache persists
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y gcc
```

**Benefits:**
- Pip downloads cached
- Apt packages cached
- Much faster rebuilds when dependencies DO change

---

### 6. Separate Dev/Prod Compose Files

**docker-compose.yml (base):**
```yaml
services:
  frontend:
    build: ./frontend
    environment:
      - DATABASE_URL=postgresql://...
```

**docker-compose.dev.yml (development overrides):**
```yaml
services:
  frontend:
    volumes:
      - ./frontend:/app  # 👈 Code mount
    command: uvicorn app:app --reload  # 👈 Hot-reload
    environment:
      - DEBUG=true
```

**docker-compose.prod.yml (production):**
```yaml
services:
  frontend:
    # No volumes (code baked in)
    command: uvicorn app:app --host 0.0.0.0
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

## Quick Reference: Build Commands

| What Changed | Command | Time | When to Use |
|--------------|---------|------|-------------|
| Python code (.py) | **No build!** Just save file | 1 sec | With hot-reload enabled (best) |
| Python code (.py) | `docker compose build frontend` | 30 sec | Without hot-reload |
| HTML/CSS/JS | **No build!** Refresh browser | 0 sec | Static files auto-update |
| requirements.txt | `docker compose build frontend` | 2-3 min | Dependencies changed |
| requirements.txt (build failed) | `docker compose build --no-cache frontend` | 15 min | Only if regular build failed |
| Dockerfile | `docker compose build frontend` | 2-3 min | Dockerfile changed |
| .env / .yaml | `docker compose restart frontend` | 5 sec | Config reload |

**Rule of Thumb:**
- 🟢 Code change? → Hot-reload or regular build (30 sec)
- 🟡 Dependency change? → Regular build (2-3 min)
- 🔴 **NEVER `--no-cache` for code!** → Wastes 15 min

---

## Quick Reference: When to Use What

### Use Hot-Reload (docker-compose with volumes):
- ✅ Daily development
- ✅ Testing full stack (DB, Redis, etc.)
- ✅ When you need container environment
- ✅ Team consistency

### Use Native Python (run_dev.ps1):
- ✅ Quick tests
- ✅ Debugging in IDE
- ✅ Fastest iteration
- ✅ When Docker is being annoying

### Use Full Rebuild:
- ✅ When `requirements.txt` changes
- ✅ When `Dockerfile` changes
- ✅ Before production deploy
- ✅ When troubleshooting weird issues

---

## MyWienerLinien Specific Commands

### Development Workflow
```powershell
# Option 1: Hot-reload in Docker (recommended)
docker compose up -d
# Edit files, save, see changes in 1 second

# Option 2: Native Python (fastest)
.\run_dev.ps1
# Edit files, save, see changes instantly

# When requirements.txt changes:
docker compose build frontend  # 3-5 minutes
docker compose up -d
```

### Production Deployment
```powershell
# Full rebuild
docker compose build --no-cache frontend

# Start
docker compose up -d

# Check logs
docker compose logs -f frontend
```

---

## Time Savings Calculator

**Example project: 100 code changes over development**

### Old Way (Rebuild Every Time):
- 100 changes × 5 minutes = **500 minutes = 8.3 hours**

### New Way (Hot-Reload):
- 100 changes × 1 second = **100 seconds = 1.7 minutes**
- 2 rebuilds (requirements.txt) × 5 minutes = **10 minutes**
- **Total: 11.7 minutes**

**Time Saved: 488 minutes = 8+ hours of your life back!** 🎉

---

## Common Mistakes

### ❌ Mistake 0: Using --no-cache When You Don't Need It

**THE WORST MISTAKE:**
```powershell
# BAD: Downloads half the internet every time (10+ minutes)
docker compose build --no-cache frontend

# GOOD: Uses cached layers (30 seconds - 2 minutes)
docker compose build frontend
```

**When to use --no-cache:**
- ✅ Only when `requirements.txt` changes
- ✅ Only when you suspect corrupted cache
- ✅ Only for production final builds
- ❌ NEVER for Python code changes (.py files)
- ❌ NEVER for static files (HTML/CSS/JS)
- ❌ NEVER for config changes (.env, .yaml)

**Why it's terrible:**
```
--no-cache with 50 dependencies:
1. Downloads 50 packages from PyPI (slow internet)
2. Compiles C extensions (CPU intensive)
3. Installs everything from scratch
4. Takes 10-20 minutes

Regular build with cache:
1. Uses cached pip packages ✅
2. Uses cached compiled extensions ✅
3. Only copies changed code
4. Takes 30 seconds - 2 minutes
```

**Decision Tree:**
```
Changed Python code (.py files)?
  → docker compose build  (30 sec)

Changed HTML/CSS/JS?
  → Don't rebuild at all! (hot-reload handles it)

Changed requirements.txt?
  → docker compose build  (2-3 min, uses cache where possible)
  → Only use --no-cache if build fails mysteriously

Changed Dockerfile?
  → docker compose build  (2-3 min)
```

**Time Comparison (50 dependencies):**
- Python code change + regular build: **30 seconds**
- Python code change + --no-cache: **15 minutes** ❌
- Python code change + hot-reload: **1 second** ✅

**You just wasted 14.5 minutes for no reason!**

---

### ❌ Mistake 1: Not using volumes
```yaml
# BAD: Code baked into image
services:
  app:
    build: .
    # No volumes
```

```yaml
# GOOD: Code mounted
services:
  app:
    build: .
    volumes:
      - ./app:/app
```

### ❌ Mistake 2: Forgetting --reload
```yaml
# BAD: Changes don't trigger restart
command: uvicorn app:app

# GOOD: Auto-restart on changes
command: uvicorn app:app --reload
```

### ❌ Mistake 3: Mounting everything
```yaml
# BAD: Mounts __pycache__, .git, etc.
volumes:
  - .:/app

# GOOD: Only mount what's needed
volumes:
  - ./app:/app
  - ./static:/static
```

### ❌ Mistake 4: No .dockerignore
```dockerfile
# BAD: Copies .git, __pycache__, etc.
COPY . .
```

**Solution: Create `.dockerignore` first!**

---

## Troubleshooting

### Changes not appearing?
1. Check volume mount: `docker inspect mycontainer | grep Mounts`
2. Check command has `--reload`: `docker logs mycontainer | grep reload`
3. Try restarting: `docker compose restart frontend`

### Port conflicts?
```bash
# Check what's using port
netstat -ano | findstr "3080"

# Change port in docker-compose.yml
ports:
  - "3081:3080"  # Use different host port
```

### Database connection fails (native dev)?
```bash
# Make sure DB container is running
docker compose up -d db

# Check DB is on correct port
docker compose ps db

# Test connection
psql -h localhost -p 5433 -U user -d db
```

---

## Further Reading

- [Docker Compose Best Practices](https://docs.docker.com/compose/production/)
- [BuildKit Cache](https://docs.docker.com/build/cache/)
- [Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)

---

**Last Updated:** 2025-12-04  
**Never suffer through another 5-minute rebuild again!** 🚀

