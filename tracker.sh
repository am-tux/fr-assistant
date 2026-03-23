#!/usr/bin/env bash
# FedRAMP Git Repository Tracker - Universal Runner
# Supports both native Python and containerized execution

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="fedramp-tracker"
CONFIG_FILE="${SCRIPT_DIR}/.tracker-config"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    cat <<EOF
FedRAMP Git Repository Tracker

Usage: $0 [--mode MODE] [COMMAND] [OPTIONS]

Modes:
  --mode native     Run using local Python (default if python3 is available)
  --mode container  Run using Podman/Docker container
  --mode auto       Auto-detect best option (default)

Special Commands:
  --build           Build container image
  --reset-config    Reset mode preference (will prompt again on next run)
  --show-config     Show current mode preference

Commands:
  All commands from main.py are supported. Run with --help for full list.

Examples:
  # First run - will prompt for mode preference
  $0 init

  # Use saved preference
  $0 daily-report

  # Override saved preference temporarily
  $0 --mode native daily-report
  $0 --mode container rfcs --repo community

  # Change your preference
  $0 --reset-config

  # Build container image (only needed once for container mode)
  $0 --build

Environment Variables:
  TRACKER_MODE      Default mode (native, container, auto) - overrides saved preference

Saved Preference:
  Your mode preference is saved in ${CONFIG_FILE}
  Delete this file or use --reset-config to choose again

EOF
    exit 0
}

is_first_run() {
    # Check if config file exists and has a mode set
    if [[ -f "${CONFIG_FILE}" ]]; then
        local saved_mode=$(grep "^MODE=" "${CONFIG_FILE}" | cut -d= -f2)
        if [[ -n "${saved_mode}" ]]; then
            return 1  # Not first run
        fi
    fi
    return 0  # First run
}

save_mode_preference() {
    local mode=$1
    cat > "${CONFIG_FILE}" <<EOF
# Tracker Runtime Configuration
# Auto-generated on first run
# Delete this file to reset and be prompted again

# Execution mode: native or container
MODE=${mode}
EOF
    echo -e "${GREEN}✓ Preference saved to ${CONFIG_FILE}${NC}" >&2
}

load_saved_mode() {
    if [[ -f "${CONFIG_FILE}" ]]; then
        local saved_mode=$(grep "^MODE=" "${CONFIG_FILE}" | cut -d= -f2)
        if [[ -n "${saved_mode}" ]]; then
            echo "${saved_mode}"
            return 0
        fi
    fi
    return 1
}

prompt_mode_selection() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}" >&2
    echo -e "${BLUE}   FedRAMP Git Repository Tracker - First Run Setup${NC}" >&2
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}" >&2
    echo "" >&2
    echo "Choose how you want to run the tracker:" >&2
    echo "" >&2
    echo "1) Native Python" >&2
    echo "   - Direct execution, faster startup (~100ms)" >&2
    echo "   - Requires: Python 3.11+" >&2
    echo "   - Best for: Development, debugging, quick queries" >&2
    echo "" >&2
    echo "2) Container (Podman/Docker)" >&2
    echo "   - Isolated environment, reproducible" >&2
    echo "   - Requires: Podman or Docker" >&2
    echo "   - Best for: Production, automation, isolation" >&2
    echo "" >&2

    # Check what's available
    local has_python=false
    local has_container=false

    if command -v python3 &> /dev/null; then
        if python3 -c "import yaml" 2>/dev/null; then
            has_python=true
            echo -e "${GREEN}✓ Python 3 with dependencies detected${NC}" >&2
        else
            echo -e "${YELLOW}⚠ Python 3 found but dependencies not installed${NC}" >&2
            echo -e "${YELLOW}  (Run: pip3 install -r requirements.txt)${NC}" >&2
        fi
    else
        echo -e "${YELLOW}⚠ Python 3 not detected${NC}" >&2
    fi

    if command -v podman &> /dev/null || command -v docker &> /dev/null; then
        has_container=true
        echo -e "${GREEN}✓ Container runtime detected${NC}" >&2
    else
        echo -e "${YELLOW}⚠ No container runtime (Podman/Docker) detected${NC}" >&2
    fi

    echo "" >&2

    # Suggest default based on what's available
    local default_choice=""
    if [[ "${has_python}" == "true" ]]; then
        default_choice="1"
        echo -e "${BLUE}Recommended: Native Python (option 1)${NC}" >&2
    elif [[ "${has_container}" == "true" ]]; then
        default_choice="2"
        echo -e "${BLUE}Recommended: Container (option 2)${NC}" >&2
    else
        default_choice="1"
        echo -e "${YELLOW}Note: You may need to install dependencies for either option${NC}" >&2
    fi

    echo "" >&2
    read -p "Enter your choice [1-2] (default: ${default_choice}): " choice

    # Use default if empty
    choice=${choice:-$default_choice}

    case $choice in
        1)
            echo "native"
            ;;
        2)
            echo "container"
            ;;
        *)
            echo -e "${YELLOW}Invalid choice. Defaulting to native.${NC}" >&2
            echo "native"
            ;;
    esac
}

detect_mode() {
    # 1. Check explicit environment variable
    if [[ -n "${TRACKER_MODE}" ]]; then
        echo "${TRACKER_MODE}"
        return
    fi

    # 2. Check saved preference
    local saved_mode=$(load_saved_mode)
    if [[ $? -eq 0 ]]; then
        echo "${saved_mode}"
        return
    fi

    # 3. First run - prompt user (only in interactive mode)
    if is_first_run && [[ -t 0 ]]; then
        local selected_mode=$(prompt_mode_selection)
        save_mode_preference "${selected_mode}"
        echo "${selected_mode}"
        return
    fi

    # 4. Non-interactive fallback: auto-detect
    # Prefer native if Python is available
    if command -v python3 &> /dev/null; then
        if python3 -c "import yaml" 2>/dev/null; then
            echo "native"
            return
        fi
    fi

    # Check for container runtime
    if command -v podman &> /dev/null || command -v docker &> /dev/null; then
        echo "container"
        return
    fi

    # Default to native
    echo "native"
}

get_container_runtime() {
    if command -v podman &> /dev/null; then
        echo "podman"
    elif command -v docker &> /dev/null; then
        echo "docker"
    else
        echo -e "${YELLOW}Warning: No container runtime found. Install Podman or Docker.${NC}" >&2
        exit 1
    fi
}

build_container() {
    local runtime=$(get_container_runtime)
    echo -e "${GREEN}Building container image with ${runtime}...${NC}"

    cd "${SCRIPT_DIR}"
    ${runtime} build -t ${IMAGE_NAME} .

    echo -e "${GREEN}✓ Container image built: ${IMAGE_NAME}${NC}"
}

run_native() {
    cd "${SCRIPT_DIR}"

    # Check if dependencies are installed
    if ! python3 -c "import yaml" 2>/dev/null; then
        echo -e "${YELLOW}Installing Python dependencies...${NC}"
        pip3 install -r requirements.txt
    fi

    python3 main.py "$@"
}

run_container() {
    local runtime=$(get_container_runtime)

    # Check if image exists
    if ! ${runtime} image exists ${IMAGE_NAME} 2>/dev/null; then
        echo -e "${YELLOW}Container image not found. Building...${NC}"
        build_container
    fi

    # Prepare volume mounts
    local mounts=(
        "-v" "${SCRIPT_DIR}/config.yaml:/data/config.yaml:ro"
        "-v" "${SCRIPT_DIR}/repos:/data/repos"
        "-v" "${SCRIPT_DIR}/reports:/data/reports"
    )

    # Run as current user to avoid permission issues
    local user_flag="--user=$(id -u):$(id -g)"

    # Execute container
    ${runtime} run --rm \
        ${user_flag} \
        "${mounts[@]}" \
        ${IMAGE_NAME} "$@"
}

# Main script
MODE="auto"
BUILD_ONLY=false
RESET_CONFIG=false
SHOW_CONFIG=false

# Parse mode flag
while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --build)
            BUILD_ONLY=true
            shift
            ;;
        --reset-config)
            RESET_CONFIG=true
            shift
            ;;
        --show-config)
            SHOW_CONFIG=true
            shift
            ;;
        --help|-h)
            usage
            ;;
        *)
            break
            ;;
    esac
done

# Show config
if [[ "${SHOW_CONFIG}" == "true" ]]; then
    if [[ -f "${CONFIG_FILE}" ]]; then
        echo -e "${BLUE}Current configuration:${NC}"
        cat "${CONFIG_FILE}"
        echo ""
        saved_mode=$(load_saved_mode)
        echo -e "Active mode: ${GREEN}${saved_mode}${NC}"
    else
        echo -e "${YELLOW}No saved configuration found.${NC}"
        echo "You will be prompted to choose on next run."
    fi
    exit 0
fi

# Reset config
if [[ "${RESET_CONFIG}" == "true" ]]; then
    if [[ -f "${CONFIG_FILE}" ]]; then
        rm "${CONFIG_FILE}"
        echo -e "${GREEN}✓ Configuration reset.${NC}"
        echo "You will be prompted to choose your preferred mode on next run."
    else
        echo -e "${YELLOW}No configuration file found (already reset).${NC}"
    fi
    exit 0
fi

# Build only
if [[ "${BUILD_ONLY}" == "true" ]]; then
    build_container
    exit 0
fi

# Detect mode if auto
if [[ "${MODE}" == "auto" ]]; then
    MODE=$(detect_mode)
fi

# Show mode
if [[ "${MODE}" == "native" ]]; then
    echo -e "${GREEN}Running in native mode (Python)${NC}" >&2
    run_native "$@"
elif [[ "${MODE}" == "container" ]]; then
    echo -e "${GREEN}Running in container mode ($(get_container_runtime))${NC}" >&2
    run_container "$@"
else
    echo "Invalid mode: ${MODE}" >&2
    echo "Use --mode native or --mode container" >&2
    exit 1
fi
