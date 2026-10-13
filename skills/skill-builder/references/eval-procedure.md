# Writing the eval suite

How to turn the skill you just wrote into something measured. Read this when you
reach the eval phase.

The premise: a well-written SKILL.md is already a spec. Its directives — "check
the prerequisite first", "never do Z", "output in this format", "ask before
drafting" — are testable claims. Generating a suite is not invention. It is
systematic extraction, and every case should be traceable back to the line it
came from.

That traceability is the whole value. A case you invented tests your
imagination. A case citing a directive tests the skill.

---

## The five categories

Every skill carries some mix of these, whatever its headings say. Do not match
on heading text — the skills on this machine share no section vocabulary. Read
for meaning.

| Category | What it is | How to spot it |
|---|---|---|
| `gate` | A precondition that must fire before any work | "Prerequisite", "Before you start", "read this first", "if X is not set up, stop" |
| `process` | A mandated order or a required step | numbered or phase-labelled sequences, "always in this order", "first… then…" |
| `output` | A required shape for the result | "Output", "Report", template blocks, named columns or filenames |
| `fence` | Something the skill must not do | "Anti-patterns", "Non-negotiables", "Rules", "Never", "Common mistakes" |
| `trigger` | Phrases that should and should not fire the skill | the quoted examples in `description`, plus the near-misses it must decline |

Read `references/extraction.md` before extracting. It has real quoted examples
from `cite-check`, `refresh-radar`, `post-image`, and `motion-taste`, so you can
see how wide the surface forms run.

**Gates and fences are the highest-value cases.** A skill that skips its gate or
crosses its fence is broken even when its output looks correct — and neither
failure shows up in a happy-path prompt. If a skill has a gate or a fence and
your core set has no case for it, the suite is wrong.

---

## Reference files

Reach for these as the work calls for them, not all at once.

| File | Read it when |
|---|---|
| `references/extraction.md` | Before extracting — how the five categories hide in a bespoke file |
| `references/assertions.md` | Before writing assertions — what makes one fail, and what makes one inert |
| `references/conditions.md` | A suite is written, valid, and scoring flat — pressure from the environment |
| `references/roles.md` | The skill feels aimed at the stated task rather than the real problem, or you can't say who consumes the output |
| `references/personas.md` | Driving an interview-shaped skill end to end with a user who behaves badly |
| `references/brevity.md` | The output is long, thorough, and read by nobody |

---

## Procedure

### 1. Resolve the target

Read the SKILL.md. If there is no YAML frontmatter, fall back to the `# H1` line
for the name. Two skills on this machine (`custom-svg-diagram`, `interview-prep`)
have no frontmatter at all — do not assume one.

### 2. Extract the directives

Walk the file and pull out each directive, tagging it with a category. Quote the
directive **verbatim** — that string becomes the case's `source`, and
`validate_evals.py` will check it appears in the file character for character
(modulo whitespace). If you cannot quote it, you are inventing it.

### 3. Build the tiered suite

**Core → `evals/evals.json`** — 8-12 cases. Must include every gate, every
scope fence, the output shape, the trigger pair (one should-fire, one near-miss
that must not), and — wherever the skill can legitimately find nothing — one
case where the correct answer is that there is nothing.

**Write the empty case — as a regression guard, not a discriminator.** It is
cheap, it tests a real failure mode, and it was missing from every suite
generated before this rule existed. But it was tested once, against `pr-triage`,
and it did **not** split: with-skill 9/9 against a baseline 8/9. Neither arm
padded, invented rows, or produced a list. A competent baseline answers "the
queue is empty" and stops.

The reasoning that it would split — *padding is a baseline behaviour* — was
wrong, and it is worth knowing why the case is still worth keeping: if a future
change to the skill makes it pad, this case catches that. That makes it a
regression guard. Do not count it toward discrimination, and do not expect it
to move a delta. See `references/conditions.md`.

If the skill genuinely has no empty state — a transformation that always
receives input, say so instead of forcing one.

**Check `safety.md` before you close the tier.** For whichever safety rules apply
to this skill — credentials, read versus write, irreversible actions, shared
surfaces, other people's data, bounds — the matching case has to be in the core
set. `safety.md` has the table of which rule produces which kind of case.

A skill that touches no connector and transforms only pasted text has no safety
cases, and that is a fine answer. Record it in the coverage table rather than
inventing one to fill the `fence` row.

**Extended → `evals/evals.extended.json`** — one case per remaining directive,
plus one adversarial case per anti-pattern. Opt-in. No size limit.

If the skill has no gates and no fences, say so and let the core set run small.
Do not pad it to reach the floor — a padded suite is worse than a short honest
one. Report the gap instead.

### 4. Write assertions that can fail

Read `references/assertions.md` first. The governing rule from
`skill-creator/agents/grader.md`: *the burden of proof to pass is on the
expectation*, there is no partial credit, and an assertion that would also pass
for a clearly wrong output is a bad assertion.

Two to four assertions per case. At least one must be capable of failing for a
plausible-but-wrong run.

### 5. Check that the suite can discriminate

An assertion can be perfectly valid and still measure nothing, because **the
baseline arm passes it too.** Those cases are inert: they lift the with-skill
score without moving the delta, so the suite looks thorough while saying nothing
about this skill.

The test, per assertion, at generation time:

> **Would a competent Claude *without* this skill satisfy this?**

If yes, it measures good practice. If no, it discriminates.

**What actually discriminates.** Measured across four full runs. It is not "a
decision the skill makes" — a strong model makes most of those unprompted.

- **External state the model must check.** *(confirmed)* A gate that depends on
  something outside the model's knowledge: a tool missing, a file absent, a
  config unset. With the skill the model stops at "install `gh` and re-run";
  without it, it finds the off-PATH binary and improvises around the gate. The
  baseline cannot know it should stop.
- **A restraint that runs against the model's grain.** *(confirmed)* Two
  directions, both measured:
  - *Withhold an addition* — refuse the options it was offered, cap the list,
    stop at "Send this one." and add nothing after. The model wants to be
    helpful by adding.
  - *Withhold an action* — ask instead of guessing, stop instead of proceeding.
    Confirmed on `pr-triage`: told to triage without a named repo, the skill
    asked 3 of 3 while the baseline produced a ranked list 3 of 3 — swept the
    whole GitHub account and ranked pull requests from unrelated repositories.
    The model wants to be helpful by acting.
- **Output shaped for a downstream consumer.** *(candidate — two sightings, one
  in each of two runs, not yet banked)* The skill produces something the next
  person can act on without a second pass; the baseline produces a plausible
  artifact that someone has to re-process. `pr-triage`'s contract — PR number,
  title, one-line reason, recommended action — exists so the shortlist is
  actionable, not because a format was specified anywhere in the prompt. The
  baseline cannot match it, because the baseline does not know who is
  downstream. Flag any split of this shape and mark it unconfirmed.

Everything else trends inert. The sharpest evidence: a skill whose gate was a
*reasoning* precondition scored a delta of exactly **+0.00 across five cases,
13/13 in both arms.** A strong model holds reasoning gates unprompted.
Conventional good-practice fences ("don't approve blindly", "don't sort by
recency") are inert for the same reason — the baseline already obeys them.

### Isolate both arms

A clean baseline is not the default. Two hazards, both real:

- **Competing installed skills.** A baseline run on this machine was hijacked by
  an unrelated slash command that matched the prompt, 401'd, and produced no
  work at all. The split looked like skill value and was an artifact. Run the
  baseline with `--disable-slash-commands` so nothing else answers first.
- **Your own scaffolding leaking into the run.** A smoke-test fixture left in a
  scratch directory became the baseline's input in one run. Use a fresh
  directory per case.

Then verify completion before computing anything: **every arm must have written
a non-empty response.** A truncated run scores zero under the strict rule, which
reads as a baseline failure and silently inflates the delta. In one attempt the
driver backgrounded the harness and returned early; only 3 of 9 arms finished and
the resulting numbers were void. Count the response files and say so.

**Do not rewrite an assertion until the baseline fails.** That manufactures a
delta instead of measuring one, and it is the one way to make this step
actively harmful. Rewrite only when you can name a true discriminator in one of
the two shapes above. If you cannot, keep the case, label it a regression guard
in `expected_output`, and report the flat delta.

**An inert case is a finding, not a failure.** A suite that reports `+0.00` has
told the truth: this skill's behaviour is what a baseline already does. That is
worth knowing, and it is not something to hide.

**A case can also be inert because it aims at the wrong altitude.** If the
assertions test the artifact and the value lives in what the consumer does with
it, a baseline that produces a plausible artifact passes. Read
`references/roles.md` for the consumer question and `references/brevity.md` for
what actionable output looks like, then ask whether each assertion measures the
artifact or its fitness for the next person.

### 6. Declare what each gate case withholds

A case whose assertion requires the skill to **ask for something** is incoherent
if the prompt already supplies it. This shipped twice from the same generator
before it was caught: a gate case about confirming the publishing cadence went
out with the word "daily" already in the prompt, so the skill correctly asked —
and the assertion marked it down for asking.

The fix is a declaration, not a heuristic. Whenever an assertion has the skill
elicit a specific value, add `withholds` to that case naming the literal string
the prompt must not contain:

```json
"withholds": "daily"
```

`validate_evals.py` then checks absence exactly. It cannot be done by word
overlap — "cadence" and "daily" are synonyms, not the same token — which is why
the declaration is explicit. The validator warns when an assertion looks like it
elicits something and no `withholds` is declared.

### 7. Validate, then hand off

```
python3 ~/.claude/skills/skill-builder/scripts/validate_evals.py \
  <skill>/evals/evals.json --tier core --source <skill>/SKILL.md
```

Fix anything it reports. Then write `<skill>/evals/PLAN.md` — a table mapping
each case to its category, tier, and source directive, so a reader can audit
coverage without opening the JSON.

Then stop and hand off to `skill-creator`, which runs the with/without arms,
grades, aggregates, and renders the viewer. Note: if the suite includes trigger
cases, `run_eval.py` must have been patched — see
`~/.claude/scripts/patch-skill-creator.py`.

---

## Output contract

`evals/evals.json`, matching `skill-creator/references/schemas.md` exactly:

```json
{
  "skill_name": "<name>",
  "evals": [
    {
      "id": 1,
      "prompt": "a realistic user prompt, in the user's voice",
      "expected_output": "one line describing a correct result",
      "files": [],
      "expectations": ["a verifiable PASS/FAIL statement"],
      "source": "verbatim directive from the SKILL.md",
      "withholds": "a literal string, or a list of them, the prompt must not contain",
      "category": "gate | process | output | fence | trigger",
      "tier": "core | extended"
    }
  ]
}
```

Required upstream: `skill_name`, and per case `id`, `prompt`, `expected_output`,
`expectations`. `source`, `category`, `tier`, and `withholds` are additions — the
runner ignores unknown keys, and the validator and `PLAN.md` read them.
`withholds` is required on any case whose assertions have the skill ask for a
specific value, and omitted otherwise.

**Write prompts in the user's voice.** Real phrasing, lowercase, a little
backstory, specifics. Not `"Reconcile a ledger"` but `"can you reconcile last
month's ledger against the deposit feed? the numbers aren't lining up"`. The
grader is judging whether the skill works on real input.

---

## Anti-Patterns

- **Inventing cases the skill never speaks to.** If nothing in the SKILL.md
  supports it, the case does not belong. Cite or cut.
- **Matching on headings.** `## Anti-Patterns` appears in 4 of 28 skills.
  `## Non-negotiables`, `## Rules`, and `## Common Mistakes` mean the same thing.
  Read for meaning.
- **All-happy-path suites.** A suite that never asks the skill to refuse
  something cannot detect scope creep, which is the most common real failure.
- **Surface assertions.** "The output is a markdown table" passes for a table
  full of invented rows. Assert on substance.
- **Inert assertions.** A valid assertion the baseline also passes measures
  nothing. General good-practice fences — don't approve blindly, don't sort by
  recency — are satisfied by an unaided Claude, so they inflate the with-skill
  score without moving the delta. Anchor on what only this skill does.
- **Prompts that supply what the assertion expects the skill to ask for.** Name
  it in `withholds` so the contradiction is caught mechanically rather than two
  runs later.
- **Padding the core tier** to hit 8 when the skill only supports 5. Report the
  gap.
- **Running the evals yourself.** Hand off to `skill-creator`.
- **Paraphrasing a `source`.** It must be the verbatim string. Paraphrase breaks
  traceability, which is the point of the whole exercise.
