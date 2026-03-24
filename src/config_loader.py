"""Configuration file parser for config.yaml"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List


class Config:
    """Configuration manager for the tracker"""

    def __init__(self, config_path: str = "config.yaml"):
        """Load configuration from YAML file

        Args:
            config_path: Path to config.yaml (relative to project root or absolute)
        """
        # Resolve config path relative to project root
        if not os.path.isabs(config_path):
            project_root = Path(__file__).parent.parent
            config_path = project_root / config_path

        self.config_path = Path(config_path)
        self.config_dir = self.config_path.parent

        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f)

    def get_repositories(self) -> List[Dict[str, Any]]:
        """Get list of repositories to track"""
        repos = self._config.get('repositories', [])

        # Convert relative paths to absolute paths
        for repo in repos:
            if 'path' in repo and not os.path.isabs(repo['path']):
                repo['path'] = str(self.config_dir / repo['path'])

        return repos

    def get_repo_by_name(self, name: str) -> Dict[str, Any]:
        """Get repository configuration by name"""
        for repo in self.get_repositories():
            if repo.get('name') == name:
                return repo
        raise ValueError(f"Repository '{name}' not found in configuration")

    def get_storage_config(self) -> Dict[str, Any]:
        """Get storage configuration"""
        storage = self._config.get('storage', {})

        # Convert relative repos directory to absolute
        if 'repos_directory' in storage and not os.path.isabs(storage['repos_directory']):
            storage['repos_directory'] = str(self.config_dir / storage['repos_directory'])

        return storage

    @property
    def repos_directory(self) -> Path:
        """Get the repos directory path"""
        storage = self.get_storage_config()
        repos_dir = storage.get('repos_directory', './repos')
        return Path(repos_dir)
