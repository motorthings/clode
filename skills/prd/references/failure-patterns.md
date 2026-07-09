# Failure Patterns

Seven patterns that kill software projects. Scan every PRD against these. Surface matches to the user in real-time — don't wait for the final document.

---

## Pattern 1: Death by 1,000 Integrations

**The problem:** Systematic underestimation of integration complexity. Each new connection potentially affects all existing ones. Developers consistently rate integration difficulty 40-60% lower than actual.

**Early warning signs:**
- "Just API calls" language — describing integrations as simple, discrete
- No integration architect — responsibility diffused across team
- No circuit breaker pattern — services can cascade-fail
- Authentication oversimplification — "OAuth will just work"
- Testing only happy path — "that's what will usually happen"

**What to ask:**
- "What's the most fragile dependency here?"
- "What happens when [system X] is down?"
- "Have you tested with real-world data, not clean test data?"
- "What's your plan for the 'five 9s deception'? (10 dependencies at 99.9% each = 99% collective)"

**Prevention:** Isolation contract (every external service behind dedicated adapter), 3-state model (normal/degraded/manual), error-first development.

---

## Pattern 2: Ghost Town Build

**The problem:** Building in cognitive isolation — no external feedback loops, echo chamber decision-making, eventual irrelevance.

**Early warning signs:**
- No user interviews before building
- "We know what users need" (without validation)
- No advisory board, mentors, or external critics
- Homogeneous team — same backgrounds, same assumptions
- Feature built without a single customer request

**What to ask:**
- "Who critiques this besides the team building it?"
- "How many potential users have you talked to?"
- "What's the riskiest assumption you're making?"
- "What would prove that assumption wrong?"

**Prevention:** Personal board of directors (5-7 people in different roles), feedback stack (daily/weekly/quarterly), community building from day 0.

---

## Pattern 3: Pre-Scale Paralysis

**The problem:** Pathological preoccupation with future scalability that sacrifices present usability and launch velocity. Solving hypothetical problems of success while ignoring actual problems of adoption.

**Early warning signs:**
- "We need microservices" (with <10 engineers)
- "The database will be the bottleneck" (before having users)
- "Real-time is table stakes" (when 30-second polling would work)
- Architecture designed for "millions of users" before having 100
- Technology choices driven by tech giants' architectures

**What to ask:**
- "How many users do you have today? What's the next milestone?"
- "What would break first if you 10x'd current usage?"
- "Could you launch with a simpler architecture and evolve?"
- "Which of these scalability concerns are actual problems vs. hypothetical?"

**Prevention:** Constraint-based design (build for 10x current, not 1000x), 10x rule (only optimize at 10% of hard limit), escape hatches (document when to switch approaches).

---

## Pattern 4: Invisible Cost Avalanche

**The problem:** Systematic failure to model total cost structure. Includes direct (infrastructure), indirect (maintenance, support), and hidden (cognitive load, opportunity cost).

**Eight hidden cost categories:**
1. Direct infrastructure (cloud, APIs, CDN)
2. Operational labor (monitoring, security, backup)
3. Software maintenance (dependency updates, compatibility)
4. Opportunity cost (low-value features, delayed learning)
5. Scaling thresholds (license tier jumps, compliance at scale)
6. Decision delay (analysis paralysis → rework)
7. Cognitive load (context switching, onboarding time)
8. Ecosystem dependency (platform risk, vendor lock-in)

**What to ask:**
- "What does this cost per month? Per user? In 12 months?"
- "What license tiers will you hit at scale?"
- "Who maintains this? What's their time worth?"
- "What's the cost of NOT doing this?"

**Prevention:** Cost component map, cost per active user tracking, cost stories in planning, cost-driven design reviews.

---

## Pattern 5: Feature Gravity Well

**The problem:** Progressive scope expansion through accretion. Each feature seems rational in isolation but collectively creates unusable complexity. N features create N² potential interactions.

**Early warning signs:**
- "And also..." language during discovery
- Stakeholders each adding "just one" critical feature
- Competitive panic — adding because competitors have it
- No feature has been removed... ever
- Can't articulate what's out of scope

**What to ask:**
- "What's the ONE thing this must do to be valuable?"
- "What could you remove and still have a viable v1?"
- "When did you last kill a feature?"
- "What percentage of current features do users actually use?"

**Prevention:** Feature constitution (core purpose + non-goals), one-in-one-out rule, monthly pruning, "weekend test" (can a new user understand it in one weekend?).

---

## Pattern 6: Technical Debt Spiral

**The problem:** Debt accumulates interest faster than it's paid down, eventually consuming all development capacity.

**Debt types and their interest:**
| Type | Interest Rate | Example |
|------|--------------|---------|
| Code Debt | 0.5-2x principal | Quick fixes, TODOs |
| Architecture Debt | 2-10x principal | Wrong abstractions, tight coupling |
| Test Debt | 1-5x principal | Missing tests, poor coverage |
| Documentation Debt | 0.5-3x principal | Missing/outdated docs |
| Dependency Debt | 1-4x principal | Outdated libraries |

**What to ask:**
- "What code is the team afraid to touch?"
- "What percentage of time is spent on maintenance vs. new features?"
- "What's the 'temporary' fix that's been there longest?"
- "Healthy debt service ratio is <30% of engineering time. Where are you?"

**Prevention:** Debt register (track it), 20% of each sprint on debt reduction, architecture decision records with review dates, "no new debt" periods.

---

## Pattern 7: Reality Distortion Build

**The problem:** Elaborate solutions built on internally-generated assumptions rather than external validation. Confirmation bias, solution attachment, eventual market rejection.

**Four validation gaps:**
1. Problem-Solution Fit — surface understanding of symptoms, not root causes
2. Solution-Market Fit — solution doesn't match actual workflow
3. Market-Product Fit — niche problem, no willingness to pay
4. Product-Channel Fit — acquisition cost exceeds lifetime value

**What to ask:**
- "What's the evidence this problem is real and painful enough to solve?"
- "What are people doing today to work around it?"
- "Have you tried to pre-sell this? Would anyone pay?"
- "What do you believe about this that might be completely wrong?"

**Prevention:** Mom Test (talk about their life, not your idea), Wizard of Oz MVP (manual backend), Fake Door test (advertise before building), quarterly assumption audit.

---

## Failure Cascade Models

Patterns rarely appear alone. Watch for these sequences:

- **Path A (Technical):** Reality Distortion → Feature Bloat → Technical Debt → Cost Avalanche → Failure
- **Path B (Social):** Ghost Town Build → Reality Distortion → Integration Complexity → Burnout → Abandonment
- **Path C (Strategic):** Pre-Scale Paralysis → Missed Market Window → Panic Features → Technical Debt → Failure

## Pattern Immunity Scorecard

Quick health check — score 1-10 on each:

1. Can we replace any integration in <2 weeks?
2. Do we have 5+ engaged advisors/critics?
3. Could a new developer contribute in 1 day?
4. Can we calculate cost per user in 5 minutes?
5. Have we removed a feature this month?
6. Is <30% of time spent on maintenance?
7. When did we last talk to dissatisfied users?

**70+:** Healthy | **50-69:** Warning | **<50:** Danger
