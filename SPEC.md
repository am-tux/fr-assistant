# FedRAMP Git Repository Tracker Specification

## Purpose
A lightweight command-line tool for tracking FedRAMP public repositories. Provides direct access to commit history, file changes, contributor activity, and GitHub Discussions (RFCs) through simple commands.

## Scope

### Data Collection
**Primary Focus:** Multi-source data retrieval for FedRAMP repository tracking.

**Capabilities:**
- Track GitHub Discussions RFCs
- View combined latest activity (RFCs + git changes)
- Query commits within date ranges
- List new files added
- View complete file history
- Track contributor activity
- Multi-repository support

**Data Sources:**
- Git log commands (local repository queries)
- Git diff operations (file changes)
- Git show for commit details
- Git fetch for updates
- Web scraping for GitHub Discussions (public pages, no API)

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

### latest
Show all recent FedRAMP activity (RFCs + git changes).

```bash
python3 main.py latest --days N
```

**Parameters:**
- `--days` (optional) - Days to look back (default: 7)

**Output:**
- RFCs from GitHub Discussions
  - Title, author, comment count, URL
- Git repository changes across all repos
  - Recent commits by repository
  - Grouped by repo name

**Example:**
```bash
python3 main.py latest --days 7
```

### rfcs
Show GitHub Discussions RFCs from FedRAMP/community.

```bash
python3 main.py rfcs --days N
```

**Parameters:**
- `--days` (optional) - Days to look back (default: 30)

**Output:**
- RFC title
- Author (if available)
- Comment count
- Discussion URL

**Example:**
```bash
python3 main.py rfcs --days 30
```

### blog
Show information about FedRAMP blog.

```bash
python3 main.py blog
```

**Output:**
- Note about JavaScript-based site
- Link to visit blog directly

**Note:** FedRAMP.gov uses JavaScript rendering, so blog posts cannot be scraped with traditional tools. This command provides a helpful message and link.

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

### Git Commands

Standard git commands for local repository queries:

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

### Web Scraping

Web scraping for public GitHub pages (no API authentication):

**GitHub Discussions (RFCs):**
- URL: `https://github.com/FedRAMP/community/discussions/categories/rfcs`
- Method: HTML parsing with BeautifulSoup
- Extracts: Title, author, date, comment count, discussion URL
- Filters: Only links matching `/discussions/\d+` pattern

**FedRAMP Blog:**
- Note: FedRAMP.gov uses JavaScript/SvelteKit rendering
- Traditional scraping not feasible without headless browser
- Command provides link to visit manually

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

### Commands Used

**Git Commands:**

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

**Web Scraping:**

**For RFCs:**
```python
# Using requests + BeautifulSoup
response = requests.get('https://github.com/FedRAMP/community/discussions/categories/rfcs')
soup = BeautifulSoup(response.text, 'html.parser')
# Parse discussion links matching /discussions/\d+ pattern
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
- **Git** installed and in PATH
- **Python Libraries:**
  - PyYAML - Configuration parsing
  - requests - HTTP requests for web scraping
  - beautifulsoup4 - HTML parsing for web scraping

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
- Web scraping only accesses public pages

**No Secrets Required:**
- No API tokens needed
- No GitHub authentication required
- All data from public sources (git repos, public web pages)
- No credentials stored

## Future Considerations

Potential enhancements (not in current scope):
- Private repository support (requires auth)
- Branch comparison queries
- Tag/release tracking
- Commit diff viewing
- Statistics aggregation
