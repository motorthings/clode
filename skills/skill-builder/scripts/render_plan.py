#!/usr/bin/env python3
"""Render a coverage plan from a generated eval suite.

Turns `evals/evals.json` into `evals/PLAN.md`: the table that lets a reader audit
what is covered without opening the JSON. Generated, not hand-written, so it can
never drift from the suite it describes.

Stdlib only.

Usage:
    python3 render_plan.py <skill>/evals/evals.json [--out <skill>/evals/PLAN.md]
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from validate_evals import CATEGORIES, load_suite  # noqa: E402

CATEGORY_MEANING = {
    "gate": "a precondition that must fire before any work",
    "process": "a mandated order or required step",
    "output": "a required shape for the result",
    "fence": "something the skill must not do",
    "trigger": "phrases that should and should not fire the skill",
}


def _cell(text: str, limit: int = 72) -> str:
    """One-line, pipe-safe table cell."""
    flat = " ".join(str(text).split()).replace("|", "\\|")
    return flat if len(flat) <= limit else flat[: limit - 1].rstrip() + "…"


def render(suite: dict) -> str:
    evals = suite.get("evals", [])
    name = suite.get("skill_name", "(unnamed)")

    by_tier: dict[str, list[dict]] = {}
    by_category: dict[str, int] = {}
    for ev in evals:
        by_tier.setdefault(ev.get("tier", "?"), []).append(ev)
        cat = ev.get("category", "?")
        by_category[cat] = by_category.get(cat, 0) + 1

    lines = [f"# Eval plan — {name}", ""]
    lines.append(
        f"{len(evals)} cases, generated from the skill's own directives. "
        "Every case cites the line it came from; run "
        "`validate_evals.py --source SKILL.md` to confirm those citations still match."
    )
    lines.append("")

    lines.append("## Coverage")
    lines.append("")
    lines.append("| Category | Cases | What it covers |")
    lines.append("|---|---|---|")
    for cat in CATEGORIES:
        n = by_category.get(cat, 0)
        note = CATEGORY_MEANING[cat]
        if n == 0:
            note = f"{note} — **none found in this skill**"
        lines.append(f"| `{cat}` | {n} | {note} |")
    lines.append("")

    for tier in ("core", "extended"):
        group = by_tier.get(tier)
        if not group:
            continue
        lines.append(f"## {tier.capitalize()} ({len(group)})")
        lines.append("")
        lines.append("| id | Category | Source directive | Prompt | Prompt withholds |")
        lines.append("|---|---|---|---|---|")
        for ev in sorted(group, key=lambda e: e.get("id", 0)):
            withheld = ev.get("withholds")
            if isinstance(withheld, list):
                withheld = ", ".join(str(w) for w in withheld)
            lines.append(
                f"| {ev.get('id', '?')} | `{ev.get('category', '?')}` | "
                f"{_cell(ev.get('source', ''))} | {_cell(ev.get('prompt', ''))} | "
                f"{_cell(withheld or '—', 30)} |"
            )
        lines.append("")

    other = [t for t in by_tier if t not in ("core", "extended")]
    if other:
        lines.append(f"Cases in unrecognised tiers: {', '.join(sorted(other))}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a coverage plan from an eval suite")
    parser.add_argument("suite", help="Path to evals.json")
    parser.add_argument("--out", default=None, help="Output path (default: PLAN.md beside the suite)")
    args = parser.parse_args()

    try:
        suite = load_suite(args.suite)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    out = pathlib.Path(args.out) if args.out else pathlib.Path(args.suite).with_name("PLAN.md")
    out.write_text(render(suite))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
