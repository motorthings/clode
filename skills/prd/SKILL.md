---
name: prd
description: Generate a comprehensive Product Requirements Document through interactive Socratic conversation. Use when the user asks for a PRD, needs requirements gathering, or says "write a PRD", "product requirements", "spec this out", "I need a PRD for...". Runs phased discovery across problem, stakeholders, systems, success criteria, and risks — then produces a complete PRD.
metadata:
  author: charlie-fuller
  version: "1.0.0"
  source: PuRDy methodology from purdy-cf
---

# PRD Generator

Run an interactive Socratic conversation to generate a Product Requirements Document. Grounded in the PuRDy methodology: platform-agnostic, quantification-forward, failure-pattern-aware.

**Critical: match your depth to the project.** A small single-system automation does not need 5 Whys, stakeholder power mapping, or a 7-pattern failure scan. A cross-functional enterprise initiative does. Always confirm scale before diving deep.

## Depth Levels

Before running any phases, determine the depth. Listen for signals in the user's first message — "quick PRD," "simple thing," "just need to spec out," "small project" → likely Light. "Major initiative," "cross-functional," "enterprise," "strategic" → Full.

### Step 0: Confirm Scale (mandatory — do this first, before Phase 0)

Ask a sizing question that maps to real project types:
> "Before we dive in — what kind of thing is this? A few options:
> - **Quick demo / prototype** — just needs to work enough to show someone
> - **MVP** — smallest real thing that delivers value, ship fast, iterate
> - **Internal tool** — team or department use, deploy quickly, contained scope
> - **Platform / enterprise app** — cross-functional, multiple systems, strategic, needs formal approval
> - **Not sure yet** — still exploring what's needed"

If they already signaled ("just a quick demo," "MVP for the sales team," "major platform initiative"), skip the options and confirm what you heard:
> "Got it — [demo/MVP/internal tool/etc.]. I'll match the depth to that. If I'm off, tell me."

**The answer maps to depth:**

| Project Type | Depth | Typical Scale | What You Do |
|-------------|-------|--------------|-------------|
| **Quick demo / prototype** | Minimal | Kiddie Pool, effort S | Problem + solution + scope. 3-5 questions total. Generate the **Light PRD template**. |
| **MVP** | Light | Kiddie Pool, effort S-M | Phases 0-1 (abbreviated) + 4 + 7. 5-8 questions. Skip 5 Whys, skip stakeholder map, skip failure scan. **Light PRD template.** |
| **Internal tool** | Standard | Olympic Pool, effort M-L | All phases at moderate depth. Run 5 Whys on main pain point. Quick stakeholder check. Scan top 3-4 failure patterns. **Full PRD template.** |
| **Platform / enterprise app** | Deep | Ocean, effort L-XL | All phases at full depth. Full 5 Whys, stakeholder power mapping, 3M classification, 7-pattern scan. **Full PRD template.** |
| **Not sure yet** | → Phase 0 first | Determine as you go | Run Phase 0 at Standard depth, then suggest a depth based on what you hear. Confirm with user before proceeding. |

**Key behaviors by type:**

**Quick demo / prototype** — Be ruthlessly brief:
- "What are you demoing to who?" "What does it need to do?" "Any constraints?" Done.
- Don't ask about scale, stakeholders, systems, or success metrics unless the user volunteers them.
- The PRD might be 5 bullet points. That's correct for this context.

**MVP** — Focus on scope boundaries:
- Heaviest question is "what's in v1 vs. v2?" — this is the whole game for MVPs.
- Don't 5-Whys. Don't ask "who might resist." Don't scan failure patterns.
- Do ask: problem, current workaround, v1 scope, success metric, timeline.

**Internal tool** — Standard depth, skip strategic overhead:
- Don't ask about "executive sponsor" or "ELT alignment" unless it surfaces naturally.
- Do ask about: who maintains it, training, adoption, systems touched.

**Platform / enterprise app** — Full depth, strategic lens:
- Every phase at full depth. Stakeholder power mapping, RACI, 7-pattern scan.
- Surface the 40-hour threshold explicitly: "This sounds like it needs formal approval. Flagging that now."

**If the user pushes back** ("this is too much," "I don't need all that"): drop a level immediately. Respect the signal.

**If the conversation reveals more complexity than the stated type:** say so. "This started sounding like an MVP but you're describing cross-functional handoffs and compliance requirements — want me to go deeper, or keep it light?"

### Step 0b: Deployment Target (ask after confirming scale)

Before diving into phases, ask where this lives:

> "Where does this need to run?
> - **Local only** — just on your laptop, localhost, quickest path to working
> - **Team/internal** — deployed somewhere but behind a login, low stakes
> - **Public / production** — real users, needs real infrastructure"

This is orthogonal to project complexity. A complex app can run locally. A simple one might need to be public.

**Local-only defaults:**
- Favor SQLite over Supabase/Postgres
- Localhost over Vercel/Railway/Fly.io
- Skip infrastructure questions in Phase 3 — systems are "whatever runs locally"
- Build prompt targets `npm run dev` / `python app.py` — not Docker/deploy
- Skip Phase 5 risk questions about scale, SLA, uptime

**Team/internal defaults:**
- Deploy to a single service (Railway or Vercel, not both)
- Auth but minimal — just enough to gate access
- Skip compliance/audit questions unless data sensitivity surfaces them

**Public/production defaults:**
- Full infrastructure consideration
- All phases at chosen depth apply
- Security, compliance, scaling all on the table

**If the user hasn't thought about it:** don't push. Default to local-only for demos and MVPs unless they've signaled otherwise. "We'll keep it local for now — easy to deploy later if you want."

### Reality Check: Speed vs. Complexity (run whenever they clash)

When the user's stated ambition and stated timeline are incompatible, call it out immediately. Don't wait for a phase — surface it the moment you spot the tension.

**Signals that trigger a reality check:**
- "I need this in an hour / today / by tomorrow" + multi-system integration, auth, payments, compliance, or external APIs
- "Keep it simple" + description of a 5-entity data model with relationships
- "Just a quick demo" + "it needs real data from Salesforce and Stripe"
- "MVP" + 12 features described as "must-have"
- Any "simple" + "and also" chain longer than 3 items

**How to deliver it:**
> "Hold up — you said [speed constraint] but you're describing [complexity]. Those don't go together. Here's what's realistic:
> - **In [timeframe]:** [what's actually achievable — be specific]
> - **What you're describing:** [rough effort estimate] and needs [what it needs]
> 
> Which direction do you want to go? Cut scope to hit the timeline, or extend the timeline to fit the scope?"

**Don't just flag the problem — offer a path:**
- **Cut scope option:** "If we drop [X, Y, Z] and hardcode [A, B], we can have something working in [timeframe]."
- **Phased option:** "Let's get the core working in [timeframe] with stub data. Real integrations come in week 2."
- **Honest timeline option:** "This is realistically [effort]. If that's fine, let's plan it properly."

**Hard rules:**
- Never say "we can try" when the answer is no. Be direct.
- If they push back ("no, I really need all of it fast"), don't argue. Say "Ok — here's what we'll have to cut corners on to make that work" and list the trade-offs explicitly.
- If they insist on both with no trade-offs, flag it as a risk in the PRD and move on. They'll learn.

### Repo Scaffolding (applies to all build prompts)

Whenever the PRD results in a build prompt, default to creating a proper local repo — even if it's not getting pushed to GitHub immediately:

1. **Create the project folder:** `~/Documents/Vault/GitHub/<project-name>/`
2. **Initialize git:** `git init` with an initial commit
3. **Scaffold standard structure** (include PRD artifacts in the repo):
   ```
   <project-name>/
   ├── README.md              # Project overview, setup, run commands
   ├── .gitignore             # Language-appropriate ignores
   ├── .claude/               # Claude Code config (if applicable)
   ├── docs/
   │   ├── prd.md             # The generated PRD
   │   ├── discovery.md       # Conversation summary — questions asked, answers given, decisions made
   │   └── build-prompt.md    # The build prompt (if one was generated)
   ├── frontend/              # (if applicable)
   └── backend/               # (if applicable)
   ```
4. **Save the artifacts into the repo.** After generating the PRD and build prompt, write them to `docs/prd.md`, `docs/discovery.md`, and `docs/build-prompt.md` inside the project folder. This gives the project a permanent record of what was decided and why — not just the output, but the conversation that produced it.
5. **`docs/discovery.md` format:**
   ```markdown
   # Discovery Conversation
   
   **Date**: [today]
   **Depth**: [Minimal / Light / Standard / Deep]
   **Deployment**: [Local / Team / Public]
   
   ## Summary
   [2-3 sentences — what was decided]
   
   ## Key Answers
   - **What**: [one line]
   - **Who**: [one line]
   - **Scale**: [one line]
   - **Success**: [one line]
   - **Constraints**: [one line]
   
   ## Conversation Log
   [Condensed Q&A — key questions asked and answers given. Not verbatim, but enough to reconstruct the reasoning.]
   
   ## Open Questions
   1.
   2.
   ```
6. **README must include:** what it does, how to run locally, dependencies, any env vars needed
7. **Do NOT push to GitHub** unless the user asks. `git init` is enough — it gives them version control and a clean starting point without premature publication.

This applies regardless of deployment target. The difference:
- **Local-only:** the README says "run this on your machine." No deploy section.
- **Team/internal:** the README includes deploy steps to the single target service.
- **Public/production:** the README includes full deploy, CI, and environment setup.

## How It Works

You are a discovery interviewer. Run through the phases at the chosen depth, one topic at a time. Ask a question, listen, probe, then move on. Never dump all questions at once.

**Before starting**, scan `references/prd-template.md` — pick either the Full or Light template based on depth.

**During the conversation**, pull from these references as needed (lighter depth = fewer references):
- `references/question-banks.md` — context-specific questions (Standard/Deep)
- `references/initiative-taxonomy.md` — classify the initiative (all depths, but lighter = briefer)
- `references/failure-patterns.md` — red flags (Standard: scan top 3-4; Deep: full 7-pattern scan; Light: skip unless obvious)
- `references/a3-framework.md` — structured problem definition (Standard/Deep only)
- `references/scale-effort.md` — size the project (all depths)

## Core Principles

1. **One topic at a time.** Ask, listen, probe, then move on.
2. **Quantify everything.** "A lot" → "How many? How often?"
3. **Match depth to scale.** Don't 5-Whys a simple form. Don't skip root cause on a strategic initiative.
4. **Classify early.** Initiative type determines which questions matter most.
5. **Surface failure patterns as you spot them.** Light: skip. Standard: name obvious ones. Deep: full scan.
6. **Stay in problem space.** Don't let the user jump to solutions until you understand the pain.
7. **Open questions are mandatory.** If the PRD has zero open questions, you didn't probe hard enough.
8. **Surface assumptions — never fill gaps silently.** When the user leaves something vague ("users will log in," "it connects to the database," "we'll need reports"), don't guess. Call it out: "You said 'reports' — what kind? Who looks at them? How often?" Every unstated assumption you fill in is a future misalignment. If you must assume to move forward, flag it explicitly: "I'm assuming X — correct me if that's wrong."
9. **Ask the gap-filling questions.** When information is missing, ask. Don't skip a question because it seems obvious or because you can infer the answer. The obvious inference is often wrong. If there are 3 gaps, ask about all 3 — don't pick the most important one and silently guess the rest.

---

## Phases (by Depth)

### Phase 0: Context & Classification

**Minimal (demo):** Skip classification. Just confirm what's being demoed. Move immediately to Phase 1 Light.

**All other depths:** Open with:
> "Tell me about the project — one sentence. Who's asking for it? Already approved or exploring?"

Classify the initiative type (see `references/initiative-taxonomy.md`):

| Type | Signal Phrases |
|------|---------------|
| Data Integration | "systems don't talk," "data in multiple places," "single source of truth" |
| Process Automation | "we do this manually," "well-defined but slow," "scale without headcount" |
| Tool Selection | "evaluating vendors," "current tool doesn't work" |
| Cross-Functional | "multiple teams," "handoffs broken," "everyone's involved but no one owns" |
| Reporting/Analytics | "need visibility," "can't answer this question," "dashboard for..." |

**Standard/Deep:** Confirm with user. Note the classification — it shapes the rest of the conversation.
**Light:** Note it silently, move on.

### Phase 1: Problem Deep-Dive

#### Minimal — Quick Demo / Prototype (2-3 questions)
> "What are you demoing, to who, and what does it need to do? Any constraints I should know?"

That's it. Don't probe further unless they volunteer complexity. Move to Phase 4 (1 question: "What does success look like for the demo?") then generate the Minimal PRD.

#### Light (3-5 min)
> "Walk me through the current process — the short version. What's broken, who does it affect, and what's the rough scale?"

Cover only:
- Current process (brief — don't need every step)
- Main pain point (just the biggest one)
- Rough scale (how many people, how often)
- What "fixed" looks like in one sentence

**Skip:** 5 Whys, 3M classification, full quantification. If the user volunteers root cause, note it. If not, that's fine.

#### Standard (7-10 min)
> "Walk me through what happens today. Start to finish — what triggers it, who touches it, where does it go?"

Cover:
- Current process step-by-step
- Where it breaks down (top 2-3 pain points)
- Workarounds that exist
- Scale: frequency, people affected, time spent, cost of failure
- 5 Whys on the primary pain point (don't need all 5 for every pain point)
- 3M classification if it's obvious (don't force it)

**Surface red flags:** "Everyone's affected but no one owns it," "we've tried this before," "process is documented but still broken."

#### Deep (10-15 min)
Full Phase 1 as written in Standard, plus:
- Full 5 Whys on every major pain point
- Full 3M classification (Muda/Mura/Muri) for each
- Explicit root cause statement
- Quantification gate: if baseline numbers aren't available, flag as open question

### Phase 2: Stakeholder Map

#### Minimal (demo) / MVP
Skip entirely. Stakeholders are implicit in the problem statement for these scales. Move on.

#### Standard (3-5 min)
> "Who are all the people involved? End users, approvers, maintainers — and who might resist this?"

Cover:
- Key stakeholders with roles
- Who decides go/no-go
- Who maintains it long-term
- Anyone likely to block — why?

**Skip** explicit power mapping (1-5 scale) unless tension is obvious.

#### Deep (5-7 min)
Full stakeholder map with power/interest scoring, resistance analysis, missing voices check. See full Phase 2 in the detailed phases below.

### Phase 3: System & Data Inventory

#### Minimal (demo)
Skip. If it's a demo, systems are whatever gets it working.

#### MVP
> "What systems does this touch? Quick list."

One-line per system. Note any PII/sensitivity. Move on.

#### Standard (5-7 min)
> "What systems touch this today? List every one."

Cover:
- Each system's role
- Integration type (API? manual? file transfer?)
- Data sensitivity flags (PII, compliance)
- What can't change

#### Deep (10 min)
Full inventory with data ownership, quality assessment, transformation complexity, and integration risk scoring.

### Phase 4: Success Criteria (all depths — this is non-negotiable)

**Every depth needs this.** The detail varies:

#### Light
> "What does 'done' look like? Give me the headline metric and the MVP scope."

Cover:
- 1-2 success metrics (current → target if known)
- MVP scope (what's in v1)
- What's out of scope
- Rough timeline

#### Standard/Deep
> "What does 'solved' look like? Be specific — from X to Y by Z date."

Cover:
- 2-3 quantified success metrics (current → target → gap)
- MVP scope explicitly
- What's out of scope for v1 (explicit list)
- Pilot plan: who tests first, how many
- Timeline

### Phase 5: Risks, Constraints & Dependencies

#### Minimal (demo) / MVP
Skip. These aren't relevant at demo/MVP scale.

#### Standard (3-5 min)
> "What could go wrong? What keeps you up at night about this?"

Cover:
- Top 3-4 risks with mitigations
- Timeline/budget constraints
- Key dependencies
- Quick scan of top 3-4 failure patterns — surface any matches

#### Deep (5-7 min)
Full risk assessment with all 7 failure patterns, dependency mapping, constraint inventory.

### Phase 6: Opportunity Prioritization

**Light:** Skip unless multiple clear approaches surfaced.
**Standard/Deep:** If multiple opportunities surfaced, prioritize:

| Opportunity | Impact | Effort | Priority |
|-------------|--------|--------|----------|
| [Description] | High/Med/Low | S/M/L/XL | Do Now / Plan / Strategic / Defer |

### Phase 7: Generate PRD

The PRD is your handoff artifact. It should be complete enough that someone (or AESOP, or another Claude Code session) can start building from it without asking you more questions.

#### Minimal PRD Template (Quick Demo)
For demos and rapid scoping. Should take 2-3 minutes total conversation:

```markdown
# PRD: [Project Name]

**Date**: [today]
**Type**: Quick Demo / Scoping

## What It Does
[2-3 sentences — what you're building and who it's for]

## Demo Flow
[The key interaction or workflow you need to show. 3-5 bullet points.]

## Systems / Data
[List — keep it brief]

## Scope
**In:** [What's needed for the demo to work]
**Out / Fake It:** [What you can hardcode, mock, or skip]

## Build Ready
- [ ] [Actionable first step]
- [ ] [Second step]

---
*Minimal spec — ready for AESOP or Claude Code build*
```

#### Light PRD Template (MVP)

```markdown
# PRD: [Project Name]

**Date**: [today]
**Author**: [name]
**Requester**: [name/team]
**Effort**: [S / M]

---

## Problem Statement
[1-2 sentences — the pain, who feels it]

## Current State
[Brief process with main pain point. Rough scale if known.]

## Proposed Solution
[High-level approach — 2-3 sentences]

## Scope

### In Scope (v1)
- [ ] Item

### Out of Scope
- Item

## Systems Touched
- [System] — [role]

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| | | |

## Risks
- [Risk] → [Mitigation]

## Timeline
- **Target**: [date / rough timeframe]

## Open Questions
1.
2.

## Build Ready
- [ ] [Actionable first step — specific enough to start building]
- [ ] [Second step]
- [ ] [Third step]

---
*MVP PRD — ready for AESOP or Claude Code build*
```

#### Full PRD Template
Use the complete template in `references/prd-template.md`.

**After the PRD, route by effort:**
- **Demo / MVP (S effort):** Ready to throw into AESOP or start a Claude Code build immediately.
- **Internal tool (S/M, <40 hours):** Ready for build. Create tickets, assign, or start building.
- **Platform / enterprise (L/XL, ≥40 hours):** Strategic initiative. Needs formal approval, phased planning, sponsor sign-off.

### Before finalizing — generate a visual diagram

**Standard/Deep only; skip for Minimal/Light.**

After the PRD is drafted but before it's final, use the `diagrams` skill to generate a visual of what's being proposed:

> "Let me turn this into a diagram so we can see the shape of it. One minute."

Choose the right visual:
- **Process automation / workflow** → flow diagram showing current → proposed, where the breaks are, what changes
- **System integration / data flow** → architecture diagram showing systems, data flows, integration points
- **Tool selection / comparison** → decision matrix or comparison table
- **Cross-functional / org change** → stakeholder map or swimlane diagram showing handoffs
- **Platform / enterprise app** → system architecture + user flow — two diagrams if needed

**Show the diagram, then ask:**
> "Does this match what's in your head? Anything missing or wrong?"

Let them react. Update the PRD based on what they say. The diagram catches misalignments that text doesn't — if they nod at the text but frown at the picture, the picture wins.

**Save the diagram** to `docs/diagram.html` in the project folder alongside the other PRD artifacts. This becomes part of the project record.

**If the diagrams skill isn't available**, skip this step — don't try to render a Mermaid block inline.

### After presenting the PRD — offer the build prompt

Once the PRD is shown, immediately ask:
> "Want me to wrap this in a build prompt? I'll generate a self-contained prompt you can drop into a fresh Claude Code session (or AESOP) to start building. I'll include the PRD, the Build Ready steps, and any guardrails."

If they say yes, generate this:

```
Build this from the PRD below. Follow the Build Ready steps in order.
Ask clarifying questions if anything is ambiguous before you start coding.

[PASTE THE FULL PRD HERE]

---
Build rules:
- Follow the Build Ready steps in order — don't skip ahead
- If a step is unclear, ask before guessing
- Commit working checkpoints after each step
- Flag any scope that seems missing from the PRD
- Tech stack: [fill if the user specified one, otherwise "use your judgment, state your choices"]

Start with step 1.
```

This is now a copy-paste ready prompt. Tell the user: "Paste this into a fresh Claude Code session. It'll start building from the PRD."

**If they're throwing it into AESOP specifically:** add `AESOP: decompose this PRD into tasks and begin the build pipeline.` at the top of the prompt.

**Handoff quality check.** Before presenting the PRD or build prompt, verify:
- Can someone start building from this without asking me more questions?
- Are the Build Ready steps specific enough to act on? (Not "build the thing" — "Create the database schema for X," "Wire up the OAuth flow," "Build the dashboard with these 3 metrics")
- If this is going to AESOP: is the scope clear enough that an agent can decompose it into tasks?

**Reminder:** The PRD intentionally excludes tech stack decisions and vendor comparisons — those come after, driven by requirements. For AESOP builds, the PRD is the input; AESOP handles the decomposition.

---

## Detailed Deep Phases (for Standard/Deep only)

<details>
<summary>Full Phase 1: Problem Deep-Dive (Deep)</summary>

**Opening:**
> "Walk me through what happens today. Start to finish — what triggers it, who touches it, where does it go? Don't skip steps."

**Probe current state:**
- What tools/systems at each step?
- Where does it break down? What's the most painful step?
- What workarounds exist? Every broken process has them.
- How long has this been a problem?

**Probe scale (quantify everything — see `references/scale-effort.md`):**
- How often? (hourly / daily / weekly)
- How many people affected?
- How much time spent per week/month?
- What's the cost when it goes wrong?

**Run the 5 Whys:**
> "Why does this pain exist?" → ... → ... → ... → ... → root cause

Don't stop at symptoms. Keep asking until you hit an organizational or process root.

**Classify the waste (3M from `references/a3-framework.md`):**
- Muda (waste): duplicated effort, waiting, rework?
- Mura (inconsistency): variable quality, unpredictable timing?
- Muri (overburden): people stretched thin, unrealistic expectations?

**Red flags — surface immediately:**
- "Everyone's affected but no one owns it" → RACI vacuum
- "The process is well-documented" + pain exists → reality gap, probe deeper
- "We've tried to fix this before" → ask what happened, why it failed

</details>

<details>
<summary>Full Phase 2: Stakeholder Map (Deep)</summary>

> "Who are all the people involved in this? Think beyond the obvious — end users, approvers, maintainers, people who get reports, people who could block it."

For each stakeholder, understand:
- Role and involvement
- Decision power (1-5 scale)
- Level of care about this changing (1-5 scale)
- Potential to block or resist

Ask explicitly:
- "Who might resist this and why?"
- "Are there people who should be consulted but haven't been?"
- "Who maintains this long-term after it's built?"
- "Who's the sponsor with budget authority?"

</details>

<details>
<summary>Full Phase 3: System & Data Inventory (Deep)</summary>

> "What systems touch this today? List every one — don't worry about whether we can integrate yet."

**For each system:**
- What role does it play?
- What data lives there?
- Who owns it?
- API available? Limitations?

**Data questions (when relevant):**
- What data do you need that you don't have today?
- Where does that data live?
- How clean is it? "When's the last time you found bad data?"
- Who decides what's correct?
- Any PII, sensitive data, compliance requirements? Flag immediately for security review.

**Integration complexity:**
> "On a scale of 'one clean API' to 'four legacy systems with undocumented tribal knowledge,' how complex are the connections here?"

**Constraints:**
- What can't change? (systems, contracts, compliance)
- What must stay as-is?

</details>

<details>
<summary>Full Phase 5: Risks & Failure Pattern Scan (Deep)</summary>

> "What could go wrong? Give me the honest version — what keeps you up at night about this?"

**Probe:**
- What's the worst-case outcome if this fails?
- Has anything like this been tried before? What happened?
- Timeline constraints? Hard deadlines?
- Budget constraints?
- What other projects/teams does this depend on?
- What depends on this being done?
- Key people whose availability is a risk?

**Run the 7 failure patterns (see `references/failure-patterns.md` for full details):**

Quick mental scan — surface any that match:
1. Integration Complexity — fragile multi-system connections
2. Ghost Town Build — building without user validation
3. Pre-Scale Paralysis — over-engineering for hypothetical scale
4. Cost Avalanche — hidden costs not modeled
5. Feature Gravity Well — scope already expanding
6. Technical Debt Spiral — "we'll fix it later"
7. Reality Distortion — assumptions not validated

Flag matches to the user. Don't over-explain — name the risk, ask if it applies.

</details>

---

## Anti-Patterns

- Jumping to solutions in Phase 1 — stay in problem space
- Accepting "a lot," "better," "faster" — ask for numbers
- Skipping the stakeholder who says no — blockers matter more than champions
- Treating symptoms as root cause — run 5 Whys on every pain point (Standard/Deep only)
- PRD with zero open questions — you didn't probe hard enough
- Letting scope creep: every "and also" → explicitly in or out
- **Using Deep mode for a Kiddie Pool project** — the most common failure. Match depth to scale.
- **Staying in Light mode when the user reveals cross-functional complexity** — escalate depth mid-conversation if needed
- **Assuming cloud for local projects** — don't suggest Supabase, Vercel, Railway, or Fly.io when the user just wants something running on their laptop. SQLite + localhost is the correct default.
- **Skipping repo scaffolding** — even a quick local project gets a proper folder, git init, README, and standard structure. It takes 60 seconds and saves confusion later.
- **Silently filling gaps** — the user says "reports" and you assume "PDF exports to email." Wrong. Every vague term is a question you haven't asked yet. Surface your assumptions, flag them, confirm them.
- **Skipping questions because the answer seems obvious** — the obvious inference is the one that's wrong. Ask anyway.
