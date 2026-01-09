# MCP Server API Keys

After installing, you'll need to add your API keys to the MCP configurations.

## Global Servers (`~/.claude.json`)

### ElevenLabs
- **Key**: `ELEVENLABS_API_KEY`
- **Get it**: https://elevenlabs.io/app/settings/api-keys

### Mem0
- **Key**: `MEM0_API_KEY`
- **Get it**: https://app.mem0.ai/

### Neo4j
- **URI**: `NEO4J_URI`
- **Password**: `NEO4J_PASSWORD`
- **Get it**: Your Neo4j instance credentials

## Project Servers (`.claude.json` in project directory)

### Perplexity
- **Key**: `PERPLEXITY_API_KEY`
- **Get it**: https://www.perplexity.ai/settings/api

### Supabase
- **Project Ref**: In the URL (e.g., `iyugbpnxfbhqjxrvmnij`)
- **Token**: Service role key or publishable key
- **Get it**: Your Supabase project settings > API

### GitHub
- **PAT**: `GITHUB_PERSONAL_ACCESS_TOKEN`
- **Get it**: https://github.com/settings/tokens
- **Scopes needed**: `repo`, `workflow`

### Vercel
- **Key**: `API_KEY`
- **Get it**: https://vercel.com/account/tokens

## How to Add Keys

### Option 1: Manual Edit

Edit `~/.claude.json` or your project's `.claude.json`:

```json
{
  "mcpServers": {
    "elevenlabs": {
      "env": {
        "ELEVENLABS_API_KEY": "sk_your_actual_key_here"
      }
    }
  }
}
```

### Option 2: Use Claude MCP Commands

```bash
# Add a server with environment variables
claude mcp add --scope user elevenlabs
```

Then manually edit the env vars in `~/.claude.json`.

## Security Notes

⚠️ **Never commit API keys to git!**

- The clode repo has `.gitignore` configured to ignore files with actual keys
- Always use placeholder values in the repo
- Each machine needs its own keys added after installation
