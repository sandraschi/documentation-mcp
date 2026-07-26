"""MCP Standards Manager - Automated MCP ecosystem standards management."""

__version__ = "1.0.0"
__author__ = "MCP Community"
__email__ = "standards@mcp.community"

from .core import StandardsManager
from .compliance import ComplianceChecker
from .documentation import DocumentationManager
from .repository import RepositoryManager

__all__ = [
    "StandardsManager",
    "ComplianceChecker",
    "DocumentationManager",
    "RepositoryManager",
]