# FedRAMP Compliance Engineer Assistant

An intelligent assistant for FedRAMP compliance engineers. Just ask "what's the latest?" and get expert-prioritized updates on RFCs, repository changes, and what matters for your authorization work.

**💬 Natural Language:** Ask questions conversationally | **🎯 Expert Guidance:** Compliance-focused insights | **📊 Comprehensive:** RFCs + Git + Events | **⚡ Simple:** No API tokens

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

- **💬 Natural Language Interface** - Ask questions like "what's the latest?" or "what's important for compliance?"
- **🎯 Context-Aware Prioritization** - Automatically prioritizes updates based on your specific systems (High/Moderate, Rev5, 20x pilot)
- **⚖️ Expert Analysis** - Clear distinction between factual data (✅) and compliance expert recommendations (🤔)
- **🗣️ Track RFCs** - Monitor GitHub Discussions for RFCs and community proposals
- **📅 Monitor Events** - Get links to upcoming FedRAMP meetings and events
- **📊 Latest Activity** - Combined view of RFCs, events, and git changes across all repos
- **📝 Repository Tracking** - Query commits, new files, file history, and contributor activity
- **🔄 Multi-Repository** - Track FedRAMP/docs, FedRAMP/roadmap, and FedRAMP/community simultaneously
- **⚡ No API Tokens** - Web scraping for public data, no authentication required

## Quick Start

### Installation

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Initialize repositories (clone/fetch)
python3 main.py init
```

### How to Use

**The assistant responds to natural language!** No need to memorize commands or syntax.

Open this directory in Claude Code and simply ask:

**Getting Updates:**
- "what's the latest?" - Shows all recent FedRAMP activity (RFCs + git changes)
- "what's new this week?" - Weekly summary of changes
- "show me today's updates" - Just today's activity
- "what's important for compliance?" - Expert-prioritized updates

**Tracking RFCs:**
- "show me RFCs" - Active GitHub Discussions and proposals
- "what discussions are happening?" - Community discussions
- "what's active?" - Group RFCs by initiative and activity

**Specific Queries:**
- "what changed in the docs repo?" - Recent documentation changes
- "what is [name] working on?" - Contributor activity
- "show me the history of [filename]" - Complete file change history
- "what new files were added?" - Recently added documentation

**Context-Aware:**
The assistant automatically prioritizes based on your systems:
- 🚨 Critical updates for your High Rev5 system
- 📌 High priority for your planned 20x Moderate system
- ⚙️ General updates and changes

**Examples:**
```
You: what's the latest?
Assistant: [Shows RFCs, git changes, prioritized by your context]

You: show me RFCs
Assistant: [Groups by Rev5, 20x pilot, with activity assessment]

You: what's important for compliance?
Assistant: [Expert recommendations on what to focus on]
```

## Underlying Python Commands

The assistant uses these Python commands behind the scenes. You can also run them directly if needed:

| Command | Description |
|---------|-------------|
| `init` | Clone/update all repositories |
| `latest --days N` | Show all recent FedRAMP activity (RFCs + events + git changes) |
| `rfcs --days N` | Show GitHub Discussions RFCs |
| `events --days N` | Show link to upcoming FedRAMP events (requires manual visit) |
| `blog` | Show note about FedRAMP blog (requires manual visit) |
| `commits --repo NAME --days N` | List recent commits with file stats |
| `new-files --repo NAME --days N` | List newly added files |
| `file-history --repo NAME --file PATH` | Show complete history of a file |
| `contributor --repo NAME --name EMAIL --days N` | Show contributor activity and stats |

**Note:** Most users won't need to run these directly - just ask the assistant in natural language!

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

## Example Interactions

### Natural Language (Recommended)

**Weekly Check-In:**
```
You: what's the latest?
Assistant: [Shows RFCs, git changes, upcoming events - prioritized for your systems]

You: what's important for compliance?
Assistant: [Expert analysis with Critical/High/Medium priority updates]
```

**Tracking RFCs:**
```
You: show me RFCs
Assistant: [Groups by Rev5, 20x pilot, specific RFCs with URLs]

You: what discussions are happening?
Assistant: [Active community discussions and Q&A threads]
```

**Specific Queries:**
```
You: what changed in the docs repo?
Assistant: [Recent commits, new files, contributor activity]

You: what is john@fedramp.gov working on?
Assistant: [Contributor's recent commits and focus areas]
```

### Direct Python Commands (Optional)

If you prefer to run commands directly:

```bash
# See everything happening in FedRAMP
python3 main.py latest --days 7

# Track RFCs
python3 main.py rfcs --days 30

# Check specific repo
python3 main.py commits --repo docs --days 7

# Find new files
python3 main.py new-files --repo docs --days 30

# Track file history
python3 main.py file-history --repo docs --file authentication.md

# Monitor contributor
python3 main.py contributor --repo docs --name "pete@fedramp.gov" --days 30
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

## Using the Assistant

### Recommended Approach: Natural Language

The FedRAMP Compliance Engineer Assistant is designed for conversational interaction:

1. **Open the directory** in Claude Code or your AI assistant
2. **Ask questions naturally**: "what's the latest?", "show me RFCs", "what's important?"
3. **Get expert analysis**: Prioritized updates with compliance-focused recommendations
4. **Drill deeper**: Ask follow-up questions about specific RFCs, contributors, or files

### Alternative: Direct Commands

You can also run Python commands directly if you prefer:
```bash
python3 main.py latest --days 7
python3 main.py rfcs --days 30
```

But most users find the natural language interface more intuitive and helpful!

## License

Configuration for tracking FedRAMP public repositories. All tracked repositories maintain their original licenses.

---

**Your expert assistant for FedRAMP compliance engineering.**

**💬 Ask Questions Naturally** | **🎯 Get Expert Guidance** | **📊 Stay Informed** | **⚡ No API Tokens**
