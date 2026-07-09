# PRD Template

The target output. Every section should be filled from the discovery conversation.

```markdown
# PRD: [Project Name]

**Date**: [today]
**Author**: [name]
**Requester**: [name/team]
**Initiative Type**: [Data Integration / Process Automation / Tool Selection / Cross-Functional / Reporting]
**Scale**: [Kiddie Pool / Olympic Pool / Ocean]
**Effort Tier**: [S / M / L / XL]

---

## Problem Statement
[2-3 sentences — the pain, who feels it, root cause, why it matters now]

## Current State
[Process description with pain points. Include quantified measures.]

| Dimension | Current | Target | Gap |
|-----------|---------|--------|-----|
| [Primary metric] | | | |
| [Secondary metric] | | | |

## Root Cause
**Surface symptom:** [What stakeholders described]
**Root cause (5 Whys):** [Actual underlying cause — ask "why" until you reach organizational/process root]
**Waste type:** [Muda / Mura / Muri — with brief explanation]

## Who's Affected

| Stakeholder | Team | Role | Impact (H/M/L) | Power (1-5) |
|-------------|------|------|---------------|-------------|
| | | | | |

## Proposed Solution
[High-level approach. Keep brief — tech stack decisions come later, driven by these requirements.]

## Opportunities Identified

| # | Opportunity | Impact | Effort | Priority |
|---|-------------|--------|--------|----------|
| 1 | | | | |

## Scope

### In Scope (v1)
- [ ] Item

### Out of Scope (future / v2)
- Item

## Systems & Integrations

| System | Role | Integration Type | Data Flow | Risk Level |
|--------|------|-----------------|-----------|------------|
| | | | | |

## Success Metrics

| Metric | Current | Target | How Measured |
|--------|---------|--------|--------------|
| | | | |

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| | | | |

**Failure Pattern Flags:** [Any of the 7 patterns that apply — see failure-patterns reference]

## Dependencies
- [Other projects, teams, systems, people]

## Timeline
- **MVP Target**: [date]
- **Pilot Users**: [who, how many]
- **Full Rollout**: [date]

## Open Questions
1. [Question — owner to resolve]
2.

## Approvals Needed
- [ ] [Approval 1]
- [ ] Security review (if PII/sensitive data)
- [ ] [Other]

---
*Generated via PuRDy methodology*
```

## Section Coverage Requirements

Every PRD must have these sections filled. If a section can't be filled, it becomes an open question.

| Section | Minimum Bar |
|---------|------------|
| Problem Statement | Clear articulation of pain + who feels it |
| Current State | Step-by-step process with at least one quantified measure |
| Root Cause | 5 Whys reaching organizational/process level |
| Who's Affected | All stakeholder groups, not just the requester |
| Success Metrics | At least 2 quantified metrics with current and target values |
| Systems & Integrations | Every system touched, even if "no integration needed" |
| Risks | At least 3 risks with mitigations |
| Open Questions | Minimum 3 — if zero, discovery was too shallow |

## What the PRD Intentionally Excludes

- **Tech stack decisions** — separate process post-PRD
- **Detailed implementation plan** — build-phase work
- **Vendor comparisons** — separate evaluation if needed
- **UI/UX designs** — separate design phase
