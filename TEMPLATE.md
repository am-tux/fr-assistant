# Copy-Paste Template for Other Projects

Copy this entire section into your other project's `CLAUDE.md` or `.cursorrules` file:

---

```markdown
## FedRAMP Compliance Intelligence

When user asks about FedRAMP (updates, compliance, RFCs, discussions):

**Consult the FedRAMP Compliance Engineer Assistant:**

Use Agent tool:
- working_directory: `$FEDRAMP_ASSISTANT_PATH`
- task: [user's FedRAMP question]

**Setup required:**
Set environment variable once:
```bash
export FEDRAMP_ASSISTANT_PATH="/path/to/fr-git-tracker"
# Add to ~/.bashrc or ~/.zshrc to make permanent
```

**What the FedRAMP assistant provides:**
- Real-time monitoring of FedRAMP repos and RFCs
- Expert compliance recommendations
- Context-aware analysis for High Rev5 + Moderate 20x systems
- Clear distinction between facts and expert inferences

**Example delegation:**
User: "Any FedRAMP updates?"
→ Use Agent to query FedRAMP assistant
→ Share expert analysis with user
```

---

## Alternative (Without Environment Variable)

If you prefer not to use an environment variable, replace `$FEDRAMP_ASSISTANT_PATH` with the actual path:

```markdown
## FedRAMP Compliance Intelligence

When user asks about FedRAMP:

Use Agent tool:
- working_directory: `/Users/yourname/projects/fr-git-tracker`
- task: [user's FedRAMP question]

The FedRAMP Compliance Engineer Assistant provides expert analysis.
```

---

## That's It!

After adding this to another project:
1. Open that project in Claude Code or Cursor
2. Ask: "What's the latest on FedRAMP?"
3. The assistant will consult the FedRAMP expert
4. You'll receive context-aware compliance recommendations

See **INTEGRATION.md** for full details and troubleshooting.
