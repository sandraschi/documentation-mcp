"""Compliance checking functionality for MCP Standards Manager."""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor

from .core import StandardsManager, ComplianceResult, Violation


class ComplianceChecker:
    """Checks repositories for standards compliance."""

    def __init__(self, standards_manager: StandardsManager):
        self.standards_manager = standards_manager
        self.logger = logging.getLogger(__name__)

    def check_repository(self, repo_path: Path) -> ComplianceResult:
        """Check a single repository for compliance."""
        self.logger.info(f"Checking compliance for repository: {repo_path}")

        violations = []
        warnings = []

        # Check project structure
        violations.extend(self._check_project_structure(repo_path))

        # Check FastMCP version
        violations.extend(self._check_fastmcp_version(repo_path))

        # Check documentation
        violations.extend(self._check_documentation(repo_path))

        # Check code quality
        warnings.extend(self._check_code_quality(repo_path))

        # Check CI/CD setup
        warnings.extend(self._check_cicd_setup(repo_path))

        return self.standards_manager.create_compliance_result(
            repo_path, violations, warnings
        )

    def check_repositories_sequential(self, repositories: List[Path]) -> Dict[Path, ComplianceResult]:
        """Check multiple repositories sequentially."""
        results = {}
        for repo in repositories:
            try:
                results[repo] = self.check_repository(repo)
            except Exception as e:
                self.logger.error(f"Failed to check repository {repo}: {e}")
                # Create a result with critical violation
                results[repo] = ComplianceResult(
                    repository=repo,
                    violations=[Violation(
                        rule="repository_access",
                        message=f"Failed to access repository: {e}",
                        severity="error"
                    )],
                    warnings=[],
                    score=0.0
                )
        return results

    def check_repositories_parallel(self, repositories: List[Path]) -> Dict[Path, ComplianceResult]:
        """Check multiple repositories in parallel."""
        async def check_async():
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor(max_workers=min(len(repositories), 10)) as executor:
                tasks = []
                for repo in repositories:
                    task = loop.run_in_executor(
                        executor,
                        self.check_repository,
                        repo
                    )
                    tasks.append((repo, task))

                results = {}
                for repo, task in tasks:
                    try:
                        results[repo] = await task
                    except Exception as e:
                        self.logger.error(f"Failed to check repository {repo}: {e}")
                        results[repo] = ComplianceResult(
                            repository=repo,
                            violations=[Violation(
                                rule="repository_access",
                                message=f"Failed to access repository: {e}",
                                severity="error"
                            )],
                            warnings=[],
                            score=0.0
                        )
                return results

        return asyncio.run(check_async())

    def create_aggregate_report(self, results: Dict[Path, ComplianceResult]) -> ComplianceResult:
        """Create an aggregate report from multiple repository results."""
        all_violations = []
        all_warnings = []

        for result in results.values():
            all_violations.extend(result.violations)
            all_warnings.extend(result.warnings)

        # Calculate aggregate score
        total_score = sum(result.score for result in results.values())
        avg_score = total_score / len(results) if results else 0.0

        return ComplianceResult(
            repository=Path("aggregate_report"),
            violations=all_violations,
            warnings=all_warnings,
            score=avg_score
        )

    def save_report(self, result: ComplianceResult, output_path: Path) -> None:
        """Save a compliance result to file."""
        if output_path.suffix.lower() == '.json':
            content = result.to_json()
        elif output_path.suffix.lower() == '.html':
            content = result.to_html()
        else:
            content = result.to_text()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')

    def fix_violations(self, result: ComplianceResult) -> int:
        """Attempt to automatically fix violations."""
        fixed_count = 0

        for violation in result.violations:
            try:
                if self._can_auto_fix(violation):
                    self._apply_fix(violation, result.repository)
                    fixed_count += 1
                    self.logger.info(f"Auto-fixed violation: {violation.rule}")
            except Exception as e:
                self.logger.warning(f"Failed to auto-fix {violation.rule}: {e}")

        return fixed_count

    def initialize_compliance(self, repo_path: Path) -> None:
        """Initialize compliance tracking for a new repository."""
        # Create .mcp-standards.yaml file
        standards_file = repo_path / ".mcp-standards.yaml"

        if not standards_file.exists():
            config_data = {
                "repository": {
                    "type": "mcp-server",
                    "standards_version": self.standards_manager.config.standards_version,
                    "fastmcp_version": self.standards_manager.config.fastmcp_target_version
                },
                "compliance": {
                    "last_check": None,
                    "score": None,
                    "critical_violations": []
                }
            }

            import yaml
            with open(standards_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False)

    def _check_project_structure(self, repo_path: Path) -> List[Violation]:
        """Check basic project structure compliance."""
        violations = []

        required_files = [
            "README.md",
            "pyproject.toml",
        ]

        required_dirs = [
            "src",
            "tests"
        ]

        for file in required_files:
            if not (repo_path / file).exists():
                violations.append(Violation(
                    rule="project_structure",
                    message=f"Missing required file: {file}",
                    severity="error",
                    suggestion=f"Create {file} following standards templates"
                ))

        for dir_name in required_dirs:
            if not (repo_path / dir_name).is_dir():
                violations.append(Violation(
                    rule="project_structure",
                    message=f"Missing required directory: {dir_name}/",
                    severity="error",
                    suggestion=f"Create {dir_name}/ directory with appropriate structure"
                ))

        return violations

    def _check_fastmcp_version(self, repo_path: Path) -> List[Violation]:
        """Check FastMCP version compliance."""
        violations = []

        pyproject_path = repo_path / "pyproject.toml"
        if not pyproject_path.exists():
            return violations

        try:
            import tomli
            with open(pyproject_path, 'rb') as f:
                pyproject_data = tomli.load(f)

            dependencies = pyproject_data.get('project', {}).get('dependencies', [])

            fastmcp_version = None
            for dep in dependencies:
                if 'fastmcp' in dep:
                    # Extract version from string like "fastmcp>=2.14.3,<3.0.0"
                    import re
                    match = re.search(r'fastmcp([><=~!]+[^,]+)', dep)
                    if match:
                        fastmcp_version = match.group(1).strip('><=~!')
                    break

            if not fastmcp_version:
                violations.append(Violation(
                    rule="fastmcp_version",
                    message="No FastMCP dependency found in pyproject.toml",
                    severity="error",
                    file_path=pyproject_path,
                    suggestion="Add FastMCP dependency to pyproject.toml"
                ))
            elif not self.standards_manager.check_version_compatibility(fastmcp_version):
                required = self.standards_manager.get_required_fastmcp_version()
                violations.append(Violation(
                    rule="fastmcp_version",
                    message=f"FastMCP version {fastmcp_version} is below required {required}",
                    severity="error",
                    file_path=pyproject_path,
                    suggestion=f"Update FastMCP to version {required} or higher"
                ))

        except Exception as e:
            violations.append(Violation(
                rule="fastmcp_version",
                message=f"Failed to parse pyproject.toml: {e}",
                severity="warning",
                file_path=pyproject_path
            ))

        return violations

    def _check_documentation(self, repo_path: Path) -> List[Violation]:
        """Check documentation compliance."""
        violations = []

        required_docs = [
            "README.md",
            "INSTALL.md",
            "CHANGELOG.md"
        ]

        for doc in required_docs:
            doc_path = repo_path / doc
            if not doc_path.exists():
                violations.append(Violation(
                    rule="documentation",
                    message=f"Missing required documentation: {doc}",
                    severity="error",
                    suggestion=f"Create {doc} following standards templates"
                ))

        # Check docs/ directory
        docs_dir = repo_path / "docs"
        if not docs_dir.is_dir():
            violations.append(Violation(
                rule="documentation",
                message="Missing docs/ directory",
                severity="warning",
                suggestion="Create docs/ directory with integration guides"
            ))

        return violations

    def _check_code_quality(self, repo_path: Path) -> List[str]:
        """Check code quality (warnings only)."""
        warnings = []

        # Check for common issues
        python_files = list(repo_path.rglob("*.py"))
        if len(python_files) > 50:
            warnings.append("Large number of Python files - consider organizing into packages")

        # Check for __pycache__ directories
        pycache_dirs = list(repo_path.rglob("__pycache__"))
        if pycache_dirs:
            warnings.append("Found __pycache__ directories - add to .gitignore")

        return warnings

    def _check_cicd_setup(self, repo_path: Path) -> List[str]:
        """Check CI/CD setup (warnings only)."""
        warnings = []

        github_workflows = repo_path / ".github" / "workflows"
        if not github_workflows.is_dir():
            warnings.append("No GitHub Actions workflows found - consider adding CI/CD")

        return warnings

    def _can_auto_fix(self, violation: Violation) -> bool:
        """Check if a violation can be automatically fixed."""
        return violation.rule in ["fastmcp_version"]

    def _apply_fix(self, violation: Violation, repo_path: Path) -> None:
        """Apply an automatic fix for a violation."""
        if violation.rule == "fastmcp_version":
            # This would update the pyproject.toml file
            # Implementation would depend on the specific violation details
            pass