---
name: skill-builder
description: Build a Claude skill, then prove it works. Use when the user says "build me a skill", "make a skill for...", "I want a slash command that...", "create a skill to...", or "help me write a skill". Opens by offering two paths and naming which a beginner should pick — Quick (a question or two, the default) or Detailed (a longer interview for complex or high-stakes skills). Works for both Claude Code skills (SKILL.md) and Claude.ai project skills (system prompt); generates the skill with named anti-patterns; then writes its eval suite — test cases derived from the skill's own directives and traced to the lines they came from — validates it, and runs it against a no-skill baseline to report what the skill actually contributes. Every skill it produces ships measured.
metadata:
  author: charlie-fuller
  version: "3.1.0"
---

# Skill Builder

Interview the user to understand what they want a skill to do, then generate the output to make it real.

The goal: produce a skill that works the first time someone invokes it — not a skeleton, not a placeholder. Complete enough to drive behavior.

Two output formats:
- **Claude Code** (`SKILL.md`) — slash command in Claude Code CLI, lives in `~/.claude/skills/<name>/`
- **Claude.ai project skill** — system prompt pasted into a Claude.ai Project's instructions, shared across a team or enterprise workspace

A skill you write here ships **measured**. The interview gets you to the right
problem. The eval step at the end is what tells you the skill does what it says.

---

## Register

Match the user's fluency. Do not average it into something that bores one person
and loses another.

**Read the signal.** If someone says *eval*, *suite*, *baseline*, *assertion*, or
*trigger* without being taught the word, they have done this before — give them
the artifact and skip the orientation. If they ask what an eval is, or describe
their situation in plain language, they have not, and orienting them is the job
rather than a failure of theirs.

**Lead with the artifact.** Show the coverage table before the explanation and
let them ask how it was built.

**State the cost once, before spending it.** A full eval run spends model calls
and real wall-clock time. One line, before you start, then never again.

**Explain a mechanism once, at the moment it first matters.** One sentence, not
a section.

**Never re-explain something you have already explained in this conversation.**
That is the line between guiding someone and pandering to them, and it gets
crossed more often by trying to be thorough than by trying to be brief.

---

## Pick a path (ask this first, before Step 0)

Before anything else, offer two paths in plain language and say which one a
beginner should take. Ask once, then follow their choice.

> "Two ways we can do this:
>
> **Quick** — I ask a question or two and build you a working skill in a few
> minutes. **Pick this if you're not sure, or you just want something that
> works.** Most people want this.
>
> **Detailed** — a longer back-and-forth that digs into the real problem first,
> catches edge cases, and tends to produce a sharper skill. Worth it for
> something complex, high-stakes, or that several people will rely on.
>
> Quick is the default. Want quick, or detailed?"

If they don't choose, or say something like "whatever's easiest," take **Quick**.
If they describe something plainly complex — a multi-step pipeline, several
stakeholders, a process with real consequences — say so and gently point at
Detailed, but let them decide.

**The choice sets how hard the gates push.** Both paths keep the same gates; what
changes is how many times you knock.

- **Quick:** every gate fires **once**. You redirect a solution-framing once, you
  push a vague answer once, and then you take whatever answer you get and build.
  You never ask a question you could answer yourself — infer the format, pick a
  sensible name, say what you picked.
- **Detailed:** the gates hold. You stay in problem space until the pain is named,
  you push a vague answer as many times as it takes, and you run every phase.

Everything below is written for Detailed. On Quick, run the same steps but stop
at the first answer to each gate and move on. The eval step at the end is the
same for both — a skill ships measured either way.

---

## Reference files

Reach for these as the work calls for them, not all at once.

| File | Read it when |
|---|---|
| `references/roles.md` | The pain won't name itself, or the skill feels aimed at the stated task rather than the real problem. Carries the consumer question |
| `references/process-tuning.md` | They brought a process they already run by hand and want it tightened into a skill |
| `references/environment.md` | **Before designing around any connector.** What tools a skill may assume, and how to add your own |
| `references/safety.md` | **After the environment check, every time.** Credentials, read vs write, irreversible actions, shared surfaces, bounds. Says which rule produces which eval case |
| `references/personas.md` | Driving a finished skill end to end with a user who behaves badly |
| `references/brevity.md` | The skill's output is long, thorough, and read by nobody |
| `references/eval-procedure.md` | You have written the skill and are ready to measure it |
| `references/extraction.md` | In the eval step, pulling directives out of a bespoke file |
| `references/assertions.md` | In the eval step, writing assertions that can fail |
| `references/conditions.md` | In the eval step, when a suite is written and scoring flat |

Scripts live in `scripts/`: `validate_evals.py` checks a suite before you run it,
`render_plan.py` writes the coverage table, and `patch-skill-creator.py` keeps
the eval runner's trigger measurement working.

---

## Step 0: Understand the situation (do this first)

Open with:
> "Tell me what you're trying to do — what's the thing you want Claude to help with?"

**If their answer describes a tool or feature** ("I want a writing assistant," "something for my morning routine," "a tracker for X") — don't start Phase 2 yet. They've given you a solution, not a problem. Reflect it back:
> "Got it. Before we figure out what to build — what's going wrong today that made you want that?"

Stay here until they describe a situation, not a tool.

**Once they're describing the situation**, infer the skill type from what you hear. Don't make them pick from a menu.

| What they describe | Type |
|---|---|
| "I want it to just do X" / "generate Y" / "run a check on Z" | Simple action |
| "I want it to ask me questions and then..." / "walk me through..." | Interactive conversation |
| "It needs to pull from X, then do Y, then output Z" | Multi-step pipeline |
| Still unclear after one follow-up | Ask: "And what would it produce at the end?" |

Only surface a menu of options if genuinely ambiguous after a follow-up. Most users won't need it — their description tells you.

| Type | Discovery Depth | Output |
|------|----------------|--------|
| Simple action | 5-8 questions, ~5 min | Single SKILL.md |
| Interactive conversation | 10-15 questions, ~10 min | SKILL.md with embedded phase structure |
| Multi-step pipeline | 15-20 questions, ~15 min | SKILL.md + reference files |
| Not sure yet | Phase 0 first | Determine as you go |

---

## Step 0b: What to call it

**Ask this after Step 0c (where it lives), not before — the right question depends on which format you're building.**

**Claude Code:** ask for a slash command name.
> "What do you want to type to run this? Like `/analyze-pr` or `/weekly-report`? Or no preference yet?"
The name becomes the directory and the `name:` field in frontmatter.

**Claude.ai (chat or cowork):** don't ask for a slash command — there are none. Ask for a trigger phrase instead.
> "What would you naturally type to kick this off? Like 'wrap up my day' or 'help me prep for this meeting'? Claude will recognize that phrase and start the skill."
Use this to write a precise trigger in the `## When to use this` section of the project instructions.

**Both:** handle Claude Code naming first, then confirm the trigger phrase for the web version.

---

## Step 0c: Where does this live? (ask early — it shapes everything downstream)

Ask this in plain language. Don't use "deployment target" with the user.

> "Quick question so I build this in the right format — how do you use Claude day-to-day?
> - **Claude.ai in my browser** (chat or cowork) — I'll generate a block of instructions you paste into a Claude Project. Anyone you share the Project with gets the skill automatically.
> - **Claude Code in my terminal** — I'll generate a `SKILL.md` file that becomes a `/slash-command` you can run from the command line.
> - **Both** — I'll generate both formats."

If they look confused by "Claude Code" or "SKILL.md," they're a web user. Confirm and move on:
> "Sounds like Claude.ai — I'll build it as a Project skill."

This shapes the output format, not the interview. The same discovery questions apply either way.

---

## How to Run It

One question at a time. Listen, probe, move on. Don't dump phases on the user — run through them naturally in conversation.

When you have enough to generate the skill, say so. Don't keep asking.

**Core principle:** the skill you write is instructions to Claude, not documentation. Every line in SKILL.md should drive specific behavior. If a section reads like a description rather than a directive, rewrite it as one.

---

## Phase 1: The Trigger (mandatory for all types)

Understand *when* this skill fires. The `description:` field in frontmatter is what Claude reads to decide whether to invoke the skill — it has to be precise.

Questions to cover:
- "What does the user say (or type) that should kick this off? Give me 3-5 real examples."
- "Are there any similar situations where it should *not* fire? What's the false-positive risk?"
- "Is this a slash command the user explicitly invokes, or should it trigger automatically when Claude recognizes the pattern?"

**Watch for:** vague triggers like "when the user needs help" or "when they want to write something." Push for specific phrases and contexts.

---

## Phase 2: The Problem (mandatory for all types)

**Stay in problem space. Don't let the user jump to the solution yet.**

If they opened with "I want a skill that does X" — that's a solution. Back up. Understand why X matters before you build X. A different problem might need a different skill entirely, or no skill at all.

Open with:
> "Before we figure out what to build — walk me through what's actually going wrong. What does the situation look like when this problem hits you?"

Then probe:
- "What do you do today when this comes up? Walk me through it."
- "What's the part that breaks down — what goes missing, gets forgotten, or takes too long?"
- "What does the fallout look like? What happens because of this problem?"
- "How often does this come up?"

**Don't move to Phase 3 until you can answer:** *what is the actual pain, and what does it cost them?*

If their answer is vague ("it's just inefficient"), push:
> "Give me a specific example — the last time this happened, what went wrong?"

**If the answer is still vague, push again.** The gate above outranks any instinct to be polite — you cannot leave this phase until you can state the pain, and "it's hard to point at one thing" is not a pain. Push toward a concrete instance as many times as it takes, varying the angle each time:

> "Walk me through the last time it actually happened — from the moment you sat down."

Then follow the story one step further than they take it. The most valuable answer is often the one they didn't know they had: ask whether it ever actually went out, or actually shipped, or actually got sent. The real problem is usually one turn past where they stop.

Concrete examples are worth ten abstractions. The example usually contains the real problem, and sometimes contains a better one underneath it.

**When the pain still won't name itself**, read
`references/roles.md` and find the role that looks
like this person. It lists what people in that kind of work usually contend
with, and the generic solution their ask is often standing in front of. Then
ask:

> "If this were solved perfectly, what stops happening?"

People answer that in concrete nouns — a specific bad Tuesday — where "what do
you want?" only ever gets answered in task language.

While you're in that file, note the **Inputs** and **Consumer** lines for the
role. Three parties are usually in play and they are rarely the same person: the
requester, the operator, and whoever receives the output. A skill tuned to the
requester can fail the consumer, and you'll want to know which one you're
building for before Phase 4.

**Watch for solution-framing disguised as a problem:**
- "I need something that tracks my tasks" → what happens when tasks don't get tracked?
- "I want a morning briefing" → what are you missing without one?
- "I want it to summarize my emails" → what decision or action are you trying to make faster?

Reframe these as problems before moving on. The skill you build from the problem will be sharper than the one you build from the solution they assumed.

**When you think you've found the root problem, name it out loud and confirm it.**

Don't silently assume you got it right. Say it back:
> "So the real problem is [X] — is that right?"

This does two things: catches misreads before you build the wrong thing, and often helps the user see their own problem more clearly. If they say "actually, it's more like..." — that's the real problem. Stay here until the confirmation lands clean.

---

## Phase 3: The Behavior (mandatory)

What does the skill actually *do*, step by step.

**If they arrived with a process they already run by hand, tune it before you
describe it.** Read `references/process-tuning.md`. The short version: get it
written as it actually happens rather than as it should, find the step that
carries the value, turn decisions made the same way every time into rules, find
the stopping condition, and cut whatever a competent model would do anyway. A
skill built from an untuned process ends up as long as the process and no more
reliable.

### Simple action
- "Walk me through the steps — what does Claude do first, then next, then at the end?"
- "What information does Claude need that it doesn't already have? Does it ask the user, or pull it from somewhere?"
- "What does the output look like? Show me an example or describe the format."

### Interactive conversation skill
This is where you go deeper. You're designing a conversation flow, not just a checklist.

- "What does Claude ask at the start? What's the opening question?"
- "What phases or topics does it need to cover? In what order?"
- "Does the depth change based on what the user says? How?"
- "What does Claude produce at the end — a doc, a prompt, a file, something it runs?"
- "Are there things Claude should never do in this skill — scope boundaries, anti-patterns, known failure modes?"

### Multi-step pipeline
- "What are the stages? What does each one do and what does it hand to the next?"
- "Which stages need the user's input, and which run autonomously?"
- "What's the success criteria — how do you know the pipeline did its job?"

---

## Phase 4: The Output (mandatory)

Understand what a successful run produces.

- "What does the final output look like? A file? A response? A command it runs?"
- "Where does it go — screen output, written to a file, saved somewhere specific?"
- "Is there a template or structure the output should follow every time?"
- "What's the output for a skill that 'fails gracefully' — what should Claude say if it can't complete the task?"

If they have an example of a good output (manual version, prior run, desired format), ask them to share it. It's the clearest spec you'll get.

---

## Phase 5: References, Dependencies, and Available Tools (skip for simple actions unless relevant)

- "Does this skill need to read any files to work? Config files, memory, style guides, templates?"
- "Does it depend on other skills or tools? (e.g. calls the diagrams skill, reads from Obsidian)"
- "Are there things Claude should read *before* starting — like a style guide or project context?"

**Then check every tool it depends on against `references/environment.md`.** Read
that file before you design around any connector. A skill may only assume tools
listed there.

- **Listed** — build against it. Note whether the solution needs read or write
  access; write access needs a confirmation step inside the skill.
- **Not listed** — ask whether they have it. If they do, add it to
  `environment.md` and continue. If they do not, write the skill so its first step
  confirms the tool is connected and stops with a clear message. That gate is the
  most valuable case in the eval suite.
- **The environment that matters is where the skill will run**, not where you are
  building it. A skill written on a laptop with no corporate mailbox is headed
  somewhere that has one.

What you must not do is design around a tool you have not confirmed exists. A
skill that assumes a connector nobody has reads correctly and fails silently.

**Then run the safety pass.** Read `references/safety.md`. That file covers what
the skill is allowed to *do* once it can reach a tool: credentials, read versus
write, irreversible actions, shared surfaces, other people's data, and bounds.

Most skills need one or two of those rules and no more. A skill that only
transforms text the user pastes in needs none, and saying so is the honest
answer. For each rule that applies:

1. The generated skill carries the corresponding gate.
2. The eval suite gets the matching case, as `references/safety.md` spells out.

Both halves. A safety rule that exists in the skill but has no eval case is an
untested claim, which is the thing this whole process exists to avoid.

If the answers are non-trivial, plan reference files alongside the SKILL.md.

---

## Phase 6: Anti-Patterns and Scope Fences

These sharpen the skill. Always ask at least one:

- "What's the version of this that would make you say 'that's not what I meant'? What would Claude have done?"
- "Is there scope creep risk — ways this could expand beyond what it's supposed to do?"
- "What should Claude never do in this skill, even if it seems helpful?"

---

## Generate the Skill

When you have enough to write it — do it. Don't ask permission. Tell them:

> "I have what I need. Writing the skill now."

### File structure

**Simple action:**
```
~/.claude/skills/<name>/
└── SKILL.md
```

**Interactive conversation / pipeline:**
```
~/.claude/skills/<name>/
├── SKILL.md
└── references/
    ├── <template-or-example>.md   (if a template was identified)
    └── <phase-reference>.md       (if phases are complex enough to warrant it)
```

Only create reference files if the SKILL.md would be unreadable without them. Prefer inline.

---

### SKILL.md structure

```markdown
---
name: <kebab-case-name>
description: <1-2 sentences — precise trigger conditions, what it does, when NOT to use it. This is what Claude reads to decide whether to invoke.>
metadata:
  author: <author>
  version: "1.0.0"
---

# <Skill Title>

<1-2 sentence summary — what this skill does and why it exists.>

---

## When to Use
<Specific trigger conditions. Phrases the user says. Contexts that invoke this. Contexts that don't.>

## [Core behavior section — name it based on what the skill does]
<The actual instructions. Step by step. Directives, not descriptions.>

## Output
<What the skill produces. Format, location, structure. Include a template if relevant.>

## Anti-Patterns
<What Claude must not do. Scope fences. Known failure modes.>
```

**Writing rules for the SKILL.md body:**
- Every instruction is a directive ("Ask X," "Generate Y," "Never do Z"), not a description ("The skill asks X")
- If a section is just background and doesn't drive behavior, cut it
- Phases/steps should be labeled and scannable — Claude reads this under pressure
- If there's a template for the output, include it inline unless it's longer than ~100 lines (then extract to `references/`)
- Anti-patterns section is mandatory — at least 3 items

---

### Claude.ai project skill output

If deployment target is **Claude.ai project** (or Both), generate a formatted system prompt instead of (or in addition to) SKILL.md:

```
# [Skill Name]

[1-2 sentence summary — what this skill does and when to use it.]

## When to use this
[Specific trigger phrases and contexts. What NOT to use it for.]

## How I work
[Step-by-step instructions in first person. What I ask, what I do, what I produce.]

## Output format
[Describe the output — format, structure, length. Include a template if there is one.]

## What I don't do
[Scope boundaries. Known failure modes. Things I'll redirect back to the user.]
```

Tell the user: "Paste this into your Claude.ai Project's instructions (Settings → Project instructions). Everyone in the project will have access to it."

If they need to share it to an enterprise workspace: "Have your workspace admin add this to a shared Project — or paste it into any new Project you create."

---

### After writing — install, then evaluate

**Do not stop at "here's your skill."** A skill that has never been measured is a guess. Three steps, in order.

**1. Install check.** Tell the user:

> "Skill written to `~/.claude/skills/<name>/SKILL.md`. Reload your Claude Code session to pick it up."

**2. Generate the evals.** Read `references/eval-procedure.md` and work through it. It takes the SKILL.md you just wrote, extracts its directives into five categories, and produces `<skill>/evals/evals.json` plus a `PLAN.md` coverage table where every case cites the line it came from. Validate the suite with `scripts/validate_evals.py` before you go further.

Then read the coverage table back to the user. Two things to say out loud:
- Which categories have cases, and which came back empty. An empty `gate` or `fence` row is a real finding — it means the skill you just wrote has no precondition and no prohibition, which is worth knowing before anyone relies on it.
- The count. A core set outside 8-12 means the skill was under-specified, not that the suite is thin.

**3. Run the loop. You are not finished until `benchmark.json` exists.**

Validation is not measurement. A suite that passes the validator has been checked for shape, not for behaviour, and stopping there is the same "narrate it back" failure this skill used to have. The completion condition for this entire procedure is a `benchmark.json` and a rendered viewer for the skill you built. If you reach the end of step 2 and stop, you have not finished.

The eval machinery lives in `skill-creator`, installed but deliberately **disabled** so it does not compete with this skill for the "build me a skill" trigger. Its procedure is still on disk and still good.

**Before you rely on it, check that the trigger measurement actually works.** `run_eval.py` scores 0% for every skill until three compounding faults are repaired, and the repair is lost on every `claude plugin update`:

```
python3 ~/.claude/skills/skill-builder/scripts/patch-skill-creator.py --check
```

Exit 0 is healthy. Anything else, run the same command without `--check` to repair it, then re-check. If it reports it cannot repair, say so plainly — it means upstream changed shape, and any trigger numbers you produce will be meaningless. Do not present them.

Then read the procedure (the version directory varies, so glob it):

```
ls ~/.claude/plugins/cache/claude-plugins-official/skill-creator/*/skills/skill-creator/SKILL.md
```

Follow its **"Running and evaluating test cases"** section verbatim — the with-skill and baseline arms, `agents/grader.md` for grading, `scripts/aggregate_benchmark.py`, and `eval-viewer/generate_review.py`. Read `references/schemas.md` in that same directory for the exact artifact shapes.

Four things to carry over, each learned the hard way:

- **Isolate the baseline.** Run it with `--disable-slash-commands`. Otherwise any other installed skill matching the prompt answers first, and the split you measure is an artifact rather than skill value.
- **Disable the skill under test.** The real skill competes with the staged copy and usually wins. Set `skillOverrides: {"<name>": "off"}` in `~/.claude/settings.json` for the duration, and restore it after.
- **Run from a scratch directory.** Not from `~/.claude` and not inside a repo. The runner resolves its project root by walking up, so a stray `.claude` above the working directory gets captured.
- **Verify completion before computing anything.** Every arm must have written a non-empty response. A truncated arm scores zero under the strict grading rule and silently inflates the delta.

**If you genuinely cannot run the loop** — no subagents available, no budget, the user asked you to stop — say so in one line and hand the user the exact command to run themselves. Saying "I couldn't run it" is fine. Saying nothing and stopping at validation is not.

**4. Close the loop, once.** They should leave able to do this without you. After
the results land, walk the arc in a short paragraph, using the skill they just
built as the example:

> "What you brought was a task. We found the problem underneath it, cut it to its
> spine, wrote that down, and measured it. That is the whole method, and you can
> run it again on your own."

Say it once, at the end. Do not narrate the method while the work is happening,
and do not repeat this in a later session.

---

## Anti-Patterns

- Writing a SKILL.md that describes what the skill does instead of directing Claude to do it — the body is instructions, not documentation
- Generating a skill before you understand the output format — the output spec is the skill
- Asking more questions after you have enough — when you can write it, write it
- Writing a skill with no anti-patterns section — every skill has a failure mode; name it
- Building a complex interactive skill without identifying the phases — the conversation structure IS the skill for interactive types
- Not asking for a real example of good output — it's the clearest spec you'll get and users almost always have one
- Skipping the trigger precision step — a vague description: field means the skill fires at the wrong time or never fires
