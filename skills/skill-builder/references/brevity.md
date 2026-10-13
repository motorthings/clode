# Brevity: output the consumer can act on

A lens, not a rule. Reach for it when a skill's output is long, thorough, and
read by nobody.

**The diagnosis.** Bloat comes from producer uncertainty, not consumer need. You
pad when you don't know what the reader will do with it, so you cover everything
in case one thing was wanted. Brevity is therefore not a discipline applied at
the end — it's evidence that you know who is downstream. A skill that cannot be
brief has not answered the consumer question in `roles.md`.

---

## The test

> **What does the reader do in the next five minutes because they read this?**

If nothing, cut the whole thing. Not shorten. Cut.

Run it against every section. Most long documents have one section that carries
the decision and several that exist because the producer was unsure which one it
was.

---

## Cut, always

- The request restated. They know what they asked.
- The method narrated. "I first fetched, then I grouped" is your work, not theirs.
- Options considered and rejected — unless the rejection changes the decision.
- The summary of the summary.
- Caveats nobody asked for.
- Tool and vendor names, unless the reader is the one who'll run the tool.
- Symmetric coverage of unequal things.

## Keep

- The decision, or the action.
- The one fact that changes it.
- What the reader could not have inferred on their own.

---

## The structure

Borrowed from Smart Brevity, and it holds up as an output contract a skill can
carry:

```
The one thing
  A sentence, in the reader's vocabulary. No preamble.

Why it matters
  One or two lines, tied to what the reader does — not to what you found.

The specifics
  The shortest form that is still actionable. A table beats prose.
  Numbers beat adjectives.

Go deeper
  Optional, and only when there is somewhere real to go.
```

**The three-line check.** Read only the first line of each paragraph. If the
piece doesn't survive that, the structure is wrong, not the prose.

**On numbers.** "The queue has 31 PRs and 4 matter" is actionable. "The queue is
quite large" is not. Adjectives are where unmeasured claims hide — prefer the
number you have over the characterization you'd guess.

---

## Asymmetric coverage

The failure people miss. A list where the critical item and the ninth item each
get one line has buried the critical item. **The top item gets more space.**

This applies to severity, to confidence, and to length. If everything is
presented with equal weight, the reader has to re-derive your ranking from
nothing — which is work you were supposed to have done.

The corollary: if two things genuinely are equal, say so. Do not manufacture
asymmetry to look decisive.

---

## Asserting it

Brevity is partly mechanical, so it can be tested rather than merely encouraged:

- `"The first line states the action, not the context"`
- `"The output does not restate the request"`
- `"No recommendation is preceded by more than two lines of setup"`
- `"The most severe item appears first"`
- `"Every shortlist entry carries a recommended action"`

Mechanical backstops, for the cases where a judge is too lenient:

- Ratio of actionable lines to total lines.
- Words before the first imperative.
- Entries in the output against items found in the input — a shortlist that
  matches the input size is not a shortlist.

**The closure worth remembering.** `pr-triage`'s output contract — number,
title, one-line reason, recommended action, nothing else — is a brevity
contract. That is precisely why it discriminated against the baseline: a
baseline writes a list, and the skill writes the list its consumer can act on
without a second pass. Compression to what the consumer needs is the same
property as discrimination. When a case splits on output shape, look here first.
