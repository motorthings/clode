---
name: glean-docs
description: Use when the user asks about Glean platform capabilities, how to build something in Glean, what Glean supports, Glean API endpoints, Glean SDK usage, agent builder features, Glean actions, triggers, workflow steps, or any question about what Glean can or cannot do. Also use when building or designing a Glean agent and you need to verify current platform behavior.
---

# Glean Documentation Lookup

Query Glean's official developer docs via Context7 MCP to answer questions about the platform with current, sourced information.

## Context7 Libraries

| Topic | Library ID |
|-------|-----------|
| Platform, agent builder, workflows, triggers, actions, tools, API concepts, guides | `/websites/developers_glean` |
| Python SDK, Python code examples | `/gleanwork/api-client-python` |
| TypeScript SDK, TS code examples | `/gleanwork/api-client-typescript` |

Default to `/websites/developers_glean`. Only use SDK libraries when the question is specifically about writing code in that language. Query multiple libraries if the question spans platform + code.

## Process

1. Parse the question. Strip filler -- use core technical terms as the query string.
2. Call `mcp__context7__query-docs` with the selected `libraryId` and focused `query`.
3. If results are thin, reformulate with different terms or try a different library.
4. Present the answer: lead with the concrete answer, include source URLs, add code examples if relevant.
5. After answering, check whether the result contradicts or extends anything in Agent Factory knowledge docs at `~/Vault/GitHub/glean-agent-factory-app/backend/engine/knowledge/`. If so, flag it:

```
KNOWLEDGE DOC UPDATE NEEDED
- File: <filename>
- Issue: <what's wrong or missing>
- Source: <URL from Context7 result>
```

If nothing conflicts, say nothing about it.

## When NOT to Use

- Questions about Contentful's specific Glean configuration (connectors, admin settings) -- those are internal, not in public docs
- Questions about Agent Factory code or architecture -- read the codebase directly
- General AI/LLM questions unrelated to Glean platform
