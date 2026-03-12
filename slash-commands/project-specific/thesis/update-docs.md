# Update Project Documentation

Update project documentation based on recent code changes. Reviews recent commits and ensures documentation reflects the current state of the codebase.

**This command operates on the current git repository.** It detects the repo root automatically.

## Usage

```
/update-docs           # Update docs based on recent changes
/update-docs --full    # Full documentation audit
```

## Instructions

### Step 0: Detect Current Repository

Determine the git repository root and identify the project:

```bash
git rev-parse --show-toplevel
```

Use this as the working directory for all subsequent steps. The repo name determines which documentation files to look for. Do NOT hardcode paths to any specific repo.

### Step 1: Review Recent Changes

Get commits from the last 7 days:

```bash
git log --oneline --since="7 days ago" | head -30
```

For each significant commit, note:
- Feature additions
- API changes
- New capabilities
- Configuration changes
- Database schema changes

### Step 2: Identify Documentation to Update

Look for documentation files in the current repo. Common locations:

| Pattern | Purpose | Update When |
|---------|---------|-------------|
| `docs/ARCHITECTURE.md` | Architecture reference | New features, agents, or schema changes |
| `docs/*RELEASE_NOTES*.md` | Release notes (monthly or per-version) | Any user-facing changes |
| `docs/deployment/*` | Deployment instructions | Infrastructure changes |
| `README.md` | Project overview | Major capability changes |
| `docs/*.md` | Any other docs | When relevant content changes |

Find what exists:

```bash
find docs/ -name "*.md" -maxdepth 2 2>/dev/null
ls README.md CHANGELOG.md 2>/dev/null
```

### Step 3: Read Current Documentation

Read each documentation file that likely needs updates based on the recent commits.

### Step 4: Make Updates

For each documentation file:

1. **Identify gaps** - What's missing or outdated?
2. **Draft updates** - Write clear, concise additions
3. **Preserve structure** - Match existing formatting
4. **Add to appropriate section** - Don't create new sections unless necessary

### Step 5: Update Release Notes

If release notes exist, add entries for user-facing changes:

```markdown
### [Date] - [Category]

- **[Feature/Fix Name]**: Brief description of what changed and why it matters to users
```

Categories: Features, Fixes, Improvements, Infrastructure

### Step 6: Verify and Commit

After making updates:

```bash
# Check what changed
git diff docs/

# Commit documentation updates
git add docs/
git commit -m "docs: update documentation for recent changes

- [List specific doc updates]

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

## Documentation Standards

### Writing Style
- Use present tense ("The system classifies..." not "The system will classify...")
- Be concise - bullet points over paragraphs
- Include code examples where helpful
- Link to related documentation

### Release Notes Format
```markdown
### January 29, 2026 - Knowledge Base

- **Document Auto-Classification**: Documents synced from Obsidian are now automatically classified by type (transcript, notes, report, etc.) enabling smarter search filtering
```

## Do NOT Update

- `CLAUDE.md` - Managed separately
- `docs/archive/*` - Historical reference only
- `docs/help/*` - Use `/update-help-docs` instead
