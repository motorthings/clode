# Initiative Taxonomy

Classify the initiative type early. Each type has specific questions, failure patterns, and success benchmarks.

---

## The Five Types

### Type 1: Data Integration
**Definition:** Connecting, consolidating, or synchronizing data across systems.

**Classification signals:**
- "Data is in multiple places"
- "Systems don't talk to each other"
- "We need a single source of truth"
- "Reports take too long because of data gathering"

**Key questions often missed:**
- Who owns the data? Who decides data rules?
- What's current data quality? Who validates?
- What logic maps source to target? Who knows the edge cases?
- Real-time or batch? Acceptable latency?
- What historical data? How far back?

**Failure patterns:**
1. Transformation Underestimation — "Just map A to B" ignores conditional logic
2. Governance Vacuum — No one owns cross-system data rules
3. Quality Cascade — Bad source data poisons target
4. Sync Wars — Conflicting updates from multiple sources

**Success benchmarks:**
| Metric | Poor | Good | Excellent |
|--------|------|------|-----------|
| Data accuracy | <90% | 95-99% | >99% |
| Sync latency | >1 day | Minutes | Real-time |
| Time to new integration | >3 months | 2-4 weeks | <2 weeks |

---

### Type 2: Process Automation
**Definition:** Automating manual tasks, workflows, or decision processes.

**Classification signals:**
- "We do this manually every day/week"
- "The process is well-defined but takes too long"
- "People make the same decisions repeatedly"
- "We need to scale without adding headcount"

**Key questions often missed:**
- What percentage follows happy path? (not 100%)
- What are the edge cases? Who handles exceptions today?
- When do humans need to override? How?
- What needs to be logged for audit? Compliance requirements?

**Failure patterns:**
1. Happy Path Bias — Works 80%, exceptions overwhelm
2. Invisible Override — No manual correction path
3. Audit Blindness — Can't prove what happened or why
4. Maintenance Orphan — No one updates rules when business changes

**Success benchmarks:**
| Metric | Poor | Good | Excellent |
|--------|------|------|-----------|
| Automation rate | <50% | 70-90% | >90% |
| Exception rate | >20% | 5-10% | <5% |
| Time to update rules | >1 month | 1-2 weeks | <1 week |

---

### Type 3: Tool Selection
**Definition:** Evaluating, selecting, and deploying new tools or platforms.

**Classification signals:**
- "We're evaluating vendors"
- "The current tool doesn't meet our needs"
- "We need to choose between X and Y"
- "We're implementing [new platform]"

**Key questions often missed:**
- How does this fit daily workflow? (not feature list)
- What data/config needs migration? Who does it?
- Who needs training? How much behavior change?
- Who champions adoption? Who might resist?

**Failure patterns:**
1. Feature Fixation — Chose for features, failed on workflow fit
2. Demo Delusion — Great demo, failed in reality
3. Migration Minimization — Underestimated data/config migration
4. Adoption Assumption — Built it, they didn't come

**Success benchmarks:**
| Metric | Poor | Good | Excellent |
|--------|------|------|-----------|
| User adoption (3 mo) | <30% | 50-80% | >80% |
| Time to productivity | >6 mo | 1-3 mo | <1 mo |
| Feature utilization | <20% | 40-70% | >70% |

---

### Type 4: Cross-Functional
**Definition:** Changes requiring coordination across multiple teams/departments.

**Classification signals:**
- "This involves multiple departments"
- "We need to improve handoffs between teams"
- "Everyone's involved but no one owns it"
- "The process crosses organizational boundaries"

**Key questions often missed:**
- RACI: Who's Responsible, Accountable, Consulted, Informed per step?
- How are teams measured? Do incentives align with shared goal?
- What happens when teams disagree? Who breaks ties?
- Who owns the end-to-end process, not just their piece?

**Failure patterns:**
1. RACI Vacuum — Everyone's responsible = no one's responsible
2. Incentive Conflict — Teams optimized for local metrics, not shared outcome
3. Escalation Gridlock — No mechanism to resolve cross-team disputes
4. Ownership Orphan — No one owns the space between teams

**Success benchmarks:**
| Metric | Poor | Good | Excellent |
|--------|------|------|-----------|
| Handoff efficiency | >5 days | 1-2 days | <1 day |
| Escalation rate | >30% | 5-15% | <5% |
| Cross-team satisfaction | <3/5 | 3.5-4/5 | >4/5 |

---

### Type 5: Reporting/Analytics
**Definition:** Creating or improving BI, dashboards, or analytics capabilities.

**Classification signals:**
- "We need better visibility into..."
- "Leadership wants a dashboard for..."
- "We can't answer this question easily"
- "Reporting takes too long"

**Key questions often missed:**
- What decisions will this inform? Who makes them? How often?
- How current must data be? (daily ≠ real-time)
- Where does data come from? Who validates accuracy?
- Who can see what? Sensitivity concerns?
- What happens after seeing the report? Who acts?

**Failure patterns:**
1. Metric Myopia — Tracking what's easy, not what matters
2. Dashboard Graveyard — Built, launched, never used
3. Trust Deficit — Users don't believe the numbers
4. Action Gap — Insights generated but not acted upon

**Success benchmarks:**
| Metric | Poor | Good | Excellent |
|--------|------|------|-----------|
| Dashboard usage (weekly) | <20% | 40-70% | >70% |
| Data freshness gap | >1 day | Minutes | Real-time |
| Decision influence | Rarely cited | Usually cited | Always cited |

---

## Classification Protocol

### Step 1: Listen for signals
During initial context, flag phrases that indicate type (see signal phrases above).

### Step 2: Confirm with user
> "Based on what I'm hearing, this is primarily a [Type] initiative with elements of [Secondary Type]. Does that match?"

### Step 3: Apply type-specific lens
- Pull relevant questions from the question bank
- Watch for the type's specific failure patterns
- Use success benchmarks to set targets

### Step 4: Document in PRD
Record the classification in the PRD header. It tells readers what lens was applied.

## Hybrid Initiatives

Most real projects span multiple types. Handle by:
1. Identify primary type (dominant pattern)
2. Note secondary elements
3. Pull questions from both — prioritize primary
4. Watch for combined failure patterns at the intersection:
   - Tool Selection + Automation: Tool picked for features, can't support automation
   - Data Integration + Cross-Functional: Integration works but teams don't use shared data
   - Reporting + Tool Selection: Dashboard built in tool users don't access

## Gap Detection by Type

| If this is missing... | The type needs... |
|----------------------|-------------------|
| No data ownership discussion | Data Integration governance review |
| No exception handling plan | Process Automation at risk |
| No adoption plan | Tool Selection likely to fail |
| No RACI defined | Cross-Functional is doomed |
| No decision mapping | Reporting will become shelfware |
