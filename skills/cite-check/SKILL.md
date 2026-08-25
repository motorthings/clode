---
name: cite-check
description: Verify every legal citation and quotation in a filing against the Descrybe Legal Engine (existence, correct cite, treatment/good-law status, and word-for-word quote accuracy). Use before filing any brief, demand, or motion, or when the user says "cite-check", "verify the cites", "confirm the quotes", or "check the authorities". Catches fabricated/AI-hallucinated cases, wrong reporter cites, garbled captions, overruled/limited authority, and misquotations.
---

# Cite-Check: verify all authorities in a filing against Descrybe

Systematically confirm that every legal authority in a document (a) **exists**, (b) is cited with the **correct caption and reporter**, (c) is **still good law** (treatment), and (d) any **verbatim quotation is accurate word-for-word**. This exists because AI-drafted and human-drafted filings both routinely contain fabricated cases, transposed reporter pages, truncated captions, and quotes that appear nowhere in the opinion. One bad cite can sink credibility with an arbitrator or judge.

## Prerequisite: Descrybe must be connected

This skill drives the **Descrybe Legal Engine** MCP tools (`mcp__claude_ai_Descrybe_Legal_Engine__*`). If they aren't loaded, run `ToolSearch` with query `descrybe` first. If Descrybe is not connected at all, tell the user and stop — do not fall back to memory (that is how hallucinated cites get through).

Descrybe covers U.S. **primary law only** (cases, statutes, regs, constitutions). It does **not** cover: private arbitral rules (JAMS/AAA/NASD), jury instructions (CJI), law-review articles, or treatises. Verify those via the official publisher's website with `WebFetch`/`WebSearch`, and say so in the report.

## Procedure

### 0. Establish the input
The target is a **local file path** (`.md`, `.txt`, `.pdf`, `.docx`). If none was given, ask. Convert opaque formats first: `markitdown <file>` for PDF/DOCX/XLSX. Work from the converted text.

### 1. Extract every authority from the target document
Formatting-agnostic — **do not assume markdown italics** (real filings are often plain text or stripped by conversion):
- Case captions: match `Case v. Case`, `In re X`, `Ex parte X`, with or without the period after `v`, and `&`/`'`/`,` inside captions. Also catch docket- or party-style fragments for later resolution.
- Short-cites and `Id.`/`supra` chains: resolve each back to its first full cite.
- Statutes / rules: `C.R.S. §`, `U.S.C. §`, `C.R.C.P.`, `CRE`, `FRCP`, regs.
- **Quotations**: every quoted string 20+ chars is a candidate for `verify_quote`.
- Build a working list with a fixed shape: `Authority | First full cite | Lines | Status`. De-dupe by authority but keep every line number so fixes can be applied everywhere.

### 2. For each CASE
1. `find_case_from_reference` (pass the full reference + any quote_hint/year/court). Outcomes:
   - **resolved** → capture `case_id`, canonical title, and citation. **Compare against the document**: flag any mismatch in party names (truncated/garbled captions), reporter, volume, page, court, or year.
   - **ambiguous (needs_user_selection)** → pick the candidate matching the document's cite/year; if none match, flag as unverified.
   - **not_found** → retry once with the exact reporter citation and a quote_hint. If still not found, **flag ❌ NOT FOUND** — either fabricated, or outside Descrybe's index (note which; a real-but-uncovered case must be verified via `WebSearch` against a primary source before it can stay in a filing).
2. `check_case_status` (needs `case_id`) → record indicator (positive/neutral/caution/negative), weight (binding/persuasive), category (followed/distinguished/declined to follow/overruled). **Any "caution"/"negative" → drill with `find_cases_that_cite`** to see *which* later case gave negative treatment and *on what point*; determine whether it touches the proposition the filing relies on. Aggregate "caution" flags are often noise on an unrelated sub-issue — the forward-citation drill is the ground truth.
3. Confirm the **holding** actually supports the proposition it's cited for (`get_case_summary` / `get_case_passages`). A real case cited for a holding it doesn't contain is as dangerous as a fake one.

### 3. For each QUOTE
- `verify_quote` (needs `case_id` + the quote). Give ≥4 words / 2 substantive terms.
- **Prepare the quote before verifying:** strip leading/trailing citation text and ellipses, and normalize case/punctuation differences (the engine matches language, not formatting). Pass only the running text.
- **found** → ✅. If it returns "found with differences," confirm the differences are non-substantive (word order, tense, punctuation) before certifying.
- **not_found** → the quote is altered or fabricated. Pull the real passage with `get_case_passages` and either correct the quotation to the actual language or convert it to an accurate paraphrase. **Never leave an unverified verbatim quote in a filing.**
- Statutory quotes → `search_laws_and_rules` and compare the returned current text verbatim.
- Non-Descrybe quotes (JAMS rules, CJI) → `WebFetch` the official source and quote-match.

### 4. For each STATUTE / RULE
- `search_laws_and_rules` → confirm the section exists, the citation is right, and the **current text** matches what the filing asserts (watch for renumbering, amendments, and effective-date/threshold figures like damage caps).

### 5. Report
Produce a table: **Authority | Doc cite | Descrybe cite | Exists? | Cite correct? | Treatment | Quote verified? | Action**. Then a prioritized **ACTION ITEMS** list: ❌ fabricated/not-found first, then wrong-cite/garbled-caption, then negative-treatment, then misquotes, then holding-mismatches. For each, give the exact fix (correct caption/cite/quote). Apply fixes to the document only when the user approves (or immediately if they've said to fix as you go), and update any source-of-truth files (e.g., a `CLAUDE.md` case table or a cite-check worklist) in the same pass.

### 6. Close the loop
After fixes are applied, **re-scan the fixed document** with the same extraction from Step 1. Assert that **0** authorities remain `❌ NOT FOUND`, unverified, or flagged `⚠️` treatment with an unresolved forward-citation. Report what is now clean and what still needs external verification (e.g., real-but-uncovered authorities). Do not call the pass done while any unresolved item remains.

## Rules
- **Never certify a cite you couldn't verify.** "Not in Descrybe" ≠ "doesn't exist," but it also ≠ "safe to file" — escalate to a web/primary-source check and label binding vs. persuasive.
- **Run calls in parallel** where independent (batch `find_case_from_reference` across many cases in one turn) — but keep `verify_quote`/`check_case_status` tied to the resolved `case_id`.
- **Preserve an audit trail.** When you correct a cite or quote, leave a dated note (in the worklist, not necessarily the filing) recording what was wrong and how it was verified.
- **Distinguish defense-win cases.** A real case whose *outcome* favored the other side is fine to cite for a *legal standard* — say so inline so no one is surprised on the pull.
- Scale depth to stakes: a pre-filing pass verifies everything; a quick sanity check can stop at existence + treatment.
