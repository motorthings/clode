#!/usr/bin/env python3
"""Validate a generated eval suite against skill-creator's contract.

skill-builder emits `evals/evals.json`. This checks the emitted file before it is
handed to skill-creator to run, so a malformed suite fails here rather than
halfway through a model-call loop.

Two things are checked that skill-creator would not catch:

  traceability  Every case carries `source`, a verbatim string from the target
                SKILL.md. With `--source`, this confirms the string is actually
                present in the file. A case that cannot cite a directive is a
                case someone invented, which is the failure this tool exists to
                prevent.

  coverage      Per-category counts, so a suite that quietly forgot gates or
                scope fences is visible rather than assumed.

Stdlib only, matching the house convention (humane-evals, op04-judge).

Usage:
    python3 validate_evals.py evals/evals.json
    python3 validate_evals.py evals/evals.json --tier core --source path/to/SKILL.md
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

CATEGORIES = ("gate", "process", "output", "fence", "trigger")
TIERS = ("core", "extended")
CORE_MIN, CORE_MAX = 8, 12
REQUIRED_EVAL_FIELDS = ("id", "prompt", "expected_output", "expectations")

# Used only to decide whether to nudge the author toward declaring `withholds`.
# A false positive here costs one line of review; a false negative leaves the
# defect invisible. That asymmetry is why a heuristic belongs in the nudge and
# not in the failure.
ELICITATION_NUDGE = re.compile(
    r"(\basks? (?:the user )?(?:for|what|whether|which|how|about)\b"
    r"|\bprompts? the user\b"
    r"|\brequests? (?:the user|confirmation)\b"
    r"|\belicits?\b"
    r"|\bwaits? for the user to\b)",
    re.IGNORECASE,
)


def load_suite(path: str | pathlib.Path) -> dict:
    """Read and parse a suite file. Raises ValueError with a clean message."""
    p = pathlib.Path(path)
    if not p.exists():
        raise ValueError(f"no such file: {p}")
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"{p} is not valid JSON: {exc}") from exc


def validate(
    suite: dict,
    tier: str | None = None,
    source_text: str | None = None,
) -> tuple[list[str], list[str], dict[str, int]]:
    """Return (errors, warnings, coverage).

    Errors mean the suite is malformed or untraceable. Warnings mean it is
    well-formed but probably will not measure anything — a prompt supplying what
    the assertion says the skill must ask for, or a case whose expectation a
    baseline would satisfy anyway.
    """
    errors: list[str] = []
    warnings: list[str] = []
    coverage: dict[str, int] = {}

    if not isinstance(suite, dict):
        return ["suite must be a JSON object"], warnings, coverage

    name = suite.get("skill_name")
    if not isinstance(name, str) or not name.strip():
        errors.append("skill_name must be a non-empty string")

    evals = suite.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals must be a non-empty list")
        return errors, warnings, coverage

    seen_ids: set = set()
    seen_prompts: dict[str, int] = {}
    seen_assertions: dict[str, int] = {}

    for idx, ev in enumerate(evals):
        where = f"evals[{idx}]"
        if not isinstance(ev, dict):
            errors.append(f"{where}: must be an object")
            continue

        ev_id = ev.get("id")
        if ev_id is None:
            errors.append(f"{where}: missing id")
        elif ev_id in seen_ids:
            errors.append(f"{where}: duplicate id {ev_id!r}")
        else:
            seen_ids.add(ev_id)

        for field in REQUIRED_EVAL_FIELDS:
            if field not in ev:
                errors.append(f"{where} (id={ev_id!r}): missing required field {field!r}")

        prompt = ev.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{where} (id={ev_id!r}): prompt must be a non-empty string")
        else:
            if prompt in seen_prompts:
                errors.append(
                    f"{where} (id={ev_id!r}): duplicate prompt, also at id {seen_prompts[prompt]}"
                )
            else:
                seen_prompts[prompt] = ev_id

        expected = ev.get("expected_output")
        if not isinstance(expected, str) or not expected.strip():
            errors.append(f"{where} (id={ev_id!r}): expected_output must be a non-empty string")

        expectations = ev.get("expectations")
        if not isinstance(expectations, list) or not expectations:
            errors.append(f"{where} (id={ev_id!r}): expectations must be a non-empty list")
        else:
            for j, assertion in enumerate(expectations):
                if not isinstance(assertion, str) or not assertion.strip():
                    errors.append(f"{where} (id={ev_id!r}): expectations[{j}] must be a non-empty string")
                    continue
                if assertion in seen_assertions:
                    errors.append(
                        f"{where} (id={ev_id!r}): assertion duplicated from id "
                        f"{seen_assertions[assertion]}: {assertion[:60]!r}"
                    )
                else:
                    seen_assertions[assertion] = ev_id

        category = ev.get("category")
        if category is None:
            errors.append(f"{where} (id={ev_id!r}): missing category")
        elif category not in CATEGORIES:
            errors.append(
                f"{where} (id={ev_id!r}): category {category!r} not one of {list(CATEGORIES)}"
            )
        else:
            coverage[category] = coverage.get(category, 0) + 1

        # Contradiction check. Two independent simulated runs hit the same
        # generator defect: a gate case about asking for the cadence shipped a
        # prompt that already contained "daily", so the skill correctly asked and
        # was then marked down for asking. A lexical overlap test cannot catch
        # that (cadence and daily are synonyms, not the same token), so a gate
        # case declares the literal string its prompt must not contain, and this
        # checks absence exactly.
        withholds = ev.get("withholds")
        if withholds is not None:
            values = [withholds] if isinstance(withholds, str) else withholds
            if (
                not isinstance(values, list)
                or not values
                or not all(isinstance(v, str) and v.strip() for v in values)
            ):
                errors.append(
                    f"{where} (id={ev_id!r}): withholds must be a non-empty string or list of "
                    "non-empty strings"
                )
            elif isinstance(prompt, str):
                leaked = [v.strip() for v in values if v.strip().lower() in prompt.lower()]
                if leaked:
                    errors.append(
                        f"{where} (id={ev_id!r}): the prompt contains {leaked}, which this case "
                        "declares it withholds. The prompt and the assertion are fighting each "
                        "other."
                    )
        elif category == "gate" and isinstance(expectations, list) and any(
            isinstance(a, str) and ELICITATION_NUDGE.search(a) for a in expectations
        ):
            warnings.append(
                f"{where} (id={ev_id!r}): an assertion has the skill elicit something, but the "
                "case declares no `withholds`. If the thing elicited is a concrete literal "
                "(a cadence, a filename, a number), name it so the prompt cannot quietly supply "
                "it. If it is open-ended (a problem statement, an example), no `withholds` is "
                "needed and this warning can be ignored."
            )

        ev_tier = ev.get("tier")
        if ev_tier is None:
            errors.append(f"{where} (id={ev_id!r}): missing tier")
        elif ev_tier not in TIERS:
            errors.append(f"{where} (id={ev_id!r}): tier {ev_tier!r} not one of {list(TIERS)}")

        source = ev.get("source")
        if not isinstance(source, str) or not source.strip():
            errors.append(
                f"{where} (id={ev_id!r}): missing source — every case must cite the "
                "directive it came from"
            )
        elif source_text is not None:
            if _normalize(source) not in _normalize(source_text):
                errors.append(
                    f"{where} (id={ev_id!r}): source not found verbatim in the target "
                    f"SKILL.md: {source[:70]!r}"
                )

    if tier == "core":
        n = len(evals)
        if not CORE_MIN <= n <= CORE_MAX:
            errors.append(
                f"core tier must hold {CORE_MIN}-{CORE_MAX} cases, found {n} "
                "(do not pad to reach the floor — report the gap instead)"
            )

    return errors, warnings, coverage


def _normalize(text: str) -> str:
    """Collapse whitespace so a source quoted across a line wrap still matches."""
    return " ".join(text.split())


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generated eval suite")
    parser.add_argument("suite", help="Path to evals.json")
    parser.add_argument("--tier", choices=TIERS, default=None, help="Apply tier size rules")
    parser.add_argument("--source", default=None, help="Path to the target SKILL.md for traceability")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as fatal (use in the build loop, not in CI on an unchanged suite)",
    )
    args = parser.parse_args()

    try:
        suite = load_suite(args.suite)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    source_text = None
    if args.source:
        sp = pathlib.Path(args.source)
        if not sp.exists():
            print(f"FAIL: --source not found: {sp}", file=sys.stderr)
            return 1
        source_text = sp.read_text()

    errors, warnings, coverage = validate(suite, tier=args.tier, source_text=source_text)

    total = len(suite.get("evals", [])) if isinstance(suite, dict) else 0
    print(f"cases: {total}")
    for category in CATEGORIES:
        print(f"  {category:<8} {coverage.get(category, 0)}")

    if errors:
        print(f"\nFAIL: {len(errors)} problem(s)", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    if warnings:
        print(f"\nWARN: {len(warnings)} case(s) probably will not measure anything", file=sys.stderr)
        for warn in warnings:
            print(f"  - {warn}", file=sys.stderr)
        if args.strict:
            print("\nFAIL (--strict): warnings are fatal", file=sys.stderr)
            return 1
        print("\nOK (warnings above are not fatal without --strict)")
        return 0

    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
