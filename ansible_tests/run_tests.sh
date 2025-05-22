#!/bin/bash

# Script to run APILama Ansible tests

set -e

# Default values
API_URL="http://localhost:8081"
VERBOSITY=""
SKIP_CLEANUP="false"

# Help message
function show_help {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help               Show this help message"
    echo "  -u, --url URL            Set the API URL (default: http://localhost:8081)"
    echo "  -v, --verbose            Increase verbosity (can be used multiple times)"
    echo "  --no-cleanup             Skip cleanup of test files and directories"
    echo ""
    echo "Example:"
    echo "  $0 --url http://localhost:8081 -vv"
    exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -h|--help)
            show_help
            ;;
        -u|--url)
            API_URL="$2"
            shift
            shift
            ;;
        -v|--verbose)
            if [[ -z "$VERBOSITY" ]]; then
                VERBOSITY="-v"
            else
                VERBOSITY="${VERBOSITY}v"
            fi
            shift
            ;;
        --no-cleanup)
            SKIP_CLEANUP="true"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
done

# Check if ansible-playbook is installed
if ! command -v ansible-playbook &> /dev/null; then
    echo "Error: ansible-playbook is not installed. Please install Ansible first."
    exit 1
fi

# Run the tests
echo "Running APILama Ansible tests with API URL: $API_URL"

CLEANUP_ARG=""
if [[ "$SKIP_CLEANUP" == "true" ]]; then
    CLEANUP_ARG="-e cleanup_enabled=false"
    echo "Cleanup is disabled"
fi

ansible-playbook $VERBOSITY apilama_test_playbook.yml -e "api_base_url=$API_URL" $CLEANUP_ARG

echo "Tests completed"
