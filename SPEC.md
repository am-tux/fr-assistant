# Git Repository Tracker Specification

## Purpose
An AI-powered tool that monitors a collection of git repositories containing primarily documentation, reports significant daily changes, and answers detailed questions about tracked projects based solely on factual data.

**Documentation-Focused:** This tool is optimized for tracking documentation repositories where the primary concern is what content changed and how much changed in specific files, rather than commit volume.

## Core Principles

### FACTUAL DATA FIRST, AI INTERPRETATION OPTIONAL

**Primary Rule: Factual Reporting**
- The tool MUST ALWAYS lead with factual information derived directly from git data
- Observable facts are the foundation: commits, diffs, file changes, timestamps, authors, branches, tags
- If information is not available or unclear, explicitly state "Information not available" or "Cannot be determined from git data"

**Secondary Capability: AI Interpretation (When Requested)**
- The tool MAY provide AI interpretation of code and documentation content
- **ALL interpretations MUST be clearly prefaced** with labels such as:
  - "🤖 AI Interpretation:"
  - "⚠️ AI Analysis (not factual):"
  - "💭 AI Assessment:"
- AI interpretations should follow factual data, never replace it
- Interpretations may include:
  - What code or documentation appears to do
  - Apparent purpose or intent based on content
  - Quality observations (clarity, completeness, structure)
  - Potential issues or improvements
- **Users must understand:** AI interpretations are educated guesses based on content analysis, not factual git data

**Separation Principle:**
Always separate factual data from AI interpretation in responses:
```
FACTS: [Observable git data]

🤖 AI INTERPRETATION: [Analysis based on content reading]
```

## Tracked Repositories

All repositories will be stored in the `./repos/` subdirectory relative to this specification file.

```yaml
repositories:
  # Add repositories to track here
  # Example:
  # - name: "project-name"
  #   url: "https://github.com/user/repo"
  #   path: "./repos/project-name"  # Relative to spec file directory
  #   primary_branch: "main"
```

**Note:** The tool will automatically clone repositories from their URLs if they don't exist locally.

## Report Generation

The tool generates two types of automated reports:
1. **Daily Reports** - Changes in the last 24 hours
2. **Weekly Reports** - Aggregated changes over the last 7 days

Both reports focus on factual data from git history and prioritize file-level changes for documentation repositories.

### Report Storage and Naming

Reports are stored in the `./reports/` directory:
```
reports/
├── daily/
│   ├── 2026-03-23.md
│   ├── 2026-03-24.md
│   └── ...
└── weekly/
    ├── 2026-W12.md      # Week 12 of 2026
    ├── 2026-W13.md
    └── ...
```

### Report Generation Schedule

- **Daily Reports:** Generated at 09:00 (configurable) covering previous 24 hours
- **Weekly Reports:** Generated on Monday at 09:00 (configurable) covering previous 7 days
- Reports are only generated if there are changes to report
- Empty periods are noted with a brief "No changes" report

## Daily Change Reporting

### What Constitutes "Big Changes"
For documentation repositories, the focus is on **content changes** rather than commit volume. Report changes that meet ANY of the following criteria:

1. **Content Volume Thresholds**
   - **ANY new files added** (ALWAYS report - indicates new documentation topics)
   - More than 100 lines changed in a single file
   - More than 5 files modified (documentation typically has fewer but larger changes)
   - Files deleted or renamed (indicates content removal or reorganization)
   - More than 3 commits in a single day (documentation repos typically have fewer commits)

2. **Documentation Structure Changes**
   - New documentation files created
   - Documentation files deleted or moved
   - Changes to navigation/TOC files (SUMMARY.md, _sidebar.md, nav.yml, etc.)
   - Changes to documentation configuration (mkdocs.yml, docusaurus.config.js, _config.yml, etc.)
   - New branches created or merged
   - New tags/releases created

3. **Critical Files Modified**
   - README.md or index files
   - CHANGELOG.md or release notes
   - Navigation/structure files
   - Build/deployment configuration (package.json, Gemfile, requirements.txt)
   - CI/CD files (.github/workflows/*, .gitlab-ci.yml, etc.)
   - Site configuration files (*.config.js, *.yml, *.toml)

### Daily Report Format

For documentation repositories, emphasize **what changed** over commit count.

```markdown
# Daily Git Activity Report - [DATE]

## [Repository Name]

### Summary
- Files modified: X
- Files added: X
- Files deleted: X
- Total lines changed: +X / -X
- Total commits: X
- Contributors: [list of author names]

### File Changes (Primary Focus)

#### 🆕 New Files Added (ALWAYS REPORT)
New files indicate new documentation topics or features being documented.

- [filename] by [author] in [commit hash] at [time]
  - Commit message: [message]
  - File size: +X lines
  - File path: [full path to show location in docs structure]

#### Modified Files
- [filename]: +X / -X lines by [author] in [commit hash]
  - [commit message]
  - Notable: [if file is critical or has large changes]

#### Deleted/Renamed Files
- [old-filename] → [new-filename] by [author] in [commit hash]
- [deleted-filename] deleted by [author] in [commit hash]

### Commits (if relevant)
- [hash] by [author] at [time]: [commit message]
  - Files affected: X
  - Total changes: +X / -X lines

### Branch/Release Activity
- Branches created: [branch names]
- Branches merged: [branch names with source→target]
- Tags/Releases: [tag names with associated commit]

### Documentation Structure Changes
- New documentation sections added
- Navigation/TOC files modified
- Configuration changes affecting site structure
```

## Weekly Change Reporting

Weekly reports provide an aggregated view of the past 7 days, useful for understanding broader documentation evolution patterns.

### Weekly Report Format

```markdown
# Weekly Git Activity Report - Week [WEEK_NUMBER], [YEAR]
**Period:** [START_DATE] to [END_DATE]

## Summary Across All Repositories

- Total repositories with changes: X
- Total files added: X
- Total files modified: X
- Total files deleted: X
- Total commits: X
- Total lines changed: +X / -X
- Active contributors: X

## [Repository Name]

### Week Summary
- Files added: X
- Files modified: X
- Files deleted: X
- Total commits: X
- Total lines changed: +X / -X
- Contributors: [list of author names with commit counts]

### 🆕 New Documentation Added This Week
List all new files added during the week:

- [filename] - Added on [date] by [author]
  - Size: +X lines
  - Commit: [hash] - [message]

### Most Active Files (by line changes)
Top 10 files with most changes:

1. [filename]: +X / -X lines (Y commits)
   - Contributors: [author list]
   - Last modified: [date]

2. [filename]: +X / -X lines (Y commits)
   - Contributors: [author list]
   - Last modified: [date]

[...]

### Files Deleted or Renamed
- [old-filename] → [new-filename] on [date] by [author]
- [deleted-filename] deleted on [date] by [author]

### Commits by Day
- Monday ([date]): X commits
- Tuesday ([date]): X commits
- Wednesday ([date]): X commits
- Thursday ([date]): X commits
- Friday ([date]): X commits
- Saturday ([date]): X commits
- Sunday ([date]): X commits

### Contributor Activity
- [author1]: X commits, +Y / -Z lines across N files
- [author2]: X commits, +Y / -Z lines across N files

### Branch/Release Activity
- Branches created: [list with dates]
- Branches merged: [list with source→target and dates]
- Tags/Releases: [list with dates and commit hashes]

### Critical File Changes
Documentation structure or configuration changes:
- [filename] modified on [date]: [brief summary of what changed]

### Day-by-Day Breakdown
For reference, link to daily reports:
- [Monday date] - [Link to daily report] - X commits, Y files changed
- [Tuesday date] - [Link to daily report] - X commits, Y files changed
[...]
```

### Weekly Report Analysis Rules

**MUST Include (Factual Data):**
- Exact counts of files added, modified, deleted
- Precise line change counts
- List of all new files (critical for documentation tracking)
- Contributor names with their commit/line counts
- Chronological listing of structural changes

**MUST NOT Include (Speculation):**
- Interpretation of why changes were made
- Assessment of documentation quality or completeness
- Predictions about future changes
- Assumptions about project health or activity
- Comparative judgments (e.g., "better than last week")

## Question Answering Capabilities

### Documentation-Specific Questions
For documentation repositories, the most valuable questions are:

**Content Changes (Prioritize NEW FILES):**
- **What new documentation files were added?** (HIGHEST PRIORITY - indicates new features/topics)
- What documentation files were modified or deleted recently?
- How much content changed in specific documentation files?
- What new documentation topics were added?
- Which documentation files have had the most changes?
- What files were reorganized or renamed?
- When was [specific file] first added to the repository?

**Documentation Structure:**
- What is the current documentation structure (file tree)?
- How has the documentation organization changed over time?
- What navigation or configuration files were modified?

**Content Authoring:**
- Who has contributed to specific documentation files?
- What documentation has a specific author written or updated?
- Which files are most actively maintained?

### General Questions
The tool must be able to answer questions about:

### Repository Metadata
- Current branch structure
- List of all branches and their last commit date
- List of all tags and releases
- Total commit count (overall and by date range)
- Repository size and file count

### Commit History
- Who committed what and when
- What files were changed in specific commits
- Line-by-line diff of any commit
- Commit message history
- Commits by specific author
- Commits in specific date ranges

### File History
- When was a specific file last modified
- Who has modified a specific file
- Complete change history of a file
- Current file content at specific commit or branch

### Branch Information
- What commits are on branch A but not on branch B
- When was a branch created
- Who has committed to a specific branch
- Branch divergence information

### Author/Contributor Analysis
- List of all contributors
- Commit count by author
- Lines changed by author
- Active time periods for each contributor

### Comparison Queries
- Diff between two commits
- Diff between two branches
- Changes between two dates
- Files that changed between versions

## Data Collection Requirements

The tool must collect and maintain:

1. **Git Log Data**
   - Full commit history with: hash, author, date, message, parent commits
   - For each commit: list of files changed with line count (+/-)
   - **File status for each change:** Added (A), Modified (M), Deleted (D), Renamed (R)
   - For new files (A): full file path and initial line count
   - For deleted files (D): file path that was deleted
   - For renamed files (R): old path → new path

2. **File Tree Data**
   - Current file structure for each tracked branch
   - File size and type information

3. **Branch/Tag Data**
   - All branches with HEAD commit and creation date
   - All tags with associated commit and creation date

4. **Diff Data**
   - Ability to retrieve full diff for any commit
   - Ability to compute diff between any two commits

5. **Author Data**
   - Author name and email from git log
   - Commit timestamps for author activity patterns

6. **File Content Data (For AI Interpretation)**
   - Ability to read actual file content at any commit using `git show [commit]:[file]`
   - Access to full diffs with content using `git diff` or `git show`
   - File content at HEAD for current state analysis
   - **Purpose:** Enable AI interpretation of what code/documentation actually does or says
   - **Usage:** Only accessed when AI interpretation is requested or beneficial

## Response Guidelines

### When Answering Questions

**MUST ALWAYS DO (Factual Data):**
- Quote exact commit messages
- Provide exact timestamps
- Give precise line counts
- List specific file names
- Show actual diff output when relevant
- Cite commit hashes for any claims
- **Lead with factual data first, always**

**MAY DO (AI Interpretation - When Useful):**
- Interpret what code or documentation appears to do
- Analyze apparent purpose based on content
- Assess documentation quality, clarity, or completeness
- Identify potential issues or improvements
- Explain what changes seem to accomplish

**REQUIREMENTS FOR AI INTERPRETATION:**
- ✅ **MUST** be clearly labeled with prefix (🤖 AI Interpretation:, ⚠️ AI Analysis:, 💭 AI Assessment:)
- ✅ **MUST** come after factual data, never before or instead of it
- ✅ **MUST** be based on actual content from files (via git show or git diff)
- ✅ **MUST** acknowledge uncertainty when appropriate ("appears to", "likely", "seems to")
- ❌ **MUST NOT** replace or obscure factual information
- ❌ **MUST NOT** predict future changes
- ❌ **MUST NOT** be presented as factual git data

### Example Responses

**Question: "What changed in the authentication documentation?"**

❌ BAD (Unlabeled interpretation): "The authentication docs were improved with better explanations and updated best practices."

✅ GOOD (Factual only): "docs/authentication.md was modified in 2 commits:
- abc123 by user@example.com on 2026-03-20: 'update auth examples' (+45/-12 lines)
- def456 by user@example.com on 2026-03-21: 'add OAuth2 section' (+78/-0 lines)

Total changes: +123 / -12 lines
New content added: OAuth2 section (78 lines)
To see exact changes, use: git show [hash]"

✅ EXCELLENT (Factual + AI interpretation): "docs/authentication.md was modified in 2 commits:
- abc123 by user@example.com on 2026-03-20: 'update auth examples' (+45/-12 lines)
- def456 by user@example.com on 2026-03-21: 'add OAuth2 section' (+78/-0 lines)

Total changes: +123 / -12 lines
New content added: OAuth2 section (78 lines)

🤖 AI INTERPRETATION (based on diff content):
The changes appear to add a new OAuth2 authentication section with code examples. The updated examples section shows more detailed step-by-step authentication flows with error handling. The new OAuth2 section includes configuration examples for common providers (Google, GitHub) and redirect URI setup. Overall, the documentation seems to have expanded authentication coverage and improved example clarity."

**Question: "Why was the documentation reorganized?"**

❌ BAD (Speculation presented as fact): "They wanted to make it easier to navigate and find information."

✅ GOOD (Factual only): "Cannot determine reasons from git data. Observable facts:
- 12 files were moved on 2026-03-22 in commit ghi789
- Commit message: 'reorganize docs structure'
- Files moved from docs/guides/* to docs/tutorials/*
- _config.yml modified to update navigation structure (+15/-8 lines)
- No explanation provided in commit message

File moves:
- docs/guides/setup.md → docs/tutorials/getting-started.md
- docs/guides/deploy.md → docs/tutorials/deployment.md
[...]"

✅ EXCELLENT (Factual + AI interpretation): "Observable facts:
- 12 files were moved on 2026-03-22 in commit ghi789
- Commit message: 'reorganize docs structure'
- Files moved from docs/guides/* to docs/tutorials/*
- _config.yml modified to update navigation structure (+15/-8 lines)
- No explanation provided in commit message

File moves:
- docs/guides/setup.md → docs/tutorials/getting-started.md
- docs/guides/deploy.md → docs/tutorials/deployment.md
[...]

💭 AI ASSESSMENT (based on the reorganization pattern):
The commit message doesn't explain why, but examining the file moves reveals a pattern: content is being categorized more specifically. 'Guides' were general documentation, while the new 'tutorials' structure appears to focus on step-by-step instructional content. The navigation changes in _config.yml add new section headings that separate conceptual docs from hands-on tutorials, suggesting an effort to improve content discoverability by user intent (learning vs. reference)."

**Question: "Is the documentation being actively maintained?"**

❌ BAD (Subjective judgment without data): "Yes, it looks very active with regular updates."

✅ GOOD (Factual only): "Cannot objectively assess 'active maintenance'. Observable facts:
- Last commit: 2026-03-22 (1 day ago)
- Commits in last 30 days: 8
- Files modified in last 30 days: 23
- Contributors in last 30 days: 4 (user1@example.com, user2@example.com, user3@example.com, user4@example.com)
- Average lines changed per week (last 4 weeks): +245 / -67
- New documentation files added in last 30 days: 3"

✅ EXCELLENT (Factual + AI interpretation): "Observable facts:
- Last commit: 2026-03-22 (1 day ago)
- Commits in last 30 days: 8
- Files modified in last 30 days: 23
- Contributors in last 30 days: 4 (user1@example.com, user2@example.com, user3@example.com, user4@example.com)
- Average lines changed per week (last 4 weeks): +245 / -67
- New documentation files added in last 30 days: 3

🤖 AI INTERPRETATION:
Based on the metrics, the documentation appears to be actively maintained. Recent activity (commit 1 day ago) and consistent weekly changes (+245/-67 lines/week) suggest ongoing work. The presence of 4 different contributors indicates collaborative maintenance rather than a single maintainer. Three new files in 30 days shows the documentation is expanding to cover new topics. However, 8 commits over 30 days is moderate frequency - this could indicate either thoughtful, substantial updates or less frequent attention depending on project size and team capacity."

## Configuration File Format

```yaml
# config.yaml

repositories:
  - name: "my-docs-project"
    url: "https://github.com/user/my-docs-project"
    # Path is optional - defaults to ./repos/[name] relative to spec file directory
    # Use relative paths (starting with ./) for portability across systems/users
    path: "./repos/my-docs-project"
    primary_branch: "main"
    critical_files:
      - "README.md"
      - "**/*.md"              # All markdown documentation
      - "_config.yml"          # Documentation site configuration
      - "mkdocs.yml"
      - ".github/workflows/*"  # Documentation build/deploy

daily_report:
  enabled: true
  time: "09:00"  # Time to generate report
  # Thresholds optimized for documentation repositories
  thresholds:
    min_commits: 3           # Docs typically have fewer commits
    min_lines_changed: 100   # Per file threshold
    min_files_changed: 5     # Fewer files changed per update

  always_report:
    - new_files_added        # Any new documentation
    - files_deleted
    - critical_files_changed

output:
  format: "markdown"
  # Output directory relative to spec file directory
  output_directory: "./reports"
  include_diffs: false  # Set to true to include full diffs in reports
  max_commits_shown: 50

reporting:
  prioritize_file_changes: true  # Focus on what files changed
  group_by_file: true            # Rather than by commit/author

# Repository storage location (relative to spec file directory)
storage:
  repos_directory: "./repos"  # Where to clone/store repositories
```

## Documentation Repository Tracking

### Key Differences from Code Repositories

Documentation repositories have different change patterns than code repositories:

1. **Commit Frequency:** Documentation typically has fewer, but more substantial commits
   - A single documentation update might add/modify entire sections (100+ lines)
   - Updates are often batched together rather than incremental

2. **Meaningful Metrics:**
   - **High Priority:** File additions, deletions, renames, and line count changes per file
   - **Medium Priority:** Number of files changed, branch merges, releases
   - **Low Priority:** Total commit count (less indicative of documentation activity)

3. **Critical Changes:**
   - New documentation files (new topics/features being documented)
   - Deleted files (deprecated features or reorganization)
   - Changes to navigation/structure files (content reorganization)
   - Large content changes (>100 lines in a file = substantial content update)

4. **Reporting Focus:**
   - What content was added or changed (file-centric view)
   - Documentation structure evolution (new sections, reorganization)
   - Content completeness (tracking new files vs deleted files)

### Documentation-Specific Analysis

When analyzing documentation repositories, report on:

- **Content Additions (HIGHEST PRIORITY):**
  - **ANY new files** (.md, .mdx, or other documentation files) - ALWAYS report these
  - New files indicate new documentation topics, features, or content areas
  - Include full file path to show where in documentation structure
  - Report file size (line count) to indicate content volume

- **Content Updates:** Large line changes (>100 lines) indicate substantial content rewrites

- **Structure Changes:** File moves/renames indicate reorganization

- **Navigation Changes:** TOC/config file changes affect user experience

- **Build Changes:** Changes to build configuration may affect site generation

**What Can Be Analyzed with AI Interpretation:**
When properly labeled with 🤖, ⚠️, or 💭 prefixes, you MAY provide:
- Quality assessment of documentation changes (clarity, organization, completeness)
- Analysis of whether changes appear to improve user experience
- Content coverage evaluation (what topics are/aren't documented)
- Apparent intent based on content and commit patterns (not definitive reasons)
- Code functionality interpretation based on actual source code

**What Should NOT Be Done (Even with Labels):**
- Predict future changes or roadmap items
- Make definitive claims about developer motivations
- Provide security assessments or vulnerability analysis (unless explicitly requested)
- Compare projects to external standards without basis

### When to Provide AI Interpretation

**Automatically Include AI Interpretation When:**
- User explicitly asks for interpretation, analysis, or assessment
- User asks "why", "what does this do", "is this good", or similar qualitative questions
- The factual data alone would not adequately answer the user's question
- Additional context would be helpful for understanding significance

**Examples:**
- "What changed?" → Factual only (unless massive changes that need context)
- "What does this code do?" → Factual + AI interpretation needed
- "Why did they change this?" → Factual + AI interpretation of apparent intent
- "Is the documentation complete?" → Factual stats + AI assessment
- "How many commits?" → Factual only

**Do NOT Include AI Interpretation When:**
- User asks for simple factual queries (counts, dates, authors)
- User explicitly requests "just the facts" or similar
- Factual data fully answers the question

### AI Interpretation Best Practices

1. **Read the actual content** - Use `git show` or `git diff` to read actual file content before interpreting
2. **Be specific** - Reference specific lines, sections, or patterns you observed
3. **Acknowledge uncertainty** - Use phrases like "appears to", "likely", "seems to", "suggests"
4. **Provide value** - Don't just restate what's obvious from the diff, add insight
5. **Stay grounded** - Base interpretations on observable content, not speculation

## Report Generation Functions

### Daily Report Generation

**Function:** `generateDailyReport(date)`

**Process:**
1. Determine the 24-hour period (from previous report to current time, or last 24 hours)
2. For each tracked repository:
   - Run `git log --since="24 hours ago" --name-status --numstat`
   - Identify all new files with `--diff-filter=A`
   - Identify deleted files with `--diff-filter=D`
   - Identify renamed files with `--diff-filter=R`
   - Calculate line changes per file
   - Track commit messages and authors
3. Generate report following the Daily Report Format template
4. Save to `./reports/daily/YYYY-MM-DD.md`
5. Return path to generated report

**Trigger:**
- Scheduled at configured time (default: 09:00 daily)
- Can be manually triggered for any specific date
- Only generates if there are changes OR if `generate_empty_reports` is true

### Weekly Report Generation

**Function:** `generateWeeklyReport(weekNumber, year)`

**Process:**
1. Determine the 7-day period (Monday to Sunday of the specified week)
2. For each tracked repository:
   - Aggregate all changes from the 7-day period
   - Collect all new files added during the week
   - Identify the top 10 most-changed files (by line count)
   - Calculate contributor statistics (commits and lines per author)
   - Track branch and release activity
   - Count commits per day of week
3. Generate summary statistics across all repositories
4. Generate report following the Weekly Report Format template
5. If `link_daily_reports_in_weekly` is true, include links to daily reports
6. Save to `./reports/weekly/YYYY-Www.md` (ISO week format)
7. Return path to generated report

**Trigger:**
- Scheduled weekly on configured day and time (default: Monday 09:00)
- Can be manually triggered for any specific week
- Only generates if there are changes OR if `generate_empty_reports` is true

### Report Generation Rules

**File Naming:**
- Daily: `YYYY-MM-DD.md` (e.g., `2026-03-23.md`)
- Weekly: `YYYY-Www.md` (e.g., `2026-W12.md` for week 12)

**Directory Structure:**
```
reports/
├── daily/
│   ├── 2026-03-23.md
│   ├── 2026-03-24.md
│   └── ...
└── weekly/
    ├── 2026-W12.md
    ├── 2026-W13.md
    └── ...
```

**Empty Reports:**
- If `generate_empty_reports: true`, create minimal report stating "No changes during this period"
- If `generate_empty_reports: false`, skip report generation for periods with no activity

**Report Overwriting:**
- If a report already exists for a date/week, it will be overwritten
- This allows re-running report generation to update or correct data

**Git Commands Used:**
```bash
# For daily reports (last 24 hours)
git log --since="24 hours ago" --name-status --numstat --all

# For weekly reports (specific date range)
git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --name-status --numstat --all

# For new files
git log --diff-filter=A --since="DATE" --name-status

# For deleted files
git log --diff-filter=D --since="DATE" --name-status

# For renamed files
git log --diff-filter=R --since="DATE" --name-status

# For contributor stats
git shortlog --since="DATE" --until="DATE" -sn
```

### Manual Report Generation

Both daily and weekly reports can be generated manually for historical periods:

**Daily Report for Specific Date:**
```
generateDailyReport("2026-03-15")
```

**Weekly Report for Specific Week:**
```
generateWeeklyReport(12, 2026)  // Week 12 of 2026
```

This allows retrospective analysis or regeneration of reports if needed.

## Implementation Notes

### Repository Storage Structure

**IMPORTANT:** All tracked repositories will be cloned and stored in subdirectories under the directory containing this specification file. All paths are relative to the spec file location, making this setup portable across different systems and users.

Directory structure:
```
[spec-file-directory]/
├── SPEC.md                    # This specification file
├── config.yaml                # Configuration file
├── repos/                     # All tracked repositories stored here (visible directory)
│   ├── [repo-name-1]/        # First repository
│   ├── [repo-name-2]/        # Second repository
│   └── [repo-name-n]/        # Nth repository
└── reports/                   # Daily reports output directory (visible directory)
    ├── YYYY-MM-DD.md         # Daily report files
    └── ...
```

**Note:** Both `repos/` and `reports/` are regular visible directories. They are NOT hidden directories (which would start with a dot like `.repos`).


**Initialization Process:**
1. On first run, the tool will check if repositories exist in the `repos/` subdirectory
2. If a repository does not exist locally, it will be cloned from the URL specified in config.yaml
3. If a repository already exists, the tool will run `git fetch` to update it
4. Repository paths in config.yaml should be specified relative to the spec file directory OR will be automatically set to `./repos/[repo-name]`

**Repository Management:**
- Repositories are read-only from the tool's perspective
- The tool will NEVER push changes or modify repository state
- The tool will only run `git fetch` to retrieve new data from remotes
- **The tool will NEVER delete downloaded git repositories unless explicitly prompted by the user**
- Local repository directories can be safely deleted manually by the user; they will be re-cloned on next run

### Data Sources
All data MUST come from:
- `git log` with various flags (especially `--name-status` and `--diff-filter=A` for new files)
- `git log --diff-filter=A` to identify newly added files
- `git log --diff-filter=D` to identify deleted files
- `git log --diff-filter=R` to identify renamed/moved files
- `git diff` between commits/branches with `--name-status` to see file changes
- `git show` for specific commits
- `git branch` and `git tag` for listings
- `git ls-tree` for file listings
- `git fetch` to retrieve remote changes
- Direct file reads from git objects when needed

**Key commands for tracking new files:**
- `git log --diff-filter=A --name-status --since="1 day ago"` - Find all files added in last day
- `git log --diff-filter=A --numstat [commit]` - Get line count for newly added files
- `git diff --name-status --diff-filter=A [ref1]..[ref2]` - Compare file additions between refs

### Forbidden Data Sources and Operations
- Do NOT use external APIs or services (except git clone/fetch from repository URLs)
- Do NOT make assumptions based solely on file names or patterns (unless clearly labeled as AI interpretation)
- Do NOT use GitHub API, issue trackers, or other external services
- Do NOT delete repository directories (only clone or fetch, never remove)
- Do NOT modify repository state (no commits, pushes, resets, or destructive operations)

### Allowed When Properly Labeled
- ✅ AI interpretation of code/documentation content (with 🤖 prefix)
- ✅ Analysis of what code appears to do (based on actual content via `git show`)
- ✅ Assessment of documentation quality/clarity (when clearly marked as interpretation)
- ✅ Pattern recognition in file organization (labeled as AI observation)

### Update Frequency
- Poll repositories every: [configurable, default: 1 hour]
- Generate daily reports at: [configurable, default: 9 AM]
- Run `git fetch` on each poll to get latest remote changes
- Cache git data in memory between polls to minimize disk access

## Error Handling

When encountering issues:
- If repository is not accessible: "Repository [name] is not accessible at [path]"
- If repository does not exist locally: Clone it from the URL, do NOT delete or modify other repositories
- If commit hash is invalid: "Commit [hash] not found in repository [name]"
- If branch doesn't exist: "Branch [name] does not exist in repository [name]"
- If date range has no commits: "No commits found between [date1] and [date2]"

Never fail silently. Always report what went wrong with specific details.

**IMPORTANT - Repository Deletion Policy:**
- NEVER delete downloaded git repositories unless explicitly prompted by the user
- Only clone or fetch repositories, never remove them automatically
- If a repository needs to be removed, ask the user for confirmation first

## Future Considerations

Potential enhancements (NOT in initial scope):
- Integration with issue trackers (if needed for cross-referencing)
- Code language statistics (factual: X% JavaScript, Y% Python)
- File size trends over time
- Automated alerts for specific patterns (e.g., secrets in commits)
