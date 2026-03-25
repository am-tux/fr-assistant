# FedRAMP Assistant Integration Guide

This guide shows how to integrate the FedRAMP Compliance Engineer Assistant into other projects so any AI assistant can access FedRAMP intelligence.

## Quick Setup

### 1. Note Your Project Location

After cloning this repository, note its full path:
```bash
cd /path/to/fr-git-tracker
pwd
# Copy this path - you'll need it for integration
```

Or set an environment variable (recommended):
```bash
# Add to your ~/.bashrc or ~/.zshrc
export FEDRAMP_ASSISTANT_PATH="/path/to/fr-git-tracker"
```

### 2. Add to Other Projects

Copy the template below into other projects' `CLAUDE.md` or `.cursorrules` files.

---

## Template for Other Projects

Add this section to any project's `CLAUDE.md` or `.cursorrules`:

```markdown
## FedRAMP Compliance Intelligence

When the user asks about FedRAMP (status, updates, compliance, RFCs, discussions):

### Use the FedRAMP Compliance Engineer Assistant

**Method 1: Via Agent Tool (Recommended)**

Use the Agent tool to consult the FedRAMP expert:

1. **Agent Configuration:**
   - `working_directory`: `$FEDRAMP_ASSISTANT_PATH` (or your project's full path)
   - `task`: Pass the user's FedRAMP question
   - The agent will load the FedRAMP expert persona

2. **What the FedRAMP Assistant Provides:**
   - Monitors FedRAMP/docs, FedRAMP/roadmap, FedRAMP/community repos
   - Tracks GitHub Discussions RFCs
   - Expert recommendations for compliance engineers
   - Context-aware analysis (High Rev5 + Moderate 20x systems)
   - Clear distinction between facts and expert inferences

3. **Example Usage:**
   ```
   User: "Any FedRAMP updates this week?"

   Action: Use Agent tool
   - working_directory: $FEDRAMP_ASSISTANT_PATH
   - task: "What's the latest on FedRAMP this week?"

   The FedRAMP expert will provide prioritized updates with
   compliance recommendations.
   ```

**Method 2: Direct Command (Alternative)**

If you can't use the Agent tool, run commands directly:

```bash
cd $FEDRAMP_ASSISTANT_PATH && python3 main.py latest --days 7
cd $FEDRAMP_ASSISTANT_PATH && python3 main.py rfcs --days 30
```

**Note:** Replace `$FEDRAMP_ASSISTANT_PATH` with the actual path where
you cloned the fr-git-tracker repository, or set it as an environment
variable as described in the setup section.

### Example Questions to Delegate

Automatically consult the FedRAMP assistant when user asks:
- "What's the latest on FedRAMP?"
- "Any FedRAMP updates?"
- "Show me recent RFCs"
- "What's happening in FedRAMP discussions?"
- "What should I know about FedRAMP compliance?"
- "Are there any Rev5 changes?"
- "What's new with the 20x pilot?"
```

---

## Setup Instructions by Editor

### For Claude Code Users

1. Clone the FedRAMP assistant repository
2. Note the path or set `FEDRAMP_ASSISTANT_PATH` environment variable
3. Copy the template above into your project's `CLAUDE.md`
4. Replace `$FEDRAMP_ASSISTANT_PATH` with actual path if not using env var

### For Cursor Users

1. Clone the FedRAMP assistant repository
2. Note the path or set `FEDRAMP_ASSISTANT_PATH` environment variable
3. Copy the template above into your project's `.cursorrules`
4. Replace `$FEDRAMP_ASSISTANT_PATH` with actual path if not using env var

---

## Example Integration

If you cloned to `/Users/yourname/fedramp-assistant`, your integration would look like:

```markdown
## FedRAMP Compliance Intelligence

When the user asks about FedRAMP:

Use the Agent tool:
- working_directory: `/Users/yourname/fedramp-assistant`
- task: [user's FedRAMP question]

The FedRAMP Compliance Engineer Assistant will provide expert analysis.
```

---

## Environment Variable Setup (Recommended)

**Bash/Zsh:**
```bash
echo 'export FEDRAMP_ASSISTANT_PATH="/full/path/to/fr-git-tracker"' >> ~/.bashrc
source ~/.bashrc
```

**Fish:**
```fish
set -Ux FEDRAMP_ASSISTANT_PATH "/full/path/to/fr-git-tracker"
```

Then use `$FEDRAMP_ASSISTANT_PATH` in your templates.

---

## Available Commands

If using direct command method:

| Command | Description |
|---------|-------------|
| `python3 main.py latest --days 7` | All recent activity (RFCs + git) |
| `python3 main.py rfcs --days 30` | GitHub Discussions RFCs |
| `python3 main.py commits --repo docs --days 7` | Git commits for specific repo |
| `python3 main.py new-files --repo docs --days 30` | Newly added files |
| `python3 main.py file-history --repo docs --file FILE` | History of specific file |
| `python3 main.py contributor --repo docs --name EMAIL --days 30` | Contributor activity |

---

## Testing Your Integration

After adding the template to another project:

1. Open that project in Claude Code or Cursor
2. Ask: "What's the latest on FedRAMP?"
3. The assistant should use the Agent tool to consult the FedRAMP expert
4. You should receive context-aware compliance recommendations

---

## Troubleshooting

**Agent tool can't find the directory:**
- Verify the path is correct: `ls $FEDRAMP_ASSISTANT_PATH`
- Make sure environment variable is set: `echo $FEDRAMP_ASSISTANT_PATH`
- Use absolute path instead of environment variable

**Commands not working:**
- Ensure Python dependencies are installed: `cd $FEDRAMP_ASSISTANT_PATH && pip3 install -r requirements.txt`
- Initialize repos: `cd $FEDRAMP_ASSISTANT_PATH && python3 main.py init`

**No response from FedRAMP assistant:**
- Check that `CLAUDE.md` exists in the fr-git-tracker directory
- Verify the Agent tool is available in your Claude Code/Cursor version

---

## Benefits of Integration

When integrated, any project can:
- ✅ Get real-time FedRAMP updates
- ✅ Access expert compliance recommendations
- ✅ Understand High Rev5 and Moderate 20x impacts
- ✅ Track RFCs and community discussions
- ✅ Receive context-aware prioritization
- ✅ Distinguish between facts and expert inferences

All without duplicating code or expertise across projects!
