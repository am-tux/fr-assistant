# FedRAMP Git Tracker - Usage Guide

## First Run Setup

**On your first run**, the tracker will interactively prompt you to choose your preferred method:

```bash
./tracker.sh init
```

You'll see a menu asking you to choose between:
1. **Native Python** - Direct execution, faster startup
2. **Container** - Isolated environment via Podman/Docker

The tracker will:
- Detect what's available on your system
- Recommend the best option
- Save your choice for future runs
- Allow you to change it anytime with `--reset-config`

---

## Choose Your Method

You can run the tracker in **two ways**:

### Option 1: Native Python (Recommended for development)
- Direct Python execution
- Faster startup (~100ms)
- Easier debugging
- **Requirements:** Python 3.11+, Git

### Option 2: Container (Recommended for production/isolation)
- Runs in Podman/Docker container
- Isolated environment (~1s startup)
- No Python installation needed on host
- **Requirements:** Podman or Docker

### Change Your Preference

```bash
# Reset and be prompted again
./tracker.sh --reset-config

# View current preference
./tracker.sh --show-config
```

---

## Installation

### Native Python Setup

1. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Initialize repositories:**
   ```bash
   python3 main.py init
   ```

### Container Setup

1. **Build the container image (one-time):**
   ```bash
   ./tracker.sh --build
   ```
   Or manually:
   ```bash
   podman build -t fedramp-tracker .
   # OR
   docker build -t fedramp-tracker .
   ```

2. **Initialize repositories:**
   ```bash
   ./tracker.sh init
   ```

---

## Universal Wrapper Script

The `tracker.sh` script **auto-detects** the best method and runs the tracker:

```bash
# Auto-detect and run
./tracker.sh daily-report

# Force native mode
./tracker.sh --mode native daily-report

# Force container mode
./tracker.sh --mode container daily-report

# Set default mode via environment variable
export TRACKER_MODE=container
./tracker.sh daily-report
```

**Note:** All examples below work with either:
- `python3 main.py [command]` (native)
- `./tracker.sh [command]` (auto-detect/container)
- Direct podman/docker run (see Advanced Usage)

---

## Quick Start

### Generate Reports

**Daily Report (git data only, no API calls):**
```bash
python3 main.py daily-report
# Or with wrapper
./tracker.sh daily-report
```

**Daily Report (specific date):**
```bash
python3 main.py daily-report --date 2026-03-22
```

**Daily Report with discussions (requires GitHub API):**
```bash
python3 main.py daily-report --with-discussions
# May hit rate limits without token
```

**Weekly Report (git data only, no API calls):**
```bash
python3 main.py weekly-report
# Or with wrapper
./tracker.sh weekly-report
```

**Weekly Report with discussions (requires GitHub API):**
```bash
python3 main.py weekly-report --with-discussions
```

**Key Points:**
- Default reports = **NO API calls** (git only, always work)
- Add `--with-discussions` = Includes community data (requires API, may hit rate limits)
- Separate detailed discussion reports available: `daily-discussions-report`, `weekly-discussions-report`

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

**Container-specific issues:**
- **Permission errors:** Container creates files as container user
  - The wrapper script runs as your user to avoid this
  - Or manually: `podman run --user $(id -u):$(id -g) ...`
- **Image not found:** Build it first: `./tracker.sh --build`
- **Volume mount errors:** Check that config.yaml exists in current directory

## Advanced Container Usage

### Direct Podman/Docker Commands

If you prefer not to use the wrapper script:

```bash
# Build image
podman build -t fedramp-tracker .

# Run a command
podman run --rm \
  --user=$(id -u):$(id -g) \
  -v ./config.yaml:/data/config.yaml:ro \
  -v ./repos:/data/repos \
  -v ./reports:/data/reports \
  -e GITHUB_TOKEN="${GITHUB_TOKEN}" \
  fedramp-tracker daily-report

# Initialize repos
podman run --rm \
  --user=$(id -u):$(id -g) \
  -v ./config.yaml:/data/config.yaml:ro \
  -v ./repos:/data/repos \
  -v ./reports:/data/reports \
  fedramp-tracker init
```

Replace `podman` with `docker` if using Docker.

### Container Image Details

- **Base:** python:3.11-slim
- **Size:** ~250MB
- **Includes:** Python, Git, PyYAML, requests
- **User:** Runs as your UID/GID to avoid permission issues
- **Volumes:**
  - `/data/config.yaml` - Configuration (read-only)
  - `/data/repos` - Git repositories (read-write)
  - `/data/reports` - Generated reports (read-write)

### When to Use Container vs Native

**Use Container when:**
- ✅ You want isolation from host system
- ✅ You're deploying to production/server
- ✅ You don't want to install Python locally
- ✅ You're running in CI/CD pipelines
- ✅ You want reproducible environments

**Use Native when:**
- ✅ You're actively developing/debugging
- ✅ You want faster startup times
- ✅ You're comfortable with Python environments
- ✅ You want direct access to git operations

## Automation Examples

### Cron Jobs (Native)
```bash
# Daily report at 9 AM
0 9 * * * cd /path/to/fr-git-tracker && python3 main.py daily-report

# Weekly report on Monday at 9 AM
0 9 * * 1 cd /path/to/fr-git-tracker && python3 main.py weekly-report
```

### Cron Jobs (Container)
```bash
# Daily report at 9 AM
0 9 * * * cd /path/to/fr-git-tracker && ./tracker.sh --mode container daily-report

# Weekly report on Monday at 9 AM
0 9 * * 1 cd /path/to/fr-git-tracker && ./tracker.sh --mode container weekly-report
```

### Systemd Timer (Container)
```ini
# /etc/systemd/system/fedramp-tracker-daily.service
[Unit]
Description=FedRAMP Tracker Daily Report

[Service]
Type=oneshot
WorkingDirectory=/opt/fr-git-tracker
ExecStart=/opt/fr-git-tracker/tracker.sh --mode container daily-report
User=tracker
Group=tracker

# /etc/systemd/system/fedramp-tracker-daily.timer
[Unit]
Description=FedRAMP Tracker Daily Report Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```
