# Question Banks by Context

Trigger-specific questions. Use the primary context as your core question set, pull from secondaries as needed.

---

## 1. Internal Tools & Workflow Automation

**Trigger:** Employee tools, admin systems, workflow automation.

### Stakeholder & Change Management
- Who are the primary sponsors and detractors?
- How will success be communicated to affected teams?
- What's the change management plan for rollout?
- How are reluctant users being addressed?

### Training & Adoption
- What training approach works best for your organization?
- How will adoption be measured and encouraged?
- What ongoing support will power users provide?

### Administration & Maintenance
- Who handles day-to-day system administration?
- What technical skills do admins currently have?
- What backup and recovery procedures are needed?

### Workflow Integration
- Which existing systems must this integrate with?
- What manual processes will this replace?
- What's the cutover/transition plan?

### ROI & Success
- What quantitative benefits justify this investment?
- How will productivity improvements be measured?
- What's the payback period expectation?

### Red Flags
- "IT will handle everything." → Probe business unit ownership
- "Training isn't in the budget." → Probe adoption risk
- "We'll figure out integration later." → Probe workflow dependencies
- "Any improvement is good enough." → Probe success criteria and ROI

---

## 2. API / Integration Projects

**Trigger:** External APIs, system integration, developer platforms.

### Rate Limiting & Quotas
- What rate limits are appropriate for different consumer tiers?
- What happens when limits are exceeded?

### Error Handling & Retry
- How detailed should error responses be?
- What retry policies should consumers implement?
- How are transient vs. permanent errors distinguished?

### Webhook Reliability
- What guarantees does webhook delivery provide?
- How are failed deliveries retried?
- How can consumers verify webhook authenticity?

### API Versioning
- What versioning strategy? (URL, header?)
- How long will old versions be supported?
- How are breaking changes communicated?

### Documentation & Developer Experience
- What API documentation format works for consumers?
- Will you provide SDKs for common languages?
- What testing sandbox will you provide?

### Red Flags
- "We don't need rate limiting." → Probe abuse prevention
- "All errors return 500." → Probe debugging complexity
- "Versioning isn't necessary." → Probe change management
- "Documentation will come later." → Probe adoption barriers

---

## 3. Data Integration

**Trigger:** Connecting, consolidating, or syncing data across systems.

### Ownership
- Who owns the data today? Who decides data rules? Who resolves conflicts?

### Quality
- What's current data quality? Who validates? What happens to bad data?

### Transformation
- What logic maps source to target? Who knows the edge cases?

### Sync
- Real-time or batch? What's acceptable latency? How to handle conflicts?

### History
- What historical data? How far back? In what granularity?

### Common Failure Patterns
1. **Transformation Underestimation** — "Just map field A to B" ignores conditional logic
2. **Governance Vacuum** — No one owns cross-system data rules
3. **Quality Cascade** — Bad source data poisons target
4. **Sync Wars** — Conflicting updates from multiple sources

### Success Benchmarks
| Metric | Poor | Good | Excellent |
|--------|------|------|-----------|
| Data accuracy | <90% | 95-99% | >99% |
| Sync latency | >1 day | Minutes | Real-time |
| Integration uptime | <99% | 99.5% | 99.9% |

---

## 4. Process Automation

**Trigger:** Automating manual tasks, workflows, or decisions.

### Happy Path
- What's the standard flow? What percentage follows happy path?

### Edge Cases
- What variations exist? Who handles exceptions today?

### Errors
- What can go wrong? How are errors handled? Who gets notified?

### Override
- When do humans need to intervene? How do they override?

### Audit
- What needs to be logged? Who reviews? Compliance requirements?

### Common Failure Patterns
1. **Happy Path Bias** — Works 80% of time, exceptions overwhelm operations
2. **Invisible Override** — No way to manually correct when automation errs
3. **Audit Blindness** — Can't prove what happened or why
4. **Maintenance Orphan** — No one owns updating rules when business changes

### Success Benchmarks
| Metric | Poor | Good | Excellent |
|--------|------|------|-----------|
| Automation rate | <50% | 70-90% | >90% |
| Exception rate | >20% | 5-10% | <5% |
| False positive rate | >10% | 2-5% | <2% |

---

## 5. Tool Selection

**Trigger:** Evaluating, selecting, deploying new tools or platforms.

### Fit
- What problems must it solve? What's nice-to-have vs. critical?

### Workflow
- How does this fit daily work? What changes for users?

### Integration
- What must it connect to? API requirements? Data flow?

### Migration
- What data/config moves? Who does migration? Timeline?

### Change
- Who needs training? How much behavior change? Who champions?

### Common Failure Patterns
1. **Feature Fixation** — Chose for features, failed on workflow fit
2. **Demo Delusion** — Looked great in demo, failed in reality
3. **Migration Minimization** — Underestimated data/config migration cost
4. **Adoption Assumption** — Built it, but they didn't come

### Success Benchmarks
| Metric | Poor | Good | Excellent |
|--------|------|------|-----------|
| User adoption (3 mo) | <30% | 50-80% | >80% |
| Time to productivity | >6 mo | 1-3 mo | <1 mo |
| Feature utilization | <20% | 40-70% | >70% |

---

## 6. Cross-Functional Initiatives

**Trigger:** Changes requiring coordination across multiple teams.

### RACI
- Who's Responsible, Accountable, Consulted, Informed for each step?

### Incentives
- How are teams measured? Do incentives align with shared goal?

### Escalation
- What happens when teams disagree? Who breaks ties?

### Governance
- Who owns the end-to-end process? How are changes approved?

### Metrics
- What does shared success look like? How is credit/blame distributed?

### Common Failure Patterns
1. **RACI Vacuum** — Everyone's responsible = no one's responsible
2. **Incentive Conflict** — Teams optimized for local, not shared, outcomes
3. **Escalation Gridlock** — No mechanism to resolve cross-team disputes
4. **Ownership Orphan** — No one owns the space between teams

### Success Benchmarks
| Metric | Poor | Good | Excellent |
|--------|------|------|-----------|
| Handoff efficiency | >5 days | 1-2 days | <1 day |
| Escalation rate | >30% | 5-15% | <5% |
| Cross-team satisfaction | <3/5 | 3.5-4/5 | >4/5 |

---

## 7. Reporting & Analytics

**Trigger:** Dashboards, BI, analytics capabilities.

### Decisions
- What decisions will this inform? Who makes them? How often?

### Freshness
- How current must data be? Daily? Hourly? Real-time?

### Trust
- Where does data come from? Who validates? What builds confidence?

### Access
- Who can see what? Any sensitivity concerns?

### Action
- What happens after seeing the report? Who acts on insights?

### Common Failure Patterns
1. **Metric Myopia** — Tracking what's easy, not what matters
2. **Dashboard Graveyard** — Built, launched, never used
3. **Trust Deficit** — Users don't believe the numbers
4. **Action Gap** — Insights generated but not acted upon

### Success Benchmarks
| Metric | Poor | Good | Excellent |
|--------|------|------|-----------|
| Dashboard usage (weekly) | <20% | 40-70% | >70% |
| Data freshness gap | >1 day | Minutes | Real-time |
| Decision influence | Rarely cited | Usually cited | Always cited |

---

## Context Trigger Matrix

| Project Characteristic | Primary Context | Secondary |
|------------------------|----------------|-----------|
| "Clients pay for our time" | Service Business | Payment, User-Facing |
| "We sell products online" | Physical Goods | Payment, Forms |
| "Users submit applications" | Forms & Data | User-Facing, Payment |
| "Monthly subscriptions" | Payment | User-Facing, Internal Tools |
| "Employee workflow system" | Internal Tools | API/Integration, Forms |
| "Partner integration" | API/Integration | Payment, Internal Tools |
| "Customer portal" | User-Facing | Auth requirements |

## Question Sequencing

1. Open with context-establishing questions
2. Move to current state questions
3. Probe pain points
4. Explore constraints
5. Identify success criteria
6. Uncover hidden risks: "What haven't we discussed that could derail this?"
