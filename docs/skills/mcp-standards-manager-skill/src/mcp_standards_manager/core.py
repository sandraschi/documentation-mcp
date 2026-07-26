"""Core MCP Standards Manager functionality."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .config import Config


@dataclass
class StandardsVersion:
    """Represents a standards version."""
    version: str
    fastmcp_minimum: str
    features: List[str]
    deprecated: List[str]


@dataclass
class ComplianceResult:
    """Result of a compliance check."""
    repository: Path
    violations: List['Violation']
    warnings: List[str]
    score: float  # 0.0 to 1.0

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps({
            'repository': str(self.repository),
            'violations': [v.to_dict() for v in self.violations],
            'warnings': self.warnings,
            'score': self.score
        }, indent=2)

    def to_html(self) -> str:
        """Convert to HTML report."""
        html = f"""
        <html>
        <head><title>Compliance Report - {self.repository.name}</title></head>
        <body>
            <h1>Standards Compliance Report</h1>
            <h2>Repository: {self.repository.name}</h2>
            <p>Compliance Score: {self.score:.1%}</p>

            <h3>Violations ({len(self.violations)})</h3>
            <ul>
        """

        for violation in self.violations:
            html += f"<li><strong>{violation.rule}:</strong> {violation.message}</li>"

        html += """
            </ul>

            <h3>Warnings</h3>
            <ul>
        """

        for warning in self.warnings:
            html += f"<li>{warning}</li>"

        html += """
            </ul>
        </body>
        </html>
        """

        return html

    def to_text(self) -> str:
        """Convert to text report."""
        lines = [
            f"Standards Compliance Report - {self.repository.name}",
            "=" * 60,
            f"Compliance Score: {self.score:.1%}",
            "",
            f"Violations ({len(self.violations)}):"
        ]

        for violation in self.violations:
            lines.append(f"  - {violation.rule}: {violation.message}")

        lines.extend(["", f"Warnings ({len(self.warnings)}):"])
        for warning in self.warnings:
            lines.append(f"  - {warning}")

        return "\n".join(lines)


@dataclass
class Violation:
    """Represents a standards violation."""
    rule: str
    message: str
    severity: str  # 'error', 'warning', 'info'
    file_path: Optional[Path] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'rule': self.rule,
            'message': self.message,
            'severity': self.severity,
            'file_path': str(self.file_path) if self.file_path else None,
            'line_number': self.line_number,
            'suggestion': self.suggestion
        }


class StandardsManager:
    """Core standards management functionality."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config = Config.load(config_path)
        self.logger = logging.getLogger(__name__)

        # Define available standards versions
        self.standards_versions = {
            "1.8": StandardsVersion(
                version="1.8",
                fastmcp_minimum="2.14.3",
                features=[
                    "AI Workflow Sampling",
                    "Modular Documentation",
                    "Enhanced Error Handling",
                    "Comprehensive Testing Standards"
                ],
                deprecated=[]
            ),
            "1.7": StandardsVersion(
                version="1.7",
                fastmcp_minimum="2.14.3",
                features=[
                    "AI Workflow Sampling",
                    "Enhanced Response Patterns"
                ],
                deprecated=[]
            )
        }

    def get_current_standards(self) -> StandardsVersion:
        """Get current standards version."""
        return self.standards_versions[self.config.standards_version]

    def validate_fastmcp_version(self, version: str) -> bool:
        """Validate FastMCP version string."""
        # Basic semantic version validation
        import re
        pattern = r'^\d+\.\d+\.\d+$'
        return bool(re.match(pattern, version))

    def get_required_fastmcp_version(self) -> str:
        """Get minimum required FastMCP version."""
        return self.get_current_standards().fastmcp_minimum

    def check_version_compatibility(self, current_version: str) -> bool:
        """Check if a version meets minimum requirements."""
        if not self.validate_fastmcp_version(current_version):
            return False

        required = self.get_required_fastmcp_version()

        # Simple version comparison
        current_parts = [int(x) for x in current_version.split('.')]
        required_parts = [int(x) for x in required.split('.')]

        return current_parts >= required_parts

    def get_available_features(self, version: Optional[str] = None) -> List[str]:
        """Get features available in a standards version."""
        if version is None:
            version = self.config.standards_version

        standards = self.standards_versions.get(version)
        return standards.features if standards else []

    def get_deprecated_features(self, version: Optional[str] = None) -> List[str]:
        """Get deprecated features in a standards version."""
        if version is None:
            version = self.config.standards_version

        standards = self.standards_versions.get(version)
        return standards.deprecated if standards else []

    def create_compliance_result(
        self,
        repository: Path,
        violations: List[Violation],
        warnings: List[str]
    ) -> ComplianceResult:
        """Create a compliance result with calculated score."""
        # Calculate score based on violations
        total_checks = len(violations) + len(warnings) + 1  # +1 for basic compliance
        violation_penalty = len(violations) * 0.2  # Each violation reduces score by 20%
        warning_penalty = len(warnings) * 0.05   # Each warning reduces score by 5%

        score = max(0.0, 1.0 - violation_penalty - warning_penalty)

        return ComplianceResult(
            repository=repository,
            violations=violations,
            warnings=warnings,
            score=score
        )

    def get_standards_documentation_url(self, section: Optional[str] = None) -> str:
        """Get URL to standards documentation."""
        base_url = "https://github.com/sandraschi/mcp-central-docs/blob/main"

        if section:
            return f"{base_url}/docs/standards/{section}.md"
        else:
            return f"{base_url}/STANDARDS.md"

    def get_template_path(self, template_name: str) -> Path:
        """Get path to a standards template."""
        templates_dir = Path(__file__).parent / "templates"
        return templates_dir / f"{template_name}.template"

    def list_available_templates(self) -> List[str]:
        """List available standards templates."""
        templates_dir = Path(__file__).parent / "templates"

        if not templates_dir.exists():
            return []

        return [f.stem for f in templates_dir.glob("*.template")]