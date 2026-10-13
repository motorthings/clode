# Roles: what the work is actually like

Not a checklist. A lens to reach for when a skill is thin and you suspect the
reason is that it was built for the stated task rather than the real one.

**How to use it.** When someone describes what they want, find the closest role
below. Read the *contends with* and *root cause* lines. Ask yourself whether the
skill in front of you is aimed at the task or at the cause. Sometimes the answer
is "neither, this person isn't like any of these" — that's a fine answer, and it
means you've found an entry worth adding.

**The question underneath all of it:**

> If this were solved perfectly, what stops happening?

People answer that in concrete nouns — a specific bad Tuesday — where they'll
answer "what do you want?" only in task language.

**Nothing here is enforced.** The shape below is a reading courtesy, not a
contract. An entry with four lines instead of six is not a broken entry.

---

## The shape

```
Role
  Contends with   the recurring pressure of the job
  Typical ask     what they'd actually say they want
  Root cause      what's underneath, usually not what they named
  Value           what changes if the cause is addressed
  Inputs          where the material comes from, and who owns its quality
  Consumer        who receives the output, and what they do with it next
  Counter-example the generic solution that solves the ask and misses the cause
```

**The counter-example is the load-bearing line.** It's what separates a root
cause from a task description. If you can't name the generic solution this entry
is warning against, you haven't found the root cause yet — and neither, probably,
has the skill.

**The consumer line is the one most often missing.** Three parties are usually
in play and they are rarely the same person:

- **Requester** — asks for the skill
- **Operator** — runs it
- **Consumer** — receives what it produces

A skill tuned to please the requester can fail the consumer, and nothing in an
artifact-shape assertion would catch it. The test that settles it:

> **What does the consumer do differently because they got this output?**

If you can't answer, the output is decorative — produced, filed, and read by no
one. And note the consumer is often a *counterparty* in one of the handoffs at
the bottom of this file, which is the same boundary seen from the other side.

---

## Engineering / developer

```
Contends with    work that expands after it's estimated, and review latency
                 from people who aren't blocked by the thing you're blocked on
Typical ask      "a skill that reviews my PRs" / "help me write tests"
Root cause       the estimate covers the build, not the waiting. The queue
                 belongs to someone whose priority is not your priority.
Value            shipping without the queue owning you
Counter-example  a code-review bot. Reviews faster; changes nothing about who
                 is waiting on whom.
```

## Product

```
Contends with    owning an outcome with no direct authority over the people
                 who deliver it
Typical ask      "a skill that writes my PRDs"
Root cause       intent has to survive translation into specs, and it doesn't.
                 What ships is a rendering of the intent by someone who wasn't
                 in the room.
Value            what ships is what was decided
Counter-example  a PRD template. Produces the document that gets translated
                 wrong.
```

## Design

```
Contends with    taste judged by people who cannot state the criteria
Typical ask      "a skill that generates variants"
Root cause       feedback arrives as preference, not criteria. "I don't like it"
                 is unanswerable, so rounds never converge.
Value            decisions that can be defended after the fact
Counter-example  a variant generator. Produces more options to be rejected
                 without reasons.
```

## Sales

```
Contends with    quota measured on the close, relationships built on trust, and
                 a system that wants both recorded
Typical ask      "a skill that writes my follow-up emails"
Root cause       the follow-up is a memory tax. What decays is the thread, not
                 the email.
Value            no deal dies of silence
Counter-example  an email template. Writes the follow-up; never tells you who
                 has gone quiet.
```

## Marketing

```
Contends with    volume demanded against attribution that can't be proved
Typical ask      "a skill that turns one post into ten"
Root cause       the pipeline assumes distribution exists. The real cost is
                 repurposing, and the real risk is that none of the ten sound
                 like anyone.
Value            consistent presence without a content treadmill
Counter-example  a repurposing script. Produces ten artifacts from one, none of
                 them yours.
```

## Customer support / success

```
Contends with    severity defined by the customer, priority defined by
                 engineering
Typical ask      "a skill that drafts my replies"
Root cause       two organisations with different definitions of urgent, and no
                 shared language between them
Value            the customer's sense of urgency survives translation
Counter-example  a reply generator. Answers faster; doesn't make the answer
                 travel with its urgency intact.
```

## Finance

```
Contends with    a close date that depends on other people's data entry
Typical ask      "a skill that reconciles my accounts"
Root cause       the close is a dependency chain. The part that fails is
                 upstream of anything you can compute.
Value            knowing early which numbers will be late
Counter-example  a reconciliation tool. Reconciles what arrived; says nothing
                 about what won't.
```

## People / HR

```
Contends with    accountability for culture with no authority over managers
Typical ask      "a skill for onboarding"
Root cause       onboarding is a handoff chain. HR owns the outcome and none of
                 the steps.
Value            no new hire arrives to a broken first week
Counter-example  an onboarding checklist. Tracks the steps; doesn't notice the
                 chain is stuck.
```

## Legal

```
Contends with    review as a bottleneck that everyone routes around
Typical ask      "a skill that reviews contracts"
Root cause       they're asked to approve outcomes they had no part in shaping,
                 and by the time they see it the deal is done
Value            risk surfacing early enough to change the decision
Counter-example  a clause linter. Flags clauses; doesn't change when anyone
                 consults you.
```

## Operations

```
Contends with    being the last to know about changes made upstream
Typical ask      "a skill that tracks my tasks"
Root cause       ops absorbs variance other functions create. The task list is
                 a symptom of not seeing the variance early.
Value            variance visible before it has to be absorbed
Counter-example  a task board. Records what already happened to you.
```

## Supply chain

```
Contends with    inventory truth split across systems and counterparties
Typical ask      "a skill that forecasts demand"
Root cause       the forecast is only as good as data other people enter for
                 reasons of their own
Value            surprises that arrive with time to act on them
Counter-example  a forecasting model. Forecasts on top of the same bad inputs.
```

## Data

```
Contends with    everyone wants numbers, nobody agrees what the words mean
Typical ask      "a skill that builds my dashboards"
Root cause       the definition is contested, not the query. A faster dashboard
                 of a disputed metric settles nothing.
Value            one number people act on
Counter-example  a dashboard builder. Ships the contested number faster.
```

---

## Handoffs: where most of it actually lives

People rarely bring a role problem. They bring a **boundary** problem, and
describe it as an intra-role one. Each of these has a single signature: *the two
sides hold different definitions of done.*

| Handoff | The failure |
|---|---|
| Sales → Delivery | promised vs buildable; both sides believe they agreed |
| Product → Engineering | intent vs spec; "done" means two different things |
| Operations → Finance | the close waits on someone else's entry |
| People → IT | onboarding begins before provisioning finishes |
| Marketing → Sales | leads vs qualified leads, an unbounded disagreement |
| Support → Engineering | severity on their scale vs priority on ours |
| Supply chain → Finance | inventory truth lives in two systems |
| Legal → everyone | review as a bottleneck people route around |

When a request describes a checklist, a tracker, or a template, look for the
handoff underneath it. Something crossing a boundary with no owner is the most
common real cause — and it's the same shape as the notes-doc problem, where a
commitment left a call and never arrived anywhere.

---

## Keeping this from rotting

The roles barely change. The tooling churns every few years, so an entry that
names a system has a short life. Write about the pressure; leave the vendor out.

**Is this line still true in 1995? In 2035?** If not, it's an instance detail —
useful in the moment, wrong for this file.

Which means: you'll rarely need to *update* an entry. You'll need to add one
when you meet a role this file doesn't describe, or when someone's root cause
doesn't match the role you filed them under. That's the signal, and it's worth
acting on while you remember the conversation.
