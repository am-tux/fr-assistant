"""High-level query functions defined in SPEC.md"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from .config_loader import Config
from .git_tracker import GitTracker
from .report_generator import ReportGenerator


class TrackerFunctions:
    """Implementation of git repository tracking functions"""

    def __init__(self, config: Config):
        """Initialize tracker functions

        Args:
            config: Configuration object
        """
        self.config = config
        self.git_trackers = {}

        # Initialize git trackers for each repository
        for repo_config in config.get_repositories():
            repo_name = repo_config['name']
            self.git_trackers[repo_name] = GitTracker(repo_config)

        # Report generator
        self.report_generator = ReportGenerator(
            config.get_output_config(),
            config.get_reporting_config()
        )

    def ensure_repositories(self) -> Dict[str, bool]:
        """Ensure all repositories are cloned and up-to-date

        Returns:
            Dictionary of repo_name -> success status
        """
        results = {}
        for repo_name, tracker in self.git_trackers.items():
            results[repo_name] = tracker.ensure_repository()
        return results

    def generate_daily_report(self, date: Optional[datetime] = None) -> str:
        """Generate daily report for a specific date

        Args:
            date: Date for report (defaults to today)

        Returns:
            Path to generated report file
        """
        if date is None:
            date = datetime.now()

        # Normalize to start of day
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)

        # Calculate time range (previous 24 hours)
        end_time = date
        start_time = end_time - timedelta(days=1)

        # Collect data for all repositories
        repos_data = []
        for repo_name, tracker in self.git_trackers.items():
            repo_data = self._collect_repo_data(tracker, start_time, end_time)
            repos_data.append(repo_data)

        # Generate report (git data only)
        return self.report_generator.generate_daily_report(date, repos_data, None)

    def generate_weekly_report(self, date: Optional[datetime] = None) -> str:
        """Generate weekly report for the week containing the given date

        Args:
            date: Date within the week (defaults to today)

        Returns:
            Path to generated report file
        """
        if date is None:
            date = datetime.now()

        # Get start of week (Monday)
        start_date = date - timedelta(days=date.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # End of week (Sunday)
        end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)

        # Collect data for all repositories
        repos_data = []
        for repo_name, tracker in self.git_trackers.items():
            repo_data = self._collect_repo_weekly_data(tracker, start_date, end_date)
            repos_data.append(repo_data)

        # Generate report (git data only)
        return self.report_generator.generate_weekly_report(start_date, end_date, repos_data, None)

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
    def _collect_repo_data(self, tracker: GitTracker,
                           start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Collect repository data for a time range (daily report)"""
        # Get commits
        commits = tracker.get_commits_since(start_time)

        # Get new files
        new_files = tracker.get_new_files_since(start_time)

        # Get deleted files
        deleted_files = tracker.get_deleted_files_since(start_time)

        # Calculate stats
        total_files_modified = set()
        total_additions = 0
        total_deletions = 0
        contributors = set()
        modified_files = []
        renamed_files = []

        for commit in commits:
            contributors.add(commit['author'])

            for file_info in commit.get('files', []):
                total_additions += file_info.get('additions', 0)
                total_deletions += file_info.get('deletions', 0)

                if file_info['status'] == 'M':
                    total_files_modified.add(file_info['path'])
                    modified_files.append({
                        'path': file_info['path'],
                        'additions': file_info.get('additions', 0),
                        'deletions': file_info.get('deletions', 0),
                        'author': commit['author'],
                        'commit': commit['hash'],
                        'subject': commit['subject']
                    })
                elif file_info['status'].startswith('R'):
                    renamed_files.append({
                        'old_path': file_info.get('old_path', ''),
                        'path': file_info['path'],
                        'author': commit['author'],
                        'commit': commit['hash']
                    })

        # Add line counts to new files
        for file_info in new_files:
            stats = tracker.get_file_stats(file_info['path'], file_info['commit'])
            file_info['lines'] = stats['lines']

        return {
            'name': tracker.name,
            'stats': {
                'files_modified': len(total_files_modified),
                'files_added': len(new_files),
                'files_deleted': len(deleted_files),
                'lines_added': total_additions,
                'lines_deleted': total_deletions,
                'total_commits': len(commits)
            },
            'contributors': list(contributors),
            'commits': commits,
            'new_files': new_files,
            'modified_files': modified_files,
            'deleted_files': deleted_files,
            'renamed_files': renamed_files
        }

    def _collect_repo_weekly_data(self, tracker: GitTracker,
                                   start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Collect repository data for a week (weekly report)"""
        # Get commits
        commits = tracker.get_commits_since(start_date)

        # Get new files
        new_files = tracker.get_new_files_since(start_date)

        # Get deleted files
        deleted_files = tracker.get_deleted_files_since(start_date)

        # Calculate stats
        total_additions = 0
        total_deletions = 0
        contributors = {}
        file_activity = {}  # Track changes per file

        for commit in commits:
            author = commit['author']
            contributors[author] = contributors.get(author, 0) + 1

            for file_info in commit.get('files', []):
                filepath = file_info['path']
                total_additions += file_info.get('additions', 0)
                total_deletions += file_info.get('deletions', 0)

                if filepath not in file_activity:
                    file_activity[filepath] = {
                        'path': filepath,
                        'additions': 0,
                        'deletions': 0,
                        'commit_count': 0,
                        'contributors': set()
                    }

                file_activity[filepath]['additions'] += file_info.get('additions', 0)
                file_activity[filepath]['deletions'] += file_info.get('deletions', 0)
                file_activity[filepath]['commit_count'] += 1
                file_activity[filepath]['contributors'].add(commit['author'])

        # Convert file activity to list and sort by total changes
        most_active_files = []
        for filepath, activity in file_activity.items():
            activity['contributors'] = list(activity['contributors'])
            activity['total_changes'] = activity['additions'] + activity['deletions']
            most_active_files.append(activity)

        most_active_files.sort(key=lambda x: x['total_changes'], reverse=True)

        # Add line counts to new files
        for file_info in new_files:
            stats = tracker.get_file_stats(file_info['path'], file_info['commit'])
            file_info['lines'] = stats['lines']

        return {
            'name': tracker.name,
            'stats': {
                'files_added': len(new_files),
                'files_modified': len(file_activity),
                'files_deleted': len(deleted_files),
                'lines_added': total_additions,
                'lines_deleted': total_deletions,
                'total_commits': len(commits)
            },
            'contributors': contributors,
            'new_files': new_files,
            'deleted_files': deleted_files,
            'most_active_files': most_active_files
        }
