#!/bin/bash

# Clode - Claude Code Configuration Installer
# Interactive installation with selective sync

set -e

CLODE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="$HOME/.claude"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

ask_yes_no() {
    while true; do
        read -p "$1 (y/n): " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

# Create machine-specific config if it doesn't exist
create_machine_config() {
    local config_file="$HOME/.clode-config.json"

    if [ ! -f "$config_file" ]; then
        cat > "$config_file" << EOF
{
  "machine_name": "$(hostname)",
  "installed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "global": {
    "commands": [],
    "hooks": [],
    "settings": false
  },
  "agents": [],
  "commands": [],
  "skills": [],
  "mcp_servers": {
    "global": [],
    "project": []
  }
}
EOF
        print_success "Created machine config at $config_file"
    fi
    echo "$config_file"
}

# Update machine config
update_config() {
    local config_file="$1"
    local category="$2"
    local item="$3"

    # Use Python to update JSON (more reliable than jq)
    python3 << EOF
import json
import sys

config_file = "$config_file"
category = "$category"
item = "$item"

with open(config_file, 'r') as f:
    config = json.load(f)

# Navigate nested structure for MCP servers
if '.' in category:
    parts = category.split('.')
    target = config
    for part in parts[:-1]:
        target = target[part]
    if item not in target[parts[-1]]:
        target[parts[-1]].append(item)
else:
    if item not in config[category]:
        config[category].append(item)

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)
EOF
}

# Check what's already installed
get_installed() {
    local config_file="$1"
    local category="$2"

    python3 << EOF
import json
config_file = "$config_file"
category = "$category"

with open(config_file, 'r') as f:
    config = json.load(f)

# Navigate nested structure
if '.' in category:
    parts = category.split('.')
    target = config
    for part in parts:
        target = target[part]
    print(' '.join(target))
else:
    print(' '.join(config[category]))
EOF
}

# Main installation
print_header "Clode Installation - Interactive Setup"

echo "This will set up Claude Code customizations from the clode repository."
echo "You can choose which components to install."
echo ""

# Create machine config
config_file=$(create_machine_config)

# Install global settings
print_header "Global Settings"

if [ -f "$CLODE_DIR/global/settings.json" ]; then
    if ask_yes_no "Install global settings (permissions, hooks config)?"; then
        mkdir -p "$CLAUDE_DIR"

        # Merge with existing settings if present
        if [ -f "$CLAUDE_DIR/settings.json" ]; then
            print_warning "Existing settings found. Creating backup..."
            cp "$CLAUDE_DIR/settings.json" "$CLAUDE_DIR/settings.json.backup"
        fi

        cp "$CLODE_DIR/global/settings.json" "$CLAUDE_DIR/settings.json"
        update_config "$config_file" "global.settings" "true"
        print_success "Global settings installed"
    fi
fi

# Install global commands
print_header "Global Commands"

if [ -d "$CLODE_DIR/global/commands" ]; then
    installed_commands=$(get_installed "$config_file" "global.commands")

    for cmd_file in "$CLODE_DIR/global/commands"/*.md; do
        if [ -f "$cmd_file" ]; then
            cmd_name=$(basename "$cmd_file")

            # Check if already installed
            if echo "$installed_commands" | grep -q "$cmd_name"; then
                print_success "$cmd_name (already installed)"
                continue
            fi

            if ask_yes_no "Install command: $cmd_name?"; then
                mkdir -p "$CLAUDE_DIR/commands"
                cp "$cmd_file" "$CLAUDE_DIR/commands/"
                update_config "$config_file" "global.commands" "$cmd_name"
                print_success "Installed $cmd_name"
            fi
        fi
    done
fi

# Install global hooks
print_header "Global Hooks"

if [ -d "$CLODE_DIR/global/hooks" ]; then
    installed_hooks=$(get_installed "$config_file" "global.hooks")

    for hook_file in "$CLODE_DIR/global/hooks"/*.py; do
        if [ -f "$hook_file" ]; then
            hook_name=$(basename "$hook_file")

            if echo "$installed_hooks" | grep -q "$hook_name"; then
                print_success "$hook_name (already installed)"
                continue
            fi

            if ask_yes_no "Install hook: $hook_name?"; then
                mkdir -p "$CLAUDE_DIR/hooks"
                cp "$hook_file" "$CLAUDE_DIR/hooks/"
                chmod +x "$CLAUDE_DIR/hooks/$hook_name"
                update_config "$config_file" "global.hooks" "$hook_name"
                print_success "Installed $hook_name"
            fi
        fi
    done
fi

# Install agents
print_header "Custom Agents"

if [ -d "$CLODE_DIR/project-templates/obsidian-vault/agents" ]; then
    installed_agents=$(get_installed "$config_file" "agents")

    for agent_file in "$CLODE_DIR/project-templates/obsidian-vault/agents"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)

            if echo "$installed_agents" | grep -q "$agent_name"; then
                print_success "$agent_name (already installed)"
                continue
            fi

            # Show description from file
            desc=$(grep -m 1 "^#" "$agent_file" | sed 's/^# //')
            echo "  Agent: $agent_name - $desc"

            if ask_yes_no "Install this agent?"; then
                echo "Where should this agent be installed?"
                echo "  1) Globally (~/.claude/agents)"
                echo "  2) Current project only"
                read -p "Choice (1/2): " choice

                case $choice in
                    1)
                        mkdir -p "$CLAUDE_DIR/agents"
                        cp "$agent_file" "$CLAUDE_DIR/agents/"
                        ;;
                    2)
                        mkdir -p ".claude/agents"
                        cp "$agent_file" ".claude/agents/"
                        ;;
                    *)
                        print_warning "Skipping $agent_name"
                        continue
                        ;;
                esac

                update_config "$config_file" "agents" "$agent_name"
                print_success "Installed $agent_name"
            fi
        fi
    done
fi

# Install project commands
print_header "Project Commands"

if [ -d "$CLODE_DIR/project-templates/obsidian-vault/commands" ]; then
    installed_commands=$(get_installed "$config_file" "commands")

    # Show count
    total_commands=$(find "$CLODE_DIR/project-templates/obsidian-vault/commands" -name "*.md" | wc -l)
    echo "Found $total_commands custom commands available"

    if ask_yes_no "Review and install project commands individually?"; then
        for cmd_file in "$CLODE_DIR/project-templates/obsidian-vault/commands"/*.md; do
            if [ -f "$cmd_file" ]; then
                cmd_name=$(basename "$cmd_file" .md)

                if echo "$installed_commands" | grep -q "$cmd_name"; then
                    continue
                fi

                # Show first line description
                desc=$(head -n 5 "$cmd_file" | grep "^#" | head -n 1 | sed 's/^# //')
                echo ""
                echo "Command: /$cmd_name"
                echo "  $desc"

                if ask_yes_no "Install this command?"; then
                    echo "Install:"
                    echo "  1) Globally (~/.claude/commands)"
                    echo "  2) Current project only"
                    read -p "Choice (1/2): " choice

                    case $choice in
                        1)
                            mkdir -p "$CLAUDE_DIR/commands"
                            cp "$cmd_file" "$CLAUDE_DIR/commands/"
                            ;;
                        2)
                            mkdir -p ".claude/commands"
                            cp "$cmd_file" ".claude/commands/"
                            ;;
                        *)
                            continue
                            ;;
                    esac

                    update_config "$config_file" "commands" "$cmd_name"
                    print_success "Installed /$cmd_name"
                fi
            fi
        done
    else
        if ask_yes_no "Install ALL project commands to current directory?"; then
            mkdir -p ".claude/commands"
            cp "$CLODE_DIR/project-templates/obsidian-vault/commands"/*.md ".claude/commands/"
            print_success "Installed all project commands"
        fi
    fi
fi

# Install skills
print_header "Custom Skills"

if [ -d "$CLODE_DIR/project-templates/obsidian-vault/skills" ]; then
    installed_skills=$(get_installed "$config_file" "skills")

    for skill_file in "$CLODE_DIR/project-templates/obsidian-vault/skills"/*.md; do
        if [ -f "$skill_file" ]; then
            skill_name=$(basename "$skill_file" .md)

            if echo "$installed_skills" | grep -q "$skill_name"; then
                print_success "$skill_name (already installed)"
                continue
            fi

            if ask_yes_no "Install skill: $skill_name?"; then
                echo "Install:"
                echo "  1) Globally (~/.claude/skills)"
                echo "  2) Current project only"
                read -p "Choice (1/2): " choice

                case $choice in
                    1)
                        mkdir -p "$CLAUDE_DIR/skills"
                        cp "$skill_file" "$CLAUDE_DIR/skills/"
                        ;;
                    2)
                        mkdir -p ".claude/skills"
                        cp "$skill_file" ".claude/skills/"
                        ;;
                    *)
                        continue
                        ;;
                esac

                update_config "$config_file" "skills" "$skill_name"
                print_success "Installed $skill_name"
            fi
        fi
    done
fi

print_header "Installation Complete!"

echo ""
echo "Configuration saved to: $config_file"
echo ""
echo "Next steps:"
echo "  1. Add your API keys (see mcp-configs/SECRETS.md)"
echo "  2. Run 'claude mcp list' to verify MCP servers"
echo "  3. Try your new commands with /help"
echo ""
print_success "Installation finished successfully!"
