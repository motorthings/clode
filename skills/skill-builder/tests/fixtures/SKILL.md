---
name: fixture-skill
description: Reconcile a ledger. Use when the user says "reconcile", "match deposits", or "find unmatched rows".
---

# Fixture Skill

A synthetic skill used only to exercise the validator. It carries all five
categories so every branch of the checker has something to bite on.

## Before you start

Confirm the ledger source is configured. If it is not, stop and tell the user — do not guess at values.

## Procedure

1. Read the ledger.
2. Match each row against the deposit feed.
3. Write the unmatched rows to `unmatched.csv`.

## Output

Always emit a markdown table with the columns `row_id`, `amount`, `reason`.

## Never

- Never modify the source ledger in place.
- Never invent a matching row to close a gap.
