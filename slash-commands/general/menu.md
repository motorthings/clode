Show me the quick reference menu for this Obsidian vault setup.

Display:

## 🤖 AGENTS (Use: "Use the [name] agent to...")

**thinking-partner**
→ Explore ideas WITHOUT writing content
→ Asks questions, helps you think
→ Use when: Brainstorming, exploring ideas

**daily-summarizer**
→ Creates end-of-day progress summaries
→ Reviews today's work and synthesizes insights
→ Use when: Ending a work session

**research-assistant**
→ Finds materials across your entire vault
→ Surfaces forgotten notes and connections
→ Use when: Starting projects, finding related content

**interviewer**
→ Structured interviews to extract your ideas
→ Asks probing questions, documents insights
→ Use when: Clarifying fuzzy ideas, preparing talks

**chat-archiver**
→ Automatically saves conversation transcripts
→ Creates structured markdown with metadata
→ Use when: End of conversation to preserve context

---

## ⚡ SLASH COMMANDS (Type: /command-name)

**/help** - Show this menu
**/menu** - Show this menu (same as /help)
**/think** - Activate thinking-partner agent
**/interview** - Activate interviewer agent
**/find-related** - Activate research-assistant agent
**/summarize-day** - Activate daily-summarizer agent
**/save-chat** - Save current conversation to Chat-History

---

## 🛠️ NPM COMMANDS (Run: npm run command-name)

```bash
npm run think              # Start thinking-partner
npm run interview          # Start interviewer
npm run summarize-day      # Daily summary
npm run find-related       # Research assistant

npm run voice-to-notes <file> [project]   # Import voice transcript
npm run sync-mobile                       # Check for new transcripts
```

---

## 🎯 COMMON WORKFLOWS

**Start Your Day:**
```
/find-related [what you're working on today]
```

**Explore an Idea:**
```
/think
```

**End Your Day:**
```
/summarize-day
```

**Import Voice Chat:**
```bash
npm run voice-to-notes /path/to/transcript.txt "Project Name"
```

**New Project Setup:**
1. Create folder: `mkdir -p "Project"/{chats,research,daily-progress}`
2. Find materials: `/find-related [topic]`
3. Start thinking: `/think`

---

## 📚 DOCUMENTATION

- `GETTING-STARTED.md` - Quick start guide
- `.claude/README.md` - Complete reference
- `.claude/MOBILE-SETUP.md` - Mobile access options
- `.claude/HOME-SERVER-SETUP.md` - Home server guide
- `.claude/agents/README.md` - Agent details

---

## 💡 PRO TIPS

**Always set thinking mode:**
"I'm in THINKING mode - do NOT write content, only help me think"

**Use front matter in notes:**
```yaml
---
mode: thinking
instruction: Do not create drafts
---
```

**Daily summaries are key:**
Run `/summarize-day` at end of each session

---

Type `/help` or `/menu` anytime to see this reference.
