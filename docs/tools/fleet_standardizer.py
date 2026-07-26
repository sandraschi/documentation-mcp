import re
import json
import argparse
import subprocess
from pathlib import Path

# SOTA v13.1 Deployment Templates
RUFF_CONFIG_TEMPLATE = """
[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "S", "UP", "RUF"]
ignore = ["S101", "B008"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
"""

JUST_DASHBOARD_TEMPLATE = r"""set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

# ── Dashboard ─────────────────────────────────────────────────────────────────

# Display the SOTA Industrial Dashboard
default:
    @$lines = Get-Content '{{justfile()}}'; \
    Write-Host ' [SOTA] Industrial Operations Dashboard v1.3.2' -ForegroundColor White -BackgroundColor Cyan; \
    Write-Host '' ; \
    $currentCategory = ''; \
    foreach ($line in $lines) { \
        if ($line -match '^# ── ([^─]+) ─') { \
            $currentCategory = $matches[1].Trim(); \
            Write-Host "`n  $currentCategory" -ForegroundColor Cyan; \
            Write-Host ('  ' + ('─' * 45)) -ForegroundColor Gray; \
        } elseif ($line -match '^# ([^─].+)') { \
            $desc = $matches[1].Trim(); \
            $idx = [array]::IndexOf($lines, $line); \
            if ($idx -lt $lines.Count - 1) { \
                $nextLine = $lines[$idx + 1]; \
                if ($nextLine -match '^([a-z0-9-]+):') { \
                    $recipe = $matches[1]; \
                    $pad = ' ' * [math]::Max(2, (18 - $recipe.Length)); \
                    Write-Host "    $recipe" -ForegroundColor White -NoNewline; \
                    Write-Host "$pad$desc" -ForegroundColor Gray; \
                } \
            } \
        } \
    } \
    Write-Host "`n  [System State: PROD/HARDENED]" -ForegroundColor DarkGray; \
    Write-Host ''

# ── Quality ───────────────────────────────────────────────────────────────────

# Execute Ruff SOTA v13.1 linting
lint:
    Set-Location '{{justfile_directory()}}'
    uv run ruff check .

# Execute Ruff SOTA v13.1 fix and formatting
fix:
    Set-Location '{{justfile_directory()}}'
    uv run ruff check . --fix --unsafe-fixes
    uv run ruff format .

# ── Hardening ─────────────────────────────────────────────────────────────────

# Execute Bandit security audit
check-sec:
    Set-Location '{{justfile_directory()}}'
    uv run bandit -r src/

# Execute safety audit of dependencies
audit-deps:
    Set-Location '{{justfile_directory()}}'
    uv run safety check
"""

class FleetStandardizer:
    def __init__(self, registry_path, dry_run=True):
        self.registry_path = Path(registry_path)
        self.dry_run = dry_run
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            self.registry = json.load(f)

    def standardize_repo(self, repo, commit=False):
        repo_path = Path(repo.get('repo_path') or repo.get('path'))
        if not repo_path.exists():
            print(f"[ERROR] Repo not found: {repo['name']} at {repo_path}")
            return

        print(f"\n[STANDARDIZING] {repo['name']} ({repo.get('category', 'N/A')})")
        
        # Core Standardization Steps
        self._upgrade_ruff(repo_path)
        self._harden_just(repo_path)
        self._sanitize_readme(repo_path)
        self._audit_axios(repo_path)
        
        if commit and not self.dry_run:
            self._git_commit(repo_path, "meta: industrial standardization (SOTA v13.1 + Dashboard v1.3.2)")

    def _upgrade_ruff(self, repo_path):
        toml_path = repo_path / "pyproject.toml"
        if not toml_path.exists():
            return

        content = toml_path.read_text(encoding='utf-8')
        
        # Identify existing ruff blocks and remove them
        lines = content.splitlines()
        new_lines = []
        skip = False
        for line in lines:
            if line.strip().startswith("[tool.ruff"):
                skip = True
                continue
            if skip and line.strip().startswith("["):
                skip = False
            
            if not skip:
                new_lines.append(line)
        
        cleaned_content = "\n".join(new_lines).strip()
        final_content = cleaned_content + "\n\n" + RUFF_CONFIG_TEMPLATE.strip() + "\n"
        
        if self.dry_run:
            print("   [DRY] Would upgrade pyproject.toml to Ruff v13.1")
        else:
            toml_path.write_text(final_content, encoding="utf-8")
            print("   [DONE] pyproject.toml upgraded")

    def _harden_just(self, repo_path: Path):
        justfile_path = repo_path / "justfile"
        if not justfile_path.exists():
            return

        content = justfile_path.read_text(encoding="utf-8")
        
        # 1. Strip all previous SOTA dashboard markers and recipes
        sota_recipes = ["default", "lint", "fix", "check-sec", "audit-deps"]
        
        lines = content.splitlines()
        new_lines = []
        skip_mode = False
        
        for line in lines:
            # Skip existing shell settings (will re-add at top)
            if line.strip().startswith("set windows-shell :="):
                continue
                
            # Skip Category Headers we use
            if re.match(r"^# ── (Dashboard|Quality|Hardening|SOTA) ─", line):
                continue
                
            # Check for recipe start
            m = re.match(r"^([a-z0-9-]+):", line.strip())
            if m:
                recipe_name = m.group(1)
                if recipe_name in sota_recipes:
                    skip_mode = True
                    continue
                else:
                    skip_mode = False
            
            # If in skip mode, skip indented lines and empty lines
            if skip_mode:
                if line.startswith(" ") or line.startswith("\t") or line.strip() == "":
                    continue
                else:
                    skip_mode = False
                    
            # Skip specific description lines for SOTA recipes
            if line.strip().startswith("# Display the SOTA Industrial") or \
               line.strip().startswith("# Execute Ruff SOTA") or \
               line.strip().startswith("# Execute Bandit") or \
               line.strip().startswith("# Execute safety"):
                continue

            new_lines.append(line)
            
        cleaned_content = "\n".join(new_lines).strip()
        while "\n\n\n" in cleaned_content:
            cleaned_content = cleaned_content.replace("\n\n\n", "\n\n")
            
        # 2. Prepend the new template
        final_content = JUST_DASHBOARD_TEMPLATE.strip() + "\n\n" + cleaned_content
        final_content = final_content.strip() + "\n"
        
        if self.dry_run:
            print(f"   [DRY] Would upgrade Justfile in {repo_path.name}")
        else:
            justfile_path.write_text(final_content, encoding="utf-8")
            print(f"   [DONE] Justfile standardized in {repo_path.name}")

    def _sanitize_readme(self, repo_path):
        readme_path = repo_path / "README.md"
        if not readme_path.exists():
            return

        content = readme_path.read_text(encoding='utf-8')
        
        # Zero Rahrah Sanitization
        new_content = re.sub(r'[^\x00-\x7F]+', '', content)
        fluff = ["awesome", "amazing", "exciting", "incredible", "revolutionary", "best", "perfect"]
        for word in fluff:
            new_content = re.compile(re.escape(word), re.IGNORECASE).sub("", new_content)

        new_content = re.sub(r'^#\s+', '# ', new_content, flags=re.MULTILINE)

        if self.dry_run:
            print("   [DRY] Would sanitize README (Zero Rahrah)")
        else:
            readme_path.write_text(new_content, encoding="utf-8")
            print("   [DONE] README sanitized")

    def _audit_axios(self, repo_path):
        pkg_path = repo_path / "package.json"
        if not pkg_path.exists():
            return

        with open(pkg_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return
        
        deps = data.get('dependencies', {})
        dev_deps = data.get('devDependencies', {})
        
        all_deps = {**deps, **dev_deps}
        if 'axios' in all_deps:
            version = all_deps['axios']
            if "1.14.1" in version or "0.30.4" in version:
                print(f"   [CRITICAL] Compromised Axios version detected: {version}")
                if not self.dry_run:
                    if "axios" in deps:
                        deps["axios"] = "1.14.0"
                    if "axios" in dev_deps:
                        dev_deps["axios"] = "1.14.0"
                    with open(pkg_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                    print("   [FIXED] Axios downgraded to 1.14.0")

    def _git_commit(self, repo_path, message):
        git_dir = repo_path / ".git"
        if not git_dir.exists():
            print(f"   [SKIP] Not a git repository: {repo_path.name}")
            return
            
        try:
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True, capture_output=True)
            print(f"   [DONE] Committed changes in {repo_path.name}")
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in e.stderr.decode().lower():
                print(f"   [SKIP] Nothing to commit in {repo_path.name}")
            else:
                print(f"   [ERROR] Git commit failed in {repo_path.name}: {e.stderr.decode()}")

    def run(self, category=None, commit=False):
        for repo in self.registry['fleet']:
            if category and repo.get('category') != category:
                continue
            self.standardize_repo(repo, commit=commit)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Industrial Fleet Standardizer v13.1")
    parser.add_argument("--registry", default="../operations/fleet-registry.json", help="Path to fleet registry")
    parser.add_argument("--category", help="Target category (AI, Dev, Infra, etc.)")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    parser.add_argument("--commit", action="store_true", help="Git add and commit changes")
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    reg_path = (script_dir / args.registry).resolve()
    
    standardizer = FleetStandardizer(reg_path, dry_run=not args.apply)
    standardizer.run(category=args.category, commit=args.commit)
