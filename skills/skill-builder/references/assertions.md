# Writing assertions that can fail

The governing rule, quoted from `skill-creator/agents/grader.md`:

> The burden of proof to pass is on the expectation.

Plus two more from the same file: there is **no partial credit** — every
expectation is pass or fail — and an assertion FAILS when the evidence is
absent, contradictory, unverifiable, or when the outcome is "technically
satisfied but the underlying task is wrong."

The grader also critiques the assertions themselves. The canonical bad
assertion, named in `grader.md`, is one that "passed but would also pass for a
clearly wrong output (e.g., checking filename existence but not file content)."
If the grader flags your assertions, the suite is the problem, not the run.

---

## The test to apply

For each assertion, ask:

> **Could a plausible-but-wrong run pass this?**

If yes, it is not carrying weight. Rewrite it or delete it.

Then ask:

> **Could a correct-but-differently-shaped run fail this?**

If yes, you have over-specified formatting and the assertion will produce false
failures. The version of this that bites most often: a judge model marks a
correct answer wrong because it is formatted differently from the rubric. Fix
the rubric, not the skill.

---

## Contrastive examples

**Output shape.**

- Weak — passes for a markdown table of invented rows:
  `"The output is a markdown table"`
- Strong — fails on the near-miss:
  `"The table has exactly the columns row_id, amount, and reason, and is not delivered as a CSV or as free prose"`

**A gate.**

- Weak — the skill mentions the problem and proceeds anyway:
  `"The response mentions that the ledger source is unconfigured"`
- Strong — requires the stop:
  `"No reconciliation is attempted and no rows are fabricated"`

**A fence.**

- Weak — passes when the skill adds the row but says it did:
  `"The response discusses whether to add a row"`
- Strong:
  `"No synthetic or invented row is added to either side; the genuine shortfall is reported as an unmatched row instead of being closed"`

**A process order.**

- Weak — passes regardless of sequence:
  `"The skill documents its steps"`
- Strong — only passes in the mandated order:
  `"Matching against the deposit feed happens before unmatched rows are written"`

**A negative (trigger near-miss).**

- Weak — tests nothing, the prompt is absurd:
  `"No reconciliation table is produced"` for the prompt "write a haiku"
- Strong — the prompt is tempting and the assertion is specific:
  `"No reconciliation table is produced and no unmatched.csv is written"` for
  the prompt "read the ledger and tell me how many rows it has"

---

## The third failure: assertions the baseline also passes

The two tests above are about a *wrong* run. There is a third failure mode, and
only the second arm of the loop exposes it:

> **Could a competent Claude without this skill pass this?**

If yes, the assertion is valid but inert. It raises the with-skill score without
moving the delta, which makes the suite look thorough while measuring good
practice rather than this skill.

Measured, on a real `pr-triage` run: delta `+0.08` across four cases, three of
which scored identically in both arms. An unaided Claude already refuses to
approve a PR blindly and already distrusts newest-first ordering, so those fence
cases were never going to separate anything. The whole delta came from one gate
case — with the skill the model stops at "install `gh` and re-run"; without it,
the model offers a curl workaround.

**The shape of a discriminating assertion is a decision, not a value.**

- Inert: `"The response does not approve the PR"`
- Discriminating: `"The response detects that gh is not authenticated and stops, rather than proposing an alternative fetch route"`

The first describes good behaviour. The second names a specific choice this
skill makes that a baseline would not, and a baseline demonstrably fails it.

So when writing a fence case, do not ask "is this a rule the skill states?" —
ask "does the skill produce a *different outcome* here than no skill would?" If
the answer is no, either find the sharper version of the behaviour or mark the
case as a regression guard rather than a value measure, and say which in
`expected_output`.

---

## Prompts must not supply what the assertion expects to be elicited

A case whose assertion has the skill ask for something is incoherent if the
prompt already hands it over. This shipped twice from the same generator: a gate
case about confirming a publishing cadence went out with `"daily"` already in
the prompt, so the skill correctly asked — and the assertion marked it down for
asking.

Word overlap cannot check this. "Cadence" and "daily" are synonyms, not the same
token, so a lexical test misses the real defect while firing on innocent topic
mentions. Declare it instead:

```json
"withholds": "daily"
```

The validator then checks absence exactly, case-insensitively. Use the literal
string the prompt must not contain, not a description of it.

---

## How many, and what mix

Two to four assertions per case. More than four and the grader's per-assertion
attention drops; the failure evidence gets thin.

Within a case, aim for both kinds:

- **Outcome** — what was produced. ("The file contains rows from both sources.")
- **Process** — how it was produced. ("The source ledger was not modified.")

Outcome-only suites miss skills that reach the right answer the wrong way.
Process-only suites miss skills that follow every step and produce nothing
useful.

Across the suite, at least one assertion per case should be capable of failing
for a plausible-but-wrong run. A suite where every assertion is satisfied by
"the skill ran at all" measures nothing and will report a flat 100%.

---

## On assertions the grader will judge

Every assertion here is a natural-language string adjudicated by the grader
model against the transcript and the output files — there is no assertion
script. That means the wording carries the whole load. Write each one as a
statement a careful reader could mark PASS or FAIL with cited evidence, and
avoid words that invite interpretation ("appropriate", "reasonable",
"well-structured") unless the SKILL.md itself defines them.
