# clode — Claude Code Configuration Sync

Sync Claude Code customizations across machines. Not an application — a portable config bundle.

## What's inside
- **Global configurations** — settings, global slash commands, hooks, plugin configs.
- **Project templates** — e.g. the Obsidian Vault template: 6 custom agents (thinking-partner, daily-summarizer, interviewer, …), 33 slash commands, custom skills.
- **MCP server configs** — global (elevenlabs, mem0, n8n, neo4j, cloner-mcp) and project-specific (perplexity, railway, supabase, github, vercel).

## Getting oriented
- `README.md` / `README-work.md` — overviews.
- `QUICK-START.md` — first-time setup on a new machine.
- `SETUP-GUIDE.md` — full setup.
- `PROJECT-SPECIFIC-GUIDE.md` — wiring per-project config.
- `WORK-LAPTOP-TODO.md` — work-machine checklist.
- `commit-history.txt` — provenance.

## Working here
Most work is editing config files (skills/, slash-commands/, global/, mcp-configs/, project-templates/). Verify config changes don't break sync — keep `global/` truly global and per-project overrides under `project-templates/`.

Last significant work (2026-08-13): added the cite-check skill.
