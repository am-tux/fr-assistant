# Running the Tracker - Quick Reference

## First Run Setup

**On your first run**, the tracker will interactively prompt you to choose your preferred mode:

```bash
./tracker.sh init

# You'll see:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   FedRAMP Git Repository Tracker - First Run Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Choose how you want to run the tracker:

1) Native Python
   - Direct execution, faster startup (~100ms)
   - Requires: Python 3.11+
   - Best for: Development, debugging, quick queries

2) Container (Podman/Docker)
   - Isolated environment, reproducible
   - Requires: Podman or Docker
   - Best for: Production, automation, isolation

Enter your choice [1-2]:
```

Your preference is saved in `.tracker-config` and used for all future runs.

**Change your preference anytime:**
```bash
./tracker.sh --reset-config  # Will prompt again on next run
./tracker.sh --show-config   # Show current preference
```

---

## Three Ways to Run

### 1. Universal Wrapper (Recommended)
```bash
./tracker.sh [command]
```
Auto-detects best method and runs it.

### 2. Native Python
```bash
python3 main.py [command]
```
Direct execution using local Python.

### 3. Container
```bash
podman run --rm \
  --user=$(id -u):$(id -g) \
  -v ./config.yaml:/data/config.yaml:ro \
  -v ./repos:/data/repos \
  -v ./reports:/data/reports \
  fedramp-tracker [command]
```
Run in isolated container (Podman/Docker).

---

## Quick Comparison

| Feature | Native Python | Container | Wrapper Script |
|---------|--------------|-----------|----------------|
| **Setup** | `pip3 install -r requirements.txt` | `./tracker.sh --build` | Auto-detects |
| **Startup** | Fast (~0.1s) | Slower (~1s) | Depends on mode |
| **Isolation** | No | Yes | Depends on mode |
| **Debugging** | Easy | Harder | Easy (if native) |
| **Python Required** | Yes (3.11+) | No | No (if container) |
| **Best For** | Development | Production | General use |

---

## Examples

### Generate Reports
```bash
# Using wrapper (auto-detect)
./tracker.sh daily-report

# Using native Python
python3 main.py daily-report

# Using container
./tracker.sh --mode container daily-report
```

### Query Data
```bash
# File history
./tracker.sh file-history --repo docs --file README.md

# Contributor activity
python3 main.py contributor --repo docs --name "pete-gov" --days 30

# New files
./tracker.sh new-files --repo docs --days 7
```

### Set Preferred Mode
```bash
# Always use native
export TRACKER_MODE=native
./tracker.sh daily-report

# Always use container
export TRACKER_MODE=container
./tracker.sh daily-report
```

---

## When to Use What

### Use Native Python When:
- ✅ You're actively developing or debugging
- ✅ You want fast startup times
- ✅ You have Python 3.11+ installed
- ✅ You're comfortable managing dependencies

### Use Container When:
- ✅ You want complete isolation
- ✅ You're deploying to production/servers
- ✅ You don't have Python installed
- ✅ You're running in CI/CD pipelines
- ✅ You want reproducible builds
- ✅ Multiple users with different environments

### Use Wrapper Script When:
- ✅ You want flexibility to switch between modes
- ✅ You want the simplest command syntax
- ✅ You're unsure which mode to use
- ✅ You want auto-detection based on environment

---

## Installation Comparison

### Native Python
```bash
# One-time setup
pip3 install -r requirements.txt

# Ready to use
python3 main.py init
```

### Container
```bash
# One-time build
./tracker.sh --build

# Ready to use
./tracker.sh init
```

### Wrapper (Auto)
```bash
# First run auto-detects and sets up
./tracker.sh init

# If native: installs pip packages
# If container: builds image automatically
```

---

## Troubleshooting

**Wrapper defaults to wrong mode:**
```bash
# Force your preferred mode
./tracker.sh --mode native [command]
./tracker.sh --mode container [command]

# Or set environment variable
export TRACKER_MODE=native
```

**Container permissions issues:**
```bash
# Wrapper script handles this automatically
# But if running podman directly, always use:
--user=$(id -u):$(id -g)
```

**Python dependencies missing:**
```bash
# Native mode
pip3 install -r requirements.txt

# Container mode (rebuild)
./tracker.sh --build
```

---

## Performance Notes

**Startup Time:**
- Native: ~100ms
- Container: ~1000ms (includes container startup)
- Wrapper overhead: ~50ms

**Execution Time:**
- Both modes: Identical once running
- Bottleneck is git operations, not runtime

**Recommendation:**
- Development: Use native for faster iteration
- Production: Use container for consistency
- Ad-hoc queries: Use wrapper for convenience
