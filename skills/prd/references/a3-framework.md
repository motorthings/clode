# A3 Problem Solving Framework

Every pain point should be expressible as: **Current State → Target State → Gap → Root Cause → Countermeasures.**

---

## The A3 Structure

```
┌──────────────────────────────────────────────────────────┐
│  A3: [PROBLEM TITLE]                                     │
│  Owner: [Name]  Date: [Date]                             │
├──────────────────────────────────────────────────────────┤
│ 1. BACKGROUND                  │ 5. COUNTERMEASURES      │
│ Why this matters now           │ Actions to close gap    │
│                                │                         │
├────────────────────────────────┤                         │
│ 2. CURRENT STATE               │                         │
│ Measured reality today         ├─────────────────────────┤
│                                │ 6. IMPLEMENTATION PLAN  │
├────────────────────────────────┤ Who, What, When         │
│ 3. TARGET STATE                │                         │
│ Specific, measurable goal      ├─────────────────────────┤
│                                │ 7. FOLLOW-UP            │
├────────────────────────────────┤ How we'll verify        │
│ 4. GAP + ROOT CAUSE            │                         │
│ Why gap exists — 5 Whys        │                         │
└──────────────────────────────────────────────────────────┘
```

---

## Section Guidance

### 1. Background (The "Why Now")
Establish context and urgency. Business impact if not addressed. Connection to strategic priorities.

**Good:** "Sales spends 15 hrs/week on manual forecast compilation, reducing customer-facing time 20%. CFO requires weekly forecasts — non-negotiable."

**Bad:** "We need better forecasting because it would be nice."

### 2. Current State (Measured Reality)
Numbers, not adjectives. Process steps with time/effort. Who is affected and how.

**Quantification requirements:**
| Element | Must Have | Nice to Have |
|---------|-----------|--------------|
| Time | Hours per week/month | Breakdown by step |
| Quality | Error rate, rework % | Error types |
| Money | Cost estimate | ROI baseline |
| People | Who + how many | Skill level |

### 3. Target State (Specific Goal)
SMART check: Specific, Measurable, Achievable, Relevant, Time-bound. Same units as Current State.

**Good:** "Reduce forecast time from 15 hrs/week to 2 hrs/week (87% reduction) by Q2 end."

**Bad:** "Better forecasting that's faster and easier."

### 4. Gap Analysis + Root Cause (5 Whys)
```
Gap: [Target] - [Current] = [Difference]

Why does this gap exist?
  → [Answer 1]
Why [Answer 1]?
  → [Answer 2]
Why [Answer 2]?
  → [Answer 3]
Why [Answer 3]?
  → [Answer 4]
Why [Answer 4]?
  → [ROOT CAUSE — organizational or process level]
```

### 5. Countermeasures
Actions tied to root cause — not symptoms. Prioritized. With expected impact.

| # | Countermeasure | Addresses | Expected Impact | Effort |
|---|---------------|-----------|-----------------|--------|
| 1 | [Action] | [Root cause] | [Quantified] | H/M/L |

### 6. Implementation Plan
Who does what by when. Dependencies explicit.

### 7. Follow-Up
How we'll verify success. Specific check dates. Plan if unsuccessful.

---

## 3M Waste Classification

Classify every pain point:

| Type | Japanese | Meaning | Example |
|------|----------|---------|---------|
| Muda | 無駄 | Waste | Duplicated effort, waiting, rework, unnecessary steps |
| Mura | 斑 | Inconsistency | Variable quality, unpredictable timing, uneven workload |
| Muri | 無理 | Overburden | People stretched thin, unrealistic expectations, overload |

---

## A3 Quality Checklist

- [ ] Background explains why this matters NOW
- [ ] Current State uses numbers, not adjectives
- [ ] Target State uses same units as Current State
- [ ] Gap explicitly calculated
- [ ] 5 Whys reaches organizational/process root cause (not symptom)
- [ ] 3M classification applied
- [ ] Countermeasures address root cause, not symptom
- [ ] Each countermeasure has an owner
- [ ] Success is measurable
- [ ] Follow-up dates set

## Anti-Patterns

| Anti-Pattern | Why Wrong | Instead |
|-------------|-----------|---------|
| "Better" as Target | Not measurable | Quantify improvement |
| Stopping 5 Whys at symptom | Treats symptom, not cause | Keep asking until organizational/process root |
| Solution as Current State | Backward reasoning | Describe reality first, solution last |
| Skipping Background | Loses urgency/context | Always anchor to business impact |
| Vague countermeasures | Not actionable | Specific actions with owners |

## A3 Thinking vs. Traditional PRD

| Dimension | Traditional PRD | A3 Thinking |
|-----------|----------------|-------------|
| Problem definition | "Users need X" | "Current: Y, Target: Z, Gap: Δ" |
| Root cause | Often skipped | Mandatory 5 Whys |
| Success criteria | Subjective | Quantified, same units as problem |
| Solutions | Jump to features | Countermeasures tied to root cause |
| Follow-up | "Launch and done" | Verification checkpoints |
