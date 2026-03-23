# FedRAMP Git Tracker - Usage Guide

## Installation

1. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Initialize repositories:**
   ```bash
   python3 main.py init
   ```

   This will clone all configured repositories to the `./repos/` directory.

## Quick Start

### Generate Reports

**Daily Report (today):**
```bash
python3 main.py daily-report
```

**Daily Report (specific date):**
```bash
python3 main.py daily-report --date 2026-03-22
```

**Weekly Report (this week):**
```bash
python3 main.py weekly-report
```

Reports are saved to:
- Daily: `./reports/daily/YYYY-MM-DD.md`
- Weekly: `./reports/weekly/YYYY-Www.md`

### Query Git Data

**Recent commits:**
```bash
python3 main.py commits --repo docs --days 7
```

**New files added:**
```bash
python3 main.py new-files --repo docs --days 30
```

**File history:**
```bash
# See all commits that modified a file
python3 main.py file-history --repo docs --file README.md
python3 main.py file-history --repo docs --file authentication.md
```

**Contributor activity:**
```bash
# See what a contributor has been working on
python3 main.py contributor --repo docs --name "john@example.com" --days 30
python3 main.py contributor --repo docs --name "Jane Smith"
```

### Query GitHub Discussions

**Open RFCs:**
```bash
python3 main.py rfcs --repo community
```

**Filter RFCs by topic:**
```bash
python3 main.py rfcs --repo community --topic Rev5
python3 main.py rfcs --repo community --topic 20x
```

**Most responded discussions:**
```bash
python3 main.py top-discussions --repo community --limit 10
```

**Filter by channel and timeframe:**
```bash
python3 main.py top-discussions --repo community --channel 20x --timeframe 7d
python3 main.py top-discussions --repo community --channel Rev5 --timeframe 30d
```

**Unanswered questions:**
```bash
# Show questions that need attention
python3 main.py unanswered --repo community --hours 48
python3 main.py unanswered --repo community --hours 72
```

**Discussions by channel:**
```bash
# See all discussions in a specific channel
python3 main.py channel-discussions --repo community --channel 20x --days 7
python3 main.py channel-discussions --repo community --channel Rev5 --days 30
```

**Detailed discussions reports (for community managers):**
```bash
# In-depth channel-by-channel analysis
python3 main.py daily-discussions-report --repo community
python3 main.py weekly-discussions-report --repo community
```

## Available Commands

### Core Reports
| Command | Description |
|---------|-------------|
| `init` | Clone/update all repositories |
| `daily-report` | Generate daily activity report (git + discussions highlights) |
| `weekly-report` | Generate weekly activity report (git + discussions summary) |

### Git Repository Queries
| Command | Description |
|---------|-------------|
| `commits` | List recent commits |
| `new-files` | List newly added files |
| `file-history` | Show complete history of a specific file |
| `contributor` | Show contributor activity and statistics |

### GitHub Discussions Queries
| Command | Description |
|---------|-------------|
| `rfcs` | List open RFCs with topic classification (Rev5/20x/General) |
| `top-discussions` | Get most responded discussions |
| `unanswered` | Show unanswered questions needing attention |
| `channel-discussions` | Show all discussions in a channel (20x/Rev5/RFCs) |

### Detailed Reports (for community managers)
| Command | Description |
|---------|-------------|
| `daily-discussions-report` | In-depth daily discussions breakdown by channel |
| `weekly-discussions-report` | In-depth weekly discussions summary by channel |

## Configuration

Edit `config.yaml` to:
- Add/remove repositories to track
- Configure discussion channels (20x, Rev5, RFCs)
- Set report thresholds and preferences
- Adjust polling intervals

## Directory Structure

```
fr-git-tracker/
├── main.py                 # CLI entry point
├── src/                    # Source code
│   ├── config_loader.py   # Configuration parser
│   ├── git_tracker.py     # Git operations
│   ├── discussions_tracker.py  # GitHub Discussions API
│   ├── report_generator.py     # Report generation
│   └── functions.py       # High-level query functions
├── config.yaml            # Configuration file
├── repos/                 # Cloned repositories (auto-created)
├── reports/               # Generated reports (auto-created)
│   ├── daily/
│   └── weekly/
└── requirements.txt       # Python dependencies
```

## Examples

**Track FedRAMP documentation changes:**
```bash
# Initialize repos
python3 main.py init

# See what changed this week
python3 main.py commits --repo docs --days 7

# Generate weekly report
python3 main.py weekly-report
```

**Monitor community discussions:**
```bash
# Get all open RFCs
python3 main.py rfcs --repo community

# Get Rev5-specific RFCs
python3 main.py rfcs --repo community --topic Rev5

# See hottest discussions
python3 main.py top-discussions --repo community --timeframe 7d --limit 5
```

**Automated reporting workflow:**
```bash
# Daily: Run every morning to get yesterday's activity
python3 main.py daily-report

# Weekly: Run every Monday for the week summary
python3 main.py weekly-report
```

## GitHub Token (Optional)

**Do you need a GitHub token?**
- **No token needed** for basic usage (daily/weekly reports)
- **Token recommended** if you're running reports frequently or querying discussions heavily

**GitHub API Limits:**
- Without token: 60 requests/hour (sufficient for occasional reports)
- With token: 5,000 requests/hour (for heavy usage)

**To set a token (optional):**
```bash
export GITHUB_TOKEN=your_github_personal_access_token
```

Get a token at: https://github.com/settings/tokens
Minimum scopes needed: `public_repo`, `read:discussion`

## Troubleshooting

**"API rate limit exceeded" error:**
- You've hit GitHub's 60 requests/hour limit
- Either wait an hour, or set a GitHub token (see above) for 5,000 requests/hour
- Reports will still generate with git data; only discussions data will be missing

**"Repository not found" error:**
- Run `python3 main.py init` first to clone repositories
- Check that repository name matches config.yaml

**No data in reports:**
- Make sure repositories are up to date: `python3 main.py init`
- Check date range - may be no activity in the selected timeframe
- For discussions, ensure GitHub token is set
