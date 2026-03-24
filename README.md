# Git Repository Tracker

A lightweight command-line tool for querying git repositories. Track file changes, commits, contributors, and file history across multiple repositories.

**📊 Track:** Git commits and file changes | **🔍 Query:** File history and contributors | **⚡ Simple:** Direct git data queries

---

## Features

- **Query commits** - List recent commits with file changes
- **Track new files** - Find newly added files in any time range
- **File history** - View complete change history for any file
- **Contributor activity** - See what contributors are working on
- **Multi-repository** - Track multiple repositories simultaneously
- **Zero dependencies** - Pure git queries, no external APIs

## Quick Start

### Installation

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Initialize repositories (clone/fetch)
python3 main.py init
```

### Basic Usage

```bash
# List commits from last 7 days
python3 main.py commits --repo docs --days 7

# Find new files added in last 30 days
python3 main.py new-files --repo docs --days 30

# View complete history of a file
python3 main.py file-history --repo docs --file README.md

# See contributor activity
python3 main.py contributor --repo docs --name "john@example.com" --days 30
```

## Available Commands

| Command | Description |
|---------|-------------|
| `init` | Clone/update all repositories |
| `commits` | List recent commits with file stats |
| `new-files` | List newly added files |
| `file-history` | Show complete history of a file |
| `contributor` | Show contributor activity and stats |

## Configuration

Edit `config.yaml` to add repositories:

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

storage:
  repos_directory: "./repos"
```

## Examples

### Track Documentation Changes

```bash
# See what changed this week
python3 main.py commits --repo docs --days 7

# Find new documentation added
python3 main.py new-files --repo docs --days 30

# Track changes to specific file
python3 main.py file-history --repo docs --file authentication.md
```

### Monitor Contributors

```bash
# See what a contributor has been working on
python3 main.py contributor --repo docs --name "pete@fedramp.gov" --days 30

# Check recent activity
python3 main.py commits --repo community --days 14
```

## Directory Structure

```
fr-git-tracker/
├── main.py                # CLI entry point
├── config.yaml           # Repository configuration
├── src/
│   ├── config_loader.py  # Configuration parser
│   ├── git_tracker.py    # Git operations
│   └── functions.py      # High-level query functions
└── repos/                # Cloned repositories (auto-created)
    ├── docs/
    ├── roadmap/
    └── community/
```

## Prerequisites

- **Git** installed and in PATH
- **Python 3.11+** with pip
- Network access to clone public repositories

## How It Works

The tracker is a pure git query tool:
- ✅ Clones repositories (if they don't exist)
- ✅ Runs `git fetch` to get updates
- ✅ Executes git commands to query data
- ❌ **NEVER** modifies repository state
- ❌ **NEVER** pushes changes
- ❌ **NEVER** makes commits

All data comes directly from git:
- `git log` - Commit history
- `git diff` - File changes
- `git show` - Commit details
- `git fetch` - Update from remote

## Troubleshooting

**Repository not found?**
```bash
python3 main.py init  # Clone/update all repos
```

**No data returned?**
```bash
# Make sure repos are up to date
python3 main.py init

# Check you're using the right repo name
# Names from config.yaml: docs, roadmap, community
```

**Python dependencies missing?**
```bash
pip3 install -r requirements.txt
```

## Documentation

- **USAGE.md** - Detailed command reference
- **SPEC.md** - Technical specification
- **config.yaml** - Configuration with examples
- **CLAUDE.md** / **.cursorrules** - AI assistant context (must stay in sync)

## Portability

This directory is fully portable:
- All paths are relative
- No hardcoded user paths
- Can be moved anywhere
- Can be shared between users

## License

Configuration for tracking FedRAMP public repositories. All tracked repositories maintain their original licenses.

---

**A simple git query tool for repository tracking.**

**📊 Pure Git Data** | **🔍 Direct Queries** | **⚡ Zero Dependencies**
