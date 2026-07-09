# Scale & Effort Framework

Size the project correctly. Don't ask "is this small or large?" — ask details that let YOU determine scale.

---

## Scale Framework

| Scale | Description | Indicators | Typical Approach |
|-------|-------------|------------|-----------------|
| **Kiddie Pool** | Single user or small team, one system | Self-contained, well-understood | Self-serve, simple build |
| **Olympic Pool** | Department-level, 2-3 systems | Some ambiguity, moderate stakeholders | IS/engineering team builds |
| **Ocean** | Cross-functional, multiple systems, strategic | Complex, phased, high stakes | Major initiative, formal approval |

### Questions That Reveal Scale

| Question | What It Tells You |
|----------|-------------------|
| Is this a user problem, team problem, department problem, or company problem? | Scope |
| How many people are affected? | Reach |
| How often does this happen? (hourly/daily/weekly/once) | Frequency |
| How many systems are involved? | Complexity |
| Is this repeatable or one-time? | Pattern |

---

## Effort Tiers

| Tier | Description | Indicators |
|------|-------------|------------|
| **S** | Simple, contained | Single system, clear process, one team |
| **M** | Moderate complexity | 2-3 systems, some ambiguity |
| **L** | Significant effort | Multiple systems, cross-team, process design needed |
| **XL** | Major initiative | Enterprise-wide, phased approach required |

### Complexity Factors

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| Systems involved | 1 | 2-3 | 4+ |
| Data sources | 1 clean | 2-3 or needs cleanup | 4+ or major cleanup |
| Stakeholder groups | 1 team | 2-3 teams | Cross-functional |
| Process clarity | Well documented | Partially documented | Tribal knowledge |
| Exception handling | Few, simple | Moderate | Many complex branches |

---

## 40-Hour Threshold

Critical routing boundary:

| Under 40 Hours | 40+ Hours |
|----------------|----------|
| Solutions team builds directly | Requires formal approval |
| PRD → Jira ticket | PRD → BRD process |
| Lightweight review | ELT sponsor sign-off |
| Single sprint/cycle | Phased with milestones |

**When in doubt:** If you can't confidently estimate it under 40 hours, it probably isn't.

---

## Impact/Effort Prioritization

```
                    HIGH IMPACT
                        |
     PLAN & BUILD       |        DO NOW
     (invest later)     |        (quick wins)
                        |
  ----------------------+----------------------
                        |
     DEPRIORITIZE       |        STRATEGIC
     (politely decline) |        (phase it)
                        |
                    LOW IMPACT
```

- **Do Now:** High impact, low effort. Quick wins. Do immediately.
- **Plan & Build:** High impact, high effort. Invest in later, phase it.
- **Strategic:** Low impact, high effort. Phase carefully — may not be worth it.
- **Deprioritize:** Low impact, low effort. Why bother? Decline or defer indefinitely.

---

## Effort Sizing Reference

| Tier | Typical Calendar Time | Team Size | Example |
|------|----------------------|-----------|---------|
| S | 1-2 weeks | 1 person | Add field to form, simple automation |
| M | 2-6 weeks | 1-2 people | New integration, moderate workflow |
| L | 6-12 weeks | 2-4 people | Multi-system integration, new tool rollout |
| XL | 3-12+ months | 4+ people, phased | Enterprise platform, cross-functional transformation |

---

## Scale/Effort Cross-Reference

| Scale | Typical Effort | Routing |
|-------|---------------|---------|
| Kiddie Pool | S-M | Build directly |
| Olympic Pool | M-L | Build with review |
| Ocean | L-XL | Formal BRD, phased |
