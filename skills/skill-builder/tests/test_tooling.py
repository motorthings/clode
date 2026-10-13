"""Tests for the repair script and the plan renderer.

The repair script is the one piece that decides whether trigger measurement
works at all on a given machine, and it runs unattended after plugin updates.
It gets tests for that reason.
"""

import importlib.util
import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"


def _load(module_name, filename):
    spec = importlib.util.spec_from_file_location(module_name, SCRIPTS / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


patcher = _load("patch_skill_creator", "patch-skill-creator.py")
planner = _load("render_plan", "render_plan.py")
sys.path.insert(0, str(SCRIPTS))


def stock_source() -> str:
    """The unpatched upstream file.

    Note what is *not* here: OLD_ROOT and OLD_CWD. Those anchor on text the
    staging fix produces, so they cannot appear in a genuinely stock file. The
    patches are chained, and a test that flattens them into one string is
    testing something upstream never shipped.
    """
    return "\n".join([
        patcher.OLD_STAGE, patcher.OLD_CLEAN, patcher.OLD_DETECT,
        patcher.OLD_DOC, patcher.OLD_LEFTOVER,
    ])


# --- repair script -------------------------------------------------------


def test_stock_source_reports_nothing_applied():
    present, unrepairable = patcher.status(stock_source())
    assert present == []
    assert unrepairable == []


def test_stock_source_can_be_fully_repaired():
    present, unrepairable = patcher.status(patcher.apply(stock_source()))
    assert unrepairable == []
    assert len(present) == len(patcher.FIXES)


def test_apply_is_idempotent():
    once = patcher.apply(stock_source())
    assert patcher.apply(once) == once


def test_every_fix_has_a_distinct_marker():
    markers = [m for _, m, _ in patcher.FIXES]
    assert len(markers) == len(set(markers))


def test_marker_absent_from_its_own_stock_form():
    # A marker that appears in the unpatched text would make `status` report a
    # fix as applied when it is not.
    stock = stock_source()
    for name, marker, _ in patcher.FIXES:
        assert marker not in stock, f"{name}: marker {marker!r} leaks into stock text"


def test_upstream_shape_change_is_reported_repairable_false():
    # Detector anchor removed, marker absent: cannot be fixed, must be said.
    mangled = stock_source().replace(patcher.OLD_DETECT, "# rewritten upstream")
    present, unrepairable = patcher.status(mangled)
    assert "detector" in unrepairable


def test_partially_patched_source_reports_only_the_gap():
    src = patcher.apply(stock_source())
    src = src.replace(patcher.NEW_DETECT, patcher.OLD_DETECT)
    present, unrepairable = patcher.status(src)
    assert "detector" not in present
    assert "detector" not in unrepairable  # repairable, just not done
    assert len(present) == len(patcher.FIXES) - 1


def test_patcher_has_no_hardcoded_user_paths():
    text = (SCRIPTS / "patch-skill-creator.py").read_text()
    assert "/Users/" not in text
    assert "Path.home()" in text


# --- plan renderer -------------------------------------------------------


def test_plan_renders_withholds_column():
    suite = {
        "skill_name": "demo",
        "evals": [{
            "id": 1, "prompt": "do the thing without naming the cadence",
            "expected_output": "asks", "expectations": ["asks for the cadence"],
            "source": "ask for the cadence", "withholds": ["daily", "hourly"],
            "category": "gate", "tier": "core",
        }],
    }
    out = planner.render(suite)
    assert "Prompt withholds" in out
    assert "daily, hourly" in out


def test_plan_marks_cases_with_nothing_withheld():
    suite = {
        "skill_name": "demo",
        "evals": [{
            "id": 1, "prompt": "p", "expected_output": "e", "expectations": ["a"],
            "source": "s", "category": "fence", "tier": "core",
        }],
    }
    assert "—" in planner.render(suite)


def test_plan_reports_an_empty_category_as_a_finding():
    suite = {
        "skill_name": "demo",
        "evals": [{
            "id": 1, "prompt": "p", "expected_output": "e", "expectations": ["a"],
            "source": "s", "category": "fence", "tier": "core",
        }],
    }
    assert "none found in this skill" in planner.render(suite)
