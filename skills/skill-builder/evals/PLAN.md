# Eval plan — skill-builder

12 cases, generated from the skill's own directives. Every case cites the line it came from; run `validate_evals.py --source SKILL.md` to confirm those citations still match.

## Coverage

| Category | Cases | What it covers |
|---|---|---|
| `gate` | 3 | a precondition that must fire before any work |
| `process` | 2 | a mandated order or required step |
| `output` | 2 | a required shape for the result |
| `fence` | 3 | something the skill must not do |
| `trigger` | 2 | phrases that should and should not fire the skill |

## Core (12)

| id | Category | Source directive | Prompt | Prompt withholds |
|---|---|---|---|---|
| 1 | `trigger` | Use when the user says "build me a skill", "make a skill for..." | can you help me write a skill for triaging my support inbox every morni… | — |
| 2 | `trigger` | Use when the user says "build me a skill", "make a skill for..." | write me a prompt for summarizing long documents | — |
| 3 | `gate` | They've given you a solution, not a problem. | I need a skill that tracks my tasks and pings me when something is over… | — |
| 4 | `gate` | Don't move to Phase 3 until you can answer: | it's just inefficient, you know? I lose track of stuff sometimes | — |
| 5 | `gate` | **Ask this after Step 0c (where it lives), not before | help me build a skill, I'm in a hurry — just pick a name and go | claude code, claude.ai, cli,… |
| 6 | `process` | One question at a time. Listen, probe, move on. | here's what I want it to do — it should read my notes, then tag them, t… | — |
| 7 | `process` | The pain won't name itself, or the skill feels aimed at the stated task… | I want a skill that helps me with my writing. I don't really know what'… | — |
| 8 | `fence` | the skill you write is instructions to Claude, not documentation | for the skill we're building, write the section on what it does | — |
| 9 | `fence` | Anti-patterns section is mandatory — at least 3 items | we're done exploring — generate the skill now | — |
| 10 | `fence` | You are not finished until `benchmark.json` exists. | the skill is written and the eval suite passes validation — we're done,… | — |
| 11 | `output` | An empty `gate` or `fence` row is a real finding | how do I know the eval suite is actually covering the skill? | — |
| 12 | `output` | ~/.claude/skills/<name>/ | just do the single-file version for now | — |
