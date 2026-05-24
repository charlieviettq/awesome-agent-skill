#!/bin/bash
# reflect-yourself installer for Cursor (macOS/Linux)
# Installs to ~/.cursor/skills/ for global availability

set -e

REPO_URL="https://raw.githubusercontent.com/maorfsdev/reflect-yourself/main"
DEST="$HOME/.cursor/skills/reflect-yourself"

echo ""
echo "reflect-yourself installer"
echo "=========================="
echo ""

# Check if running from local clone or remote
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" 2>/dev/null)" && pwd 2>/dev/null)" || SCRIPT_DIR=""

# Create destination directories
mkdir -p "$DEST/commands" "$DEST/rules"

if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/SKILL.md" ]; then
    # Local install - copy from cloned repo
    echo "Installing from local files..."
    cp "$SCRIPT_DIR/SKILL.md" "$DEST/"
    cp "$SCRIPT_DIR/commands/"* "$DEST/commands/"
    cp "$SCRIPT_DIR/rules/"* "$DEST/rules/"
else
    # Remote install - download from GitHub
    echo "Downloading from GitHub..."
    curl -fsSL "$REPO_URL/SKILL.md" -o "$DEST/SKILL.md"
    curl -fsSL "$REPO_URL/commands/reflect-yourself.md" -o "$DEST/commands/reflect-yourself.md"
    curl -fsSL "$REPO_URL/commands/reflect-yourself-skills.md" -o "$DEST/commands/reflect-yourself-skills.md"
    curl -fsSL "$REPO_URL/commands/reflect-yourself-queue.md" -o "$DEST/commands/reflect-yourself-queue.md"
    curl -fsSL "$REPO_URL/commands/reflect-yourself-skip.md" -o "$DEST/commands/reflect-yourself-skip.md"
    curl -fsSL "$REPO_URL/rules/session-reflect.mdc" -o "$DEST/rules/session-reflect.mdc"
fi

# Create empty queue file if it doesn't exist
QUEUE_FILE="$HOME/.cursor/reflect-queue.json"
if [ ! -f "$QUEUE_FILE" ]; then
    echo '{"version": 1, "learnings": []}' > "$QUEUE_FILE"
    echo "Created queue file at $QUEUE_FILE"
fi

echo ""
echo "Installed to $DEST"
echo ""
echo "The skill is now available in ALL your Cursor projects."
echo ""
echo "Commands:"
echo "  /reflect-yourself        - Capture learnings from session"
echo "  /reflect-yourself-skills - Discover skill patterns"
echo "  /reflect-yourself-queue  - View pending learnings"
echo "  /reflect-yourself-skip   - Clear the queue"
echo ""
echo "Run /reflect-yourself at the end of your sessions!"
echo ""
