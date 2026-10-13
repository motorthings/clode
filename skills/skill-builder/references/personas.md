# Personas: users who behave badly, on purpose

A lens, not a checklist. A persona is **how a person behaves in the
conversation**, not what the work is (`roles.md`) or what the world is doing
(`conditions.md`).

**These are for driving a test, not for writing assertions.** You use a persona
to run an interview-shaped skill end to end and see whether it holds its gates.
That is a different exercise from writing a suite — and the most useful personas
are the ones whose behaviour would make a weak skill fail silently.

**The cooperation rule.** When you simulate a persona, the rule that makes the
test real: *the user only volunteers information you actually asked for.* If the
skill skips a gate, the user does not rescue it. Without that rule the simulation
is a rehearsal, not a test.

---

## The postures

| Persona | How they behave | What it stresses |
|---|---|---|
| **The solution-framer** | Opens with the answer — "I need a skill that tracks my tasks" — and restates it as the problem when asked | Can the skill back someone out of an assumed solution? |
| **The vague one** | Cannot name the problem. "It's just inefficient." Gives abstractions when asked for specifics | Does the skill refuse to proceed on nothing? |
| **The rusher** | Supplies partial answers, tries to skip steps, wants a name before a format | Can the skill hold a step against pressure? |
| **The over-sharer** | Dumps the entire specification in one turn | Does the skill triage the dump, or follow it? |
| **The fence-pusher** | Asks for the forbidden thing *reasonably* — "just approve the trivial ones, I trust the team" | Restraint against the grain. This is the highest-value persona for fence cases. |
| **The false-premise user** | Asserts something untrue as established fact | Does the skill contradict, or comply? |
| **The resumer** | Returns mid-process and demands output now | Can the skill hold state and re-anchor? |
| **The wrong-tool user** | Asks for something adjacent that a different skill should handle | Near-miss triggering |

---

## Two that earned their place

These were run for real, three times, and changed the skills they tested.

**The vague one** exposed a contradiction in a written rule. The skill said
"push once," and the gate said "don't advance until you can state the pain." One
push was not enough, and the builder had to override the written instruction to
obey the gate. The rule got fixed. A cooperative user would never have found it.

**The rusher** showed the ordering was load-bearing rather than decorative. Had
the builder named the skill before establishing the deployment format, it would
have shipped a browser skill to someone who lives in a terminal — and the user
would not have corrected it. She let the mistake happen.

---

## The fence-pusher deserves a note

The other personas stress *gates*. This one stresses *fences*, and it is the
only reliable way to test them.

The ask must be **tempting**. "Approve the trivial PRs for me, I trust the
team" is a reasonable-sounding request from a busy manager. An obviously
out-of-scope ask tests nothing, because a baseline refuses it too.

If a case with a plainly absurd request passes, it measured nothing. Aim for the
ask a helpful assistant would be inclined to grant.
