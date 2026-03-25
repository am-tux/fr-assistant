#!/usr/bin/env python3
"""FedRAMP Git Repository Tracker - Main CLI Entry Point"""

import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

from src.config_loader import Config
from src.functions import TrackerFunctions


def main():
    """Main entry point for the tracker CLI"""
    parser = argparse.ArgumentParser(
        description='FedRAMP Git Repository Tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Initialize and ensure all repositories are cloned/updated
  %(prog)s init

  # Show all recent FedRAMP activity
  %(prog)s latest --days 7

  # Show GitHub RFCs
  %(prog)s rfcs --days 30

  # Show FedRAMP blog posts
  %(prog)s blog --days 30

  # Show upcoming FedRAMP events
  %(prog)s events --days 7

  # Get new files added in last 7 days
  %(prog)s new-files --repo docs --days 7

  # List recent commits
  %(prog)s commits --repo docs --days 30

  # Show history of a specific file
  %(prog)s file-history --repo docs --file README.md

  # Show contributor activity
  %(prog)s contributor --repo docs --name "john@example.com" --days 30
        '''
    )

    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize repositories (clone/fetch)')

    # New files command
    files_parser = subparsers.add_parser('new-files', help='List new files added')
    files_parser.add_argument('--repo', required=True, help='Repository name')
    files_parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')

    # Commits command
    commits_parser = subparsers.add_parser('commits', help='List recent commits')
    commits_parser.add_argument('--repo', required=True, help='Repository name')
    commits_parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')

    # File history command
    history_parser = subparsers.add_parser('file-history', help='Show history of a specific file')
    history_parser.add_argument('--repo', required=True, help='Repository name')
    history_parser.add_argument('--file', required=True, help='File path')

    # Contributor activity command
    contributor_parser = subparsers.add_parser('contributor', help='Show contributor activity')
    contributor_parser.add_argument('--repo', required=True, help='Repository name')
    contributor_parser.add_argument('--name', required=True, help='Contributor name or email')
    contributor_parser.add_argument('--days', type=int, default=30, help='Days to look back (default: 30)')

    # RFCs command
    rfcs_parser = subparsers.add_parser('rfcs', help='Show GitHub Discussions RFCs')
    rfcs_parser.add_argument('--days', type=int, default=30, help='Days to look back (default: 30)')

    # Blog command
    blog_parser = subparsers.add_parser('blog', help='Show FedRAMP blog posts')
    blog_parser.add_argument('--days', type=int, default=30, help='Days to look back (default: 30)')

    # Events command
    events_parser = subparsers.add_parser('events', help='Show upcoming FedRAMP events')
    events_parser.add_argument('--days', type=int, default=7, help='Days ahead to look (default: 7)')

    # Latest command (everything)
    latest_parser = subparsers.add_parser('latest', help='Show all recent FedRAMP activity')
    latest_parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        # Load configuration
        config = Config(args.config)
        functions = TrackerFunctions(config)

        # Execute command
        if args.command == 'init':
            return cmd_init(functions)

        elif args.command == 'new-files':
            return cmd_new_files(functions, args)

        elif args.command == 'commits':
            return cmd_commits(functions, args)

        elif args.command == 'file-history':
            return cmd_file_history(functions, args)

        elif args.command == 'contributor':
            return cmd_contributor(functions, args)

        elif args.command == 'rfcs':
            return cmd_rfcs(functions, args)

        elif args.command == 'blog':
            return cmd_blog(functions, args)

        elif args.command == 'events':
            return cmd_events(functions, args)

        elif args.command == 'latest':
            return cmd_latest(functions, args)

        else:
            print(f"Unknown command: {args.command}")
            return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_init(functions: TrackerFunctions) -> int:
    """Initialize repositories (clone/fetch)"""
    print("Initializing repositories...")
    results = functions.ensure_repositories()

    for repo_name, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {repo_name}")

    if all(results.values()):
        print("\nAll repositories ready!")
        return 0
    else:
        print("\nSome repositories failed to initialize.")
        return 1


def cmd_new_files(functions: TrackerFunctions, args) -> int:
    """List new files added"""
    since = datetime.now() - timedelta(days=args.days)

    print(f"Fetching new files from {args.repo} (last {args.days} days)...")

    # Ensure repo is up to date
    functions.ensure_repositories()

    files = functions.get_new_files_since(args.repo, since)

    if not files:
        print(f"No new files found in the last {args.days} days.")
        return 0

    print(f"\nFound {len(files)} new files:")
    print()

    for file_info in files:
        print(f"- {file_info['path']}")
        print(f"  Added: {file_info['date']} by {file_info['author']}")
        print(f"  Commit: {file_info['commit'][:7]} - {file_info['subject']}")
        print()

    return 0


def cmd_commits(functions: TrackerFunctions, args) -> int:
    """List recent commits"""
    since = datetime.now() - timedelta(days=args.days)

    print(f"Fetching commits from {args.repo} (last {args.days} days)...")

    # Ensure repo is up to date
    functions.ensure_repositories()

    commits = functions.get_commits_since(args.repo, since)

    if not commits:
        print(f"No commits found in the last {args.days} days.")
        return 0

    print(f"\nFound {len(commits)} commits:")
    print()

    for commit in commits:
        print(f"- {commit['hash'][:7]} by {commit['author']} on {commit['date']}")
        print(f"  {commit['subject']}")
        if commit.get('files'):
            files_count = len(commit['files'])
            total_add = sum(f.get('additions', 0) for f in commit['files'])
            total_del = sum(f.get('deletions', 0) for f in commit['files'])
            print(f"  Files: {files_count}, +{total_add}/-{total_del} lines")
        print()

    return 0


def cmd_file_history(functions: TrackerFunctions, args) -> int:
    """Show history of a specific file"""
    print(f"Fetching history for {args.file} in {args.repo}...")

    # Ensure repo is up to date
    functions.ensure_repositories()

    history = functions.get_file_history(args.repo, args.file)

    if not history:
        print(f"No history found for {args.file} (file may not exist).")
        return 0

    print(f"\nFound {len(history)} commits that modified {args.file}:")
    print()

    for commit in history:
        print(f"- {commit['hash'][:7]} by {commit['author']} on {commit['date']}")
        print(f"  {commit['subject']}")
        print(f"  Changes: +{commit['additions']}/-{commit['deletions']} lines")
        print()

    return 0


def cmd_contributor(functions: TrackerFunctions, args) -> int:
    """Show contributor activity"""
    since = datetime.now() - timedelta(days=args.days) if args.days else None

    print(f"Fetching activity for {args.name} in {args.repo}...")
    if args.days:
        print(f"Looking back {args.days} days...")

    # Ensure repo is up to date
    functions.ensure_repositories()

    activity = functions.get_contributor_activity(args.repo, args.name, since)

    if activity['total_commits'] == 0:
        print(f"\nNo activity found for {args.name}.")
        return 0

    print(f"\n## Activity Summary")
    print(f"- Total commits: {activity['total_commits']}")
    print(f"- Files modified: {activity['total_files']}")
    print(f"- Lines added: +{activity['total_additions']}")
    print(f"- Lines deleted: -{activity['total_deletions']}")
    print()

    print(f"## Files Modified ({len(activity['files'])})")
    for filepath in sorted(activity['files'])[:20]:  # Show first 20
        print(f"- {filepath}")
    if len(activity['files']) > 20:
        print(f"... and {len(activity['files']) - 20} more")
    print()

    print(f"## Recent Commits ({min(len(activity['commits']), 10)})")
    for commit in activity['commits'][:10]:
        print(f"- {commit['hash'][:7]} on {commit['date']}")
        print(f"  {commit['subject']}")
    if len(activity['commits']) > 10:
        print(f"... and {len(activity['commits']) - 10} more commits")
    print()

    return 0


def cmd_rfcs(functions: TrackerFunctions, args) -> int:
    """Show GitHub Discussions RFCs"""
    since = datetime.now() - timedelta(days=args.days)

    print(f"Fetching RFCs from GitHub Discussions (last {args.days} days)...")
    print()

    rfcs = functions.get_github_rfcs(since)

    if not rfcs:
        print(f"No RFCs found in the last {args.days} days.")
        return 0

    print(f"Found {len(rfcs)} RFCs:")
    print()

    for rfc in rfcs:
        print(f"- {rfc['title']}")
        print(f"  By: {rfc['author']} | Comments: {rfc['comments']}")
        print(f"  {rfc['url']}")
        print()

    return 0


def cmd_blog(functions: TrackerFunctions, args) -> int:
    """Show FedRAMP blog posts"""
    print("FedRAMP Blog Post Tracking")
    print()
    print("Note: FedRAMP.gov is a JavaScript-based site that cannot be scraped")
    print("with traditional tools. Blog posts require a headless browser to access.")
    print()
    print("To view FedRAMP blog posts, visit:")
    print("https://www.fedramp.gov/blog/")
    print()
    return 0


def cmd_events(functions: TrackerFunctions, args) -> int:
    """Show upcoming FedRAMP events"""
    print(f"Upcoming FedRAMP Events (next {args.days} days)")
    print()
    print("Note: FedRAMP.gov is a JavaScript-based site that cannot be scraped")
    print("with traditional tools. Events require a headless browser to access.")
    print()
    print("To view upcoming FedRAMP events, visit:")
    print("https://www.fedramp.gov/events/?view=cards")
    print()
    return 0


def cmd_latest(functions: TrackerFunctions, args) -> int:
    """Show all recent FedRAMP activity"""
    since = datetime.now() - timedelta(days=args.days)

    print(f"Fetching all FedRAMP activity (last {args.days} days)...")
    print()

    # Update repositories first
    functions.ensure_repositories()

    # Get RFCs
    print("## RFCs (GitHub Discussions)")
    print()
    rfcs = functions.get_github_rfcs(since)
    if rfcs:
        for rfc in rfcs[:5]:  # Show first 5
            print(f"- {rfc['title']}")
            print(f"  By: {rfc['author']} | Comments: {rfc['comments']}")
            print(f"  {rfc['url']}")
            print()
        if len(rfcs) > 5:
            print(f"... and {len(rfcs) - 5} more RFCs")
            print()
    else:
        print("No recent RFCs")
        print()

    # Events - currently not available via scraping
    # (FedRAMP.gov requires JavaScript rendering)
    print("## Upcoming Events")
    print()
    print("(Event scraping not available - visit https://www.fedramp.gov/events/?view=cards)")
    print()

    # Blog posts - currently not available via scraping
    # (FedRAMP.gov requires JavaScript rendering)
    print("## Blog Posts")
    print()
    print("(Blog scraping not available - visit https://www.fedramp.gov/blog/)")
    print()

    # Get git repository changes
    print("## Git Repository Changes")
    print()

    repo_configs = functions.config.get_repositories()
    total_commits = 0

    for repo_config in repo_configs:
        repo_name = repo_config['name']
        commits = functions.get_commits_since(repo_name, since)

        if commits:
            print(f"### {repo_name}")
            for commit in commits[:3]:  # Show first 3
                print(f"- {commit['hash'][:7]}: {commit['subject']}")
            if len(commits) > 3:
                print(f"  ... and {len(commits) - 3} more commits")
            print()
            total_commits += len(commits)

    if total_commits == 0:
        print("No recent commits")
        print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
