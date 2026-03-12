# Update Help Documentation

Update the in-app help documentation and reindex for the help search function. Help docs are RAG-indexed for the Manual agent's help chat.

**This command always reindexes embeddings after updating docs.**

## Usage

```
/update-help-docs              # Update help docs and reindex embeddings
```

## Help Docs Structure

Help docs live in two places (kept in sync):
- **Local dev**: `docs/help/` (source of truth)
- **Railway**: `backend/docs_help/` (deployed copy)

```
docs/help/
├── user/           # End-user documentation
│   ├── 00-quick-start.md
│   ├── 01-agents.md
│   ├── 02-chat.md
│   ├── 03-meeting-rooms.md
│   ├── 04-knowledge-base.md
│   ├── 05-tasks.md
│   ├── 06-projects.md
│   ├── 07-stakeholders.md
│   ├── 08-faq.md
│   ├── 09-disco-initiatives.md
│   └── 10-discovery-inbox.md
├── admin/          # Admin documentation
│   ├── 00-getting-started.md
│   ├── 01-agents.md
│   ├── 02-users.md
│   ├── 03-document-management.md
│   ├── 04-help-system.md
│   └── 05-troubleshooting.md
├── INDEX_HELP_DOCS.md
└── README.md
```

## Instructions

### Step 1: Review Recent Changes

Check what features need documentation:

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis
git log --oneline --since="7 days ago" | head -20
```

Identify user-facing features that need help documentation.

### Step 2: Read Existing Help Docs

For each area being updated, read the current help doc:

```bash
# Example: Knowledge Base help
cat docs/help/user/04-knowledge-base.md
```

### Step 3: Update Help Documentation

Edit the appropriate help doc files. Follow these guidelines:

**Format:**
- Use markdown with clear headings (##, ###)
- Include step-by-step instructions
- Add screenshots references where helpful (format: `![Description](image-path)`)
- Keep language simple and direct

**Structure per topic:**
```markdown
## Feature Name

Brief description of what it does and why you'd use it.

### How to [Action]

1. Step one
2. Step two
3. Step three

### Tips

- Helpful tip 1
- Helpful tip 2

### Troubleshooting

**Problem:** Description
**Solution:** How to fix it
```

### Step 4: Sync to backend/docs_help

After updating `docs/help/`, sync to the backend copy:

```bash
# Sync docs to backend for Railway deployment
rsync -av --delete docs/help/ backend/docs_help/
```

### Step 5: Reindex Help Embeddings

Reindex the help documentation in the database:

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
DOTENV_PRIVATE_KEY=4980b243281755774eab2a5107d475ceecdeceb0b7aef97e014d9cfcece1c230 \
dotenvx run -f .env -- .venv/bin/python scripts/index_help_docs.py --force
```

This will:
1. Delete all existing help_chunks
2. Re-process all markdown files
3. Generate fresh embeddings with Voyage AI
4. Store in help_documents and help_chunks tables

### Step 6: Verify and Commit

```bash
# Check what changed
git status
git diff docs/help/

# Commit help doc updates
git add docs/help/ backend/docs_help/
git commit -m "docs: update help documentation

- [List specific updates]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# Push to deploy
git push origin main
```

## Help Doc Topics by File

| File | Topics Covered |
|------|----------------|
| `00-quick-start.md` | First-time setup, basic navigation |
| `01-agents.md` | Agent roster, @mentions, agent selection |
| `02-chat.md` | Chat interface, conversation management |
| `03-meeting-rooms.md` | Multi-agent meetings, autonomous mode |
| `04-knowledge-base.md` | Document upload, Obsidian sync, search |
| `05-tasks.md` | Kanban board, task management |
| `06-projects.md` | Project pipeline, triage scoring |
| `07-stakeholders.md` | Stakeholder tracking, engagement |
| `08-faq.md` | Common questions and answers |
| `09-disco-initiatives.md` | DISCo product discovery workflow |
| `10-discovery-inbox.md` | Unified inbox for candidates |

## When to Update Each File

| Change Type | Update File |
|-------------|-------------|
| New agent added | `01-agents.md` |
| Chat feature change | `02-chat.md` |
| KB/sync changes | `04-knowledge-base.md` |
| Task workflow change | `05-tasks.md` |
| New FAQ needed | `08-faq.md` |
| DISCo workflow change | `09-disco-initiatives.md` |

## Embedding Info

- **Model**: Voyage AI `voyage-3` (1024 dimensions)
- **Chunk size**: 1000 chars with 200 char overlap
- **Context**: Title + heading prepended for better semantic search
- **Tables**: `help_documents` (full docs), `help_chunks` (embeddings)
