#!/usr/bin/env python3
"""FedRAMP Git & Community Tracker - Main CLI Entry Point"""

import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

from src.config_loader import Config
from src.functions import TrackerFunctions


def main():
    """Main entry point for the tracker CLI"""
    parser = argparse.ArgumentParser(
        description='FedRAMP Git Repository & Community Tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Initialize and ensure all repositories are cloned/updated
  %(prog)s init

  # Generate today's daily report
  %(prog)s daily-report

  # Generate daily report for a specific date
  %(prog)s daily-report --date 2026-03-22

  # Generate this week's weekly report
  %(prog)s weekly-report

  # Get open RFCs
  %(prog)s rfcs --repo community

  # Get open RFCs by topic
  %(prog)s rfcs --repo community --topic Rev5
  %(prog)s rfcs --repo community --topic 20x

  # Get most responded discussions
  %(prog)s top-discussions --repo community --limit 10

  # Get most responded discussions in specific channel
  %(prog)s top-discussions --repo community --channel 20x --timeframe 7d

  # Get new files added in last 7 days
  %(prog)s new-files --repo docs --days 7

  # Show history of a specific file
  %(prog)s file-history --repo docs --file README.md

  # Show contributor activity
  %(prog)s contributor --repo docs --name "john@example.com" --days 30

  # Show unanswered questions
  %(prog)s unanswered --repo community --hours 48

  # Show discussions in a specific channel
  %(prog)s channel-discussions --repo community --channel 20x --days 7

  # Generate detailed discussions reports (for community managers)
  %(prog)s daily-discussions-report --repo community
  %(prog)s weekly-discussions-report --repo community
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

    # Daily report command
    daily_parser = subparsers.add_parser('daily-report', help='Generate daily report (git only, no API calls)')
    daily_parser.add_argument('--date', help='Date for report (YYYY-MM-DD, defaults to today)')
    daily_parser.add_argument('--with-discussions', action='store_true',
                               help='Include discussions data (requires GitHub API, may hit rate limits)')

    # Weekly report command
    weekly_parser = subparsers.add_parser('weekly-report', help='Generate weekly report (git only, no API calls)')
    weekly_parser.add_argument('--date', help='Date within the week (YYYY-MM-DD, defaults to this week)')
    weekly_parser.add_argument('--with-discussions', action='store_true',
                                help='Include discussions data (requires GitHub API, may hit rate limits)')

    # RFCs command
    rfcs_parser = subparsers.add_parser('rfcs', help='List open RFCs')
    rfcs_parser.add_argument('--repo', required=True, help='Repository name')
    rfcs_parser.add_argument('--status', default='open', choices=['open', 'answered', 'closed', 'all'],
                             help='RFC status filter (default: open)')
    rfcs_parser.add_argument('--sort', default='newest',
                             choices=['newest', 'oldest', 'most_comments', 'most_reactions'],
                             help='Sort order (default: newest)')
    rfcs_parser.add_argument('--topic', choices=['Rev5', '20x', 'General'],
                             help='Filter by topic classification')

    # Top discussions command
    top_parser = subparsers.add_parser('top-discussions', help='Get most responded discussions')
    top_parser.add_argument('--repo', required=True, help='Repository name')
    top_parser.add_argument('--timeframe', default='7d', choices=['24h', '7d', '30d', 'all'],
                            help='Timeframe (default: 7d)')
    top_parser.add_argument('--channel', default='all',
                            help='Channel filter (20x, Rev5, RFCs, General, all)')
    top_parser.add_argument('--limit', type=int, default=10, help='Number of discussions (default: 10)')

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

    # Unanswered questions command
    unanswered_parser = subparsers.add_parser('unanswered', help='Show unanswered discussions')
    unanswered_parser.add_argument('--repo', required=True, help='Repository name')
    unanswered_parser.add_argument('--hours', type=int, default=48,
                                     help='Show questions older than N hours (default: 48)')

    # Discussions by channel command
    channel_parser = subparsers.add_parser('channel-discussions', help='Show discussions in a channel')
    channel_parser.add_argument('--repo', required=True, help='Repository name')
    channel_parser.add_argument('--channel', required=True, choices=['20x', 'Rev5', 'RFCs', 'General'],
                                 help='Channel name')
    channel_parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')

    # Detailed discussions reports
    daily_disc_parser = subparsers.add_parser('daily-discussions-report',
                                               help='Generate detailed daily discussions report')
    daily_disc_parser.add_argument('--repo', required=True, help='Repository name')
    daily_disc_parser.add_argument('--date', help='Date for report (YYYY-MM-DD, defaults to today)')

    weekly_disc_parser = subparsers.add_parser('weekly-discussions-report',
                                                help='Generate detailed weekly discussions report')
    weekly_disc_parser.add_argument('--repo', required=True, help='Repository name')
    weekly_disc_parser.add_argument('--date', help='Date within the week (YYYY-MM-DD, defaults to this week)')

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

        elif args.command == 'daily-report':
            return cmd_daily_report(functions, args)

        elif args.command == 'weekly-report':
            return cmd_weekly_report(functions, args)

        elif args.command == 'rfcs':
            return cmd_rfcs(functions, args)

        elif args.command == 'top-discussions':
            return cmd_top_discussions(functions, args)

        elif args.command == 'new-files':
            return cmd_new_files(functions, args)

        elif args.command == 'commits':
            return cmd_commits(functions, args)

        elif args.command == 'file-history':
            return cmd_file_history(functions, args)

        elif args.command == 'contributor':
            return cmd_contributor(functions, args)

        elif args.command == 'unanswered':
            return cmd_unanswered(functions, args)

        elif args.command == 'channel-discussions':
            return cmd_channel_discussions(functions, args)

        elif args.command == 'daily-discussions-report':
            return cmd_daily_discussions_report(functions, args)

        elif args.command == 'weekly-discussions-report':
            return cmd_weekly_discussions_report(functions, args)

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


def cmd_daily_report(functions: TrackerFunctions, args) -> int:
    """Generate daily report"""
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = datetime.now()

    print(f"Generating daily report for {date.strftime('%Y-%m-%d')}...")
    if args.with_discussions:
        print("  Including discussions data (this requires GitHub API access)...")
    else:
        print("  Git data only (no API calls). Use --with-discussions to include community data.")

    # Ensure repos are up to date
    functions.ensure_repositories()

    # Generate report
    report_path = functions.generate_daily_report(date, include_discussions=args.with_discussions)
    print(f"\n✓ Report generated: {report_path}")

    return 0


def cmd_weekly_report(functions: TrackerFunctions, args) -> int:
    """Generate weekly report"""
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = datetime.now()

    # Get week info
    start_date = date - timedelta(days=date.weekday())
    week_num = start_date.isocalendar()[1]
    year = start_date.year

    print(f"Generating weekly report for Week {week_num}, {year}...")
    if args.with_discussions:
        print("  Including discussions data (this requires GitHub API access)...")
    else:
        print("  Git data only (no API calls). Use --with-discussions to include community data.")

    # Ensure repos are up to date
    functions.ensure_repositories()

    # Generate report
    report_path = functions.generate_weekly_report(date, include_discussions=args.with_discussions)
    print(f"\n✓ Report generated: {report_path}")

    return 0


def cmd_rfcs(functions: TrackerFunctions, args) -> int:
    """List open RFCs"""
    print(f"Fetching {args.status} RFCs from {args.repo}...")

    rfcs = functions.get_open_rfcs(args.repo, args.status, args.sort)

    # Filter by topic if specified
    if args.topic:
        rfcs = [rfc for rfc in rfcs if rfc.get('topic') == args.topic]

    if not rfcs:
        print(f"No {args.status} RFCs found.")
        return 0

    # Group by topic for display
    topics = {'Rev5': [], '20x': [], 'General': []}
    for rfc in rfcs:
        topic = rfc.get('topic', 'General')
        topics[topic].append(rfc)

    # Display
    print(f"\nFound {len(rfcs)} RFCs:")
    print()

    for topic in ['Rev5', '20x', 'General']:
        topic_rfcs = topics[topic]
        if topic_rfcs:
            print(f"## {topic} RFCs ({len(topic_rfcs)})")
            print()
            for rfc in topic_rfcs:
                status = "Answered" if rfc['is_answered'] else "Open"
                print(f"- [{status}] {rfc['title']}")
                print(f"  Topic: {rfc.get('topic', 'N/A')} | Comments: {rfc['comment_count']} | Reactions: {rfc['reaction_count']}")
                print(f"  Created: {rfc['created_at'].strftime('%Y-%m-%d')} by {rfc['author']}")
                print(f"  URL: {rfc['url']}")
                print()

    return 0


def cmd_top_discussions(functions: TrackerFunctions, args) -> int:
    """Get most responded discussions"""
    print(f"Fetching top {args.limit} discussions from {args.repo} ({args.channel}, {args.timeframe})...")

    discussions = functions.get_most_responded_discussions(
        args.repo, args.timeframe, args.channel, args.limit
    )

    if not discussions:
        print("No discussions found.")
        return 0

    print(f"\nTop {len(discussions)} discussions by response count:")
    print()

    for idx, disc in enumerate(discussions, 1):
        status = "Answered" if disc['is_answered'] else "Open"
        print(f"{idx}. [{status}] {disc['title']}")
        print(f"   Channel: {disc['channel']} | Comments: {disc['comment_count']} | Reactions: {disc['reaction_count']}")
        print(f"   Created: {disc['created_at'].strftime('%Y-%m-%d')} by {disc['author']}")
        print(f"   URL: {disc['url']}")
        print()

    return 0


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


def cmd_unanswered(functions: TrackerFunctions, args) -> int:
    """Show unanswered discussions"""
    print(f"Fetching unanswered questions from {args.repo} (older than {args.hours} hours)...")

    unanswered = functions.get_unanswered_questions(args.repo, args.hours)

    if not unanswered:
        print(f"\n✓ No unanswered questions older than {args.hours} hours!")
        return 0

    print(f"\nFound {len(unanswered)} unanswered questions:")
    print()

    for disc in unanswered:
        age_hours = (datetime.now().astimezone() - disc['created_at']).total_seconds() / 3600
        age_days = int(age_hours / 24)

        print(f"- **{disc['title']}**")
        print(f"  Channel: {disc['channel']} | Age: {age_days} days")
        print(f"  Comments: {disc['comment_count']} | Reactions: {disc['reaction_count']}")
        print(f"  Created: {disc['created_at'].strftime('%Y-%m-%d')} by {disc['author']}")
        print(f"  URL: {disc['url']}")
        print()

    return 0


def cmd_channel_discussions(functions: TrackerFunctions, args) -> int:
    """Show discussions in a specific channel"""
    since = datetime.now() - timedelta(days=args.days)

    print(f"Fetching {args.channel} channel discussions from {args.repo} (last {args.days} days)...")

    discussions = functions.get_discussions_by_channel(args.repo, args.channel, since)

    if not discussions:
        print(f"\nNo discussions found in {args.channel} channel.")
        return 0

    print(f"\nFound {len(discussions)} discussions in {args.channel} channel:")
    print()

    for disc in discussions:
        status = "Answered" if disc['is_answered'] else "Open"
        print(f"- [{status}] **{disc['title']}**")
        print(f"  Comments: {disc['comment_count']} | Reactions: {disc['reaction_count']}")
        print(f"  Created: {disc['created_at'].strftime('%Y-%m-%d')} by {disc['author']}")
        print(f"  URL: {disc['url']}")
        print()

    return 0


def cmd_daily_discussions_report(functions: TrackerFunctions, args) -> int:
    """Generate detailed daily discussions report"""
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = datetime.now()

    print(f"Generating detailed daily discussions report for {args.repo} ({date.strftime('%Y-%m-%d')})...")

    report_path = functions.generate_daily_discussions_report(args.repo, date)
    print(f"\n✓ Report generated: {report_path}")

    return 0


def cmd_weekly_discussions_report(functions: TrackerFunctions, args) -> int:
    """Generate detailed weekly discussions report"""
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
    else:
        date = datetime.now()

    # Get week info
    start_date = date - timedelta(days=date.weekday())
    week_num = start_date.isocalendar()[1]
    year = start_date.year

    print(f"Generating detailed weekly discussions report for {args.repo} (Week {week_num}, {year})...")

    report_path = functions.generate_weekly_discussions_report(args.repo, date)
    print(f"\n✓ Report generated: {report_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
