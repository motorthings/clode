# Skill Builder

Write a skill, and you've made a guess. This measures it.

## The problem

A SKILL.md tells Claude what to do. Until you run it, you don't know whether it
fires when it should or holds its ground when someone pushes back on it. Most
skills ship on the strength of having been written.

## What you get

One command.

**`/skill-builder`** interviews you, writes the skill, generates its eval suite,
and runs it. The interview is the beginning. The measurement at the end is what
makes the skill worth trusting.

It handles both Claude Code skills and Claude.ai project skills. It won't let you
skip the problem to get to the build, and it won't let you ship without
anti-patterns named.

## The eval step

Every case in the suite is derived from a line in the skill's own instructions,
and cites it verbatim. A case that can't cite one doesn't ship. That rule does
most of the work. It stops anyone inventing plausible scenarios the skill was
never written to handle, which is where generated test suites normally go to die.

You get a coverage table showing which of the skill's rules are tested, and a
pass rate with and without the skill. That second number is the only one that
tells you what the skill actually contributes.

## What we learned building it, in four lines

**Gates and fences are where skills break.** A skill that skips a precondition,
or crosses a line it drew for itself, fails quietly. The output still looks
fine. Cases that test those are the ones that catch something.

**Some cases measure nothing.** A valid case can still prove nothing, because a
competent Claude does the same thing without your skill. We can tell you which
ones. A flat result is worth reporting.

**Two things separate a skill from a baseline.** Checking state the model can't
otherwise know, like a tool that isn't installed. And holding back where a
helpful assistant would barge in, like asking a question instead of guessing.
Almost everything else measures good manners.

**The instrument lies if you don't watch it.** The eval runner we depend on
reports 0% for every skill out of the box, for three separate reasons. That's
why setup is a command you run rather than a step you trust.

## What it doesn't do

Skills only. Not subagents, not commands, not MCP servers.

It won't tell you whether your skill is a good idea. It tells you whether it does
what it says.

## Installing it

Two routes, and they do not overlap.

**Claude Code, the CLI or the desktop app's local sessions.** No install command
exists. Copy the folder to `~/.claude/skills/skill-builder/` and it loads. A
change to `SKILL.md` is picked up live; a brand-new skill folder needs
`/reload-skills`.

**Claude Desktop and claude.ai.** A folder on disk does nothing here. Skills come
from your account, added by uploading a ZIP at **Customize > Skills**. Two traps:

- **Code execution has to be on first** (Settings > Capabilities). Otherwise the
  upload appears to succeed and nothing runs.
- **The ZIP must contain the skill folder as its top level.** A `SKILL.md` at the
  archive root is not recognized as a skill.

```
cd ~/.claude/skills && zip -r skill-builder.zip skill-builder/
unzip -l skill-builder.zip | head    # every entry must start with skill-builder/
```

Include `scripts/` in the ZIP; that path is where the eval tooling lives. The
`tests/` folder travels along but only runs in Claude Code.

**The trap worth knowing.** A desktop *Cowork* or cloud session does not read
`~/.claude/skills/`. It reads your account skills instead. A skill that works in
a local session can be invisible in Cowork unless it also went through the ZIP.

## Setup, once per machine

```
python3 ~/.claude/skills/skill-builder/scripts/patch-skill-creator.py --check
```

If that doesn't exit clean, run the same command without `--check`. It repairs
the trigger measurement in `skill-creator`, and it takes a second. Re-run it
after any `claude plugin update`, because the update silently puts the broken
version back.
