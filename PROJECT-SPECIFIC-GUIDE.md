# Project-Specific Claude Code Configuration Guide

This guide explains how to manage Claude Code configurations within individual project repositories.

## Why Project-Specific Configs?

Project-specific `.claude/` directories should be **committed to each project's repo** because:

1. **Team Collaboration** - Share project-specific agents and commands with teammates
2. **Consistent Workflows** - Same commands work for everyone on the project
3. **Project Context** - Agents that understand your specific codebase
4. **Reproducibility** - New team members get the same setup

## What Goes in Project `.claude/` Directories?

### ✅ Should Be Committed

```
project-repo/
├── .claude/
│   ├── agents/              # Project-specific agents
│   │   └── api-expert.md    # Knows your API architecture
│   ├── commands/            # Project commands
│   │   ├── deploy.md        # Deployment workflow
│   │   ├── test-suite.md    # Run project tests
│   │   └── db-migrate.md    # Database operations
│   ├── skills/              # Project skills
│   │   └── code-reviewer.md # Review code for this project
│   └── settings.local.json  # Project settings (sanitized)
```

### ❌ Should NOT Be Committed

```
.claude/
├── .mcp.json               # Contains API keys! Add to .gitignore
└── settings.local.json     # If it has secrets, sanitize first
```

## Setting Up Project Configs

### 1. Initialize Project Claude Config

```bash
cd your-project
mkdir -p .claude/{agents,commands,skills}
```

### 2. Create Project-Specific Agent

Example: `.claude/agents/deployment-expert.md`

```markdown
---
model: sonnet
allowed-tools:
  - Bash(npm run *)
  - Bash(git *)
  - mcp__railway__*
  - mcp__vercel__*
---

# Deployment Expert

You are an expert in deploying this specific application. You know:

- Build command: `npm run build`
- Deploy targets: Railway (backend) and Vercel (frontend)
- Required env vars: DATABASE_URL, API_KEY, FRONTEND_URL

Always verify tests pass before deploying.
```

### 3. Create Project Commands

Example: `.claude/commands/deploy.md`

```markdown
---
user-invocable: true
agent: deployment-expert
---

# /deploy

Deploy the application to production.

Steps:
1. Run tests (`npm test`)
2. Build frontend and backend
3. Deploy backend to Railway
4. Deploy frontend to Vercel
5. Verify deployment health
```

### 4. Add to `.gitignore`

```bash
echo ".claude/.mcp.json" >> .gitignore
echo ".claude/settings.local.json" >> .gitignore  # If it has secrets
```

### 5. Create Template Settings

Create `.claude/settings.local.template.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npm test *)",
      "mcp__railway__*"
    ]
  },
  "mcpServers": {
    "railway": {
      "type": "stdio",
      "command": "npx",
      "args": ["@railway/mcp-server"],
      "env": {}
    }
  }
}
```

Then in README:

```markdown
## Setup

1. Copy `.claude/settings.local.template.json` to `.claude/settings.local.json`
2. Add your Railway token (see Railway dashboard)
```

## Using Clode with Projects

### Pull Project-Relevant Agents from Clode

```bash
# In your project directory
cd ~/your-project

# Pull specific agent from clode
cp ~/Documents/GitHub/clode/project-templates/obsidian-vault/agents/daily-summarizer.md .claude/agents/

# Or use sync script with filter
~/Documents/GitHub/clode/scripts/sync.sh pull --project-only
```

### Push Project Agents to Clode

If you create a great agent in a project that could be useful elsewhere:

```bash
# Copy to clode repo
cp .claude/agents/awesome-agent.md ~/Documents/GitHub/clode/project-templates/obsidian-vault/agents/

# Then push to clode
cd ~/Documents/GitHub/clode
./scripts/sync.sh push
```

## Example Project Setups

### Full-Stack Web App

```
.claude/
├── agents/
│   ├── frontend-expert.md    # React/Next.js specialist
│   ├── backend-expert.md     # API specialist
│   └── db-expert.md          # Database operations
├── commands/
│   ├── dev.md               # Start dev servers
│   ├── test.md              # Run test suite
│   ├── deploy-staging.md    # Deploy to staging
│   └── deploy-prod.md       # Deploy to production
└── settings.local.json      # Project permissions
```

### Data Science Project

```
.claude/
├── agents/
│   ├── data-analyst.md      # Data exploration
│   └── model-trainer.md     # ML training
├── commands/
│   ├── analyze.md          # Run analysis pipeline
│   ├── train.md            # Train models
│   └── evaluate.md         # Evaluate results
└── skills/
    └── notebook-helper.md  # Jupyter notebook assistance
```

## Best Practices

### 1. Document in README

Add to your project README:

```markdown
## Claude Code Setup

This project has custom Claude Code configurations in `.claude/`:

- `/deploy` - Deploy to production
- `/test-suite` - Run all tests
- Agent: `@api-expert` - API development help

Setup: `cp .claude/settings.local.template.json .claude/settings.local.json`
```

### 2. Version Control

```bash
# Commit project configs
git add .claude/agents .claude/commands .claude/skills
git add .claude/settings.local.template.json
git commit -m "Add Claude Code project configuration"

# Ensure secrets are ignored
git add .gitignore
git commit -m "Ignore Claude Code secrets"
```

### 3. Team Onboarding

Create `.claude/README.md` in your project:

```markdown
# Claude Code Configuration

## Available Commands

- `/deploy` - Deploy the app
- `/test-suite` - Run tests
- `/db-migrate` - Run migrations

## Available Agents

- `@api-expert` - Help with API development
- `@frontend-expert` - Help with React/UI

## Setup

1. Install Claude Code globally
2. Copy settings template: `cp settings.local.template.json settings.local.json`
3. Add API keys (see main README)
```

## Syncing Between Machines

### Machine 1 (with changes)

```bash
cd ~/your-project
git add .claude/
git commit -m "Update Claude Code configs"
git push
```

### Machine 2 (pulling changes)

```bash
cd ~/your-project
git pull
# New commands and agents are now available!
```

### Using Clode for Shared Configs

```bash
# Machine 1: Push general-purpose agent to clode
cp .claude/agents/general-helper.md ~/clode/project-templates/obsidian-vault/agents/
cd ~/clode
git add . && git commit -m "Add general helper agent" && git push

# Machine 2: Pull from clode
cd ~/clode
git pull
./scripts/sync.sh pull  # Selectively install new agent
```

## Migration Guide

### Moving Existing Configs to Project

If you have global configs that should be project-specific:

```bash
# Copy from global to project
cp ~/.claude/commands/project-specific-cmd.md .claude/commands/

# Remove from global
rm ~/.claude/commands/project-specific-cmd.md

# Commit to project repo
git add .claude/commands/
git commit -m "Move project-specific command to repo"
```

### Creating Template from Existing Project

```bash
# Your project has great configs
cd ~/your-project

# Copy to clode as templates
cp .claude/agents/awesome-agent.md ~/clode/project-templates/obsidian-vault/agents/

# Share with other projects
cd ~/clode
git add . && git commit -m "Add awesome agent template" && git push
```

## Summary

- **Global configs** → `~/.claude/` and synced via **clode repo**
- **Project configs** → `.claude/` in **each project repo**
- **Secrets** → `.gitignore` and use templates
- **Team sharing** → Commit `.claude/` directories (except secrets)
- **Cross-machine** → Git for projects, clode for global

This gives you the best of both worlds: shared team configurations in projects, and personal tools synced across your machines!
