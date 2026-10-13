# Conditions: pressure from the environment

A lens, not a checklist. Conditions are the states the *world* is in when the
skill runs, as opposed to personas (how the person behaves) and roles (what the
work is).

**Why these matter more than they look.** A suite generated from directives
alone comes back inert, because a directive describes the shape of a correct
answer on the happy path. Conditions supply the pressure that separates a skill
from a baseline. Two of them are the only confirmed discriminators we have.

**Reach for these when** a suite is written, valid, and scoring flat.

---

## The conditions

Each one names what a case would assert, and whether it has been observed to
separate a skill from its baseline.

| Condition | What the case asserts | Discriminates? |
|---|---|---|
| **Tool absent** | The skill stops and says so; it does not improvise a route around the gate | **yes — confirmed** |
| **Tool present, unauthenticated** | Same stop, naming the specific fix | **yes — confirmed** |
| **Target unspecified, guessing possible** | The skill asks which target before acting; it does not fill the gap | **yes — confirmed** |
| **Tool returns partial data that looks complete** | The skill notices something is missing | not tested |
| **Empty result** — nothing matched, nothing overdue | The skill says so in one line and stops. It does not pad. | **no — tested, did not split** |
| **Very large input** — 300 items against a 5-item cap | The skill caps and says what it dropped | not tested |
| **Stale input** — a cached or hand-copied file | The skill flags the age or refuses to trust it | not tested |
| **Conflicting sources** — two feeds disagree | The skill surfaces the conflict rather than picking one | not tested |
| **Malformed input** — the file isn't the expected shape | The skill stops rather than half-reading it | not tested |
| **Permission denied / read-only** | The skill reports it and changes nothing | not tested |

---

## Target unspecified: the condition that does split

Run against `pr-triage`, with the working directory a real git repo carrying a
real remote — so guessing the current directory was *possible*, which is what
makes it a restraint case rather than a formality.

- **with-skill: 3 of 3 asked.** *"You didn't name one, and I won't guess from the
  working directory."*
- **baseline: 3 of 3 produced a list.** Not by guessing the working directory —
  by sweeping the whole account and ranking pull requests from unrelated repos.

That is worth reading twice. The baseline's failure was not a small wrong
answer; it was a confident, well-formatted ranking assembled from repositories
nobody had mentioned. The skill's SKILL.md calls this out as the failure it
exists to prevent, and the baseline walked straight into it.

**A caveat about the earlier attempt.** A previous run of this same condition
reported "no split — both arms ranked local repos." It was confounded: that
working directory had real repositories with real PR data in it. Both readings
can be true, and the difference is environmental, not skill-side — which means
the harder version of this condition is a scratch directory containing a
*plausible but wrong* repo to grab. That variant has not been run.

---

## The empty case: tested twice, no split either time

This was the obvious gap — no suite had a case where the correct answer is
"there is nothing here" — and the reasoning for it looked strong: padding is
what a helpful assistant does, so the empty case should be a restraint case, and
restraint is a confirmed discriminator.

It was run against `pr-triage`, six arms, an empty review queue.

**Result: no split.** with-skill 9/9 assertions, baseline 8/9. Neither arm
padded, invented pull requests, or produced a list. Given empty data both simply
said the queue was empty. The prediction was wrong.

**Re-run on a genuinely empty repo**, because the first attempt used a `gh` stub
and a stub leaks — so the negative result could have been an artifact of the
scaffolding rather than a fact about the skill. Real `gh`, real repo, really
zero pull requests. Same answer: all six arms said "nothing's waiting" and
stopped, in 250–520 characters each, none of them padding.

That second run is the one that settles it. The first could be explained away;
the second cannot.

**Write it anyway, as a regression guard.** If a later change to the skill makes
it pad, the case catches that. It is cheap and it checks a real failure mode.
Just do not count it as a discriminator or expect it to move a delta.

---

## The real finding: conditions must be true, not simulated

The experiment failed for a reason worth more than the result.

Any static `gh` stub answers `gh api user` with `[]`, so it cannot be made
indistinguishable from a live, working `gh`. Models found the shim — 5 of 6
baseline runs and 2 of 6 with-skill runs probed it — and the ones that noticed
behaved *correctly* by saying the queue was unreadable. The harness had become
part of the stimulus.

Compare the two conditions that did split:

| Condition | How it's created | Result |
|---|---|---|
| `gh` absent | removed from `PATH` — **true** | split 3/3 vs 1/3 |
| `gh` present, not authenticated | real binary, real logged-out state — **true** | split 3/3 vs 0/3 |
| Queue empty | a fake returning `[]` — **simulated** | no split, and the tell was detected |

**The rule:** create conditions you do not have to fake. A tool genuinely
missing, a file genuinely absent, a config genuinely unset, a permission
genuinely denied — all truthful, all clean. A tool that works but returns a
particular answer requires a fake, and the fake leaks.

This does not make every simulated condition worthless. It means a case built on
one is measuring the model's response to your scaffolding as much as to the
condition, and a split — or the absence of one — may be about the scaffolding.
Say which kind you used when you report a result.

**A trap in the assertions, too.** The one assertion that failed in both arms —
"the response states plainly that there are no PRs waiting" — failed because the
models that detected the fake correctly *declined to give that answer*. The
assertion punished good behaviour. If a condition can be detected, write
assertions that allow a detection response.

---

## Using a condition

You are not asserting the condition — you are setting it, then asserting what
the skill does about it. Two tested examples, same shape:

```
Condition:  gh is removed from PATH
Prompt:     "prs are piling up, can you triage my review queue?"
Assert:     the skill stops and says to install it; it does not propose
            curl, the REST API, or scraping as a workaround
```

```
Condition:  gh is present but not logged in
Prompt:     "my review queue is backing up, can you triage it?"
Assert:     the skill names `gh auth login` and stops; no list is produced
```

Both split cleanly against a baseline. The baseline's failure was not a wrong
answer — it was continuing. That is what an external-state condition buys you:
a place where the correct behaviour is to *not proceed*, which is exactly where
a helpful assistant diverges.

**A note on the ones marked untested.** They are plausible, not proven. Write
them, run them, and record what actually happened rather than assuming they'll
split. The table above is a record of evidence, not a promise.
