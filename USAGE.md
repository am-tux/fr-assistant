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

**Daily Report:**
```bash
python3 main.py daily-report
# Or with wrapper
./tracker.sh daily-report
```

**Daily Report (specific date):**
```bash
python3 main.py daily-report --date 2026-03-22
```

**Weekly Report:**
```bash
python3 main.py weekly-report
# Or with wrapper
./tracker.sh weekly-report
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

## Available Commands

### Core Reports
| Command | Description |
|---------|-------------|
| `init` | Clone/update all repositories |
| `daily-report` | Generate daily activity report |
| `weekly-report` | Generate weekly activity report |

### Git Repository Queries
| Command | Description |
|---------|-------------|
| `commits` | List recent commits |
| `new-files` | List newly added files |
| `file-history` | Show complete history of a specific file |
| `contributor` | Show contributor activity and statistics |

## Command Reference

### init

Clone or update all configured repositories.

```bash
./tracker.sh init
python3 main.py init
```

**What it does:**
- Clones repositories that don't exist locally
- Runs `git fetch` on existing repositories
- Creates necessary directories (`repos/`, `reports/`)

### daily-report

Generate a daily activity report for the last 24 hours.

```bash
./tracker.sh daily-report
./tracker.sh daily-report --date 2026-03-20
```

**Options:**
- `--date YYYY-MM-DD` - Generate report for specific date

**Output:**
- Saved to `./reports/daily/YYYY-MM-DD.md`
- Includes: new files, modified files, commits, contributors

### weekly-report

Generate a weekly summary report.

```bash
./tracker.sh weekly-report
./tracker.sh weekly-report --week 12 --year 2026
```

**Options:**
- `--week N` - Specific ISO week number
- `--year YYYY` - Specific year

**Output:**
- Saved to `./reports/weekly/YYYY-Www.md`
- Includes: summary statistics, top files, contributor activity

### commits

List recent commits for a repository.

```bash
./tracker.sh commits --repo docs --days 7
./tracker.sh commits --repo community --days 30
```

**Options:**
- `--repo NAME` - Repository name (required)
- `--days N` - Number of days to look back (default: 7)

**Output:**
- List of commits with hash, author, date, message
- File changes per commit

### new-files

List newly added files in a repository.

```bash
./tracker.sh new-files --repo docs --days 7
./tracker.sh new-files --repo roadmap --days 30
```

**Options:**
- `--repo NAME` - Repository name (required)
- `--days N` - Number of days to look back (default: 7)

**Output:**
- List of new files with creation date, author, size
- Helps identify new documentation topics

### file-history

Show complete change history for a specific file.

```bash
./tracker.sh file-history --repo docs --file README.md
./tracker.sh file-history --repo docs --file tools/site/content/index.md
```

**Options:**
- `--repo NAME` - Repository name (required)
- `--file PATH` - File path relative to repo root (required)

**Output:**
- All commits that modified the file
- Line changes per commit
- Complete timeline of file evolution

### contributor

Show activity and statistics for a specific contributor.

```bash
./tracker.sh contributor --repo docs --name "john@example.com"
./tracker.sh contributor --repo docs --name "John Smith" --days 30
```

**Options:**
- `--repo NAME` - Repository name (required)
- `--name NAME` - Contributor name or email (required)
- `--days N` - Number of days to look back (default: 30)

**Output:**
- Commit count and timeline
- Files modified
- Line changes (+/-)
- Activity summary

## Configuration

Edit `config.yaml` to:
- Add/remove repositories to track
- Set report thresholds and preferences
- Adjust polling intervals

## Directory Structure

```
fr-git-tracker/
├── main.py                 # CLI entry point
├── src/                    # Source code
│   ├── config_loader.py   # Configuration parser
│   ├── git_tracker.py     # Git operations
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

**Monitor specific files:**
```bash
# Track changes to README
./tracker.sh file-history --repo docs --file README.md

# See new files added
./tracker.sh new-files --repo docs --days 30
```

**Automated reporting workflow:**
```bash
# Daily: Run every morning to get yesterday's activity
python3 main.py daily-report

# Weekly: Run every Monday for the week summary
python3 main.py weekly-report
```

## Troubleshooting

**"Repository not found" error:**
- Run `python3 main.py init` first to clone repositories
- Check that repository name matches config.yaml

**No data in reports:**
- Make sure repositories are up to date: `python3 main.py init`
- Check date range - may be no activity in the selected timeframe

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
- **Size:** ~200MB
- **Includes:** Python, Git, PyYAML
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
