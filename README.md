# Git Repository Tracker for Documentation

An AI-powered tool that monitors git repositories containing documentation, tracks daily changes, and answers detailed questions about projects based solely on factual data.

## Overview

This tracker is specifically designed for **documentation repositories** (like the FedRAMP organization repos), where the focus is on:
- **What files changed** (especially new files added)
- **How much content changed** in each file
- **Documentation structure** evolution

Rather than code-centric metrics like commit volume, this tool prioritizes content-level changes that matter for documentation tracking.

## Key Features

### 📄 Documentation-Focused Tracking
- **NEW FILES** are always reported and highlighted (highest priority)
- File additions, deletions, and renames are tracked separately
- Content changes measured per file (not just total commit count)
- Lower thresholds optimized for documentation update patterns

### 📊 Factual Data + AI Interpretation
**Factual Data First (Always):**
- **Primary focus:** Factual information from git data
- Observable facts: commits, diffs, file changes, timestamps, authors
- Explicitly states when information is not available

**AI Interpretation (When Helpful):**
- **Clearly labeled** with 🤖 prefix to distinguish from facts
- Can interpret what code/documentation appears to do
- Can assess quality, clarity, or completeness
- Can analyze apparent purpose of changes
- Based on actual file content, not speculation
- Never replaces or obscures factual data

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

### 💬 Question Answering
Answer detailed questions about repositories:
- "What new documentation was added this week?"
- "What files changed in the last 30 days?"
- "Who has contributed to [specific file]?"
- "When was [file] first added?"
- All answers based on factual git data only

## Directory Structure

```
fr-git-tracker/
├── README.md           # This file
├── SPEC.md            # Detailed specification
├── config.yaml        # Configuration file
├── repos/             # Cloned repositories (visible directory)
│   ├── docs/
│   ├── roadmap/
│   └── community/
└── reports/           # Generated reports (visible directory)
    ├── daily/         # Daily reports
    │   ├── 2026-03-23.md
    │   ├── 2026-03-24.md
    │   └── ...
    └── weekly/        # Weekly reports
        ├── 2026-W12.md
        ├── 2026-W13.md
        └── ...
```

All paths are relative to this directory, making the setup portable across systems and users.

## Quick Start

### Prerequisites

- **Git** installed and accessible in PATH
- Network access to clone from GitHub (repositories are public)
- AI tool capable of running this specification (e.g., Claude)

### Setup

1. **Clone or place this directory** anywhere on your system
   ```bash
   # The entire directory is portable and user-agnostic
   cd /path/to/your/location
   ```

2. **Review configuration** in `config.yaml`
   - Repositories to track are already configured for FedRAMP organization
   - Adjust thresholds if needed
   - All paths are relative and will work automatically

3. **Run the tracker**
   - The tool will automatically:
     - Create `./repos/` directory if it doesn't exist
     - Clone repositories to `./repos/[repo-name]/` if not present
     - Run `git fetch` on existing repositories to get updates
     - Create `./reports/daily/` and `./reports/weekly/` directories
     - Generate daily and weekly reports based on configured schedule

### Manual Setup (Optional)

The tool handles setup automatically, but you can manually prepare repositories:

```bash
# Navigate to this directory
cd fr-git-tracker

# Create directories
mkdir -p repos reports/daily reports/weekly

# Clone repositories
cd repos
git clone https://github.com/FedRAMP/docs
git clone https://github.com/FedRAMP/roadmap
git clone https://github.com/FedRAMP/community
```

## Configuration

### Tracked Repositories

Currently tracking 3 FedRAMP repositories (excludes docs-alpha, fedramp-marketplace-preview, and Marketplace-poc):
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

### Manual Report Generation

Both daily and weekly reports can be generated manually for any historical period, allowing retrospective analysis or report regeneration.

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

All data comes exclusively from git commands:
- `git log --diff-filter=A` - Track new files added
- `git log --diff-filter=D` - Track deleted files
- `git log --diff-filter=R` - Track renamed/moved files
- `git log --name-status` - File changes per commit
- `git diff` - Changes between commits/branches
- `git show` - Specific commit details
- `git branch` and `git tag` - Branch/tag listings

### Update Frequency

- **Polling:** Every 60 minutes (configurable)
- **Daily reports:** Generated at 09:00 daily (configurable)
- **Weekly reports:** Generated at 09:00 on Mondays (configurable)
- **Data caching:** Git data cached in memory between polls

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

## Example Questions

The tool can answer questions like:

**New Content Tracking:**
- "What new documentation files were added this week?"
- "Show me all files added to the docs repository in March"
- "When was the authentication.md file first added?"

**Content Changes:**
- "What files changed in the last 7 days?"
- "How much did the README.md change this month?"
- "What documentation files were deleted recently?"

**Contributor Analysis:**
- "Who has contributed to the deployment guide?"
- "What files did john@example.com modify this week?"
- "List all contributors to the docs repository"

**Structure Analysis:**
- "What files were renamed or moved recently?"
- "Show changes to navigation configuration files"
- "What branches were merged this week?"

**Interpretation Questions:**
- "What does this new documentation cover?" (Factual + AI interpretation)
- "Is the documentation complete?" (Factual stats + AI assessment)
- "Why was this file changed?" (Factual + AI analysis of apparent intent)

### Example Response: Factual + AI Interpretation

**Question:** "What changed in the authentication guide?"

**Response:**
```
FACTS:
docs/authentication.md was modified in 2 commits:
- abc123 by user@example.com on 2026-03-20: 'update auth examples' (+45/-12 lines)
- def456 by user@example.com on 2026-03-21: 'add OAuth2 section' (+78/-0 lines)

Total changes: +123 / -12 lines

🤖 AI INTERPRETATION:
Based on the diff content, the changes add a new OAuth2 authentication section
with configuration examples for Google and GitHub providers. The updated examples
section now includes more detailed step-by-step flows with error handling. The
documentation appears to have expanded authentication coverage and improved
example clarity with real-world scenarios.
```

## How the Tool Works: Factual Data + AI Interpretation

### ✅ What the Tool DOES:

**Factual Reporting (Always):**
- Reports exact commits, diffs, file changes, timestamps, authors from git
- Shows precise line counts and file statistics
- Tracks new files, deletions, and renames
- Lists branches, tags, and releases

**AI Interpretation (When Labeled as 🤖):**
- Interprets what code/documentation appears to do (based on actual content)
- Assesses documentation quality, clarity, organization
- Analyzes apparent purpose of changes
- Provides context for understanding significance
- All clearly marked with 🤖 AI INTERPRETATION prefix

### ❌ What the Tool Does NOT Do:

- Does NOT predict future changes or roadmaps
- Does NOT make definitive claims about developer motivations
- Does NOT use external APIs (GitHub API, issue trackers, etc.)
- Does NOT modify or delete repositories
- Does NOT present AI interpretation as factual git data

**Key Principle:** Factual data always comes first, AI interpretation is clearly labeled and supplementary.

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
- **config.yaml** - Configuration with inline comments
- This README - User guide and quick start

## License

Configuration for tracking FedRAMP public repositories. All tracked repositories maintain their original licenses.

---

**Built for factual, reliable documentation tracking with zero speculation.**
