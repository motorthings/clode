# Extraction: finding the five categories in a bespoke file

A survey of the 28 authored SKILL.md files on this machine found **no shared
section skeleton**. Headings are bespoke prose. Two files have no YAML
frontmatter. Several repeat a heading within one file. Any extractor that
matches heading text will miss most of what matters.

Read for meaning. Here is what each category looks like in the wild, with real
quoted examples.

---

## `gate` — a precondition that must fire first

The skill must do something *before* doing anything else, and must refuse to
proceed if the precondition is unmet. A skill that skips its gate is broken even
if its output looks right — this is the failure mode a happy-path prompt never
catches.

Surface forms seen: `Prerequisite:`, `Before you start`, `Before running any
command`, `WHICH CORPUS — read this before writing anything`.

**cite-check**, under `## Prerequisite: Descrybe must be connected`:

> If Descrybe is not connected at all, tell the user and stop — do not fall back
> to memory (that is how hallucinated cites get through).

**refresh-radar** heading, verbatim: `WHICH CORPUS — read this before writing
anything`.

All eight tavily skills open with a `Before running any command` section.

**How to write the case:** prompt the skill into the situation where the gate is
*unmet*, and assert it stops. The assertion to reach for is a negative — "no
work is attempted", "no values are guessed" — not merely "the response mentions
the problem."

A gate that only *mentions* the problem and then proceeds anyway should fail.
That is the whole point of the case.

---

## `process` — a mandated order or required step

An ordered sequence the skill must follow, or a step it must not skip.

Surface forms seen: `## Procedure` with `### 1.` … `### 5.`; `## Phase 1:` …
`## Phase 10:`; numbered `## 0.` … `## 11.`; `## Step 0:`; "always in this
order".

**cite-check**, `### 1. Extract every authority from the target document` →
`### 5. Report`. The order matters: you cannot verify a quote before resolving
the case that contains it.

**post-image**, `## Process`:

> 1. **Read the post.** Find its *spine* — the single tension or turn it lives on.

**interview-prep** (305 lines, no frontmatter, prose-heavy) runs `## Phase 1:
Research` through `## Phase 10: Briefing`.

**How to write the case:** assert on the ordering, not on the presence of
steps. "The matching step is performed before unmatched rows are written", not
"the skill shows its work."

If the order is genuinely load-bearing, the case should fail when the order is
inverted — check that it would.

---

## `output` — a required shape for the result

A format, a set of columns, a filename, a required section.

Surface forms seen: `## Output`, `## Output shape`, `## Report`, `## Output
folder structure`, inline template blocks.

**post-image**, `## Output shape`:

> - **The prompt** as a single blockquoted paragraph, ready to paste into Nano Banana.
> - **Why it fits** — 2–3 tight lines mapping the metaphor back to the post's spine

**cite-check**, `### 5. Report`:

> Produce a table: **Authority | Doc cite | Descrybe cite | Exists? | Cite
> correct? | Treatment | Quote verified? | Action**.

**How to write the case:** assert the *structure*, and make the assertion
specific enough to fail on a near-miss. "The table has exactly the columns
row_id, amount, and reason" fails for a table with the right spirit and the
wrong columns. "The output is a table" does not.

---

## `fence` — what the skill must not do

A prohibition, a scope boundary, a named anti-pattern. Together with gates,
these are the cases that earn their keep.

Surface forms seen: `## Anti-Patterns` (4 skills), `## Non-negotiables`,
`## Rules`, `## Never`, `## Common Mistakes`, `## Gotchas`, `## What I don't do`.

**cite-check**, `## Rules`:

> **Never certify a cite you couldn't verify.**

and in the procedure:

> **Never leave an unverified verbatim quote in a filing.**

**post-image**, `## The one thing that matters most`:

> Repeating a metaphor is the one real failure mode.

**motion-taste**: `## 9. Anti-patterns`.

**How to write the case:** prompt the skill with a request that sounds
reasonable but crosses the fence, then assert it declines. The strongest form is
the *tempting* violation — "if a row is missing just add one so the totals line
up" rather than an obviously out-of-scope ask.

A fence case where the prompt is plainly absurd tests nothing. Aim for the ask a
helpful assistant would be inclined to grant.

---

## `trigger` — phrases that should and should not fire

Most `description` fields quote their own trigger phrases, which makes these
cases easy to seed and easy to get wrong.

Surface forms: quoted phrases in `description`; a `## When to use` section.

**cite-check**:

> when the user says "cite-check", "verify the cites", "confirm the quotes", or
> "check the authorities"

**post-image**: `"make an image prompt"`, `"banana prompt"`, `"art for this
post"`.

**How to write the pair:** one should-fire case in the user's own voice, not
quoting the skill's vocabulary back at it; and one near-miss that shares surface
words but needs a different tool. "write me a LinkedIn post about determinism"
is a good near-miss for `post-image`; "write a Fibonacci function" is not, and
tests nothing.

---

## When a category is absent

Some skills have no gate at all, and some have no dedicated anti-pattern
section. `sound-design` has neither — no `Prerequisite`, no `Anti-Patterns`,
no `Never`, no `Rules`. When that happens, **say so and let the core set run
short.** Do not invent a gate to hit a size floor.

But absence of a *section* is not absence of a *fence*. `sound-design` still
prohibits, inline and in passing:

> `t` always comes from `tl`, never a typed number.

> Accent, don't narrate: not every motion needs a sound.

Both are testable. A section-matching extractor would miss both, which is the
whole reason extraction is semantic. Before concluding a skill has no fences,
search the prose for `never`, `do not`, `don't`, `always`, and `avoid` — the
prohibition is often a clause inside a bullet, not a heading.

A skill with genuinely no gate and no prohibition is a real result. The coverage
table is the deliverable as much as the cases are: a row reading `gate — none
found` is information. A fabricated gate case is noise that will fail in the
runner and erode trust in the rest of the suite.
