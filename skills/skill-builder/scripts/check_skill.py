#!/usr/bin/env python3
"""Lint a SKILL.md for well-formedness.

This is the quality check skill-builder runs when it cannot run the measured
eval loop — in Claude Desktop or claude.ai, where the sandbox has no `claude`
CLI and no network, so no skill-free baseline can be formed. It does not measure
what the skill contributes against a baseline. It confirms the skill is well
formed and worth shipping: a name and a description, named triggers, an
anti-patterns section with real teeth, and no authoring stubs left behind.

Checks, and why each is here:

  name            A skill with no name cannot be addressed. Taken from YAML
                  frontmatter `name:`, or the `# H1` when there is no frontmatter
                  (two skills in the wild carry no frontmatter at all).

  description     The description is what Claude matches a request against. No
                  description, no reliable trigger. Required when frontmatter is
                  present; its absence is only a warning when there is no
                  frontmatter to carry it.

  triggers        A description that names no trigger phrase ("use when...",
                  quoted examples) is a description the model cannot match on.

  anti-patterns   skill-builder makes this section mandatory — at least three
                  items — because a skill that never says what not to do cannot
                  catch its own scope creep. Missing or thin is an error.

  placeholders    TODO, FIXME, "fill in", lorem, TKTK: authoring stubs that mean
                  the skill was never finished.

Stdlib only, matching the house convention (humane-evals, op04-judge).

Usage:
    python3 check_skill.py path/to/SKILL.md
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S")

# A heading means "here is what not to do", whatever its exact words. Four of 28
# skills say "Anti-Patterns"; the rest say "Non-negotiables", "Rules", "Common
# mistakes", "Never". Read for meaning, not heading text.
FENCE_HEADING = re.compile(
    r"anti[-\s]?patterns?|non[-\s]?negotiable|common\s+mistakes|\brules?\b|\bnever\b|\bavoid\b",
    re.IGNORECASE,
)

# Trigger signals in a description: an explicit "use when", or a quoted example
# phrase the model would match a request against.
TRIGGER_SIGNAL = re.compile(r"use\s+when|\buse\s+this\b|[\"“”']", re.IGNORECASE)

# Authoring stubs. Deliberately conservative: a bare <word> is NOT flagged,
# because generated skills legitimately show <name>-style templates in their
# output examples. Only unambiguous leftovers.
PLACEHOLDER = re.compile(
    r"\bTODO\b|\bFIXME\b|\bXXX\b|\bTKTK\b|\bTBD\b"
    r"|fill\s+in\b|your\s+text\s+here|lorem\s+ipsum|<insert\b|\[insert\b",
    re.IGNORECASE,
)

MIN_FENCE_ITEMS = 3


def split_frontmatter(text: str) -> tuple[dict[str, str], str, bool]:
    """Return (frontmatter dict, body, had_frontmatter).

    Parses only top-level `key: value` lines — enough for name and description
    without a YAML dependency. A folded or quoted value is taken verbatim.
    """
    lines = text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        return {}, text, False

    fm: dict[str, str] = {}
    j = i + 1
    while j < len(lines) and lines[j].strip() != "---":
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[j])
        if m:
            fm[m.group(1).lower()] = m.group(2).strip().strip('"').strip("'")
        j += 1
    if j >= len(lines):
        # No closing fence — treat the whole thing as body, flag nothing here.
        return {}, text, False
    body = "\n".join(lines[j + 1 :])
    return fm, body, True


def first_h1(body: str) -> str | None:
    for line in body.splitlines():
        m = HEADING.match(line)
        if m and len(m.group(1)) == 1:
            return m.group(2).strip()
    return None


def fence_item_count(body: str) -> int:
    """Count list items under the fence-like heading with the most items.

    Every fence-like heading is scored, not just the first, because a word like
    "RULE" shows up mid-title in procedure steps ("For each STATUTE / RULE") and
    would otherwise be mistaken for the anti-patterns section. The real section
    is the one carrying the items, so take the max. Returns -1 if no fence-like
    heading exists at all."""
    lines = body.splitlines()
    starts: list[tuple[int, int]] = []  # (index after heading, heading level)
    for idx, line in enumerate(lines):
        m = HEADING.match(line)
        if m and FENCE_HEADING.search(m.group(2)):
            starts.append((idx + 1, len(m.group(1))))
    if not starts:
        return -1

    best = 0
    for start, level in starts:
        count = 0
        for line in lines[start:]:
            m = HEADING.match(line)
            if m and len(m.group(1)) <= level:
                break
            if LIST_ITEM.match(line):
                count += 1
        best = max(best, count)
    return best


def check(text: str) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    if not text.strip():
        return ["file is empty"], warnings

    fm, body, had_fm = split_frontmatter(text)

    name = fm.get("name") or first_h1(body)
    if not name:
        errors.append("no name — needs YAML frontmatter `name:` or a `# H1`")

    if had_fm:
        desc = fm.get("description", "")
        if not desc:
            errors.append("frontmatter has no description — the model matches requests against it")
        elif not TRIGGER_SIGNAL.search(desc):
            warnings.append(
                "description names no trigger — add a \"use when...\" clause or quoted example "
                "phrases so the model can match a request to this skill"
            )
    else:
        warnings.append(
            "no YAML frontmatter — the skill carries no description for trigger matching. "
            "Valid for some skills, but most want one"
        )

    items = fence_item_count(body)
    if items == -1:
        errors.append(
            "no anti-patterns section — skill-builder requires one (a heading like "
            "Anti-Patterns, Non-negotiables, Rules, or Never) so the skill can catch its own "
            "scope creep"
        )
    elif items < MIN_FENCE_ITEMS:
        errors.append(
            f"anti-patterns section has {items} item(s); at least {MIN_FENCE_ITEMS} are required"
        )

    stubs = sorted({m.group(0).lower() for m in PLACEHOLDER.finditer(text)})
    if stubs:
        warnings.append(f"authoring stubs left in the skill: {stubs}")

    headings = [m for line in body.splitlines() if (m := HEADING.match(line)) and len(m.group(1)) == 2]
    if len(headings) < 2:
        warnings.append(
            f"only {len(headings)} top-level (##) section(s) — this reads like a skeleton, not a "
            "finished skill"
        )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a SKILL.md for well-formedness")
    parser.add_argument("skill", help="Path to SKILL.md")
    args = parser.parse_args()

    p = pathlib.Path(args.skill)
    if not p.exists():
        print(f"FAIL: no such file: {p}", file=sys.stderr)
        return 1

    errors, warnings = check(p.read_text())

    if errors:
        print(f"FAIL: {len(errors)} problem(s)", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
    if warnings:
        print(f"WARN: {len(warnings)} issue(s)", file=sys.stderr)
        for warn in warnings:
            print(f"  - {warn}", file=sys.stderr)

    if errors:
        return 1
    if not warnings:
        print("OK — skill is well formed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
