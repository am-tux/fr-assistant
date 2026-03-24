# Git Repository Tracker Specification

## Purpose
A lightweight command-line tool for querying git repositories. Provides direct access to commit history, file changes, and contributor activity through simple commands.

## Scope

### Git Repository Queries
**Primary Focus:** Direct git data retrieval through command-line queries.

**Capabilities:**
- Query commits within date ranges
- List new files added
- View complete file history
- Track contributor activity
- Multi-repository support

**Data Sources:**
- Git log commands
- Git diff operations
- Git show for commit details
- Git fetch for updates

## Tracked Repositories

Repositories are stored in `./repos/` relative to the configuration file:

```yaml
repositories:
  - name: "project-name"
    url: "https://github.com/user/repo"
    path: "./repos/project-name"
    primary_branch: "main"
```

The tool automatically clones repositories from URLs if they don't exist locally.

## Available Commands

### init
Initialize repositories by cloning or fetching updates.

```bash
python3 main.py init
```

**What it does:**
- Clones repositories that don't exist locally
- Runs `git fetch` on existing repositories
- Creates `./repos/` directory if needed

### commits
List commits within a date range.

```bash
python3 main.py commits --repo REPO_NAME --days N
```

**Parameters:**
- `--repo` (required) - Repository name from config
- `--days` (optional) - Days to look back (default: 7)

**Output:**
- Commit hash (short)
- Author name and email
- Commit date
- Commit message
- Files changed count
- Lines added/deleted

**Example:**
```bash
python3 main.py commits --repo docs --days 30
```

### new-files
List files added within a date range.

```bash
python3 main.py new-files --repo REPO_NAME --days N
```

**Parameters:**
- `--repo` (required) - Repository name from config
- `--days` (optional) - Days to look back (default: 7)

**Output:**
- File path
- Date added
- Author
- Commit hash
- Commit message

**Example:**
```bash
python3 main.py new-files --repo docs --days 14
```

### file-history
Show complete change history for a specific file.

```bash
python3 main.py file-history --repo REPO_NAME --file FILE_PATH
```

**Parameters:**
- `--repo` (required) - Repository name from config
- `--file` (required) - Path to file (relative to repo root)

**Output:**
- All commits that modified the file
- Commit hash, author, date
- Lines added/deleted per commit
- Commit message

**Example:**
```bash
python3 main.py file-history --repo docs --file README.md
```

### contributor
Show activity for a specific contributor.

```bash
python3 main.py contributor --repo REPO_NAME --name NAME_OR_EMAIL --days N
```

**Parameters:**
- `--repo` (required) - Repository name from config
- `--name` (required) - Contributor name or email address
- `--days` (optional) - Days to look back (default: 30)

**Output:**
- Total commits
- Files modified count
- Lines added/deleted
- List of files modified
- Recent commits with details

**Example:**
```bash
python3 main.py contributor --repo docs --name "john@example.com" --days 30
```

## Configuration File Format

```yaml
repositories:
  - name: "docs"
    url: "https://github.com/org/docs"
    path: "./repos/docs"
    primary_branch: "main"

  - name: "roadmap"
    url: "https://github.com/org/roadmap"
    path: "./repos/roadmap"
    primary_branch: "main"

storage:
  repos_directory: "./repos"
```

**Configuration Options:**

- `repositories` - List of repositories to track
  - `name` - Internal name for the repository
  - `url` - GitHub URL (https, public repos)
  - `path` - Local path (relative to config file)
  - `primary_branch` - Main branch to track (usually "main")

- `storage` - Storage configuration
  - `repos_directory` - Where to clone repositories

## Data Collection

All data comes from standard git commands:

```bash
# List commits
git log --since="DATE" --format="%H|%an|%ae|%ai|%s"

# Find new files
git log --diff-filter=A --since="DATE" --name-status

# Get file history
git log --follow --format="%H|%an|%ai|%s" -- FILE_PATH

# Contributor activity
git log --author="NAME" --since="DATE" --numstat

# Update from remote
git fetch origin
```

## Implementation Details

### Repository Storage

All repositories are cloned to `./repos/` subdirectory:

```
project-root/
├── config.yaml
├── main.py
├── src/
└── repos/
    ├── docs/
    ├── roadmap/
    └── community/
```

**Initialization:**
1. Check if repository exists in `./repos/[name]/`
2. If not, clone from URL
3. If exists, run `git fetch origin`

**Repository Management:**
- Read-only operations
- Never delete repositories automatically
- User can manually delete and re-clone

### Git Commands Used

**For commits:**
```bash
git log origin/BRANCH --since="DATE" --format="%H" --all
git show HASH --format="%H|%an|%ae|%ai|%s" --numstat
```

**For new files:**
```bash
git log origin/BRANCH --diff-filter=A --since="DATE" --name-status --format="%H|%an|%ai|%s"
```

**For file history:**
```bash
git log origin/BRANCH --follow --format="%H|%an|%ai|%s" --numstat -- FILE_PATH
```

**For contributor:**
```bash
git log origin/BRANCH --author="NAME" --since="DATE" --format="%H" --all
```

## Error Handling

**Repository not found:**
```
Repository 'NAME' not found in configuration
```

**Repository not accessible:**
```
Repository 'NAME' is not accessible at PATH
```

**File doesn't exist:**
```
No history found for FILE (file may not exist)
```

**No commits found:**
```
No commits found in the last N days
```

**Invalid date:**
```
Invalid date format. Use YYYY-MM-DD
```

## Requirements

- **Python 3.11+** with pip
- **PyYAML** library
- **Git** installed and in PATH

```bash
pip3 install -r requirements.txt
python3 main.py COMMAND
```

## Portability

The tool is fully portable:
- All paths relative to config file location
- No hardcoded user paths
- Can be moved anywhere on any system
- Can be shared between users
- Works on Linux, macOS, Windows (with git)

## Security

**Read-Only Operations:**
- Only clones and fetches from public repositories
- Never modifies repository state
- Never pushes changes
- Never commits anything

**No Secrets Required:**
- No API tokens needed
- No authentication required (public repos only)
- No credentials stored

## Future Considerations

Potential enhancements (not in current scope):
- Private repository support (requires auth)
- Branch comparison queries
- Tag/release tracking
- Commit diff viewing
- Statistics aggregation
