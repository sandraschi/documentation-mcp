"""Repository management functionality."""

import logging
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

from .core import StandardsManager


class RepositoryManager:
    """Manages MCP repositories and their standards compliance."""

    def __init__(self, standards_manager: StandardsManager):
        self.standards_manager = standards_manager
        self.logger = logging.getLogger(__name__)

    def discover_repositories(self, base_path: Path) -> List[Path]:
        """Discover MCP repositories in a directory."""
        repositories = []

        if not base_path.exists():
            self.logger.warning(f"Base path does not exist: {base_path}")
            return repositories

        # Look for directories that look like MCP repositories
        for item in base_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if self._is_mcp_repository(item):
                    repositories.append(item)

        self.logger.info(f"Discovered {len(repositories)} MCP repositories")
        return repositories

    def create_repository(
        self,
        repo_path: Path,
        repo_type: str,
        template: str = "python"
    ) -> None:
        """Create a new MCP repository with proper structure."""
        self.logger.info(f"Creating {repo_type} repository at {repo_path}")

        repo_path.mkdir(parents=True, exist_ok=True)

        # Create basic directory structure
        self._create_directory_structure(repo_path, repo_type)

        # Generate basic files
        self._generate_basic_files(repo_path, repo_type, template)

        # Initialize git repository
        self._initialize_git_repo(repo_path)

        self.logger.info(f"Repository created successfully: {repo_path}")

    def update_fastmcp_version(self, repo_path: Path, version: str, dry_run: bool = False) -> bool:
        """Update FastMCP version in repository."""
        pyproject_path = repo_path / "pyproject.toml"

        if not pyproject_path.exists():
            self.logger.warning(f"No pyproject.toml found in {repo_path}")
            return False

        try:
            import tomli
            with open(pyproject_path, 'rb') as f:
                data = tomli.load(f)

            # Update dependencies
            dependencies = data.get('project', {}).get('dependencies', [])
            updated = False

            for i, dep in enumerate(dependencies):
                if 'fastmcp' in dep:
                    # Update version constraint
                    new_dep = f"fastmcp>={version},<3.0.0"
                    if dep != new_dep:
                        dependencies[i] = new_dep
                        updated = True
                        break

            if updated and not dry_run:
                data['project']['dependencies'] = dependencies

                import tomllib
                with open(pyproject_path, 'wb') as f:
                    # This is a simplified write - in practice you'd use tomli_w
                    import tomli_w
                    tomli_w.dump(data, f)

                self.logger.info(f"Updated FastMCP version to {version} in {repo_path}")
                return True
            elif updated and dry_run:
                self.logger.info(f"Would update FastMCP version to {version} in {repo_path}")
                return True

        except Exception as e:
            self.logger.error(f"Failed to update FastMCP version in {repo_path}: {e}")

        return False

    def get_repository_status(self, repo_path: Path) -> Dict[str, Any]:
        """Get comprehensive status of a repository."""
        status = {
            "type": "unknown",
            "standards_version": "unknown",
            "fastmcp_version": "unknown",
            "has_docs": False,
            "has_tests": False,
            "has_cicd": False,
            "has_monitoring": False,
            "last_commit": None,
            "branch": None
        }

        # Check repository type
        if (repo_path / "pyproject.toml").exists():
            status["type"] = "mcp-server"

        # Check standards file
        standards_file = repo_path / ".mcp-standards.yaml"
        if standards_file.exists():
            try:
                import yaml
                with open(standards_file, 'r') as f:
                    standards_data = yaml.safe_load(f)
                status["standards_version"] = standards_data.get("repository", {}).get("standards_version", "unknown")
                status["fastmcp_version"] = standards_data.get("repository", {}).get("fastmcp_version", "unknown")
            except Exception:
                pass

        # Check documentation
        status["has_docs"] = (repo_path / "docs").is_dir()
        status["has_tests"] = (repo_path / "tests").is_dir()

        # Check CI/CD
        status["has_cicd"] = (repo_path / ".github" / "workflows").is_dir()

        # Check monitoring (basic check for config files)
        monitoring_files = ["docker-compose.yml", "prometheus.yml", "grafana.yml"]
        status["has_monitoring"] = any((repo_path / f).exists() for f in monitoring_files)

        # Get git info
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%H %s"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                commit_hash, commit_msg = result.stdout.strip().split(' ', 1)
                status["last_commit"] = f"{commit_hash[:8]}: {commit_msg}"

            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                status["branch"] = result.stdout.strip()

        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Git not available or not a git repo
            pass

        return status

    def setup_cicd(self, repo_path: Path) -> None:
        """Set up CI/CD for a repository."""
        workflows_dir = repo_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)

        # Create basic CI workflow
        ci_workflow = workflows_dir / "ci.yml"
        if not ci_workflow.exists():
            ci_content = """name: CI

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
"""
            ci_workflow.write_text(ci_content, encoding='utf-8')
            self.logger.info(f"Created CI workflow for {repo_path.name}")

    def setup_monitoring(self, repo_path: Path) -> None:
        """Set up basic monitoring for a repository."""
        # Create docker-compose for monitoring
        docker_compose = repo_path / "docker-compose.monitoring.yml"
        if not docker_compose.exists():
            monitoring_content = """version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3100:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data:
"""
            docker_compose.write_text(monitoring_content, encoding='utf-8')
            self.logger.info(f"Created monitoring setup for {repo_path.name}")

    def _is_mcp_repository(self, repo_path: Path) -> bool:
        """Check if a directory is an MCP repository."""
        # Check for common MCP repository indicators
        indicators = [
            "pyproject.toml",  # Python project
            "src/",           # Source code directory
            "fastmcp"         # FastMCP in dependencies
        ]

        # Must have pyproject.toml
        if not (repo_path / "pyproject.toml").exists():
            return False

        # Check for FastMCP in dependencies
        try:
            import tomli
            with open(repo_path / "pyproject.toml", 'rb') as f:
                data = tomli.load(f)

            dependencies = data.get('project', {}).get('dependencies', [])
            has_fastmcp = any('fastmcp' in dep for dep in dependencies)

            if has_fastmcp:
                return True
        except Exception:
            pass

        # Check for MCP-specific files
        mcp_files = ["mcpb/", ".mcp-standards.yaml"]
        for mcp_file in mcp_files:
            if (repo_path / mcp_file).exists():
                return True

        return False

    def _create_directory_structure(self, repo_path: Path, repo_type: str) -> None:
        """Create basic directory structure for repository."""
        directories = [
            "src",
            "tests",
            "docs",
            "docs/api",
            "docs/integrations",
            "scripts"
        ]

        if repo_type == "mcp-server":
            directories.extend([
                ".github/workflows",
                "mcpb"
            ])

        for dir_path in directories:
            (repo_path / dir_path).mkdir(parents=True, exist_ok=True)

    def _generate_basic_files(self, repo_path: Path, repo_type: str, template: str) -> None:
        """Generate basic files for repository."""
        repo_name = repo_path.name

        # pyproject.toml
        pyproject_content = f"""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{repo_name}"
version = "0.1.0"
description = "{repo_name} - MCP server"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "fastmcp>=2.14.3,<3.0.0",
]

[project.scripts]
{repo_name.replace('-', '_')} = "{repo_name.replace('-', '_')}.cli:main"
"""
        (repo_path / "pyproject.toml").write_text(pyproject_content, encoding='utf-8')

        # Basic __init__.py
        init_content = f'''"""MCP server for {repo_name}."""

__version__ = "0.1.0"
'''
        (repo_path / "src" / repo_name.replace('-', '_') / "__init__.py").mkdir(parents=True, exist_ok=True)
        (repo_path / "src" / repo_name.replace('-', '_') / "__init__.py").write_text(init_content, encoding='utf-8')

    def _initialize_git_repo(self, repo_path: Path) -> None:
        """Initialize git repository."""
        try:
            subprocess.run(
                ["git", "init"],
                cwd=repo_path,
                check=True,
                capture_output=True
            )

            # Create .gitignore
            gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Distribution
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
"""
            (repo_path / ".gitignore").write_text(gitignore_content, encoding='utf-8')

            # Initial commit
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                check=True
            )

        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to initialize git repo: {e}")
        except FileNotFoundError:
            self.logger.warning("Git not available, skipping repository initialization")