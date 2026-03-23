# Git Repository & Community Tracker for Documentation Projects

An AI-powered tool that monitors **both documentation repositories and community discussions**, providing a complete picture of what's being built and what the community is saying about it.

**📊 Track:** Git commits + GitHub Discussions | **🤖 Analyze:** Content changes + Community sentiment | **📝 Report:** Daily + Weekly summaries

---

## Overview

This tracker monitors **two complementary data sources** for documentation-focused projects:

### 🔍 Git Repository Tracking
Track what's being built and documented:
- **What files changed** (especially new files added - highest priority)
- **How much content changed** in each file
- **Documentation structure** evolution
- Commit history, contributors, and release activity

### 💬 GitHub Discussions Tracking
Track what the community is saying:
- Discussions organized by channels: **20x**, **Rev5**, **RFCs**
- Questions, feedback, announcements, and ideas
- Community engagement patterns and sentiment
- Unanswered questions and trending topics

Rather than code-centric metrics like commit volume, this tool prioritizes:
- **Content-level changes** (what documentation was added/modified)
- **Community engagement patterns** (what people are asking/discussing)
- **Correlation between commits and discussions** (addressing community needs)

## Quick Start

1. **Place this directory** anywhere on your system (fully portable)
2. **Set GitHub token** (optional): `export GITHUB_TOKEN=your_token_here`
3. **Run the tracker** - it will automatically:
   - Clone FedRAMP repositories (docs, roadmap, community)
   - Fetch GitHub Discussions data
   - Generate daily and weekly reports
4. **Ask questions:**
   - "What new documentation was added this week?"
   - "What are the top discussions in the 20x channel?"
   - "What RFCs are currently open?"
   - "Show me what changed in authentication.md"
5. **Review automated reports** in `./reports/`:
   - `daily/` - Repository changes
   - `weekly/` - Repository summaries
   - `discussions/daily/` - Community activity by channel
   - `discussions/weekly/` - Community insights with AI analysis

## Use Cases

**For Documentation Teams:**
- Track what documentation has been added or updated
- Understand which files are most actively maintained
- Correlate documentation updates with community questions
- Identify documentation gaps based on frequently asked questions

**For Community Managers:**
- Monitor discussion channels (20x, Rev5, RFCs) in one place
- **Track open RFCs** - see all Request for Comments proposals and their status
- **Track most responded discussions** to identify hot topics and community priorities
- Identify trending topics and common concerns
- Track answer rates and response times
- Get AI-powered insights on community sentiment and themes
- Find unanswered questions needing attention
- Discover high-engagement discussions needing official response
- Identify RFCs ready for decision or needing more input
- Track time-to-answer for RFCs and community questions
- Understand what makes discussions generate high participation

**For Project Leaders:**
- See both technical progress (commits) and community feedback (discussions)
- Understand if documentation updates address community needs
- Track engagement trends week over week
- Get actionable insights for improving community support

**For Contributors:**
- Find out what changed recently in the documentation
- See what topics the community is actively discussing
- Identify areas where contributions would be valuable
- Understand project evolution over time

## Key Features

### 📄 Documentation-Focused Tracking
- **NEW FILES** are always reported and highlighted (highest priority)
- File additions, deletions, and renames are tracked separately
- Content changes measured per file (not just total commit count)
- Lower thresholds optimized for documentation update patterns

### 💬 GitHub Discussions Tracking
- **Community engagement monitoring** for repositories with GitHub Discussions
- **RFC (Request for Comments) tracking** - list open RFCs, track status, identify readiness
- Track new discussions, questions, announcements, and ideas
- Monitor discussion activity (comments, reactions, answers)
- Identify unanswered questions and trending topics
- Track most responded discussions to find hot topics
- **Clearly labeled** with 💬 prefix to distinguish from git data
- Separate from repository code/documentation changes
- Organized by channels: 20x, Rev5, RFCs

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
- 💬 GitHub Discussions activity (new discussions, active discussions)
- Saved to `./reports/daily/YYYY-MM-DD.md`

**Weekly Reports** (generated Monday at 09:00):
- Summary across all repositories
- All new documentation added during the week
- Top 10 most active files
- Contributor activity statistics
- Commit timeline by day of week
- Aggregated changes and trends
- 💬 GitHub Discussions summary (top discussions, answered questions)
- Links to daily reports
- Saved to `./reports/weekly/YYYY-Www.md`

**Daily Discussions Reports** (generated at 09:00 each day):
- 💬 Community engagement grouped by channels: **20x**, **Rev5**, **RFCs**
- New discussions, active discussions, answered questions per channel
- **Top 3 most responded discussions** from last 24 hours
- 🤖 AI interpretation of themes, sentiment, and urgency
- Unanswered questions needing attention
- Saved to `./reports/discussions/daily/YYYY-MM-DD.md`

**Weekly Discussions Reports** (generated Monday at 09:00):
- 💬 Community summary grouped by channels: **20x**, **Rev5**, **RFCs**
- Top discussions, engagement metrics, answer rates per channel
- **Top 10 most responded discussions** from last 7 days with analysis
- Cross-channel theme analysis
- Community health indicators
- 🤖 AI interpretation with actionable insights and recommendations
- 🤖 AI analysis of why high-response discussions are generating engagement
- Saved to `./reports/discussions/weekly/YYYY-Www.md`

### 💬 Question Answering
Answer detailed questions about repositories and community:
- "What new documentation was added this week?"
- "What files changed in the last 30 days?"
- "Who has contributed to [specific file]?"
- "When was [file] first added?"
- "What discussions are active in the community?"
- "What questions are unanswered?"
- "What are the top community topics this week?"
- Git data answers are factual, discussions data labeled with 💬

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
    ├── daily/         # Daily repository reports
    │   ├── 2026-03-23.md
    │   ├── 2026-03-24.md
    │   └── ...
    ├── weekly/        # Weekly repository reports
    │   ├── 2026-W12.md
    │   ├── 2026-W13.md
    │   └── ...
    └── discussions/   # GitHub Discussions reports
        ├── daily/     # Daily discussions reports (grouped by channels)
        │   ├── 2026-03-23.md
        │   ├── 2026-03-24.md
        │   └── ...
        └── weekly/    # Weekly discussions reports (with AI analysis)
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
- **GitHub API token** (optional but recommended for Discussions tracking)
  - Without token: 60 API requests/hour
  - With token: 5,000 API requests/hour
  - Create token at: https://github.com/settings/tokens
  - Set environment variable: `export GITHUB_TOKEN=your_token_here`

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
mkdir -p repos reports/daily reports/weekly reports/discussions/daily reports/discussions/weekly

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
  - 💬 Also tracks GitHub Discussions (https://github.com/FedRAMP/community/discussions)
  - **Discussion Channels:** 20x, Rev5, RFCs
  - Generates dedicated daily and weekly discussions reports with AI interpretation

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

## GitHub Discussions Activity

💬 GITHUB DISCUSSIONS (community repository):

### New Discussions Created
- [Discussion Title](URL) by @username in Q&A
  - Created: 2026-03-23 10:30
  - Current: 3 comments, 5 reactions

### Active Discussions (Updated Today)
- [Discussion Title](URL)
  - Last updated: 2026-03-23 14:15
  - Activity: +2 new comments by @user1, @user2
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

## GitHub Discussions Summary

💬 GITHUB DISCUSSIONS (community repository):

### Week Overview
- New discussions created: 8
- Total comments added: 34
- Questions answered: 5
- Most active category: Q&A

### Top Discussions This Week (by engagement)
1. [How to implement X feature?](URL) - 12 comments, 8 reactions
2. [Announcement: New guidelines](URL) - 6 comments, 15 reactions

### Unanswered Questions
- [Question about Y](URL) - Created 2026-03-20, 3 days old

### Day-by-Day Breakdown
- Monday 2026-03-17 - [Link to daily report] - 5 commits, 8 files
- Tuesday 2026-03-18 - [Link to daily report] - 3 commits, 4 files
[...]
```

### Manual Report Generation

Both daily and weekly reports can be generated manually for any historical period, allowing retrospective analysis or report regeneration.

## Example Commands

### Git Repository Queries

**Find what changed:**
```
"What new documentation files were added this week?"
"Show me all files changed in the last 7 days"
"What files were deleted or renamed in March?"
"How much did the authentication.md file change this month?"
```

**Understand content changes:**
```
"What changed in the deployment guide?"
# Returns: Git diff data + 🤖 AI interpretation of changes

"What does the new OAuth2 section cover?"
# Returns: File content + 🤖 AI summary of what it explains

"Show me the diff for commit abc123"
# Returns: Exact git diff output
```

**Track contributors:**
```
"Who has contributed to the security documentation?"
"What files did john@example.com modify this week?"
"List all contributors to the docs repository"
```

### GitHub Discussions Queries

**Channel-specific questions:**
```
"What are the active discussions in the 20x channel?"
"Show me new questions in the Rev5 channel this week"
"List unanswered questions in the RFCs channel"
```

**RFC (Request for Comments) tracking:**
```
# Get all currently open RFCs
getOpenRFCs("community", "open", "newest")
# Returns: List of open RFC proposals with status + 🤖 AI assessment

# Natural language queries
"What RFCs are currently open?"
"Show me open RFCs from the RFC discussion group"
"Which RFCs have been answered recently?"
"What are the most discussed RFCs?"
"Are there any stale RFCs that need attention?"

# Topic-specific queries (RFCs are classified as Rev5, 20x, or General)
"What Rev5 RFCs are currently open?"
"Show me all 20x-related RFCs"
"Are there more Rev5 or 20x RFCs in the pipeline?"
"What RFCs are about Rev5 baseline updates?"
"Show me RFCs related to FedRAMP 2.0 modernization"
# Returns: RFCs grouped by topic with classification (Rev5, 20x, or General)

# Get RFCs by status
getOpenRFCs("community", "answered", "newest")  # Recently answered
getOpenRFCs("community", "closed", "newest")    # Closed RFCs
getOpenRFCs("community", "all", "most_comments") # All RFCs, most discussed first

# Find specific types
"Show me RFCs ready for decision"
# Returns: RFCs with good engagement and apparent consensus + 🤖 AI recommendation

"Which RFCs need more community input?"
# Returns: RFCs with low engagement or aging without resolution
```

**Engagement and trends:**
```
"What are the top discussions by engagement this week?"
"Which discussions have the most comments?"
"What questions were answered today?"
"Show me discussions with no response in the last 48 hours"
```

**Most responded discussions:**
```
# Get top 10 most responded discussions from last 7 days (all channels)
getMostRespondedDiscussions("community", "7d", "all", 10)
# Returns: Ranked list with comment counts + 🤖 AI analysis of engagement drivers

# Get top 5 most responded 20x discussions from last 30 days
getMostRespondedDiscussions("community", "30d", "20x", 5)
# Returns: 20x channel top discussions + why they're generating high engagement

# Get top discussions that need attention (high responses, no resolution)
"Show me high-response discussions without official answers"
# Returns: Discussions with 30+ comments needing attention

# Analyze most responded discussions
"Why is discussion X getting so many responses?"
# Returns: Comment count data + 🤖 AI analysis of engagement patterns
```

**Community insights:**
```
"What are the common themes in Rev5 discussions?"
# Returns: Discussion list + 🤖 AI theme analysis

"What is the community sentiment about the new guidelines?"
# Returns: Engagement data + 🤖 AI sentiment assessment

"What topics are trending in the community?"
# Returns: Metrics + 🤖 AI pattern analysis
```

### Combined Git + Discussions Analysis

**Correlate commits and discussions:**
```
"Show me what was committed this week and what the community is discussing"
# Returns: Git changes + related discussions activity

"Are there discussions about the recent authentication documentation changes?"
# Returns: Recent commits + discussions mentioning those topics

"What documentation is missing based on community questions?"
# Returns: Analysis of common questions + gaps in current docs
```

**Trend analysis:**
```
"Compare documentation updates with community question topics"
"What new documentation corresponds to recent RFCs?"
"How has community engagement changed with the new Rev5 updates?"
```

### Report Generation

**Generate reports:**
```
# Today's repository report
generateDailyReport(today)

# Specific date repository report
generateDailyReport("2026-03-15")

# Weekly repository report
generateWeeklyReport(12, 2026)

# Today's discussions report (includes top 3 most responded discussions)
generateDailyDiscussionsReport(today, "community")

# Weekly discussions report (includes top 10 most responded discussions)
generateWeeklyDiscussionsReport(12, 2026, "community")

# On-demand most responded discussions report
getMostRespondedDiscussions("community", "7d", "all", 10)

# Get most responded discussions by specific channel
getMostRespondedDiscussions("community", "30d", "20x", 5)
getMostRespondedDiscussions("community", "30d", "Rev5", 5)
getMostRespondedDiscussions("community", "30d", "RFCs", 5)

# Open RFCs report
getOpenRFCs("community", "open", "newest")  # All currently open RFCs
getOpenRFCs("community", "all", "most_comments")  # All RFCs by engagement
getOpenRFCs("community", "answered", "newest")  # Recently answered RFCs
```

### Example Response

**Query:** "What changed in authentication docs and what is the community asking about it?"

**Response:**
```
GIT REPOSITORY DATA:
docs/authentication.md modified in 2 commits:
- abc123: 'update OAuth2 examples' (+67/-12 lines)
- def456: 'add SAML configuration' (+145/-3 lines)

🤖 AI INTERPRETATION (Git):
OAuth2 section enhanced with error handling examples.
New SAML configuration section added covering setup and troubleshooting.

---

💬 GITHUB DISCUSSIONS:
20x Channel:
- "How to implement OAuth2 with Azure AD?" (answered)
- Asked before the doc update, addressed in new changes

Rev5 Channel:
- "SAML configuration questions" (unanswered, 2 days old)
- Asked after SAML docs were added

🤖 AI INTERPRETATION (Discussions):
Community questions align with documentation updates. OAuth2 question
was answered and addressed in docs. SAML discussion needs response
pointing to the new documentation section.

CORRELATION:
Documentation updates are responsive to community needs. Consider
linking to new SAML docs in the unanswered discussion.
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

**GitHub Discussions Data** (from GitHub API - when enabled):
- `GET /repos/{owner}/{repo}/discussions` - Fetch discussions
- Track: new discussions, comments, reactions, answers
- Labeled with 💬 to distinguish from git data
- Cached to respect API rate limits

### Update Frequency

- **Git polling:** Every 60 minutes (configurable)
- **Discussions polling:** Every 60 minutes for new, every 6 hours for updates (configurable)
- **Daily reports:** Generated at 09:00 daily (configurable)
- **Weekly reports:** Generated at 09:00 on Mondays (configurable)
- **Data caching:** Git data and discussions data cached to minimize API calls

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

## How the Tool Works

### Dual Data Sources

**Git Repository Data (Factual):**
- Exact commits, diffs, file changes, timestamps, authors
- Precise line counts and file statistics
- New files, deletions, and renames
- Branches, tags, and releases
- All sourced from git commands

**GitHub Discussions Data (Factual + Community):**
- Discussion titles, bodies, authors, timestamps
- Comments, reactions, answers, engagement metrics
- Grouped by channels (20x, Rev5, RFCs)
- All sourced from GitHub API
- Labeled with 💬 to distinguish from git data

### ✅ What the Tool DOES:

**Repository Tracking:**
- Monitors git repositories for documentation changes
- Identifies new content, modifications, and reorganizations
- Tracks contributor activity and commit patterns
- Generates daily and weekly repository reports

**Community Tracking:**
- Monitors GitHub Discussions across organized channels
- Identifies questions, feedback, and community concerns
- Tracks engagement, answers, and trending topics
- Generates daily and weekly discussions reports with AI insights

**AI Interpretation (Clearly Labeled with 🤖):**
- Interprets what code/documentation appears to do (based on actual content)
- Assesses documentation quality, clarity, or completeness
- Analyzes apparent purpose of changes
- Identifies discussion themes and community sentiment
- Provides actionable insights for community managers
- Offers context for understanding significance
- Never replaces or obscures factual data

### ❌ What the Tool Does NOT Do:

**Repository Management:**
- Does NOT modify or delete repositories
- Does NOT push changes or create commits
- Does NOT modify repository state

**Predictions and Speculation:**
- Does NOT predict future changes or roadmaps
- Does NOT make definitive claims about developer motivations
- Does NOT speculate about internal FedRAMP decisions

**External Services:**
- Does NOT use issue trackers or pull request APIs
- Does NOT access private repositories
- Only uses GitHub API for public discussions (when configured)

**AI Limitations:**
- Does NOT present AI interpretation as factual data (always labeled with 🤖)
- Does NOT make security assessments without explicit request
- Does NOT compare to external standards without basis

**Key Principles:**
1. **Factual data always comes first** - Git/API data before interpretation
2. **Clear labeling** - 💬 for discussions, 🤖 for AI interpretation
3. **Read-only operations** - Never modifies tracked repositories
4. **Transparency** - Always clear about data source and certainty level

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

- **SPEC.md** - Complete technical specification with example commands
- **config.yaml** - Configuration with inline comments and channel definitions
- **README.md** - This file: user guide and quick start

## License

Configuration for tracking FedRAMP public repositories. All tracked repositories maintain their original licenses.

---

**Built for comprehensive documentation and community tracking.**

**📊 Dual-Source Data:** Git commits + GitHub Discussions
**🤖 AI-Enhanced:** Factual data first, AI interpretation clearly labeled
**💬 Channel-Organized:** 20x, Rev5, and RFCs discussions grouped and analyzed
**📝 Automated Reports:** Daily and weekly summaries for both repos and community
