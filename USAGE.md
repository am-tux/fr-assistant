# Git Repository Tracker - Usage Guide

## Quick Start

```bash
# Install dependencies
pip3 install -r requirements.txt

# Initialize repositories
python3 main.py init
```

---

## Command Reference

### init

Initialize all repositories (clone or fetch updates).

```bash
python3 main.py init
```

**What it does:**
- Clones repositories that don't exist locally
- Runs `git fetch` on existing repositories
- Creates necessary directories

**Example output:**
```
Initializing repositories...
  ✓ docs
  ✓ roadmap
  ✓ community

All repositories ready!
```

---

### commits

List commits within a date range.

```bash
python3 main.py commits --repo REPO_NAME --days N
```

**Options:**
- `--repo NAME` (required) - Repository name
- `--days N` (optional) - Days to look back (default: 7)

**Examples:**
```bash
# Last 7 days of commits
python3 main.py commits --repo docs --days 7

# Last 30 days
python3 main.py commits --repo roadmap --days 30
```

**Output:**
```
Fetching commits from docs (last 7 days)...

Found 3 commits:

- adf8891 by Pete Waterman on 2026-03-17 10:17:06 -0400
  CCM-AGM-SSR fixes Low and Moderate rules (#58)
  Files: 1, +9/-5 lines

- 09bbb67 by pete-gov on 2026-03-11 15:33:36 -0400
  fix marketplace link typos
  Files: 6, +6/-6 lines
```

---

### new-files

List files added within a date range.

```bash
python3 main.py new-files --repo REPO_NAME --days N
```

**Options:**
- `--repo NAME` (required) - Repository name
- `--days N` (optional) - Days to look back (default: 7)

**Examples:**
```bash
# New files in last 7 days
python3 main.py new-files --repo docs --days 7

# New files in last month
python3 main.py new-files --repo docs --days 30
```

**Output:**
```
Fetching new files from docs (last 7 days)...

Found 2 new files:

- tools/new-script.py
  Added: 2026-03-15 by developer@example.com
  Commit: abc1234 - Add automation script

- docs/new-guide.md
  Added: 2026-03-16 by writer@example.com
  Commit: def5678 - Add setup guide
```

---

### file-history

Show complete change history for a specific file.

```bash
python3 main.py file-history --repo REPO_NAME --file FILE_PATH
```

**Options:**
- `--repo NAME` (required) - Repository name
- `--file PATH` (required) - File path (relative to repo root)

**Examples:**
```bash
# History of README
python3 main.py file-history --repo docs --file README.md

# History of nested file
python3 main.py file-history --repo docs --file tools/site/content/index.md
```

**Output:**
```
Fetching history for README.md in docs...

Found 29 commits that modified README.md:

- 41dc1c0 by Pete Waterman on 2026-02-04 16:53:47 -0500
  Release v0.9.0 (#47)
  Changes: +11/-53 lines

- 0143678 by Pete Waterman on 2025-12-15 12:56:50 -0500
  refactor zensical (#42)
  Changes: +23/-17 lines
```

---

### contributor

Show activity for a specific contributor.

```bash
python3 main.py contributor --repo REPO_NAME --name NAME_OR_EMAIL --days N
```

**Options:**
- `--repo NAME` (required) - Repository name
- `--name NAME` (required) - Contributor name or email
- `--days N` (optional) - Days to look back (default: 30)

**Examples:**
```bash
# Activity by email
python3 main.py contributor --repo docs --name "pete@fedramp.gov" --days 30

# Activity by name
python3 main.py contributor --repo docs --name "Pete Waterman" --days 60
```

**Output:**
```
Fetching activity for pete@fedramp.gov in docs...
Looking back 30 days...

## Activity Summary
- Total commits: 5
- Files modified: 12
- Lines added: +89
- Lines deleted: -31

## Files Modified (12)
- README.md
- tools/script.py
- docs/guide.md
... and 9 more

## Recent Commits (5)
- adf8891 on 2026-03-17 10:17:06 -0400
  CCM-AGM-SSR fixes Low and Moderate rules (#58)
```

---

## Configuration

Edit `config.yaml` to configure repositories:

```yaml
repositories:
  - name: "docs"
    url: "https://github.com/FedRAMP/docs"
    path: "./repos/docs"
    primary_branch: "main"

  - name: "roadmap"
    url: "https://github.com/FedRAMP/roadmap"
    path: "./repos/roadmap"
    primary_branch: "main"

  - name: "community"
    url: "https://github.com/FedRAMP/community"
    path: "./repos/community"
    primary_branch: "main"

storage:
  repos_directory: "./repos"
```

**Adding a new repository:**
1. Add entry to `repositories` list in config.yaml
2. Run `python3 main.py init` to clone it

---

## Common Workflows

### Track Recent Activity

```bash
# Initialize repos
python3 main.py init

# See recent commits across repos
python3 main.py commits --repo docs --days 7
python3 main.py commits --repo roadmap --days 7
python3 main.py commits --repo community --days 7
```

### Monitor Specific Files

```bash
# Track changes to important files
python3 main.py file-history --repo docs --file README.md
python3 main.py file-history --repo docs --file config.yaml
```

### Contributor Analysis

```bash
# See what a contributor is working on
python3 main.py contributor --repo docs --name "developer@example.com" --days 30

# Find new files they added
python3 main.py new-files --repo docs --days 30 | grep "developer@example.com"
```

---

## Troubleshooting

### "Repository not found"
```bash
# Run init to clone repositories
python3 main.py init

# Check repository name matches config.yaml
# Valid names: docs, roadmap, community
```

### "No commits found"
```bash
# Ensure repos are up to date
python3 main.py init

# Try a longer time range
python3 main.py commits --repo docs --days 60
```

### Python Dependencies Missing
```bash
pip3 install -r requirements.txt
```

---

## Automation

**Daily query via cron:**
```bash
0 9 * * * cd /path/to/tracker && python3 main.py commits --repo docs --days 1
```

---

## Tips

1. **Run `init` regularly** to keep repos updated
2. **Use longer `--days`** if you don't see expected results
3. **File paths** are relative to repository root
4. **Contributor names** can be name or email from git log

---

## Getting Help

```bash
# Show all commands
python3 main.py --help

# Show command-specific help
python3 main.py commits --help
python3 main.py contributor --help
```
