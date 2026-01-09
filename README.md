# Clode - Claude Code Configuration Sync

Sync your Claude Code customizations across multiple machines.

## What's Included

### Global Configurations
- **Settings** - Global Claude Code settings and preferences
- **Commands** - Global slash commands available in all projects
- **Hooks** - Custom hooks for workflow automation
- **Plugins** - Plugin configurations

### Project Templates
- **Obsidian Vault** - Custom agents, commands, and skills for Obsidian projects
  - 6 custom agents (thinking-partner, daily-summarizer, interviewer, etc.)
  - 33 custom slash commands (including danger mode!)
  - Custom skills

### MCP Server Configurations
- Global MCP servers (elevenlabs, mem0, n8n, neo4j, cloner-mcp)
- Project-specific servers (perplexity, railway, supabase, github, vercel)

## Installation

### First Time Setup (New Machine)

```bash
# Clone the repo
git clone https://github.com/motorthings/clode.git
cd clode

# Run installation script
./scripts/install.sh
```

This will:
- Copy global settings to `~/.claude/`
- Set up MCP server configurations
- Create project template directories

### Syncing Updates

```bash
# Pull latest changes from GitHub
git pull

# Sync configurations to your machine
./scripts/sync.sh pull
```

## Updating Configurations

When you make changes on one machine:

```bash
# From the clode directory
./scripts/sync.sh push

# Commit and push to GitHub
git add .
git commit -m "Update configurations"
git push
```

## Project-Specific Setup

To use the Obsidian vault template in a new project:

```bash
# In your project directory
cp -r /path/to/clode/project-templates/obsidian-vault/.claude .
```

Or use the sync script:

```bash
./scripts/sync.sh apply-template /path/to/your/project
```

## Customizations Included

### Custom Agents
- **thinking-partner** (`/think`) - Brainstorming without writing
- **daily-summarizer** (`/summarize-day`) - End-of-day summaries
- **interviewer** (`/interview`) - Structured interviews
- **research-assistant** (`/find-related`) - Find related materials
- **chat-archiver** - Archive conversations

### Notable Slash Commands
- **/danger** - Danger mode with bypass permissions
- **/repo** - Repository-specific commands
- **/obsidian** - Obsidian vault operations
- **/elevenlabs** - Text-to-speech and voice operations
- Many more workflow automation commands

### MCP Servers
- **ElevenLabs** - Voice and audio processing
- **Mem0** - Long-term memory across sessions
- **n8n** - Workflow automation
- **Neo4j** - Graph database operations
- **Perplexity** - Real-time web research
- **Railway** - Deployment management
- **Supabase** - Database operations
- **GitHub** - Repository management
- **Vercel** - Deployment and hosting

## Security Notes

⚠️ **API Keys and Secrets**

The sync scripts automatically filter out sensitive data:
- API keys are stored as placeholders
- You'll need to manually add your keys after installation
- Check `mcp-configs/SECRETS.md` for required keys

## File Structure

```
clode/
├── README.md
├── global/
│   ├── settings.json
│   ├── commands/
│   ├── hooks/
│   └── plugins/
├── project-templates/
│   └── obsidian-vault/
│       ├── agents/
│       ├── commands/
│       ├── skills/
│       └── settings.local.json
├── mcp-configs/
│   ├── global-servers.json
│   ├── project-servers.json
│   └── SECRETS.md
└── scripts/
    ├── install.sh
    ├── sync.sh
    └── README.md
```

## Contributing

This is a personal configuration repo, but feel free to fork and adapt for your own use!

## License

MIT
