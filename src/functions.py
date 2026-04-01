"""High-level query functions for git repository tracking"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from .config_loader import Config
from .git_tracker import GitTracker
from .web_scraper import WebScraper


class TrackerFunctions:
    """Implementation of git repository tracking functions"""

    def __init__(self, config: Config):
        """Initialize tracker functions

        Args:
            config: Configuration object
        """
        self.config = config
        self.git_trackers = {}
        self.web_scraper = WebScraper()

        # Initialize git trackers for each repository
        for repo_config in config.get_repositories():
            repo_name = repo_config['name']
            self.git_trackers[repo_name] = GitTracker(repo_config)

    def ensure_repositories(self) -> Dict[str, bool]:
        """Ensure all repositories are cloned and up-to-date

        Returns:
            Dictionary of repo_name -> success status
        """
        results = {}
        for repo_name, tracker in self.git_trackers.items():
            results[repo_name] = tracker.ensure_repository()
        return results

    def get_new_files_since(self, repository: str, since: datetime,
                            branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get new files added since a specific date

        Args:
            repository: Repository name
            since: Get files added after this datetime
            branch: Branch to check (defaults to primary branch)

        Returns:
            List of file dictionaries
        """
        if repository not in self.git_trackers:
            raise ValueError(f"Repository '{repository}' not found")

        tracker = self.git_trackers[repository]
        return tracker.get_new_files_since(since, branch)

    def get_commits_since(self, repository: str, since: datetime,
                          branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get commits since a specific date

        Args:
            repository: Repository name
            since: Get commits after this datetime
            branch: Branch to check (defaults to primary branch)

        Returns:
            List of commit dictionaries
        """
        if repository not in self.git_trackers:
            raise ValueError(f"Repository '{repository}' not found")

        tracker = self.git_trackers[repository]
        return tracker.get_commits_since(since, branch)

    def get_file_history(self, repository: str, filepath: str,
                         branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get complete history of a specific file

        Args:
            repository: Repository name
            filepath: Path to file
            branch: Branch to check (defaults to primary branch)

        Returns:
            List of commits that modified this file
        """
        if repository not in self.git_trackers:
            raise ValueError(f"Repository '{repository}' not found")

        tracker = self.git_trackers[repository]
        return tracker.get_file_history(filepath, branch)

    def get_contributor_activity(self, repository: str, contributor: str,
                                  since: Optional[datetime] = None,
                                  branch: Optional[str] = None) -> Dict[str, Any]:
        """Get activity for a specific contributor

        Args:
            repository: Repository name
            contributor: Author name or email
            since: Get activity after this datetime
            branch: Branch to check (defaults to primary branch)

        Returns:
            Dictionary with contributor stats and commits
        """
        if repository not in self.git_trackers:
            raise ValueError(f"Repository '{repository}' not found")

        tracker = self.git_trackers[repository]
        return tracker.get_contributor_activity(contributor, since, branch)

    def get_github_rfcs(self, since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get GitHub Discussions RFCs from FedRAMP/community

        Args:
            since: Get RFCs after this datetime

        Returns:
            List of RFC dictionaries
        """
        return self.web_scraper.get_github_rfcs(since)

    def get_fedramp_blog_posts(self, since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get FedRAMP.gov blog posts

        Args:
            since: Get posts after this datetime

        Returns:
            List of blog post dictionaries
        """
        return self.web_scraper.get_fedramp_blog_posts(since)

    def get_fedramp_events(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Get FedRAMP.gov upcoming events

        Args:
            days_ahead: Number of days ahead to look for events

        Returns:
            List of event dictionaries
        """
        return self.web_scraper.get_fedramp_events(days_ahead)

    def get_fedramp_notices(self, since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get FedRAMP notices from RSS feed

        Args:
            since: Get notices after this datetime

        Returns:
            List of notice dictionaries
        """
        return self.web_scraper.get_fedramp_notices(since)

    def search_content(self, pattern: str, repository: Optional[str] = None,
                       case_sensitive: bool = False, context_lines: int = 0,
                       file_pattern: Optional[str] = None,
                       branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for a pattern in repository content

        Args:
            pattern: Search pattern (regex supported)
            repository: Repository name (searches all repos if None)
            case_sensitive: Whether search should be case-sensitive (default: False)
            context_lines: Number of context lines to show (default: 0)
            file_pattern: Optional glob pattern to filter files (e.g., '*.md')
            branch: Branch to search (defaults to primary branch)

        Returns:
            List of match dictionaries from all searched repositories
        """
        all_matches = []

        if repository:
            # Search specific repository
            if repository not in self.git_trackers:
                raise ValueError(f"Repository '{repository}' not found")

            tracker = self.git_trackers[repository]
            matches = tracker.search_content(
                pattern=pattern,
                branch=branch,
                case_sensitive=case_sensitive,
                context_lines=context_lines,
                file_pattern=file_pattern
            )
            all_matches.extend(matches)
        else:
            # Search all repositories
            for repo_name, tracker in self.git_trackers.items():
                matches = tracker.search_content(
                    pattern=pattern,
                    branch=branch,
                    case_sensitive=case_sensitive,
                    context_lines=context_lines,
                    file_pattern=file_pattern
                )
                all_matches.extend(matches)

        return all_matches
