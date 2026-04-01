#!/usr/bin/env python3
"""FedRAMP Git Repository Tracker - Main CLI Entry Point"""

import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

from src.config_loader import Config
from src.functions import TrackerFunctions
from src.tracker import TrackingManager


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

  # Show FedRAMP notices (official announcements)
  %(prog)s notices --days 30

  # Get new files added in last 7 days
  %(prog)s new-files --repo docs --days 7

  # List recent commits
  %(prog)s commits --repo docs --days 30

  # Show history of a specific file
  %(prog)s file-history --repo docs --file README.md

  # Show contributor activity
  %(prog)s contributor --repo docs --name "john@example.com" --days 30

  # Search repository content
  %(prog)s search "Rev5" --repo docs
  %(prog)s search "control SA-4" --context 3 --case-sensitive
  %(prog)s search "baseline" --file-pattern "*.md"
  %(prog)s search "High baseline"  # searches all repos

  # Track a discussion
  %(prog)s track add-discussion --url "https://github.com/..." --title "Title" --reason "Why" --priority critical

  # Track a keyword
  %(prog)s track add-keyword --term "High baseline" --context "Why tracking" --priority critical

  # List tracked items
  %(prog)s track list

  # Check tracked items for updates
  %(prog)s track check --days 7
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

    # Search command
    search_parser = subparsers.add_parser('search', help='Search repository content')
    search_parser.add_argument('pattern', help='Search pattern (supports regex)')
    search_parser.add_argument('--repo', help='Repository name (searches all repos if not specified)')
    search_parser.add_argument('--case-sensitive', action='store_true', help='Case-sensitive search')
    search_parser.add_argument('--context', type=int, default=0, help='Number of context lines to show (default: 0)')
    search_parser.add_argument('--file-pattern', help='Filter files by pattern (e.g., "*.md", "*.py")')

    # RFCs command
    rfcs_parser = subparsers.add_parser('rfcs', help='Show GitHub Discussions RFCs')
    rfcs_parser.add_argument('--days', type=int, default=30, help='Days to look back (default: 30)')

    # Blog command
    blog_parser = subparsers.add_parser('blog', help='Show FedRAMP blog posts')
    blog_parser.add_argument('--days', type=int, default=30, help='Days to look back (default: 30)')

    # Events command
    events_parser = subparsers.add_parser('events', help='Show upcoming FedRAMP events')
    events_parser.add_argument('--days', type=int, default=7, help='Days ahead to look (default: 7)')

    # Notices command
    notices_parser = subparsers.add_parser('notices', help='Show FedRAMP notices')
    notices_parser.add_argument('--days', type=int, default=30, help='Days to look back (default: 30)')

    # Latest command (everything)
    latest_parser = subparsers.add_parser('latest', help='Show all recent FedRAMP activity')
    latest_parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')

    # Track command (tracking management)
    track_parser = subparsers.add_parser('track', help='Manage tracked discussions and keywords')
    track_subparsers = track_parser.add_subparsers(dest='track_command', help='Tracking command')

    # track add-discussion
    track_add_disc = track_subparsers.add_parser('add-discussion', help='Add discussion to tracking')
    track_add_disc.add_argument('--url', required=True, help='GitHub discussion URL')
    track_add_disc.add_argument('--title', default='', help='Discussion title (optional)')
    track_add_disc.add_argument('--reason', default='', help='Why tracking this (optional)')
    track_add_disc.add_argument('--priority', default='medium',
                                choices=['critical', 'high', 'medium', 'low'],
                                help='Priority level (default: medium)')

    # track remove-discussion
    track_rem_disc = track_subparsers.add_parser('remove-discussion', help='Remove discussion from tracking')
    track_rem_disc.add_argument('--url', required=True, help='GitHub discussion URL to remove')

    # track add-keyword
    track_add_kw = track_subparsers.add_parser('add-keyword', help='Add keyword to tracking')
    track_add_kw.add_argument('--term', required=True, help='Keyword to track')
    track_add_kw.add_argument('--context', default='', help='Context/reason (optional)')
    track_add_kw.add_argument('--priority', default='medium',
                             choices=['critical', 'high', 'medium', 'low'],
                             help='Priority level (default: medium)')

    # track remove-keyword
    track_rem_kw = track_subparsers.add_parser('remove-keyword', help='Remove keyword from tracking')
    track_rem_kw.add_argument('--term', required=True, help='Keyword to remove')

    # track list
    track_list = track_subparsers.add_parser('list', help='List all tracked items')

    # track check
    track_check = track_subparsers.add_parser('check', help='Check tracked items for updates')
    track_check.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')

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

        elif args.command == 'search':
            return cmd_search(functions, args)

        elif args.command == 'rfcs':
            return cmd_rfcs(functions, args)

        elif args.command == 'blog':
            return cmd_blog(functions, args)

        elif args.command == 'events':
            return cmd_events(functions, args)

        elif args.command == 'notices':
            return cmd_notices(functions, args)

        elif args.command == 'latest':
            return cmd_latest(functions, args)

        elif args.command == 'track':
            return cmd_track(functions, args)

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


def cmd_search(functions: TrackerFunctions, args) -> int:
    """Search repository content"""
    repo_msg = f"in {args.repo}" if args.repo else "across all repositories"
    print(f"Searching {repo_msg} for: \"{args.pattern}\"")
    if args.file_pattern:
        print(f"Filtering files: {args.file_pattern}")
    print()

    # Ensure repos are up to date
    functions.ensure_repositories()

    try:
        matches = functions.search_content(
            pattern=args.pattern,
            repository=args.repo,
            case_sensitive=args.case_sensitive,
            context_lines=args.context,
            file_pattern=args.file_pattern
        )
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    if not matches:
        print(f"No matches found for \"{args.pattern}\"")
        return 0

    # Group matches by file
    by_file = {}
    for match in matches:
        file_key = f"{match['repository']}:{match['file']}"
        if file_key not in by_file:
            by_file[file_key] = []
        by_file[file_key].append(match)

    print(f"Found {len(matches)} matches in {len(by_file)} files:")
    print()

    # Display results grouped by file
    for file_key, file_matches in by_file.items():
        repo_name = file_matches[0]['repository']
        filepath = file_matches[0]['file']

        print(f"## [{repo_name}] {filepath}")
        print()

        for match in file_matches:
            if match.get('is_context'):
                # Context line (grayed out)
                print(f"    {match['line_number']:4d}  {match['content']}")
            else:
                # Actual match (highlighted)
                print(f"  → {match['line_number']:4d}  {match['content']}")

        print()

    # Summary
    total_repos = len(set(m['repository'] for m in matches))
    print(f"Summary: {len(matches)} matches across {len(by_file)} files in {total_repos} repositories")

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


def cmd_notices(functions: TrackerFunctions, args) -> int:
    """Show FedRAMP notices from RSS feed"""
    since = datetime.now() - timedelta(days=args.days)

    print(f"Fetching FedRAMP notices (last {args.days} days)...")
    print()

    notices = functions.get_fedramp_notices(since)

    if not notices:
        print(f"No notices found in the last {args.days} days.")
        print()
        print("To view all FedRAMP notices, visit:")
        print("https://www.fedramp.gov/notices/")
        return 0

    print(f"Found {len(notices)} notices:")
    print()

    for notice in notices:
        print(f"📢 {notice['title']}")
        print(f"   Date: {notice['date']}")
        print(f"   {notice['link']}")
        if notice.get('description'):
            # Truncate long descriptions
            desc = notice['description']
            if len(desc) > 200:
                desc = desc[:200] + "..."
            print(f"   {desc}")
        print()

    return 0


def cmd_latest(functions: TrackerFunctions, args) -> int:
    """Show all recent FedRAMP activity"""
    from src.tracker import TrackingManager, search_keywords_in_commits, search_keywords_in_discussions
    from src.web_scraper import WebScraper

    since = datetime.now() - timedelta(days=args.days)

    print(f"Fetching all FedRAMP activity (last {args.days} days)...")
    print()

    # Update repositories first
    functions.ensure_repositories()

    # Load tracking to see if we should prioritize items
    tracker = TrackingManager()
    tracked_discussions = tracker.get_tracked_discussions()
    tracked_keywords = tracker.get_tracked_keywords()
    has_tracking = tracker.has_tracked_items()

    # Get all data
    rfcs = functions.get_github_rfcs(since)

    # Get git repository changes
    repo_configs = functions.config.get_repositories()
    all_commits = []
    for repo_config in repo_configs:
        repo_name = repo_config['name']
        commits = functions.get_commits_since(repo_name, since)
        for commit in commits:
            commit['repository'] = repo_name
        all_commits.extend(commits)

    # If tracking is enabled, show tracked items first
    if has_tracking:
        print("⭐ TRACKED ITEMS - NEW ACTIVITY:")
        print()

        tracked_shown = False

        # Check tracked discussions
        if tracked_discussions:
            scraper = WebScraper()
            for disc in tracked_discussions:
                priority_emoji = {
                    'critical': '🚨',
                    'high': '📌',
                    'medium': '⚙️',
                    'low': 'ℹ️'
                }.get(disc.get('priority', 'medium'), '⚙️')

                print(f"{priority_emoji} {disc.get('title', 'Untitled')}")

                # Get discussion activity
                activity = scraper.get_discussion_activity(disc['url'])
                if activity:
                    print(f"   📊 {activity['comment_count']} comments | Last: {activity['last_activity']}")

                if disc.get('reason'):
                    print(f"   Why: {disc['reason']}")
                print(f"   {disc['url']}")
                print()
                tracked_shown = True

        # Search for tracked keywords
        if tracked_keywords:
            settings = tracker.get_settings()
            keyword_matches = []

            if settings.get('search_commits', True):
                keyword_matches.extend(search_keywords_in_commits(all_commits, tracked_keywords))

            if settings.get('search_discussions', True):
                keyword_matches.extend(search_keywords_in_discussions(rfcs, tracked_keywords))

            if keyword_matches:
                # Group by keyword
                by_keyword = {}
                for match in keyword_matches:
                    keyword = match['keyword']
                    if keyword not in by_keyword:
                        by_keyword[keyword] = []
                    by_keyword[keyword].append(match)

                print("🔍 KEYWORD ALERTS:")
                print()

                for keyword, matches in by_keyword.items():
                    keyword_info = matches[0]['keyword_info']
                    priority_emoji = {
                        'critical': '🚨',
                        'high': '📌',
                        'medium': '⚙️',
                        'low': 'ℹ️'
                    }.get(keyword_info.get('priority', 'medium'), '⚙️')

                    print(f"{priority_emoji} \"{keyword}\" found in {len(matches)} places")
                    for match in matches[:3]:  # Show first 3
                        if match['match_type'] == 'commit_message':
                            commit = match['commit']
                            print(f"   • [{match['repository']}] {commit['hash'][:7]}: {commit['subject']}")
                        elif match['match_type'] == 'discussion_title':
                            disc = match['discussion']
                            print(f"   • [Discussion] {disc['title']}")
                    if len(matches) > 3:
                        print(f"   ... and {len(matches) - 3} more")
                    print()

                tracked_shown = True

        if tracked_shown:
            print("---")
            print()

    # Get FedRAMP Notices (IMPORTANT - official announcements)
    notices = functions.get_fedramp_notices(since)
    print("## 📢 FedRAMP Notices (Official Announcements)")
    print()
    if notices:
        for notice in notices[:5]:  # Show first 5
            print(f"- {notice['title']}")
            print(f"  Date: {notice['date']}")
            print(f"  {notice['link']}")
            print()
        if len(notices) > 5:
            print(f"... and {len(notices) - 5} more notices")
            print()
    else:
        print("No recent notices")
        print()

    # Get RFCs
    print("## RFCs (GitHub Discussions)")
    print()
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

    total_commits = 0

    for repo_config in repo_configs:
        repo_name = repo_config['name']
        repo_commits = [c for c in all_commits if c.get('repository') == repo_name]

        if repo_commits:
            print(f"### {repo_name}")
            for commit in repo_commits[:3]:  # Show first 3
                print(f"- {commit['hash'][:7]}: {commit['subject']}")
            if len(repo_commits) > 3:
                print(f"  ... and {len(repo_commits) - 3} more commits")
            print()
            total_commits += len(repo_commits)

    if total_commits == 0:
        print("No recent commits")
        print()

    return 0


def cmd_track(functions: TrackerFunctions, args) -> int:
    """Manage tracked discussions and keywords"""
    tracker = TrackingManager()

    if not args.track_command:
        print("Track command requires a subcommand.")
        print("Use: track {add-discussion|remove-discussion|add-keyword|remove-keyword|list|check}")
        return 1

    if args.track_command == 'add-discussion':
        return cmd_track_add_discussion(tracker, args)

    elif args.track_command == 'remove-discussion':
        return cmd_track_remove_discussion(tracker, args)

    elif args.track_command == 'add-keyword':
        return cmd_track_add_keyword(tracker, args)

    elif args.track_command == 'remove-keyword':
        return cmd_track_remove_keyword(tracker, args)

    elif args.track_command == 'list':
        return cmd_track_list(tracker, args)

    elif args.track_command == 'check':
        return cmd_track_check(tracker, functions, args)

    else:
        print(f"Unknown track command: {args.track_command}")
        return 1


def cmd_track_add_discussion(tracker: TrackingManager, args) -> int:
    """Add discussion to tracking"""
    print(f"Adding discussion to tracking: {args.url}")

    success = tracker.add_discussion(
        url=args.url,
        title=args.title,
        reason=args.reason,
        priority=args.priority
    )

    if success:
        print("✓ Discussion added to tracking")
        return 0
    else:
        print("✗ Failed to add discussion (may already be tracked)")
        return 1


def cmd_track_remove_discussion(tracker: TrackingManager, args) -> int:
    """Remove discussion from tracking"""
    print(f"Removing discussion from tracking: {args.url}")

    success = tracker.remove_discussion(args.url)

    if success:
        print("✓ Discussion removed from tracking")
        return 0
    else:
        print("✗ Discussion not found in tracking")
        return 1


def cmd_track_add_keyword(tracker: TrackingManager, args) -> int:
    """Add keyword to tracking"""
    print(f"Adding keyword to tracking: \"{args.term}\"")

    success = tracker.add_keyword(
        term=args.term,
        context=args.context,
        priority=args.priority
    )

    if success:
        print("✓ Keyword added to tracking")
        return 0
    else:
        print("✗ Failed to add keyword (may already be tracked)")
        return 1


def cmd_track_remove_keyword(tracker: TrackingManager, args) -> int:
    """Remove keyword from tracking"""
    print(f"Removing keyword from tracking: \"{args.term}\"")

    success = tracker.remove_keyword(args.term)

    if success:
        print("✓ Keyword removed from tracking")
        return 0
    else:
        print("✗ Keyword not found in tracking")
        return 1


def cmd_track_list(tracker: TrackingManager, args) -> int:
    """List all tracked items"""
    print(tracker.list_all())
    return 0


def cmd_track_check(tracker: TrackingManager, functions: TrackerFunctions, args) -> int:
    """Check tracked items for updates"""
    from src.tracker import search_keywords_in_commits, search_keywords_in_discussions
    from src.web_scraper import WebScraper

    since = datetime.now() - timedelta(days=args.days)

    print(f"Checking tracked items for updates (last {args.days} days)...")
    print()

    if not tracker.has_tracked_items():
        print("No tracked items. Add some with:")
        print("  python3 main.py track add-discussion --url <URL>")
        print("  python3 main.py track add-keyword --term <TERM>")
        return 0

    # Update repositories
    functions.ensure_repositories()

    # Get tracked items
    tracked_discussions = tracker.get_tracked_discussions()
    tracked_keywords = tracker.get_tracked_keywords()
    settings = tracker.get_settings()

    # Check tracked discussions for activity
    if tracked_discussions:
        print("⭐ TRACKED DISCUSSIONS - ACTIVITY CHECK:")
        print()

        scraper = WebScraper()

        for disc in tracked_discussions:
            print(f"🔔 {disc.get('title', 'Untitled')}")
            print(f"   URL: {disc['url']}")
            print(f"   Priority: {disc.get('priority', 'medium')} | Reason: {disc.get('reason', 'N/A')}")

            # Get discussion activity
            activity = scraper.get_discussion_activity(disc['url'])

            if activity:
                print(f"   📊 Comments: {activity['comment_count']}")
                print(f"   📅 Last activity: {activity['last_activity']}")
                print(f"   👥 Participants: {activity['participant_count']}")
            else:
                print(f"   ⚠️  Could not fetch activity details")

            print()

    # Search for tracked keywords
    if tracked_keywords and (settings.get('search_commits', True) or settings.get('search_discussions', True)):
        print("⭐ KEYWORD ALERTS:")
        print()

        all_matches = []

        # Search in commits
        if settings.get('search_commits', True):
            for repo_config in functions.config.get_repositories():
                repo_name = repo_config['name']
                commits = functions.get_commits_since(repo_name, since)

                if commits:
                    # Add repository info to commits
                    for commit in commits:
                        commit['repository'] = repo_name

                    matches = search_keywords_in_commits(commits, tracked_keywords)
                    all_matches.extend(matches)

        # Search in discussions
        if settings.get('search_discussions', True):
            rfcs = functions.get_github_rfcs(since)
            if rfcs:
                matches = search_keywords_in_discussions(rfcs, tracked_keywords)
                all_matches.extend(matches)

        # Display matches
        if all_matches:
            # Group by keyword
            by_keyword = {}
            for match in all_matches:
                keyword = match['keyword']
                if keyword not in by_keyword:
                    by_keyword[keyword] = []
                by_keyword[keyword].append(match)

            for keyword, matches in by_keyword.items():
                keyword_info = matches[0]['keyword_info']
                priority_emoji = {
                    'critical': '🚨',
                    'high': '📌',
                    'medium': '⚙️',
                    'low': 'ℹ️'
                }.get(keyword_info.get('priority', 'medium'), '⚙️')

                print(f"{priority_emoji} \"{keyword}\" found in {len(matches)} places:")
                if keyword_info.get('context'):
                    print(f"   Context: {keyword_info['context']}")

                for match in matches[:5]:  # Show first 5 matches per keyword
                    if match['match_type'] == 'commit_message':
                        commit = match['commit']
                        print(f"   • [{match['repository']}] {commit['hash'][:7]}: {commit['subject']}")
                    elif match['match_type'] == 'discussion_title':
                        disc = match['discussion']
                        print(f"   • [Discussion] {disc['title']}")
                        print(f"     {disc['url']}")

                if len(matches) > 5:
                    print(f"   ... and {len(matches) - 5} more matches")

                print()
        else:
            print("No keyword matches found in the specified time range.")
            print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
