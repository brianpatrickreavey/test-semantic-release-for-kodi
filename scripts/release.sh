#!/bin/bash

# Portable release script for triggering GitHub Actions workflow
# Usage: ./scripts/release.sh

set -e

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed. Please install it from https://cli.github.com/"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir &> /dev/null; then
    echo "Error: Not in a git repository."
    exit 1
fi

# Check if gh is authenticated
if ! gh auth status &> /dev/null; then
    echo "Error: GitHub CLI is not authenticated. Run 'gh auth login' first."
    exit 1
fi

echo "Triggering release workflow..."
gh workflow run release

echo "Release workflow triggered successfully!"
echo "Monitor progress at: https://github.com/$(gh repo view --json owner,name -q '.owner.login + \"/\" + .name')/actions"