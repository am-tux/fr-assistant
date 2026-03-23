# Git Repository Tracker Specification

## Purpose
An AI-powered tool that monitors a collection of git repositories containing primarily documentation, reports significant daily changes, and answers detailed questions about tracked projects based solely on factual data.

**Documentation-Focused:** This tool is optimized for tracking documentation repositories where the primary concern is what content changed and how much changed in specific files, rather than commit volume.

## Core Principles

### NO GUESSING RULE
- The tool MUST ONLY report factual information derived directly from git data
- If information is not available or unclear, explicitly state "Information not available" or "Cannot be determined from git data"
- Do NOT infer intentions, reasons, or future implications
- Do NOT speculate about code quality, purpose, or developer motivations
- Only report observable facts: commits, diffs, file changes, timestamps, authors, branches, tags

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

## Response Guidelines

### When Answering Questions

**MUST DO:**
- Quote exact commit messages
- Provide exact timestamps
- Give precise line counts
- List specific file names
- Show actual diff output when relevant
- Cite commit hashes for any claims

**MUST NOT DO:**
- Interpret what code does
- Explain why changes were made
- Predict future changes
- Assess code quality
- Make assumptions about developer intent
- Fill in gaps with probable information

### Example Good vs Bad Responses

**Question: "What changed in the authentication documentation?"**

❌ BAD: "The authentication docs were improved with better explanations and updated best practices."

✅ GOOD: "docs/authentication.md was modified in 2 commits:
- abc123 by user@example.com on 2026-03-20: 'update auth examples' (+45/-12 lines)
- def456 by user@example.com on 2026-03-21: 'add OAuth2 section' (+78/-0 lines)

Total changes: +123 / -12 lines
New content added: OAuth2 section (78 lines)
To see exact changes, use: git show [hash]"

**Question: "Why was the documentation reorganized?"**

❌ BAD: "They probably wanted to make it easier to navigate and find information."

✅ GOOD: "Cannot determine reasons from git data. Observable facts:
- 12 files were moved on 2026-03-22 in commit ghi789
- Commit message: 'reorganize docs structure'
- Files moved from docs/guides/* to docs/tutorials/*
- _config.yml modified to update navigation structure (+15/-8 lines)
- No explanation provided in commit message

File moves:
- docs/guides/setup.md → docs/tutorials/getting-started.md
- docs/guides/deploy.md → docs/tutorials/deployment.md
[...]"

**Question: "Is the documentation being actively maintained?"**

❌ BAD: "Yes, it looks very active with regular updates."

✅ GOOD: "Cannot assess 'active maintenance' from git data. Observable facts:
- Last commit: 2026-03-22 (1 day ago)
- Commits in last 30 days: 8
- Files modified in last 30 days: 23
- Contributors in last 30 days: 4 (user1@example.com, user2@example.com, user3@example.com, user4@example.com)
- Average lines changed per week (last 4 weeks): +245 / -67
- New documentation files added in last 30 days: 3"

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

**Do NOT speculate about:**
- Quality of the documentation changes
- Whether changes improve clarity or user experience
- Completeness or accuracy of documentation
- Why certain topics were added or removed

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
- Local repository directories can be safely deleted; they will be re-cloned on next run

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

### Forbidden Data Sources
- Do NOT use external APIs or services (except git clone/fetch from repository URLs)
- Do NOT make assumptions based on file names or patterns
- Do NOT use AI to interpret code semantics
- Do NOT use GitHub API, issue trackers, or other external services

### Update Frequency
- Poll repositories every: [configurable, default: 1 hour]
- Generate daily reports at: [configurable, default: 9 AM]
- Run `git fetch` on each poll to get latest remote changes
- Cache git data in memory between polls to minimize disk access

## Error Handling

When encountering issues:
- If repository is not accessible: "Repository [name] is not accessible at [path]"
- If commit hash is invalid: "Commit [hash] not found in repository [name]"
- If branch doesn't exist: "Branch [name] does not exist in repository [name]"
- If date range has no commits: "No commits found between [date1] and [date2]"

Never fail silently. Always report what went wrong with specific details.

## Future Considerations

Potential enhancements (NOT in initial scope):
- Integration with issue trackers (if needed for cross-referencing)
- Code language statistics (factual: X% JavaScript, Y% Python)
- File size trends over time
- Automated alerts for specific patterns (e.g., secrets in commits)
