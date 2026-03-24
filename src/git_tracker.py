"""Git repository tracking and analysis"""

import subprocess
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import re


class GitTracker:
    """Handles git operations for repository tracking"""

    def __init__(self, repo_config: Dict[str, Any]):
        """Initialize git tracker for a repository

        Args:
            repo_config: Repository configuration from config.yaml
        """
        self.name = repo_config['name']
        self.url = repo_config['url']
        self.path = Path(repo_config['path'])
        self.primary_branch = repo_config.get('primary_branch', 'main')
        self.critical_files = repo_config.get('critical_files', [])

    def ensure_repository(self) -> bool:
        """Ensure repository exists locally (clone if needed, fetch if exists)

        Returns:
            True if repository is ready, False if there was an error
        """
        if self.path.exists():
            return self.fetch()
        else:
            return self.clone()

    def clone(self) -> bool:
        """Clone repository from remote URL

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create parent directory if needed
            self.path.parent.mkdir(parents=True, exist_ok=True)

            # Clone repository
            result = subprocess.run(
                ['git', 'clone', self.url, str(self.path)],
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error cloning {self.name}: {e.stderr}")
            return False

    def fetch(self) -> bool:
        """Fetch latest changes from remote

        Returns:
            True if successful, False otherwise
        """
        try:
            result = subprocess.run(
                ['git', 'fetch', '--all'],
                cwd=self.path,
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error fetching {self.name}: {e.stderr}")
            return False

    def get_commits_since(self, since: datetime, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get commits since a specific datetime

        Args:
            since: Get commits after this datetime
            branch: Branch to check (defaults to primary_branch)

        Returns:
            List of commit dictionaries with hash, author, date, message, files
        """
        if branch is None:
            branch = self.primary_branch

        since_str = since.strftime('%Y-%m-%d %H:%M:%S')

        try:
            # Get commit hashes
            result = subprocess.run(
                ['git', 'log', f'origin/{branch}', f'--since={since_str}', '--format=%H'],
                cwd=self.path,
                capture_output=True,
                text=True,
                check=True
            )

            commit_hashes = result.stdout.strip().split('\n')
            if not commit_hashes or commit_hashes[0] == '':
                return []

            commits = []
            for commit_hash in commit_hashes:
                commit_info = self.get_commit_info(commit_hash)
                if commit_info:
                    commits.append(commit_info)

            return commits

        except subprocess.CalledProcessError as e:
            print(f"Error getting commits for {self.name}: {e.stderr}")
            return []

    def get_commit_info(self, commit_hash: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a commit

        Args:
            commit_hash: Git commit hash

        Returns:
            Dictionary with commit details
        """
        try:
            # Get commit metadata
            result = subprocess.run(
                ['git', 'show', commit_hash, '--format=%H%n%an%n%ae%n%ai%n%s%n%b', '--name-status', '--no-patch'],
                cwd=self.path,
                capture_output=True,
                text=True,
                check=True
            )

            lines = result.stdout.strip().split('\n')
            if len(lines) < 5:
                return None

            commit_info = {
                'hash': lines[0],
                'author': lines[1],
                'author_email': lines[2],
                'date': lines[3],
                'subject': lines[4],
                'body': '\n'.join(lines[5:]) if len(lines) > 5 else '',
                'files': self.get_commit_files(commit_hash)
            }

            return commit_info

        except subprocess.CalledProcessError as e:
            print(f"Error getting commit info for {commit_hash}: {e.stderr}")
            return None

    def get_commit_files(self, commit_hash: str) -> List[Dict[str, Any]]:
        """Get files changed in a commit with their status and stats

        Args:
            commit_hash: Git commit hash

        Returns:
            List of file dictionaries with path, status, additions, deletions
        """
        try:
            # Get file statuses
            result = subprocess.run(
                ['git', 'show', commit_hash, '--name-status', '--format='],
                cwd=self.path,
                capture_output=True,
                text=True,
                check=True
            )

            status_lines = [line for line in result.stdout.strip().split('\n') if line]

            # Get numstat for line counts
            result = subprocess.run(
                ['git', 'show', commit_hash, '--numstat', '--format='],
                cwd=self.path,
                capture_output=True,
                text=True,
                check=True
            )

            numstat_lines = [line for line in result.stdout.strip().split('\n') if line]

            # Parse file changes
            files = []
            numstat_dict = {}

            # Build numstat dictionary
            for line in numstat_lines:
                parts = line.split('\t')
                if len(parts) >= 3:
                    additions = parts[0] if parts[0] != '-' else '0'
                    deletions = parts[1] if parts[1] != '-' else '0'
                    filepath = parts[2]
                    numstat_dict[filepath] = {
                        'additions': int(additions),
                        'deletions': int(deletions)
                    }

            # Parse status lines
            for line in status_lines:
                parts = line.split('\t')
                if len(parts) < 2:
                    continue

                status = parts[0]
                filepath = parts[1]

                file_info = {
                    'path': filepath,
                    'status': status,
                    'additions': 0,
                    'deletions': 0
                }

                # Handle rename (R100, R095, etc.) and copy
                if status.startswith('R') or status.startswith('C'):
                    if len(parts) >= 3:
                        file_info['old_path'] = filepath
                        file_info['path'] = parts[2]
                        filepath = parts[2]

                # Add line counts if available
                if filepath in numstat_dict:
                    file_info['additions'] = numstat_dict[filepath]['additions']
                    file_info['deletions'] = numstat_dict[filepath]['deletions']

                files.append(file_info)

            return files

        except subprocess.CalledProcessError as e:
            print(f"Error getting commit files for {commit_hash}: {e.stderr}")
            return []

    def get_new_files_since(self, since: datetime, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get files added since a specific datetime

        Args:
            since: Get files added after this datetime
            branch: Branch to check (defaults to primary_branch)

        Returns:
            List of file dictionaries with path, commit, author, date
        """
        if branch is None:
            branch = self.primary_branch

        since_str = since.strftime('%Y-%m-%d %H:%M:%S')

        try:
            result = subprocess.run(
                ['git', 'log', f'origin/{branch}', f'--since={since_str}',
                 '--diff-filter=A', '--name-status', '--format=%H|%an|%ai|%s'],
                cwd=self.path,
                capture_output=True,
                text=True,
                check=True
            )

            lines = result.stdout.strip().split('\n')
            new_files = []

            i = 0
            while i < len(lines):
                if '|' in lines[i]:
                    # Commit info line
                    parts = lines[i].split('|')
                    if len(parts) >= 4:
                        commit_hash = parts[0]
                        author = parts[1]
                        date = parts[2]
                        subject = parts[3]

                        # Next lines are files until we hit another commit or end
                        i += 1
                        while i < len(lines) and '|' not in lines[i] and lines[i].strip():
                            file_line = lines[i].strip()
                            if file_line.startswith('A\t'):
                                filepath = file_line[2:]
                                new_files.append({
                                    'path': filepath,
                                    'commit': commit_hash,
                                    'author': author,
                                    'date': date,
                                    'subject': subject
                                })
                            i += 1
                else:
                    i += 1

            return new_files

        except subprocess.CalledProcessError as e:
            print(f"Error getting new files for {self.name}: {e.stderr}")
            return []

    def get_deleted_files_since(self, since: datetime, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get files deleted since a specific datetime

        Args:
            since: Get files deleted after this datetime
            branch: Branch to check (defaults to primary_branch)

        Returns:
            List of file dictionaries with path, commit, author, date
        """
        if branch is None:
            branch = self.primary_branch

        since_str = since.strftime('%Y-%m-%d %H:%M:%S')

        try:
            result = subprocess.run(
                ['git', 'log', f'origin/{branch}', f'--since={since_str}',
                 '--diff-filter=D', '--name-status', '--format=%H|%an|%ai|%s'],
                cwd=self.path,
                capture_output=True,
                text=True,
                check=True
            )

            lines = result.stdout.strip().split('\n')
            deleted_files = []

            i = 0
            while i < len(lines):
                if '|' in lines[i]:
                    parts = lines[i].split('|')
                    if len(parts) >= 4:
                        commit_hash = parts[0]
                        author = parts[1]
                        date = parts[2]
                        subject = parts[3]

                        i += 1
                        while i < len(lines) and '|' not in lines[i] and lines[i].strip():
                            file_line = lines[i].strip()
                            if file_line.startswith('D\t'):
                                filepath = file_line[2:]
                                deleted_files.append({
                                    'path': filepath,
                                    'commit': commit_hash,
                                    'author': author,
                                    'date': date,
                                    'subject': subject
                                })
                            i += 1
                else:
                    i += 1

            return deleted_files

        except subprocess.CalledProcessError as e:
            print(f"Error getting deleted files for {self.name}: {e.stderr}")
            return []

    def get_file_stats(self, filepath: str, commit_hash: str) -> Dict[str, int]:
        """Get line count statistics for a file at a specific commit

        Args:
            filepath: Path to file
            commit_hash: Git commit hash

        Returns:
            Dictionary with 'lines' count
        """
        try:
            result = subprocess.run(
                ['git', 'show', f'{commit_hash}:{filepath}'],
                cwd=self.path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                lines = len(result.stdout.split('\n'))
                return {'lines': lines}
            else:
                return {'lines': 0}

        except subprocess.CalledProcessError:
            return {'lines': 0}

    def get_file_history(self, filepath: str, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get complete history of a specific file

        Args:
            filepath: Path to file
            branch: Branch to check (defaults to primary_branch)

        Returns:
            List of commits that modified this file
        """
        if branch is None:
            branch = self.primary_branch

        try:
            # Get commits that touched this file
            result = subprocess.run(
                ['git', 'log', f'origin/{branch}', '--follow', '--format=%H|%an|%ae|%ai|%s', '--', filepath],
                cwd=self.path,
                capture_output=True,
                text=True,
                check=True
            )

            if not result.stdout.strip():
                return []

            commits = []
            for line in result.stdout.strip().split('\n'):
                parts = line.split('|')
                if len(parts) >= 5:
                    commit_hash = parts[0]

                    # Get file changes for this commit
                    stat_result = subprocess.run(
                        ['git', 'show', commit_hash, '--numstat', '--format=', '--', filepath],
                        cwd=self.path,
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    additions = 0
                    deletions = 0
                    if stat_result.stdout.strip():
                        stat_parts = stat_result.stdout.strip().split('\t')
                        if len(stat_parts) >= 2:
                            additions = int(stat_parts[0]) if stat_parts[0] != '-' else 0
                            deletions = int(stat_parts[1]) if stat_parts[1] != '-' else 0

                    commits.append({
                        'hash': parts[0],
                        'author': parts[1],
                        'author_email': parts[2],
                        'date': parts[3],
                        'subject': parts[4],
                        'additions': additions,
                        'deletions': deletions
                    })

            return commits

        except subprocess.CalledProcessError as e:
            print(f"Error getting file history for {filepath}: {e.stderr}")
            return []

    def get_contributor_activity(self, contributor: str, since: Optional[datetime] = None,
                                  branch: Optional[str] = None) -> Dict[str, Any]:
        """Get activity for a specific contributor

        Args:
            contributor: Author name or email
            since: Get activity after this datetime
            branch: Branch to check (defaults to primary_branch)

        Returns:
            Dictionary with contributor stats and commits
        """
        if branch is None:
            branch = self.primary_branch

        # Build git log command
        cmd = ['git', 'log', f'origin/{branch}', f'--author={contributor}', '--format=%H']

        if since:
            since_str = since.strftime('%Y-%m-%d')
            cmd.append(f'--since={since_str}')

        try:
            result = subprocess.run(
                cmd,
                cwd=self.path,
                capture_output=True,
                text=True,
                check=False
            )

            # Check for git errors
            if result.returncode != 0 and result.stderr:
                print(f"Git error for {contributor}: {result.stderr}")

            commit_hashes = [h for h in result.stdout.strip().split('\n') if h]

            commits = []
            total_additions = 0
            total_deletions = 0
            files_modified = set()

            for commit_hash in commit_hashes:
                commit_info = self.get_commit_info(commit_hash)
                if commit_info:
                    commits.append(commit_info)

                    for file_info in commit_info.get('files', []):
                        files_modified.add(file_info['path'])
                        total_additions += file_info.get('additions', 0)
                        total_deletions += file_info.get('deletions', 0)

            return {
                'contributor': contributor,
                'total_commits': len(commits),
                'total_files': len(files_modified),
                'total_additions': total_additions,
                'total_deletions': total_deletions,
                'commits': commits,
                'files': list(files_modified)
            }

        except Exception as e:
            print(f"Error getting contributor activity for {contributor}: {e}")
            return {
                'contributor': contributor,
                'total_commits': 0,
                'total_files': 0,
                'total_additions': 0,
                'total_deletions': 0,
                'commits': [],
                'files': []
            }
