# Clode Setup Guide - Complete Walkthrough

This is your step-by-step guide to setting up Claude Code customizations on a new machine using the clode repository.

## 📋 Prerequisites

Before starting, make sure you have:

- [ ] **Claude Code installed** - Install from https://claude.ai/download or via:
  ```bash
  npm install -g claude-code
  # OR
  brew install claude-code
  ```

- [ ] **Git installed**
  ```bash
  git --version  # Should show version number
  ```

- [ ] **GitHub authentication** configured
  ```bash
  gh auth status  # Should show "Logged in"
  # If not: gh auth login
  ```

- [ ] **Node.js and npm** (for MCP servers)
  ```bash
  node --version  # Should be v18 or higher
  npm --version
  ```

- [ ] **Python 3** (for hooks and some MCP servers)
  ```bash
  python3 --version  # Should be 3.8 or higher
  ```

- [ ] **uv** (for Python MCP servers like elevenlabs)
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

## 🚀 Step 1: Clone the Repository

Open Terminal and run:

```bash
# Create GitHub directory if it doesn't exist
mkdir -p ~/Documents/GitHub

# Navigate there
cd ~/Documents/GitHub

# Clone clode
git clone https://github.com/motorthings/clode.git

# Enter the directory
cd clode

# Verify files are there
ls -la
```

You should see:
- `README.md`
- `SETUP-GUIDE.md` (this file!)
- `global/` directory
- `project-templates/` directory
- `mcp-configs/` directory
- `scripts/` directory

## 🛠️ Step 2: Run Interactive Installation

The install script will guide you through selecting what to install:

```bash
# Make sure scripts are executable
chmod +x scripts/*.sh

# Run installation
./scripts/install.sh
```

### What the Installer Will Ask You

#### 2.1 Global Settings
```
Install global settings (permissions, hooks config)? (y/n):
```
- **Recommended: y**
- This sets up bypass permissions mode and hook configurations

#### 2.2 Global Commands
For each global command (like `gigawatt`):
```
Install command: gigawatt.md? (y/n):
```
- **gigawatt** - Advanced prompt engineering agent
- Press `y` if you want it, `n` to skip

#### 2.3 Global Hooks
For each hook:
```
Install hook: precompact-context-preserver.py? (y/n):
```
Hooks available:
- **precompact-context-preserver.py** - Saves context before compaction
- **sessionstart-context-injector.py** - Injects context at session start
- **userpromptsubmit-context-injector.py** - Injects context when you submit prompts

**Recommended: Install all hooks** - They work together to preserve important context

#### 2.4 Custom Agents
For each of 6 agents:
```
Agent: thinking-partner - Helps think without writing
Install this agent? (y/n): y

Where should this agent be installed?
  1) Globally (~/.claude/agents)
  2) Current project only
Choice (1/2): 1
```

**Available Agents:**
1. **thinking-partner** (`/think`) - Brainstorming and ideation
2. **daily-summarizer** (`/summarize-day`) - End-of-day summaries
3. **interviewer** (`/interview`) - Structured interviews to extract ideas
4. **research-assistant** (`/find-related`) - Find related content in your vault
5. **chat-archiver** - Archive conversation transcripts

**Recommendation:**
- Install **thinking-partner**, **daily-summarizer**, **interviewer** globally
- Skip the others unless you need them (you can add them later)

#### 2.5 Project Commands
```
Found 33 custom commands available
Review and install project commands individually? (y/n):
```

**Options:**
- `y` - Review each command one by one (takes time but you see everything)
- `n` - Then it asks if you want to install ALL commands

**Key Commands to Consider:**

Must-have (say yes):
- **/danger** - Bypass permissions mode
- **/help** - Custom help menu
- **/think** - Quick thinking mode
- **/summarize-day** - Daily summaries

Useful if you work with Obsidian:
- **/obsidian** - Vault operations
- **/process-meeting** - Process meeting notes
- **/transcribe** - Audio transcription

Useful for development:
- **/repo** - Repository operations
- **/elevenlabs** - Voice/audio tools

**Recommendation:**
- Say `n` to individual review
- Say `n` to install ALL
- Come back later with `./scripts/sync.sh pull` to selectively add commands you want

#### 2.6 Custom Skills
```
Install skill: folder-organization-skill? (y/n):
```

**Recommendation:** Say `y` if you work with Obsidian vaults, otherwise `n`

## 🔑 Step 3: Add API Keys

The installation created template configs with placeholders. Now add your real API keys.

### 3.1 Locate Your Config Files

Global MCP servers are in:
```bash
# View your global config
cat ~/.claude.json
```

### 3.2 Add Each API Key

Open the config file:
```bash
nano ~/.claude.json
```

You'll see entries like:
```json
{
  "mcpServers": {
    "elevenlabs": {
      "env": {
        "ELEVENLABS_API_KEY": "YOUR_ELEVENLABS_API_KEY_HERE"
      }
    }
  }
}
```

Replace `YOUR_ELEVENLABS_API_KEY_HERE` with your actual key.

### 3.3 Where to Get API Keys

#### ElevenLabs
1. Go to https://elevenlabs.io/app/settings/api-keys
2. Create new API key
3. Copy and paste into `ELEVENLABS_API_KEY`

#### Mem0
1. Go to https://app.mem0.ai/
2. Navigate to Settings → API Keys
3. Create new key
4. Copy and paste into `MEM0_API_KEY`

#### Perplexity
1. Go to https://www.perplexity.ai/settings/api
2. Generate new API key
3. Copy and paste into `PERPLEXITY_API_KEY`

#### GitHub
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`
4. Generate token
5. Copy and paste into `GITHUB_PERSONAL_ACCESS_TOKEN`

#### Supabase
1. Go to your Supabase project dashboard
2. Settings → API
3. Copy **Project URL** and **Service Role Key**
4. Update the URL and token in config

#### Vercel
1. Go to https://vercel.com/account/tokens
2. Create new token
3. Copy and paste into `API_KEY`

#### Neo4j (if you have an instance)
1. Your Neo4j connection string (e.g., `neo4j+s://xxxxx.databases.neo4j.io`)
2. Your database password
3. Add to `NEO4J_URI` and `NEO4J_PASSWORD`

### 3.4 Save the Config

In nano:
- Press `Ctrl+X` to exit
- Press `Y` to save
- Press `Enter` to confirm filename

### 3.5 Verify MCP Servers

```bash
claude mcp list
```

You should see:
- ✓ Connected servers (green checkmarks)
- ⚠ Pending servers (need API keys)

If a server shows "✗ Failed", double-check the API key.

## ✅ Step 4: Test Your Installation

### 4.1 Start Claude Code

```bash
claude
```

### 4.2 Test Global Settings

Try danger mode (bypass permissions):
```bash
# In Claude, press Shift+Tab and select "danger" mode
# Or type:
/danger
```

### 4.3 Test Custom Agents

```bash
# In Claude:
/think

# Or @mention the agent:
@thinking-partner help me brainstorm
```

### 4.4 Test Custom Commands

```bash
# Try the help command:
/help

# Try thinking mode:
/think
```

### 4.5 Test MCP Servers

```bash
# In Claude:
Search the web for Claude Code documentation

# Try Mem0:
Remember that I prefer concise summaries
```

If everything works, you're all set! 🎉

## 📱 Step 5: Set Up Your Machine Config

The installer created `~/.clode-config.json` to track what's installed on this machine.

View it:
```bash
cat ~/.clode-config.json | python3 -m json.tool
```

This file tracks:
- Machine name
- Installation date
- Which agents are installed
- Which commands are installed
- Which MCP servers are configured

**Don't edit this manually** - it's updated by the sync scripts.

## 🔄 Step 6: Daily Usage Workflows

### Checking for Updates from Other Machine

When you've added something on Machine 1:

```bash
# On Machine 2
cd ~/Documents/GitHub/clode
./scripts/sync.sh pull
```

This will:
1. Pull latest from GitHub
2. Show you NEW items
3. Let you selectively install them

### Pushing Local Changes

Created a great new agent on this machine?

```bash
cd ~/Documents/GitHub/clode
./scripts/sync.sh push
```

This will:
1. Detect new local items
2. Ask if you want to add them to the repo
3. Help you commit and push

### Seeing What's Available

```bash
cd ~/Documents/GitHub/clode
./scripts/sync.sh diff
```

Shows:
- ✓ Items you have
- - Items available but not installed

## 🎯 Step 7: Optional - Project-Specific Setup

If you're working on a project that should have its own Claude Code configs:

### 7.1 Initialize Project Config

```bash
cd ~/your-project
mkdir -p .claude/{agents,commands,skills}
```

### 7.2 Copy Template Settings

```bash
# Copy project template
cp ~/Documents/GitHub/clode/project-templates/obsidian-vault/settings.local.json .claude/
```

### 7.3 Add Project-Specific Items

For example, a project-specific agent:

```bash
nano .claude/agents/deployment-expert.md
```

See `PROJECT-SPECIFIC-GUIDE.md` for full details.

## 🔧 Step 8: Customization Tips

### Adding Your Own Agent

```bash
# Create new agent globally
nano ~/.claude/agents/my-agent.md

# Or in current project
mkdir -p .claude/agents
nano .claude/agents/my-agent.md
```

Agent template:
```markdown
---
model: sonnet
allowed-tools:
  - Bash(*)
  - Read(*)
---

# My Custom Agent

You are an expert in [your domain].

Your responsibilities:
- [Task 1]
- [Task 2]
```

### Adding Your Own Command

```bash
# Create new command
nano ~/.claude/commands/my-command.md
```

Command template:
```markdown
---
user-invocable: true
---

# /my-command

[Description of what this command does]

[Instructions for Claude]
```

### Push to Clode Repo

```bash
cd ~/Documents/GitHub/clode
./scripts/sync.sh push
```

## 🆘 Troubleshooting

### Issue: Scripts Won't Run

**Problem:** `Permission denied` when running scripts

**Solution:**
```bash
chmod +x ~/Documents/GitHub/clode/scripts/*.sh
```

### Issue: MCP Server Failed to Connect

**Problem:** Server shows "✗ Failed" in `claude mcp list`

**Solution:**
1. Check API key is correct
2. Check API key has no extra spaces
3. Test the API key directly:
```bash
# For ElevenLabs example:
curl https://api.elevenlabs.io/v1/models \
  -H "xi-api-key: YOUR_KEY_HERE"
```

### Issue: Command Not Found

**Problem:** `/my-command` not recognized

**Solution:**
1. Check the file exists:
```bash
ls ~/.claude/commands/my-command.md
# or
ls .claude/commands/my-command.md
```

2. Restart Claude Code:
```bash
exit  # Exit Claude
claude  # Start again
```

### Issue: Agent Not Available

**Problem:** `@my-agent` not found

**Solution:**
1. Check agent file exists:
```bash
ls ~/.claude/agents/my-agent.md
```

2. Check frontmatter has no syntax errors
3. Restart Claude Code

### Issue: Git Push Failed

**Problem:** `git push` fails with "remote not configured"

**Solution:**
```bash
cd ~/Documents/GitHub/clode
git remote add origin https://github.com/motorthings/clode.git
git push -u origin main
```

### Issue: Lost Track of What's Installed

**Problem:** Don't remember what's on this machine

**Solution:**
```bash
# See machine config
cat ~/.clode-config.json | python3 -m json.tool

# Or use sync diff
cd ~/Documents/GitHub/clode
./scripts/sync.sh diff
```

### Issue: Want to Start Over

**Problem:** Installation got messy, want fresh start

**Solution:**
```bash
# Back up current config
cp ~/.claude.json ~/.claude.json.backup

# Remove machine config
rm ~/.clode-config.json

# Re-run installation
cd ~/Documents/GitHub/clode
./scripts/install.sh
```

## 📚 Next Steps

After setup, explore:

1. **Read the docs:**
   - `README.md` - Complete overview
   - `PROJECT-SPECIFIC-GUIDE.md` - Project configs
   - `QUICK-START.md` - Quick reference

2. **Try your commands:**
   - `/help` - See all commands
   - `/think` - Thinking mode
   - `/danger` - Bypass permissions

3. **Customize:**
   - Create your own agents
   - Add your own commands
   - Push to repo to share with other machine

4. **Set up projects:**
   - Add `.claude/` directories to your repos
   - Share with team members
   - Use clode for personal customizations

## 🎓 Learning Resources

- **Claude Code Docs:** https://code.claude.com/docs
- **MCP Documentation:** https://modelcontextprotocol.io/
- **Your Clode Repo:** https://github.com/motorthings/clode

## ✅ Verification Checklist

After setup, verify:

- [ ] Claude Code starts: `claude`
- [ ] Custom commands work: `/help`, `/think`
- [ ] Custom agents available: `@thinking-partner`
- [ ] MCP servers connected: `claude mcp list` shows ✓
- [ ] Sync works: `cd ~/Documents/GitHub/clode && ./scripts/sync.sh diff`
- [ ] Machine config exists: `cat ~/.clode-config.json`
- [ ] Can create new items and push: `./scripts/sync.sh push`

## 🎉 You're All Set!

Your Claude Code setup is now:
- ✅ Synced across machines via GitHub
- ✅ Customized with your agents and commands
- ✅ Configured with selective installation
- ✅ Ready to evolve as you add more customizations

Happy coding with Claude! 🚀

---

**Quick Reference Commands:**

```bash
# Check for updates from other machine
cd ~/Documents/GitHub/clode && ./scripts/sync.sh pull

# Push local changes to repo
cd ~/Documents/GitHub/clode && ./scripts/sync.sh push

# See what's installed vs available
cd ~/Documents/GitHub/clode && ./scripts/sync.sh diff

# List MCP servers
claude mcp list

# Start Claude Code
claude
```
