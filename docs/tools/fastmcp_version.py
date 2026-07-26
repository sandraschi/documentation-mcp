"""Parse declared FastMCP dependency version from pyproject.toml text (PEP 621, Poetry-style)."""

from __future__ import annotations

import re
from pathlib import Path


def parse_fastmcp_version_from_text(text: str) -> str | None:
    """Return the first version-like token for a fastmcp dependency, or None."""
    patterns = (
        # PEP 621 / uv: "fastmcp>=3.1" or fastmcp>=3.1.0,<4
        r"fastmcp\s*(?:\[[^\]]*\])?\s*(?:>=|==|~=)\s*[\"']?([\d.]+)",
        # Poetry / loose: fastmcp = "^3.1.0"
        r"(?m)^\s*fastmcp\s*=\s*[\"']?\^?([\d.]+)",
    )
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def parse_fastmcp_version_from_pyproject(pyproject_path: Path) -> str | None:
    if not pyproject_path.is_file():
        return None
    try:
        text = pyproject_path.read_text(encoding="utf-8")
    except OSError:
        return None
    return parse_fastmcp_version_from_text(text)
