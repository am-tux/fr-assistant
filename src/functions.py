"""High-level query functions defined in SPEC.md"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from .config_loader import Config
from .git_tracker import GitTracker
from .discussions_tracker import DiscussionsTracker
from .report_generator import ReportGenerator


class TrackerFunctions:
    """Implementation of all query functions from SPEC.md"""

    def __init__(self, config: Config):
        """Initialize tracker functions

        Args:
            config: Configuration object
        """
        self.config = config
        self.git_trackers = {}
        self.discussions_trackers = {}

        # Initialize trackers for each repository
        for repo_config in config.get_repositories():
            repo_name = repo_config['name']

            # Git tracker
            self.git_trackers[repo_name] = GitTracker(repo_config)

            # Discussions tracker (if enabled)
            if repo_config.get('track_discussions', False):
                github_api_config = config.get_github_api_config()
                self.discussions_trackers[repo_name] = DiscussionsTracker(
                    repo_config, github_api_config
                )

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

        # Collect discussions data
        discussions_data = None
        if self.discussions_trackers:
            discussions_data = self._collect_discussions_daily_data(start_time, end_time)

        # Generate report
        return self.report_generator.generate_daily_report(date, repos_data, discussions_data)

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

        # Collect discussions data
        discussions_data = None
        if self.discussions_trackers:
            discussions_data = self._collect_discussions_weekly_data(start_date, end_date)

        # Generate report
        return self.report_generator.generate_weekly_report(start_date, end_date, repos_data, discussions_data)

    def get_open_rfcs(self, repository: str, status: str = 'open',
                      sort_by: str = 'newest') -> List[Dict[str, Any]]:
        """Get open RFCs from a repository

        Args:
            repository: Repository name
            status: RFC status (open, answered, closed, all)
            sort_by: Sort order (newest, oldest, most_comments, most_reactions)

        Returns:
            List of RFC dictionaries with topic classification
        """
        if repository not in self.discussions_trackers:
            raise ValueError(f"Repository '{repository}' does not have discussions tracking enabled")

        tracker = self.discussions_trackers[repository]
        rfcs = tracker.get_open_rfcs(sort_by=sort_by)

        # Filter by status if needed
        if status == 'answered':
            rfcs = [rfc for rfc in rfcs if rfc['is_answered']]
        elif status == 'open':
            rfcs = [rfc for rfc in rfcs if not rfc['is_answered']]
        # 'all' returns everything

        return rfcs

    def get_most_responded_discussions(self, repository: str, timeframe: str = '7d',
                                        channel: str = 'all',
                                        limit: int = 10) -> List[Dict[str, Any]]:
        """Get discussions with most responses

        Args:
            repository: Repository name
            timeframe: Time window (24h, 7d, 30d, all)
            channel: Channel filter (20x, Rev5, RFCs, General, all)
            limit: Maximum number to return

        Returns:
            List of discussion dictionaries sorted by response count
        """
        if repository not in self.discussions_trackers:
            raise ValueError(f"Repository '{repository}' does not have discussions tracking enabled")

        tracker = self.discussions_trackers[repository]
        return tracker.get_most_responded_discussions(timeframe, channel, limit)

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

    def get_unanswered_questions(self, repository: str,
                                  older_than_hours: int = 48) -> List[Dict[str, Any]]:
        """Get unanswered discussions older than specified hours

        Args:
            repository: Repository name
            older_than_hours: Get unanswered discussions older than this many hours

        Returns:
            List of unanswered discussion dictionaries
        """
        if repository not in self.discussions_trackers:
            raise ValueError(f"Repository '{repository}' does not have discussions tracking enabled")

        tracker = self.discussions_trackers[repository]
        return tracker.get_unanswered_discussions(older_than_hours)

    def get_discussions_by_channel(self, repository: str, channel: str,
                                    since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get discussions for a specific channel

        Args:
            repository: Repository name
            channel: Channel name (20x, Rev5, RFCs, General)
            since: Optional datetime filter

        Returns:
            List of discussion dictionaries
        """
        if repository not in self.discussions_trackers:
            raise ValueError(f"Repository '{repository}' does not have discussions tracking enabled")

        tracker = self.discussions_trackers[repository]
        return tracker.get_discussions_by_channel(channel, since)

    def generate_daily_discussions_report(self, repository: str,
                                           date: Optional[datetime] = None) -> str:
        """Generate detailed daily discussions report for community managers

        Args:
            repository: Repository name
            date: Date for report (defaults to today)

        Returns:
            Path to generated report file
        """
        if repository not in self.discussions_trackers:
            raise ValueError(f"Repository '{repository}' does not have discussions tracking enabled")

        if date is None:
            date = datetime.now()

        # Normalize to start of day
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = date - timedelta(days=1)

        tracker = self.discussions_trackers[repository]

        # Collect data by channel
        channels_data = {}
        for channel_name in ['20x', 'Rev5', 'RFCs', 'General']:
            new_discussions = [d for d in tracker.get_discussions_by_channel(channel_name, start_time)
                               if d['created_at'] >= start_time]
            active_discussions = [d for d in tracker.get_discussions_by_channel(channel_name, start_time)
                                  if d['updated_at'] >= start_time]
            channels_data[channel_name] = {
                'new': new_discussions,
                'active': active_discussions
            }

        # Generate report
        report_date = date.strftime('%Y-%m-%d')
        filename = f"{report_date}.md"
        discussions_daily_dir = self.config.output_directory / 'discussions' / 'daily'
        discussions_daily_dir.mkdir(parents=True, exist_ok=True)
        filepath = discussions_daily_dir / filename

        lines = [
            f"# Daily GitHub Discussions Report - {report_date}",
            f"**Repository:** {repository}",
            "",
            "## Overview",
            ""
        ]

        total_new = sum(len(data['new']) for data in channels_data.values())
        total_active = sum(len(data['active']) for data in channels_data.values())

        lines.append(f"- New discussions today: {total_new}")
        lines.append(f"- Active discussions today: {total_active}")
        lines.append("")

        # Per-channel breakdown
        for channel_name, data in channels_data.items():
            if data['new'] or data['active']:
                lines.append(f"## {channel_name} Channel")
                lines.append("")

                if data['new']:
                    lines.append(f"### New Discussions ({len(data['new'])})")
                    for disc in data['new']:
                        lines.append(f"- **{disc['title']}**")
                        lines.append(f"  - By: {disc['author']} | Created: {disc['created_at'].strftime('%Y-%m-%d %H:%M')}")
                        lines.append(f"  - Comments: {disc['comment_count']} | Reactions: {disc['reaction_count']}")
                        lines.append(f"  - URL: {disc['url']}")
                        lines.append("")

                if data['active']:
                    lines.append(f"### Active Discussions ({len(data['active'])})")
                    for disc in data['active']:
                        status = "Answered" if disc['is_answered'] else "Open"
                        lines.append(f"- [{status}] **{disc['title']}**")
                        lines.append(f"  - Updated: {disc['updated_at'].strftime('%Y-%m-%d %H:%M')} | Comments: {disc['comment_count']}")
                        lines.append(f"  - URL: {disc['url']}")
                        lines.append("")

        content = '\n'.join(lines)
        filepath.write_text(content)

        return str(filepath)

    def generate_weekly_discussions_report(self, repository: str,
                                            date: Optional[datetime] = None) -> str:
        """Generate detailed weekly discussions report for community managers

        Args:
            repository: Repository name
            date: Date within the week (defaults to today)

        Returns:
            Path to generated report file
        """
        if repository not in self.discussions_trackers:
            raise ValueError(f"Repository '{repository}' does not have discussions tracking enabled")

        if date is None:
            date = datetime.now()

        # Get start of week (Monday)
        start_date = date - timedelta(days=date.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)

        tracker = self.discussions_trackers[repository]

        # Collect data by channel
        channels_data = {}
        for channel_name in ['20x', 'Rev5', 'RFCs', 'General']:
            discussions = tracker.get_discussions_by_channel(channel_name, start_date)
            channels_data[channel_name] = discussions

        # Generate report
        week_num = start_date.isocalendar()[1]
        year = start_date.year
        filename = f"{year}-W{week_num:02d}.md"
        discussions_weekly_dir = self.config.output_directory / 'discussions' / 'weekly'
        discussions_weekly_dir.mkdir(parents=True, exist_ok=True)
        filepath = discussions_weekly_dir / filename

        lines = [
            f"# Weekly GitHub Discussions Report - Week {week_num}, {year}",
            f"**Repository:** {repository}",
            f"**Period:** {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "",
            "## Overview",
            ""
        ]

        total_discussions = sum(len(discussions) for discussions in channels_data.values())
        total_comments = sum(d['comment_count'] for discussions in channels_data.values() for d in discussions)

        lines.append(f"- Total discussions this week: {total_discussions}")
        lines.append(f"- Total comments: {total_comments}")
        lines.append("")

        # Per-channel breakdown
        for channel_name, discussions in channels_data.items():
            if discussions:
                lines.append(f"## {channel_name} Channel ({len(discussions)} discussions)")
                lines.append("")

                # Sort by comment count
                discussions.sort(key=lambda x: x['comment_count'], reverse=True)

                for disc in discussions[:20]:  # Top 20 per channel
                    status = "Answered" if disc['is_answered'] else "Open"
                    lines.append(f"- [{status}] **{disc['title']}**")
                    lines.append(f"  - Comments: {disc['comment_count']} | Reactions: {disc['reaction_count']}")
                    lines.append(f"  - Created: {disc['created_at'].strftime('%Y-%m-%d')} by {disc['author']}")
                    lines.append(f"  - URL: {disc['url']}")
                    lines.append("")

        content = '\n'.join(lines)
        filepath.write_text(content)

        return str(filepath)

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

    def _collect_discussions_daily_data(self, start_time: datetime,
                                         end_time: datetime) -> Dict[str, Any]:
        """Collect discussions data for daily report"""
        # For now, use the first discussions tracker
        # In the future, this could aggregate across multiple repos
        tracker = list(self.discussions_trackers.values())[0]

        new_discussions = tracker.get_new_discussions(start_time)
        active_discussions = tracker.get_active_discussions(start_time)
        top_engagement = tracker.get_most_responded_discussions('24h', 'all', 3)

        return {
            'new_discussions': [self._format_discussion_summary(d) for d in new_discussions],
            'active_discussions': [self._format_discussion_summary(d) for d in active_discussions],
            'top_engagement': [self._format_discussion_summary(d) for d in top_engagement]
        }

    def _collect_discussions_weekly_data(self, start_date: datetime,
                                          end_date: datetime) -> Dict[str, Any]:
        """Collect discussions data for weekly report"""
        tracker = list(self.discussions_trackers.values())[0]

        new_discussions = tracker.get_new_discussions(start_date)
        active_discussions = tracker.get_active_discussions(start_date)
        top_discussions = tracker.get_most_responded_discussions('7d', 'all', 5)

        return {
            'overview': {
                'new_discussions': len(new_discussions),
                'active_discussions': len(active_discussions),
                'answered': sum(1 for d in active_discussions if d['is_answered']),
                'total_comments': sum(d['comment_count'] for d in active_discussions),
                'participants': len(set(d['author'] for d in active_discussions))
            },
            'top_discussions': [self._format_discussion_summary(d) for d in top_discussions]
        }

    def _format_discussion_summary(self, discussion: Dict[str, Any]) -> Dict[str, Any]:
        """Format discussion for report inclusion"""
        return {
            'title': discussion['title'],
            'url': discussion['url'],
            'author': discussion['author'],
            'created_at': discussion['created_at'].strftime('%Y-%m-%d %H:%M'),
            'channel': discussion['channel'],
            'category': discussion['category'],
            'comment_count': discussion['comment_count'],
            'total_comments': discussion['comment_count'],
            'status': 'Answered' if discussion['is_answered'] else 'Open',
            'preview': discussion['body'][:150] + '...' if len(discussion['body']) > 150 else discussion['body']
        }
