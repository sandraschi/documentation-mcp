"""Cross-reference index parser and utilities"""

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class CrossReferenceParser:
    """Parse and utilize CROSS_REFERENCE_INDEX.md for intelligent linking"""

    def __init__(self, docs_root: Path):
        self.docs_root = docs_root
        self.cross_ref_path = docs_root / "CROSS_REFERENCE_INDEX.md"
        self.index_cache = None

    def parse_cross_reference_index(self) -> dict[str, Any]:
        """Parse CROSS_REFERENCE_INDEX.md into structured data"""
        if self.index_cache:
            return self.index_cache

        if not self.cross_ref_path.exists():
            logger.warning(f"Cross-reference index not found: {self.cross_ref_path}")
            return {}

        try:
            with open(self.cross_ref_path, encoding="utf-8") as f:
                content = f.read()

            parsed = self._parse_markdown_sections(content)
            self.index_cache = parsed
            return parsed

        except Exception as e:
            logger.error(f"Failed to parse cross-reference index: {e}")
            return {}

    def _parse_markdown_sections(self, content: str) -> dict[str, Any]:
        """Parse markdown sections into structured data"""
        sections = {}
        current_section = None
        current_content = []

        lines = content.split("\n")
        for line in lines:
            if line.startswith("### "):
                # Save previous section
                if current_section:
                    sections[current_section] = "\n".join(current_content)

                # Start new section
                current_section = line[4:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content)

        return sections

    def get_topic_references(self, topic: str) -> dict[str, list[str]]:
        """Get all cross-references for a specific topic"""
        index = self.parse_cross_reference_index()

        # Look for topic sections (case-insensitive)
        topic_lower = topic.lower()

        for section_name, section_content in index.items():
            if topic_lower in section_name.lower():
                return self._extract_references_from_section(section_content)

        return {"error": f"No cross-references found for: {topic}"}

    def _extract_references_from_section(self, content: str) -> dict[str, list[str]]:
        """Extract references from a section content"""
        references = {
            "primary_location": [],
            "all_references": [],
            "warnings": [],
            "search_commands": [],
        }

        lines = content.split("\n")
        current_key = None

        for line in lines:
            line = line.strip()

            # Identify keys
            if line.startswith("**Primary Location**"):
                current_key = "primary_location"
            elif line.startswith("**All References**"):
                current_key = "all_references"
            elif line.startswith("**Warning**"):
                current_key = "warnings"
            elif line.startswith("**Search Command**"):
                current_key = "search_commands"
            # Extract references
            elif line.startswith("- ") and current_key:
                reference = line[2:].strip()
                # Clean up markdown formatting
                reference = re.sub(r"`([^`]+)`", r"\1", reference)
                reference = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", reference)
                references[current_key].append(reference)

        return references

    def check_version_references(self, content: str) -> list[dict[str, str]]:
        """Check for outdated version references in content"""
        issues = []

        # Look for FastMCP version references
        fastmcp_pattern = r"FastMCP\s+([0-9]+\.[0-9]+)"
        matches = re.findall(fastmcp_pattern, content, re.IGNORECASE)

        for version in matches:
            if version < "2.13":
                issues.append(
                    {
                        "type": "outdated_version",
                        "version": f"FastMCP {version}",
                        "severity": "high",
                        "recommendation": "Update to FastMCP 2.13+",
                    }
                )
            elif version < "2.14":
                issues.append(
                    {
                        "type": "stale_version",
                        "version": f"FastMCP {version}",
                        "severity": "medium",
                        "recommendation": "Consider updating to FastMCP 2.14+",
                    }
                )

        return issues

    def get_related_topics(self, topic: str) -> list[str]:
        """Find topics related to the given topic"""
        index = self.parse_cross_reference_index()
        related = []

        topic_lower = topic.lower()

        # Search for topic mentions across all sections
        for section_name, section_content in index.items():
            if topic_lower in section_content.lower() and topic_lower not in section_name.lower():
                related.append(section_name)

        return related

    def update_cross_reference(self, topic: str, new_references: list[str]):
        """Update cross-reference index with new references"""
        # This would be used to maintain the cross-reference index
        # when new documentation is added
        logger.info(f"Updating cross-references for: {topic}")

        # Implementation would:
        # 1. Parse existing index
        # 2. Find or create section for topic
        # 3. Add new references
        # 4. Write updated index back to file

        pass


# Global parser instance
cross_ref_parser = None


def get_cross_ref_parser(docs_root: Path | None = None) -> CrossReferenceParser:
    """Get or create cross-reference parser instance"""
    global cross_ref_parser

    if cross_ref_parser is None:
        if docs_root is None:
            docs_root = Path(__file__).parent.parent.parent.parent
        cross_ref_parser = CrossReferenceParser(docs_root)

    return cross_ref_parser
