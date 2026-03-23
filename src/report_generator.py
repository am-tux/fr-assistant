"""Generate daily and weekly reports"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import os


class ReportGenerator:
    """Generates markdown reports for git activity"""

    def __init__(self, output_config: Dict[str, Any], reporting_config: Dict[str, Any]):
        """Initialize report generator

        Args:
            output_config: Output configuration from config.yaml
            reporting_config: Reporting preferences from config.yaml
        """
        self.output_dir = Path(output_config.get('output_directory', './reports'))
        self.format = output_config.get('format', 'markdown')
        self.include_diffs = output_config.get('include_diffs', False)
        self.max_commits_shown = output_config.get('max_commits_shown', 50)
        self.truncate_long_messages = output_config.get('truncate_long_messages', True)
        self.highlight_new_files = output_config.get('highlight_new_files', True)
        self.list_new_files_first = output_config.get('list_new_files_first', True)

        self.reporting_config = reporting_config

        # Create output directories
        self.daily_dir = self.output_dir / 'daily'
        self.weekly_dir = self.output_dir / 'weekly'
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.weekly_dir.mkdir(parents=True, exist_ok=True)

    def generate_daily_report(self, date: datetime, repos_data: List[Dict[str, Any]],
                              discussions_data: Optional[Dict[str, Any]] = None) -> str:
        """Generate daily report for a specific date

        Args:
            date: Date for the report
            repos_data: List of repository data dictionaries
            discussions_data: Optional discussions data to include

        Returns:
            Path to generated report file
        """
        report_date = date.strftime('%Y-%m-%d')
        filename = f"{report_date}.md"
        filepath = self.daily_dir / filename

        # Build report content
        lines = [
            f"# Daily Git Activity Report - {report_date}",
            ""
        ]

        # Process each repository
        for repo_data in repos_data:
            lines.extend(self._format_repo_section(repo_data))

        # Add discussions section if provided
        if discussions_data:
            lines.extend(self._format_discussions_highlights(discussions_data))

        # Write report
        content = '\n'.join(lines)
        filepath.write_text(content)

        return str(filepath)

    def generate_weekly_report(self, start_date: datetime, end_date: datetime,
                               repos_data: List[Dict[str, Any]],
                               discussions_data: Optional[Dict[str, Any]] = None) -> str:
        """Generate weekly report for a date range

        Args:
            start_date: Start of week
            end_date: End of week
            repos_data: List of repository data dictionaries
            discussions_data: Optional discussions data to include

        Returns:
            Path to generated report file
        """
        # Get ISO week number
        week_num = start_date.isocalendar()[1]
        year = start_date.year
        filename = f"{year}-W{week_num:02d}.md"
        filepath = self.weekly_dir / filename

        # Build report content
        lines = [
            f"# Weekly Git Activity Report - Week {week_num}, {year}",
            f"**Period:** {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            ""
        ]

        # Summary across all repositories
        lines.extend(self._format_weekly_summary(repos_data))

        # Process each repository
        for repo_data in repos_data:
            lines.extend(self._format_repo_weekly_section(repo_data, start_date, end_date))

        # Add discussions section if provided
        if discussions_data:
            lines.extend(self._format_discussions_weekly_summary(discussions_data))

        # Write report
        content = '\n'.join(lines)
        filepath.write_text(content)

        return str(filepath)

    def _format_repo_section(self, repo_data: Dict[str, Any]) -> List[str]:
        """Format repository section for daily report"""
        lines = [
            f"## {repo_data['name']}",
            "",
            "### Summary"
        ]

        stats = repo_data.get('stats', {})
        lines.append(f"- Files modified: {stats.get('files_modified', 0)}")
        lines.append(f"- Files added: {stats.get('files_added', 0)}")
        lines.append(f"- Files deleted: {stats.get('files_deleted', 0)}")
        lines.append(f"- Total lines changed: +{stats.get('lines_added', 0)} / -{stats.get('lines_deleted', 0)}")
        lines.append(f"- Total commits: {stats.get('total_commits', 0)}")

        contributors = repo_data.get('contributors', [])
        if contributors:
            lines.append(f"- Contributors: {', '.join(contributors)}")

        lines.append("")

        # File changes section
        lines.append("### File Changes (Primary Focus)")
        lines.append("")

        # New files (ALWAYS REPORT - highest priority)
        new_files = repo_data.get('new_files', [])
        if new_files:
            lines.append("#### 🆕 New Files Added (ALWAYS REPORT)")
            lines.append("New files indicate new documentation topics or features being documented.")
            lines.append("")

            for file_info in new_files:
                lines.append(f"- {file_info['path']} by {file_info['author']} in {file_info['commit'][:7]} at {file_info.get('time', 'N/A')}")
                lines.append(f"  - Commit message: {file_info.get('subject', 'N/A')}")
                if 'lines' in file_info:
                    lines.append(f"  - File size: +{file_info['lines']} lines")
                lines.append(f"  - File path: {file_info['path']}")
                lines.append("")

        # Modified files
        modified_files = repo_data.get('modified_files', [])
        if modified_files:
            lines.append("#### Modified Files")
            for file_info in modified_files:
                additions = file_info.get('additions', 0)
                deletions = file_info.get('deletions', 0)
                lines.append(f"- {file_info['path']}: +{additions} / -{deletions} lines by {file_info.get('author', 'N/A')} in {file_info.get('commit', 'N/A')[:7]}")
                if 'subject' in file_info:
                    lines.append(f"  - {file_info['subject']}")
                lines.append("")

        # Deleted/Renamed files
        deleted_files = repo_data.get('deleted_files', [])
        renamed_files = repo_data.get('renamed_files', [])

        if deleted_files or renamed_files:
            lines.append("#### Deleted/Renamed Files")

            for file_info in renamed_files:
                lines.append(f"- {file_info.get('old_path', 'N/A')} → {file_info['path']} by {file_info.get('author', 'N/A')} in {file_info.get('commit', 'N/A')[:7]}")

            for file_info in deleted_files:
                lines.append(f"- {file_info['path']} deleted by {file_info.get('author', 'N/A')} in {file_info.get('commit', 'N/A')[:7]}")

            lines.append("")

        # Commits section
        commits = repo_data.get('commits', [])
        if commits and len(commits) <= self.max_commits_shown:
            lines.append("### Commits (if relevant)")
            for commit in commits[:self.max_commits_shown]:
                commit_hash = commit.get('hash', 'N/A')[:7]
                author = commit.get('author', 'N/A')
                date = commit.get('date', 'N/A')
                subject = commit.get('subject', 'N/A')

                if self.truncate_long_messages and len(subject) > 200:
                    subject = subject[:197] + '...'

                lines.append(f"- {commit_hash} by {author} at {date}: {subject}")

                if 'files' in commit:
                    files_count = len(commit['files'])
                    total_add = sum(f.get('additions', 0) for f in commit['files'])
                    total_del = sum(f.get('deletions', 0) for f in commit['files'])
                    lines.append(f"  - Files affected: {files_count}")
                    lines.append(f"  - Total changes: +{total_add} / -{total_del} lines")

            lines.append("")

        lines.append("")
        return lines

    def _format_repo_weekly_section(self, repo_data: Dict[str, Any],
                                     start_date: datetime, end_date: datetime) -> List[str]:
        """Format repository section for weekly report"""
        lines = [
            f"## {repo_data['name']}",
            "",
            "### Week Summary"
        ]

        stats = repo_data.get('stats', {})
        lines.append(f"- Files added: {stats.get('files_added', 0)}")
        lines.append(f"- Files modified: {stats.get('files_modified', 0)}")
        lines.append(f"- Files deleted: {stats.get('files_deleted', 0)}")
        lines.append(f"- Total commits: {stats.get('total_commits', 0)}")
        lines.append(f"- Total lines changed: +{stats.get('lines_added', 0)} / -{stats.get('lines_deleted', 0)}")

        contributors = repo_data.get('contributors', {})
        if contributors:
            contributor_list = [f"{name} ({count} commits)" for name, count in contributors.items()]
            lines.append(f"- Contributors: {', '.join(contributor_list)}")

        lines.append("")

        # New documentation added this week
        new_files = repo_data.get('new_files', [])
        if new_files:
            lines.append("### 🆕 New Documentation Added This Week")
            lines.append("List all new files added during the week:")
            lines.append("")

            for file_info in new_files:
                date_str = file_info.get('date', 'N/A')
                lines.append(f"- {file_info['path']} - Added on {date_str} by {file_info.get('author', 'N/A')}")
                if 'lines' in file_info:
                    lines.append(f"  - Size: +{file_info['lines']} lines")
                lines.append(f"  - Commit: {file_info.get('commit', 'N/A')[:7]} - {file_info.get('subject', 'N/A')}")
                lines.append("")

        # Most active files
        active_files = repo_data.get('most_active_files', [])
        if active_files:
            lines.append("### Most Active Files (by line changes)")
            lines.append("Top 10 files with most changes:")
            lines.append("")

            for idx, file_info in enumerate(active_files[:10], 1):
                additions = file_info.get('additions', 0)
                deletions = file_info.get('deletions', 0)
                commit_count = file_info.get('commit_count', 0)
                lines.append(f"{idx}. {file_info['path']}: +{additions} / -{deletions} lines ({commit_count} commits)")

                if 'contributors' in file_info:
                    lines.append(f"   - Contributors: {', '.join(file_info['contributors'])}")
                if 'last_modified' in file_info:
                    lines.append(f"   - Last modified: {file_info['last_modified']}")
                lines.append("")

        lines.append("")
        return lines

    def _format_weekly_summary(self, repos_data: List[Dict[str, Any]]) -> List[str]:
        """Format overall summary for weekly report"""
        lines = ["## Summary Across All Repositories", ""]

        total_files_added = 0
        total_files_modified = 0
        total_files_deleted = 0
        total_commits = 0
        total_lines_added = 0
        total_lines_deleted = 0
        all_contributors = set()
        repos_with_changes = 0

        for repo_data in repos_data:
            stats = repo_data.get('stats', {})
            if stats.get('total_commits', 0) > 0:
                repos_with_changes += 1

            total_files_added += stats.get('files_added', 0)
            total_files_modified += stats.get('files_modified', 0)
            total_files_deleted += stats.get('files_deleted', 0)
            total_commits += stats.get('total_commits', 0)
            total_lines_added += stats.get('lines_added', 0)
            total_lines_deleted += stats.get('lines_deleted', 0)

            contributors = repo_data.get('contributors', {})
            if isinstance(contributors, dict):
                all_contributors.update(contributors.keys())
            elif isinstance(contributors, list):
                all_contributors.update(contributors)

        lines.append(f"- Total repositories with changes: {repos_with_changes}")
        lines.append(f"- Total files added: {total_files_added}")
        lines.append(f"- Total files modified: {total_files_modified}")
        lines.append(f"- Total files deleted: {total_files_deleted}")
        lines.append(f"- Total commits: {total_commits}")
        lines.append(f"- Total lines changed: +{total_lines_added} / -{total_lines_deleted}")
        lines.append(f"- Active contributors: {len(all_contributors)}")
        lines.append("")

        return lines

    def _format_discussions_highlights(self, discussions_data: Dict[str, Any]) -> List[str]:
        """Format discussions highlights for daily report"""
        lines = [
            "### 💬 GitHub Discussions Highlights (if enabled)",
            ""
        ]

        # New discussions
        new_discussions = discussions_data.get('new_discussions', [])
        if new_discussions:
            lines.append("#### New Discussions Today")
            for disc in new_discussions:
                lines.append(f"- **{disc['title']}** in [Channel: {disc.get('channel', 'General')}]")
                lines.append(f"  - By: {disc.get('author', 'N/A')} | Opened: {disc.get('created_at', 'N/A')}")
                lines.append(f"  - Category: {disc.get('category', 'N/A')}")
                lines.append(f"  - Link: {disc.get('url', 'N/A')}")
                if 'preview' in disc:
                    lines.append(f"  - Preview: {disc['preview']}")
                lines.append("")

        # Active discussions
        active_discussions = discussions_data.get('active_discussions', [])
        if active_discussions:
            lines.append("#### Active Discussions (with activity today)")
            for disc in active_discussions:
                lines.append(f"- **{disc['title']}** in [Channel: {disc.get('channel', 'General')}]")
                lines.append(f"  - New comments today: {disc.get('new_comments', 0)} | Total comments: {disc.get('total_comments', 0)}")
                lines.append(f"  - Last activity: {disc.get('last_activity', 'N/A')} by {disc.get('last_author', 'N/A')}")
                lines.append(f"  - Status: {disc.get('status', 'Open')}")
                lines.append(f"  - Link: {disc.get('url', 'N/A')}")
                lines.append("")

        # Top engagement
        top_discussions = discussions_data.get('top_engagement', [])
        if top_discussions:
            lines.append("#### Top Engagement Today")
            lines.append("Top 3 discussions by comment count in last 24 hours:")
            for idx, disc in enumerate(top_discussions[:3], 1):
                lines.append(f"{idx}. **{disc['title']}** ({disc.get('comment_count', 0)} comments)")
                lines.append(f"   - Channel: {disc.get('channel', 'General')}")
                lines.append(f"   - Link: {disc.get('url', 'N/A')}")
                lines.append("")

        lines.append("")
        return lines

    def _format_discussions_weekly_summary(self, discussions_data: Dict[str, Any]) -> List[str]:
        """Format discussions weekly summary"""
        lines = [
            "### 💬 GitHub Discussions Weekly Summary (if enabled)",
            "",
            "#### Week Overview"
        ]

        overview = discussions_data.get('overview', {})
        lines.append(f"- New discussions this week: {overview.get('new_discussions', 0)}")
        lines.append(f"- Total active discussions: {overview.get('active_discussions', 0)}")
        lines.append(f"- Discussions answered: {overview.get('answered', 0)}")
        lines.append(f"- Total comments this week: {overview.get('total_comments', 0)}")
        lines.append(f"- Active participants: {overview.get('participants', 0)}")
        lines.append("")

        # Top discussions
        top_discussions = discussions_data.get('top_discussions', [])
        if top_discussions:
            lines.append("#### Top Discussions by Engagement")
            lines.append("Top 5 discussions by total comment count this week:")
            for idx, disc in enumerate(top_discussions[:5], 1):
                lines.append(f"{idx}. **{disc['title']}** ({disc.get('total_comments', 0)} total comments, {disc.get('new_comments', 0)} new this week)")
                lines.append(f"   - Channel: {disc.get('channel', 'General')}")
                lines.append(f"   - Status: {disc.get('status', 'Open')}")
                lines.append(f"   - Participants: {disc.get('participants', 0)}")
                lines.append(f"   - Link: {disc.get('url', 'N/A')}")
                if 'summary' in disc:
                    lines.append(f"   - Summary: {disc['summary']}")
                lines.append("")

        lines.append("")
        return lines
