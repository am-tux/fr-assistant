# FedRAMP Compliance Engineer Assistant

An intelligent tool for FedRAMP compliance engineers. Track repositories, monitor RFCs, and get expert recommendations on what matters for your authorization work.

**🎯 Expert Guidance:** Compliance-focused insights | **📊 Monitor:** Git commits and RFCs | **⚡ Simple:** No API tokens required

---

## Why This Exists

Staying current with FedRAMP is challenging. Changes happen across multiple repositories, RFCs emerge in GitHub Discussions, and understanding what matters for your specific authorization work requires expertise.

**This tool keeps you comprehensively informed about everything FedRAMP:**

- **📋 GitHub Discussions & RFCs** - Track community proposals, RFCs, and Q&A discussions as they happen
- **📅 Upcoming Events** - Links to FedRAMP meetings, webinars, and community events
- **📂 Repository Changes** - Monitor all commits, new files, and updates across FedRAMP/docs, FedRAMP/roadmap, and FedRAMP/community
- **🎯 Expert Analysis** - Get compliance-focused recommendations on what matters for your authorization work
- **⚖️ Fact vs Inference** - Clear labeling distinguishes verified facts (✅) from expert recommendations (🤔)
- **🔍 Context-Aware** - Prioritizes updates based on your specific systems (High/Moderate, Rev4/Rev5, 20x pilot)

Instead of manually checking multiple sources, you get a unified view of all FedRAMP activity with expert guidance on what requires your attention.

---

## Features

- **Track RFCs** - Monitor GitHub Discussions for RFCs and community proposals
- **Monitor events** - Get links to upcoming FedRAMP meetings and events
- **Latest activity** - Combined view of RFCs, events, and git changes across all repos
- **Query commits** - List recent commits with file changes
- **Track new files** - Find newly added files in any time range
- **File history** - View complete change history for any file
- **Contributor activity** - See what contributors are working on
- **Multi-repository** - Track multiple repositories simultaneously
- **No API tokens** - Web scraping for public data, no authentication required

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
# See all recent FedRAMP activity (RFCs + git changes)
python3 main.py latest --days 7

# Track GitHub Discussions RFCs
python3 main.py rfcs --days 30

# View upcoming FedRAMP events
python3 main.py events --days 7

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
| `latest` | Show all recent FedRAMP activity (RFCs + events + git changes) |
| `rfcs` | Show GitHub Discussions RFCs |
| `events` | Show link to upcoming FedRAMP events (requires manual visit) |
| `blog` | Show note about FedRAMP blog (requires manual visit) |
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

### Get Latest FedRAMP Activity

```bash
# See everything happening in FedRAMP
python3 main.py latest --days 7

# Output shows:
# - RFCs from GitHub Discussions
# - Git commits across all repos
```

### Track RFCs and Discussions

```bash
# See recent RFCs
python3 main.py rfcs --days 30

# Shows:
# - RFC title
# - Author
# - Comment count
# - Discussion URL
```

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
│   ├── web_scraper.py    # Web scraping for RFCs and blogs
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

The tracker combines git queries with web scraping:

**Git Operations:**
- ✅ Clones repositories (if they don't exist)
- ✅ Runs `git fetch` to get updates
- ✅ Executes git commands to query data
- ❌ **NEVER** modifies repository state
- ❌ **NEVER** pushes changes
- ❌ **NEVER** makes commits

**Data Sources:**
- `git log` - Commit history from local repos
- `git diff` - File changes and stats
- `git show` - Commit details
- `git fetch` - Update from remote
- Web scraping - GitHub Discussions (RFCs) from public pages
- No API tokens required - all data from public sources

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
- **INTEGRATION.md** - How to access this assistant from other projects
- **config.yaml** - Configuration with examples
- **CLAUDE.md** / **.cursorrules** - AI assistant context (must stay in sync)

## Integration with Other Projects

This FedRAMP assistant can be accessed from any other project! See **INTEGRATION.md** for details.

**Quick setup:**
```bash
# Set environment variable (recommended)
export FEDRAMP_ASSISTANT_PATH="/path/to/fr-git-tracker"

# Add to other project's CLAUDE.md
# (See INTEGRATION.md for template)
```

Any AI assistant in another project can then ask the FedRAMP expert for:
- Latest FedRAMP updates
- RFC analysis
- Compliance recommendations
- Context-aware prioritization

## Portability

This directory is fully portable:
- All paths are relative
- No hardcoded user paths
- Can be moved anywhere
- Can be shared between users

## License

Configuration for tracking FedRAMP public repositories. All tracked repositories maintain their original licenses.

---

**Your expert assistant for FedRAMP compliance engineering.**

**🎯 Expert Guidance** | **📊 Monitor Changes** | **⚡ No API Tokens**
