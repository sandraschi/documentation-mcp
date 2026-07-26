"""Configuration management for MCP Standards Manager."""

import os
from pathlib import Path
from typing import List, Optional
import yaml


class Config:
    """Configuration for MCP Standards Manager."""

    def __init__(
        self,
        standards_version: str = "1.8",
        repositories: Optional[List[Path]] = None,
        fastmcp_target_version: str = "2.14.3",
        auto_update: bool = False,
        documentation_auto_generate: bool = True,
        validate_links: bool = True,
        monitoring_enabled: bool = True,
        dashboard_url: str = "http://localhost:3100"
    ):
        self.standards_version = standards_version
        self.repositories = repositories or []
        self.fastmcp_target_version = fastmcp_target_version
        self.auto_update = auto_update
        self.documentation_auto_generate = documentation_auto_generate
        self.validate_links = validate_links
        self.monitoring_enabled = monitoring_enabled
        self.dashboard_url = dashboard_url

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> 'Config':
        """Load configuration from file or use defaults."""
        if config_path and config_path.exists():
            return cls._load_from_file(config_path)

        # Try default locations
        default_paths = [
            Path.home() / ".mcp-standards" / "config.yaml",
            Path.home() / ".config" / "mcp-standards" / "config.yaml",
            Path.cwd() / ".mcp-standards.yaml"
        ]

        for path in default_paths:
            if path.exists():
                return cls._load_from_file(path)

        # Use defaults
        return cls()

    @classmethod
    def _load_from_file(cls, config_path: Path) -> 'Config':
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Convert string paths to Path objects
            repositories = []
            if 'repositories' in data:
                for repo_path in data['repositories']:
                    if isinstance(repo_path, str):
                        repositories.append(Path(repo_path))
                    elif isinstance(repo_path, dict) and 'path' in repo_path:
                        repositories.append(Path(repo_path['path']))

            return cls(
                standards_version=data.get('standards', {}).get('version', '1.8'),
                repositories=repositories,
                fastmcp_target_version=data.get('fastmcp', {}).get('target_version', '2.14.3'),
                auto_update=data.get('fastmcp', {}).get('auto_update', False),
                documentation_auto_generate=data.get('documentation', {}).get('auto_generate', True),
                validate_links=data.get('documentation', {}).get('validate_links', True),
                monitoring_enabled=data.get('monitoring', {}).get('enabled', True),
                dashboard_url=data.get('monitoring', {}).get('dashboard_url', 'http://localhost:3100')
            )
        except Exception as e:
            # Log warning and use defaults
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to load config from {config_path}: {e}")
            return cls()

    def save(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        if not config_path:
            config_path = Path.home() / ".mcp-standards" / "config.yaml"

        config_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'standards': {
                'version': self.standards_version
            },
            'repositories': [str(path) for path in self.repositories],
            'fastmcp': {
                'target_version': self.fastmcp_target_version,
                'auto_update': self.auto_update
            },
            'documentation': {
                'auto_generate': self.documentation_auto_generate,
                'validate_links': self.validate_links
            },
            'monitoring': {
                'enabled': self.monitoring_enabled,
                'dashboard_url': self.dashboard_url
            }
        }

        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def add_repository(self, repo_path: Path) -> None:
        """Add a repository to the configuration."""
        if repo_path not in self.repositories:
            self.repositories.append(repo_path)

    def remove_repository(self, repo_path: Path) -> None:
        """Remove a repository from the configuration."""
        if repo_path in self.repositories:
            self.repositories.remove(repo_path)