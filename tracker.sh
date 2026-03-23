#!/usr/bin/env bash
# FedRAMP Git & Community Tracker - Universal Runner
# Supports both native Python and containerized execution

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="fedramp-tracker"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    cat <<EOF
FedRAMP Git & Community Tracker

Usage: $0 [--mode MODE] [COMMAND] [OPTIONS]

Modes:
  --mode native     Run using local Python (default if python3 is available)
  --mode container  Run using Podman/Docker container
  --mode auto       Auto-detect best option (default)

Commands:
  All commands from main.py are supported. Run with --help for full list.

Examples:
  # Auto-detect mode and run init
  $0 init

  # Force native mode
  $0 --mode native daily-report

  # Force container mode
  $0 --mode container rfcs --repo community

  # Build container image (only needed once for container mode)
  $0 --build

Environment Variables:
  GITHUB_TOKEN      GitHub API token (optional, recommended for discussions)
  TRACKER_MODE      Default mode (native, container, auto)

EOF
    exit 0
}

detect_mode() {
    # Check user preference
    if [[ -n "${TRACKER_MODE}" ]]; then
        echo "${TRACKER_MODE}"
        return
    fi

    # Auto-detect: prefer native if Python is available
    if command -v python3 &> /dev/null; then
        if python3 -c "import yaml, requests" 2>/dev/null; then
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
    if ! python3 -c "import yaml, requests" 2>/dev/null; then
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

    # Prepare volume mounts and environment
    local mounts=(
        "-v" "${SCRIPT_DIR}/config.yaml:/data/config.yaml:ro"
        "-v" "${SCRIPT_DIR}/repos:/data/repos"
        "-v" "${SCRIPT_DIR}/reports:/data/reports"
    )

    # Pass GitHub token if set
    local env_vars=()
    if [[ -n "${GITHUB_TOKEN}" ]]; then
        env_vars+=("-e" "GITHUB_TOKEN=${GITHUB_TOKEN}")
    fi

    # Run as current user to avoid permission issues
    local user_flag="--user=$(id -u):$(id -g)"

    # Execute container
    ${runtime} run --rm \
        ${user_flag} \
        "${mounts[@]}" \
        "${env_vars[@]}" \
        ${IMAGE_NAME} "$@"
}

# Main script
MODE="auto"
BUILD_ONLY=false

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
        --help|-h)
            usage
            ;;
        *)
            break
            ;;
    esac
done

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
