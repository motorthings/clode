"""Tests for the SKILL.md well-formedness linter.

One good skill, then each test breaks exactly one thing and asserts the linter
catches it. The stray-RULE case is a regression guard: a procedure step titled
"For each STATUTE / RULE" must not be mistaken for the anti-patterns section.
"""

import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

from check_skill import check, fence_item_count  # noqa: E402

WELL_FORMED = """---
name: ledger-reconcile
description: Reconcile a ledger against a feed. Use when the user says "reconcile my books".
---

# Ledger Reconcile

Do the thing.

## Procedure
1. Read the ledger.
2. Match the feed.

## Anti-Patterns
- Never invent a transaction to force a balance.
- Do not drop a line you cannot match — flag it.
- Avoid rounding silently.
"""


def errors(text):
    return check(text)[0]


def warnings(text):
    return check(text)[1]


def test_well_formed_skill_passes_clean():
    errs, warns = check(WELL_FORMED)
    assert errs == []
    assert warns == []


def test_empty_file_fails():
    assert any("empty" in e for e in errors(""))


def test_missing_name_fails():
    text = WELL_FORMED.replace("name: ledger-reconcile\n", "").replace("# Ledger Reconcile", "")
    assert any("no name" in e for e in errors(text))


def test_h1_satisfies_name_without_frontmatter():
    text = "# Just An H1\n\n## Rules\n- a\n- b\n- c\n"
    assert not any("no name" in e for e in errors(text))


def test_frontmatter_without_description_fails():
    text = WELL_FORMED.replace(
        'description: Reconcile a ledger against a feed. Use when the user says "reconcile my books".\n',
        "",
    )
    assert any("no description" in e for e in errors(text))


def test_description_without_trigger_warns():
    text = WELL_FORMED.replace(
        'description: Reconcile a ledger against a feed. Use when the user says "reconcile my books".',
        "description: Reconcile a ledger against a feed.",
    )
    assert any("names no trigger" in w for w in warnings(text))


def test_no_frontmatter_warns_not_errors():
    text = "# A Skill\n\n## Rules\n- a\n- b\n- c\n"
    errs, warns = check(text)
    assert not any("description" in e for e in errs)
    assert any("no YAML frontmatter" in w for w in warns)


def test_missing_anti_patterns_fails():
    text = WELL_FORMED.split("## Anti-Patterns")[0]
    assert any("no anti-patterns" in e for e in errors(text))


def test_thin_anti_patterns_fails():
    text = WELL_FORMED.rsplit("- Avoid rounding silently.\n", 1)[0].rsplit(
        "- Do not drop a line you cannot match — flag it.\n", 1
    )[0]
    assert any("at least 3" in e for e in errors(text))


def test_placeholder_warns():
    text = WELL_FORMED.replace("Do the thing.", "TODO: write this")
    assert any("stub" in w for w in warnings(text))


def test_stray_rule_in_procedure_is_not_the_fence_section():
    # "For each STATUTE / RULE" matches the fence vocabulary but has no items.
    # The real "## Rules" below carries five. Max-count must find the real one.
    body = (
        "# Cite Check\n"
        "## Procedure\n"
        "### 4. For each STATUTE / RULE\n"
        "Resolve it.\n"
        "## Rules\n"
        "- one\n- two\n- three\n- four\n- five\n"
    )
    assert fence_item_count(body) == 5


def test_skeleton_warns_on_too_few_sections():
    text = "---\nname: x\ndescription: use when foo\n---\n# X\n## Anti-Patterns\n- a\n- b\n- c\n"
    assert any("skeleton" in w for w in warnings(text))
