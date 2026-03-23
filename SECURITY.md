# Security Best Practices

## ⚠️ Protecting Your GitHub Token

### DO NOT Commit Tokens

Your GitHub token is a **secret credential** that provides access to your GitHub account. **Never commit it to version control.**

### ✅ Safe Methods

**1. Environment Variable (Recommended)**
```bash
# Set in your shell
export GITHUB_TOKEN=ghp_your_token_here

# Run the tracker
./tracker.sh daily-report
```

**2. Shell Profile (Persistent)**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export GITHUB_TOKEN=ghp_your_token_here' >> ~/.bashrc
source ~/.bashrc
```

**3. .env File (Local Only)**
```bash
# Create .env file (already gitignored)
echo "GITHUB_TOKEN=ghp_your_token_here" > .env

# Load it before running
source .env
./tracker.sh daily-report
```

**4. Secret Management Tools**
```bash
# Using pass
export GITHUB_TOKEN=$(pass github/fedramp-tracker)

# Using 1Password CLI
export GITHUB_TOKEN=$(op read "op://Private/GitHub Token/credential")

# Using macOS Keychain
export GITHUB_TOKEN=$(security find-generic-password -s "fedramp-tracker" -w)
```

### ❌ Unsafe Methods - NEVER DO THESE

```yaml
# ❌ NEVER hardcode in config.yaml
github_api:
  token: "ghp_actual_token_here"  # THIS WILL BE COMMITTED TO GIT!

# ❌ NEVER store in version-controlled files
# ❌ NEVER commit .env files with actual tokens
# ❌ NEVER put tokens in scripts tracked by git
```

---

## Protected Files (.gitignore)

The following files are automatically excluded from git to prevent accidental token commits:

```
# Environment files
.env, .env.*, .envrc, *.env, env.sh, setenv.sh

# Token files
.token, *.token, token.txt, secrets.*, .secrets

# Credentials
credentials.*, .credentials

# Local config overrides
config.local.yaml, config.*.yaml

# Backups
*.bak, *.backup, *.old, *.orig, *~
```

**The main `config.yaml` is tracked** because it uses `${GITHUB_TOKEN}` (environment variable) instead of hardcoded values.

---

## Creating a GitHub Token

### Step 1: Generate Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a descriptive name: `fedramp-tracker`
4. Select scopes:
   - ✅ `public_repo` (for public repositories)
   - ✅ `read:discussion` (for GitHub Discussions)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

### Step 2: Store Securely

```bash
# Store in environment variable
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Verify it works
./tracker.sh rfcs --repo community
```

### Step 3: Revoke If Compromised

If you accidentally commit a token:

1. **Immediately revoke it** at https://github.com/settings/tokens
2. Generate a new token
3. Update your environment variable
4. **Remove the token from git history:**
   ```bash
   # If you committed it
   git reset --soft HEAD~1  # Undo the commit
   git reset HEAD <file>    # Unstage the file
   # Edit file to remove token
   git add <file>
   git commit -m "remove token"
   ```

---

## Token Scope Permissions

**Minimum required scopes:**
- `public_repo` - Access public repositories
- `read:discussion` - Read GitHub Discussions

**Do NOT grant:**
- ❌ `repo` (full repo access) - unnecessarily broad
- ❌ `write:*` permissions - tracker is read-only
- ❌ `delete:*` permissions - never needed

---

## Security Checklist

Before committing changes:

- [ ] `git diff` - Check no tokens in modified files
- [ ] `git status` - Verify no `.env` or token files staged
- [ ] `.gitignore` - Confirm sensitive files are excluded
- [ ] `config.yaml` - Contains `${GITHUB_TOKEN}`, not actual token

---

## Automated Protections

This project includes:

1. **Comprehensive .gitignore** - Blocks common token file patterns
2. **Environment variable parsing** - Config reads from `${GITHUB_TOKEN}`
3. **Clear warnings** - Config file includes security warnings
4. **Documentation** - Multiple reminders about token safety

---

## What If I Accidentally Commit a Token?

### Immediate Actions:

1. **Revoke the token immediately**
   - Go to https://github.com/settings/tokens
   - Find the token and click "Delete"

2. **Generate a new token**
   - Create a new token with same scopes
   - Update your environment variable

3. **Remove from git history** (if not pushed yet)
   ```bash
   git reset HEAD~1
   # Remove token from files
   git add .
   git commit -m "remove sensitive data"
   ```

4. **If already pushed to GitHub**
   - GitHub will **auto-detect** and revoke the token
   - You'll receive an email notification
   - Follow steps 1-2 above to create a new token

---

## Additional Security Tips

1. **Use fine-grained tokens** (Personal Access Tokens - fine-grained)
   - More secure than classic tokens
   - Can limit to specific repositories
   - Can set expiration dates

2. **Set token expiration**
   - Use 90-day or 1-year expiration
   - Rotate tokens regularly

3. **Use different tokens** for different projects
   - Easier to revoke if one is compromised
   - Better audit trail

4. **Monitor token usage**
   - Check https://github.com/settings/tokens regularly
   - Review "Last used" dates
   - Revoke unused tokens

---

## Getting Help

If you have questions about token security:

- GitHub Docs: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- Security Issues: Report to repository maintainers
- General Help: Open an issue (DO NOT include token in issue!)

---

**Remember:** When in doubt, revoke and regenerate. It's always safer to create a new token than risk using a compromised one.
