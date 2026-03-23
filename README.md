# Git Repository Tracker for Documentation Projects

A lightweight tool that monitors **git repositories**, providing detailed tracking of documentation changes, file history, and contributor activity.

**📊 Track:** Git commits and file changes | **📝 Report:** Daily + Weekly summaries | **🔍 Query:** File history and contributors

---

## Overview

This tracker monitors git repositories with a focus on documentation-focused projects:

### 🔍 Git Repository Tracking
Track what's being built and documented:
- **What files changed** (especially new files added - highest priority)
- **How much content changed** in each file
- **Documentation structure** evolution
- Commit history, contributors, and release activity

Rather than code-centric metrics like commit volume, this tool prioritizes:
- **Content-level changes** (what documentation was added/modified)
- **File-level tracking** (new, modified, deleted, renamed files)
- **Contributor activity** (who's working on what)

## Quick Start

### First Run - Choose Your Method

On your **first run**, the tracker will interactively ask how you want to run it:

```bash
./tracker.sh init

# You'll be prompted to choose:
# 1) Native Python - Fast, direct execution
# 2) Container - Isolated, reproducible environment
```

Your choice is saved and used automatically for future runs.

### Manual Method Selection

**Option 1: Native Python** (direct execution, faster)
```bash
pip3 install -r requirements.txt
python3 main.py init
python3 main.py daily-report
```

**Option 2: Container** (isolated, no Python install needed)
```bash
./tracker.sh --build
./tracker.sh init
./tracker.sh daily-report
```

**Change Your Preference:**
```bash
./tracker.sh --reset-config  # Choose again
./tracker.sh --show-config   # See current choice
```

### Basic Workflow

1. **Place this directory** anywhere on your system (fully portable)
2. **Initialize:** `./tracker.sh init` or `python3 main.py init`
3. **Generate reports:**
   - `./tracker.sh daily-report` - Git activity from last 24 hours
   - `./tracker.sh weekly-report` - Git summary from last 7 days
4. **Query repository data:**
   - `./tracker.sh new-files --repo docs --days 7` - Recently added files
   - `./tracker.sh commits --repo docs --days 30` - Recent commits
   - `./tracker.sh file-history --repo docs --file README.md` - File changes
   - `./tracker.sh contributor --repo docs --name "john@example.com"` - Contributor activity
5. **Review generated reports** in `./reports/`:
   - `daily/` - Daily git activity
   - `weekly/` - Weekly summaries

---

## Use Cases

**For Documentation Teams:**
- Track what documentation has been added or updated
- Understand which files are most actively maintained
- Monitor documentation completeness and evolution
- Identify documentation update patterns

**For Project Leaders:**
- See technical progress through commit history
- Track contributor activity and engagement
- Monitor project evolution over time
- Generate status reports automatically

**For Contributors:**
- Find out what changed recently in the documentation
- Understand project evolution over time
- Identify areas where contributions would be valuable
- Track your own contribution history

## Key Features

### 📄 Documentation-Focused Tracking
- **NEW FILES** are always reported and highlighted (highest priority)
- File additions, deletions, and renames tracked separately
- Content changes measured per file (not just total commit count)
- Lower thresholds optimized for documentation update patterns

### 📊 Automated Reports

**Daily Reports** (generated at 09:00 each day):
- New documentation files added (highest priority)
- Modified files with line change counts
- Deleted or renamed files
- Documentation structure changes
- Branch and release activity
- Saved to `./reports/daily/YYYY-MM-DD.md`

**Weekly Reports** (generated Monday at 09:00):
- Summary across all repositories
- All new documentation added during the week
- Top 10 most active files
- Contributor activity statistics
- Commit timeline by day of week
- Aggregated changes and trends
- Links to daily reports
- Saved to `./reports/weekly/YYYY-Www.md`

### Manual Report Generation

Both daily and weekly reports can be generated manually for any historical period, allowing retrospective analysis or report regeneration.

## Directory Structure

```
fr-git-tracker/
├── README.md              # This file
├── SPEC.md                # Detailed specification
├── USAGE.md               # Complete usage guide
├── config.yaml            # Configuration file
├── main.py                # Python CLI entry point
├── tracker.sh             # Universal wrapper (native/container)
├── Dockerfile             # Container image definition
├── requirements.txt       # Python dependencies
├── src/                   # Python source code
│   ├── config_loader.py   # Config parser
│   ├── git_tracker.py     # Git operations
│   ├── report_generator.py     # Report generation
│   └── functions.py       # High-level query functions
├── repos/                 # Cloned repositories (auto-created)
│   ├── docs/
│   ├── roadmap/
│   └── community/
└── reports/               # Generated reports (auto-created)
    ├── daily/             # Daily git activity
    │   ├── 2026-03-23.md
    │   └── ...
    └── weekly/            # Weekly summaries
        ├── 2026-W12.md
        └── ...
```

All paths are relative to this directory, making the setup portable across systems and users.

## Prerequisites

- **Git** installed and accessible in PATH
- Network access to clone from GitHub (repositories are public)
- **For Native Mode:** Python 3.11+ with pip
- **For Container Mode:** Podman or Docker

## Setup

### Native Python Setup

1. **Clone or place this directory** anywhere on your system
   ```bash
   cd /path/to/your/location
   ```

2. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Review configuration** in `config.yaml`
   - Repositories to track are already configured for FedRAMP organization
   - Adjust thresholds if needed
   - All paths are relative and will work automatically

4. **Initialize repositories**
   ```bash
   python3 main.py init
   ```

### Container Setup

1. **Clone or place this directory** anywhere on your system
   ```bash
   cd /path/to/your/location
   ```

2. **Build the container image (one-time)**
   ```bash
   ./tracker.sh --build
   ```

3. **Initialize repositories**
   ```bash
   ./tracker.sh init
   ```

The tool will automatically:
- Create `./repos/` directory if it doesn't exist
- Clone repositories to `./repos/[repo-name]/` if not present
- Run `git fetch` on existing repositories to get updates
- Create `./reports/daily/` and `./reports/weekly/` directories
- Generate daily and weekly reports based on configured schedule

## Configuration

### Tracked Repositories

Currently tracking 3 FedRAMP repositories:
- **docs** - Main documentation
- **roadmap** - FedRAMP roadmap
- **community** - Community resources

### Thresholds (Optimized for Documentation)

```yaml
thresholds:
  min_commits: 3            # Docs have fewer commits than code
  min_lines_changed: 100    # Per file threshold
  min_files_changed: 5      # Fewer files per update

always_report:
  - new_files_added         # ANY new files - CRITICAL
  - files_deleted
  - files_renamed
  - critical_files_changed
```

### Critical Files Tracked

For each repository, the following file types are considered critical:
- All `.md` and `.mdx` documentation files
- Navigation/structure files (`SUMMARY.md`, `_sidebar.md`, `_config.yml`, `mkdocs.yml`)
- Root documentation (`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`)
- Build/deploy configuration affecting documentation
- GitHub workflows for documentation builds

## Generated Reports

Reports are automatically generated and saved in `./reports/` with separate subdirectories for daily and weekly reports.

### Daily Report Format

Generated daily at 09:00 (configurable), covering the previous 24 hours:

```markdown
# Daily Git Activity Report - [DATE]

## [Repository Name]

### Summary
- Files modified: X
- Files added: X (highlighted)
- Files deleted: X
- Total lines changed: +X / -X

### 🆕 New Files Added
- path/to/new/file.md by author@example.com
  - Commit: abc123
  - Size: +150 lines

### Modified Files
- path/to/file.md: +45 / -12 lines
  - Updated by author@example.com in commit def456

### Documentation Structure Changes
- Files renamed, navigation changes, etc.
```

### Weekly Report Format

Generated weekly on Monday at 09:00 (configurable), covering the previous 7 days:

```markdown
# Weekly Git Activity Report - Week [WEEK], [YEAR]
**Period:** [START_DATE] to [END_DATE]

## Summary Across All Repositories
- Total repositories with changes: X
- Total files added: X
- Total files modified: X
- Total commits: X
- Active contributors: X

## [Repository Name]

### 🆕 New Documentation Added This Week
- path/to/new/file.md - Added on [date] by [author]
  - Size: +150 lines

### Most Active Files (by line changes)
1. path/to/file.md: +450 / -120 lines (8 commits)
   - Contributors: author1, author2

### Contributor Activity
- author1: 12 commits, +500 / -100 lines across 8 files
- author2: 6 commits, +200 / -50 lines across 4 files

### Commits by Day
- Monday: 5 commits
- Tuesday: 3 commits
[...]

### Day-by-Day Breakdown
- Monday 2026-03-17 - [Link to daily report] - 5 commits, 8 files
- Tuesday 2026-03-18 - [Link to daily report] - 3 commits, 4 files
[...]
```

## Example Commands

### Git Repository Queries

**Find what changed:**
```bash
./tracker.sh new-files --repo docs --days 7
./tracker.sh commits --repo docs --days 30
python3 main.py file-history --repo docs --file authentication.md
```

**Track contributors:**
```bash
./tracker.sh contributor --repo docs --name "john@example.com" --days 30
python3 main.py contributor --repo community --name "Jane Smith"
```

### Report Generation

```bash
# Generate today's report
./tracker.sh daily-report

# Generate report for specific date
python3 main.py daily-report --date 2026-03-15

# Generate weekly report
./tracker.sh weekly-report
```

## Report-Only Principle

The tracker operates in **read-only mode**:
- ✅ Clones repositories (if they don't exist)
- ✅ Runs `git fetch` to get updates
- ✅ Reads git history and data
- ❌ **NEVER** pushes changes
- ❌ **NEVER** modifies repository state
- ❌ **NEVER** makes commits

Local repository directories can be safely deleted; they will be re-cloned on next run.

## How It Works

### Data Collection

**Git Repository Data** (from git commands):
- `git log --diff-filter=A` - Track new files added
- `git log --diff-filter=D` - Track deleted files
- `git log --diff-filter=R` - Track renamed/moved files
- `git log --name-status` - File changes per commit
- `git diff` - Changes between commits/branches
- `git show` - Specific commit details
- `git branch` and `git tag` - Branch/tag listings

### Update Frequency

- **Git polling:** Every 60 minutes (configurable)
- **Daily reports:** Generated at 09:00 daily (configurable)
- **Weekly reports:** Generated at 09:00 on Mondays (configurable)
- **Data caching:** Git data cached to minimize operations

### Report Generation

The tool automatically generates two types of reports:

1. **Daily Reports** - Created each day covering the previous 24 hours
   - Saved to `./reports/daily/YYYY-MM-DD.md`
   - Focus on immediate changes and new files

2. **Weekly Reports** - Created weekly covering the previous 7 days
   - Saved to `./reports/weekly/YYYY-Www.md` (ISO week format)
   - Aggregate statistics and trends
   - Top 10 most active files
   - Contributor activity summary
   - Links to daily reports for detailed breakdown

## Customization

### Adding Repositories

Edit `config.yaml`:

```yaml
repositories:
  - name: "your-repo"
    url: "https://github.com/org/your-repo"
    path: "./repos/your-repo"
    primary_branch: "main"
    critical_files:
      - "**/*.md"
      - "README.md"
```

### Adjusting Thresholds

Modify thresholds in `config.yaml` based on your repository patterns:

```yaml
daily_report:
  thresholds:
    min_commits: 3          # Adjust based on activity level
    min_lines_changed: 100  # Per file threshold
    min_files_changed: 5    # Total files threshold
```

### Excluding Files from Reports

Add patterns to exclude from "big change" alerts (still tracked):

```yaml
excluded_patterns:
  - "package-lock.json"
  - "dist/*"
  - "_site/*"
```

## Portability

This entire directory is **fully portable**:
- All paths are relative to the directory location
- No hardcoded user paths
- Can be moved anywhere on any system
- Can be shared between users
- Can be checked into version control

## Troubleshooting

**Repositories not cloning?**
- Check network access to GitHub
- Verify git is installed: `git --version`
- Check repository URLs are accessible

**Reports not generating?**
- Verify `./reports/` directory exists or can be created
- Check file permissions
- Ensure repositories have been fetched

**Missing data?**
- Run `git fetch` manually in repository directories
- Verify repositories are on correct branch
- Check that repositories have commits in the tracking period

## Documentation

- **SPEC.md** - Complete technical specification
- **USAGE.md** - Detailed usage guide with all commands
- **RUNNING.md** - Quick reference for running modes
- **config.yaml** - Configuration with inline comments

## License

Configuration for tracking FedRAMP public repositories. All tracked repositories maintain their original licenses.

---

**Built for comprehensive git repository tracking.**

**📊 Pure Git Data:** No external API dependencies
**📝 Automated Reports:** Daily and weekly summaries
**🔍 Detailed Queries:** File history, contributors, and more
