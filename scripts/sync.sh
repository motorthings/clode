#!/bin/bash

# Clode - Smart Sync Script
# Detects changes and allows selective sync

set -e

CLODE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="$HOME/.claude"
CONFIG_FILE="$HOME/.clode-config.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${CYAN}ℹ${NC} $1"
}

print_new() {
    echo -e "${GREEN}NEW${NC} $1"
}

# Check if repo has been initialized
if [ ! -d "$CLODE_DIR/.git" ]; then
    print_warning "Clode repo not initialized. Run from clode directory:"
    echo "  git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

# Create config if it doesn't exist
if [ ! -f "$CONFIG_FILE" ]; then
    print_warning "No machine config found. Run ./install.sh first"
    exit 1
fi

# Get installed items
get_installed() {
    local category="$1"
    python3 << EOF
import json
with open("$CONFIG_FILE", 'r') as f:
    config = json.load(f)

if '.' in "$category":
    parts = "$category".split('.')
    target = config
    for part in parts:
        target = target[part]
    print(' '.join(target))
else:
    print(' '.join(config["$category"]))
EOF
}

# Update config
update_config() {
    local category="$1"
    local item="$2"

    python3 << EOF
import json
with open("$CONFIG_FILE", 'r') as f:
    config = json.load(f)

if '.' in "$category":
    parts = "$category".split('.')
    target = config
    for part in parts[:-1]:
        target = target[part]
    if "$item" not in target[parts[-1]]:
        target[parts[-1]].append("$item")
else:
    if "$item" not in config["$category"]:
        config["$category"].append("$item")

with open("$CONFIG_FILE", 'w') as f:
    json.dump(config, f, indent=2)
EOF
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

# PULL: Sync from repo to local
sync_pull() {
    print_header "Syncing FROM Repository"

    # Pull latest changes
    cd "$CLODE_DIR"
    print_info "Pulling latest changes from Git..."

    if git pull origin main 2>/dev/null; then
        print_success "Repository updated"
    else
        print_warning "No remote configured or on different branch"
    fi

    # Check for new additions
    local new_items_found=false

    # Check agents
    print_header "Checking for New Agents"
    installed_agents=$(get_installed "agents")

    for agent_file in "$CLODE_DIR/project-templates/obsidian-vault/agents"/*.md; do
        if [ -f "$agent_file" ]; then
            agent_name=$(basename "$agent_file" .md)

            if ! echo "$installed_agents" | grep -q "$agent_name"; then
                new_items_found=true
                desc=$(grep -m 1 "^#" "$agent_file" | sed 's/^# //')
                print_new "Agent: $agent_name - $desc"

                if ask_yes_no "Install this new agent?"; then
                    echo "Install location:"
                    echo "  1) Global (~/.claude/agents)"
                    echo "  2) Current project"
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
                    esac

                    update_config "agents" "$agent_name"
                    print_success "Installed $agent_name"
                fi
            fi
        fi
    done

    # Check commands
    print_header "Checking for New Commands"
    installed_commands=$(get_installed "commands")

    for cmd_file in "$CLODE_DIR/project-templates/obsidian-vault/commands"/*.md; do
        if [ -f "$cmd_file" ]; then
            cmd_name=$(basename "$cmd_file" .md)

            if ! echo "$installed_commands" | grep -q "$cmd_name"; then
                new_items_found=true
                print_new "Command: /$cmd_name"

                if ask_yes_no "Install this new command?"; then
                    echo "Install location:"
                    echo "  1) Global (~/.claude/commands)"
                    echo "  2) Current project"
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
                    esac

                    update_config "commands" "$cmd_name"
                    print_success "Installed /$cmd_name"
                fi
            fi
        fi
    done

    # Check skills
    print_header "Checking for New Skills"
    installed_skills=$(get_installed "skills")

    for skill_file in "$CLODE_DIR/project-templates/obsidian-vault/skills"/*.md; do
        if [ -f "$skill_file" ]; then
            skill_name=$(basename "$skill_file" .md)

            if ! echo "$installed_skills" | grep -q "$skill_name"; then
                new_items_found=true
                print_new "Skill: $skill_name"

                if ask_yes_no "Install this new skill?"; then
                    echo "Install location:"
                    echo "  1) Global (~/.claude/skills)"
                    echo "  2) Current project"
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
                    esac

                    update_config "skills" "$skill_name"
                    print_success "Installed $skill_name"
                fi
            fi
        fi
    done

    # Check global commands
    print_header "Checking for New Global Commands"
    installed_global_commands=$(get_installed "global.commands")

    for cmd_file in "$CLODE_DIR/global/commands"/*.md; do
        if [ -f "$cmd_file" ]; then
            cmd_name=$(basename "$cmd_file")

            if ! echo "$installed_global_commands" | grep -q "$cmd_name"; then
                new_items_found=true
                print_new "Global Command: $cmd_name"

                if ask_yes_no "Install this new global command?"; then
                    mkdir -p "$CLAUDE_DIR/commands"
                    cp "$cmd_file" "$CLAUDE_DIR/commands/"
                    update_config "global.commands" "$cmd_name"
                    print_success "Installed $cmd_name"
                fi
            fi
        fi
    done

    # Check hooks
    print_header "Checking for New Hooks"
    installed_hooks=$(get_installed "global.hooks")

    for hook_file in "$CLODE_DIR/global/hooks"/*.py; do
        if [ -f "$hook_file" ]; then
            hook_name=$(basename "$hook_file")

            if ! echo "$installed_hooks" | grep -q "$hook_name"; then
                new_items_found=true
                print_new "Hook: $hook_name"

                if ask_yes_no "Install this new hook?"; then
                    mkdir -p "$CLAUDE_DIR/hooks"
                    cp "$hook_file" "$CLAUDE_DIR/hooks/"
                    chmod +x "$CLAUDE_DIR/hooks/$hook_name"
                    update_config "global.hooks" "$hook_name"
                    print_success "Installed $hook_name"
                fi
            fi
        fi
    done

    if [ "$new_items_found" = false ]; then
        print_success "No new items found. You're up to date!"
    fi

    print_header "Sync Complete"
}

# PUSH: Sync local changes to repo
sync_push() {
    print_header "Syncing TO Repository"

    print_info "Collecting local customizations..."

    # Copy any new agents
    if [ -d "$CLAUDE_DIR/agents" ]; then
        for agent in "$CLAUDE_DIR/agents"/*.md; do
            if [ -f "$agent" ]; then
                agent_name=$(basename "$agent")
                if [ ! -f "$CLODE_DIR/project-templates/obsidian-vault/agents/$agent_name" ]; then
                    print_new "Found new local agent: $agent_name"
                    if ask_yes_no "Add to repository?"; then
                        cp "$agent" "$CLODE_DIR/project-templates/obsidian-vault/agents/"
                        print_success "Added to repo"
                    fi
                fi
            fi
        done
    fi

    # Copy any new commands
    if [ -d "$CLAUDE_DIR/commands" ]; then
        for cmd in "$CLAUDE_DIR/commands"/*.md; do
            if [ -f "$cmd" ]; then
                cmd_name=$(basename "$cmd")
                if [ ! -f "$CLODE_DIR/global/commands/$cmd_name" ]; then
                    print_new "Found new local command: $cmd_name"
                    echo "Add as:"
                    echo "  1) Global command"
                    echo "  2) Project command"
                    echo "  3) Skip"
                    read -p "Choice (1/2/3): " choice

                    case $choice in
                        1)
                            cp "$cmd" "$CLODE_DIR/global/commands/"
                            print_success "Added as global command"
                            ;;
                        2)
                            cp "$cmd" "$CLODE_DIR/project-templates/obsidian-vault/commands/"
                            print_success "Added as project command"
                            ;;
                        *)
                            print_info "Skipped"
                            ;;
                    esac
                fi
            fi
        done
    fi

    # Copy any new hooks
    if [ -d "$CLAUDE_DIR/hooks" ]; then
        for hook in "$CLAUDE_DIR/hooks"/*.py; do
            if [ -f "$hook" ]; then
                hook_name=$(basename "$hook")
                if [ ! -f "$CLODE_DIR/global/hooks/$hook_name" ]; then
                    print_new "Found new local hook: $hook_name"
                    if ask_yes_no "Add to repository?"; then
                        cp "$hook" "$CLODE_DIR/global/hooks/"
                        print_success "Added to repo"
                    fi
                fi
            fi
        done
    fi

    # Copy any new skills
    if [ -d "$CLAUDE_DIR/skills" ]; then
        for skill in "$CLAUDE_DIR/skills"/*.md; do
            if [ -f "$skill" ]; then
                skill_name=$(basename "$skill")
                if [ ! -f "$CLODE_DIR/project-templates/obsidian-vault/skills/$skill_name" ]; then
                    print_new "Found new local skill: $skill_name"
                    if ask_yes_no "Add to repository?"; then
                        cp "$skill" "$CLODE_DIR/project-templates/obsidian-vault/skills/"
                        print_success "Added to repo"
                    fi
                fi
            fi
        done
    fi

    # Show git status
    cd "$CLODE_DIR"
    if [ -n "$(git status --porcelain)" ]; then
        echo ""
        print_info "Changes to commit:"
        git status --short

        echo ""
        if ask_yes_no "Commit and push changes?"; then
            read -p "Commit message: " commit_msg
            git add .
            git commit -m "${commit_msg:-Update configurations}"
            git push origin main 2>/dev/null || print_warning "Push failed. Set up remote with: git remote add origin <url>"
            print_success "Changes pushed to repository"
        fi
    else
        print_success "No changes to push"
    fi
}

# DIFF: Show differences
sync_diff() {
    print_header "Configuration Differences"

    echo "Installed vs Available:"
    echo ""

    # Compare agents
    echo "AGENTS:"
    installed_agents=$(get_installed "agents")
    repo_agents=$(cd "$CLODE_DIR/project-templates/obsidian-vault/agents" && ls *.md 2>/dev/null | sed 's/.md$//' || echo "")

    for agent in $repo_agents; do
        if echo "$installed_agents" | grep -q "$agent"; then
            echo "  ✓ $agent (installed)"
        else
            echo "  - $agent (not installed)"
        fi
    done

    echo ""
    echo "COMMANDS:"
    installed_commands=$(get_installed "commands")
    repo_commands=$(cd "$CLODE_DIR/project-templates/obsidian-vault/commands" && ls *.md 2>/dev/null | sed 's/.md$//' || echo "")

    # Show first 10
    count=0
    for cmd in $repo_commands; do
        if [ $count -ge 10 ]; then
            echo "  ... and more (total: $(echo $repo_commands | wc -w))"
            break
        fi

        if echo "$installed_commands" | grep -q "$cmd"; then
            echo "  ✓ /$cmd (installed)"
        else
            echo "  - /$cmd (not installed)"
        fi
        ((count++))
    done
}

# Main menu
case "${1:-help}" in
    pull)
        sync_pull
        ;;
    push)
        sync_push
        ;;
    diff)
        sync_diff
        ;;
    *)
        echo "Clode Sync - Smart Configuration Sync"
        echo ""
        echo "Usage: $0 <command>"
        echo ""
        echo "Commands:"
        echo "  pull    Pull updates from repo and install new items interactively"
        echo "  push    Push local changes to repo"
        echo "  diff    Show what's installed vs available"
        echo ""
        echo "Examples:"
        echo "  $0 pull    # Check for new agents/commands and install selectively"
        echo "  $0 push    # Upload your local customizations to repo"
        echo "  $0 diff    # See what you have vs what's available"
        ;;
esac
