---
name: glean-docs-refresh
description: Use when checking whether Agent Factory knowledge docs are current, when running a weekly Glean documentation freshness check, or when the user asks to compare internal Glean docs against official docs. Also triggers on Monday session starts if more than 7 days since last freshness report.
---

# Glean Docs Freshness Check

Compare Agent Factory knowledge docs against Context7's current Glean developer platform docs. Find gaps, outdated info, and new capabilities.

## Step 1: Read Internal Knowledge Docs

Read key files from `~/Vault/GitHub/glean-agent-factory-app/backend/engine/knowledge/`:

- `glean-json-schema.md`
- `glean-platform-reference-slim.md`
- `glean-actions-catalog.md`
- `glean-external-integrations.md`
- `glean-orchestration-decisions-slim.md`
- `glean-community-patterns-slim.md`
- `feasibility-rules.md`
- `tyler-glean-best-practices.md`

Extract: topics covered, version numbers, API endpoints, step types, action names, config schemas, dates.

## Step 2: Query Context7

Use `mcp__context7__query-docs` with library `/websites/developers_glean` for each topic:

1. "agent builder workflow step types configuration"
2. "available actions tools integrations"
3. "API endpoints agents create update run"
4. "triggers input types form chat message scheduled"
5. "Python SDK client agents" (library: `/gleanwork/api-client-python`)
6. "TypeScript SDK client agents" (library: `/gleanwork/api-client-typescript`)
7. "new features changelog updates"
8. "workflow JSON schema configuration format"

## Step 3: Cross-Reference

Classify findings into four categories:

- **New in Glean** -- capabilities in Context7 not in our docs. Name the feature, cite the snippet.
- **Potentially Outdated** -- our docs contradict Context7. Include: our claim (file + text), what Context7 shows, severity (Critical/High/Medium/Low).
- **Confirmed Current** -- alignment. One-liner per topic.
- **Gaps to Investigate** -- Context7 coverage too thin to conclude. Needs manual verification.

## Step 4: Write Report

Save to `~/Vault/GitHub/glean-agent-factory-app/docs/updates/glean-docs-freshness-YYYY-MM-DD.md` using today's date.

Include: summary counts, detailed findings per category, prioritized next steps with specific files to edit.

## Step 5: Surface Critical Findings

If Critical or High severity items found: list them in the response before the report location, suggest specific edits, ask if the user wants fixes applied now.

If nothing critical: confirm report location and summarize key stats.
