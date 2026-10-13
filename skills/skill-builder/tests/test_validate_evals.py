"""Tests for the eval-suite validator.

Each test takes the one valid fixture and breaks exactly one thing, then asserts
the validator catches it. That keeps the fixtures readable (one good suite, not
fourteen bad ones) while still pinning every failure mode.
"""

import copy
import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

from validate_evals import CATEGORIES, load_suite, validate  # noqa: E402

FIXTURES = HERE / "fixtures"
VALID = json.loads((FIXTURES / "valid_suite.json").read_text())
SKILL_MD = (FIXTURES / "SKILL.md").read_text()


@pytest.fixture
def suite():
    return copy.deepcopy(VALID)


def errors_for(suite, **kwargs):
    errors, _, _ = validate(suite, **kwargs)
    return errors


def warnings_for(suite, **kwargs):
    _, warnings, _ = validate(suite, **kwargs)
    return warnings


# --- the happy path -------------------------------------------------------


def test_valid_suite_passes(suite):
    assert errors_for(suite) == []


def test_valid_suite_passes_traceability_and_tier(suite):
    assert errors_for(suite, tier="core", source_text=SKILL_MD) == []


def test_coverage_counts_every_category(suite):
    _, _, coverage = validate(suite, tier="core", source_text=SKILL_MD)
    assert set(coverage) <= set(CATEGORIES)
    assert sum(coverage.values()) == len(suite["evals"])


# --- withholds: prompt/assertion contradictions ---------------------------


def test_valid_fixture_has_no_warnings(suite):
    assert warnings_for(suite, tier="core", source_text=SKILL_MD) == []


def test_prompt_supplying_a_withheld_value_is_an_error(suite):
    # The exact defect two simulated runs hit: the prompt says "daily" and the
    # assertion expects the skill to ask about cadence.
    suite["evals"][3]["prompt"] = "reconcile the ledger daily, I'm not sure how often to run it"
    errors = errors_for(suite, tier="core", source_text=SKILL_MD)
    assert any("fighting each other" in e for e in errors)


def test_withholds_match_is_case_insensitive(suite):
    suite["evals"][3]["prompt"] = "reconcile the ledger. Daily would be fine."
    errors = errors_for(suite, tier="core", source_text=SKILL_MD)
    assert any("fighting each other" in e for e in errors)


def test_withholds_empty_string_is_an_error(suite):
    suite["evals"][3]["withholds"] = "   "
    assert any("withholds" in e for e in errors_for(suite))


def test_withholds_accepts_a_list(suite):
    suite["evals"][3]["withholds"] = ["daily", "hourly"]
    assert errors_for(suite, tier="core", source_text=SKILL_MD) == []


def test_withholds_list_catches_the_second_literal(suite):
    suite["evals"][3]["prompt"] = "reconcile the ledger, hourly is fine"
    suite["evals"][3]["withholds"] = ["daily", "hourly"]
    errors = errors_for(suite, tier="core", source_text=SKILL_MD)
    assert any("hourly" in e for e in errors)


def test_withholds_rejects_a_list_with_an_empty_entry(suite):
    suite["evals"][3]["withholds"] = ["daily", "  "]
    assert any("withholds" in e for e in errors_for(suite))


def test_elicitation_without_withholds_warns(suite):
    del suite["evals"][3]["withholds"]
    warnings = warnings_for(suite, tier="core", source_text=SKILL_MD)
    assert any("withholds" in w for w in warnings)
    assert errors_for(suite, tier="core", source_text=SKILL_MD) == []


def test_non_elicitation_expectations_do_not_warn(suite):
    # "emits"/"is not modified" are not elicitation verbs, so no nudge.
    del suite["evals"][3]["withholds"]
    suite["evals"][3]["expectations"] = ["The output is a markdown table"]
    assert warnings_for(suite) == []


# --- structural failures --------------------------------------------------


def test_missing_skill_name(suite):
    del suite["skill_name"]
    assert any("skill_name" in e for e in errors_for(suite))


def test_blank_skill_name(suite):
    suite["skill_name"] = "   "
    assert any("skill_name" in e for e in errors_for(suite))


def test_empty_evals(suite):
    suite["evals"] = []
    assert any("non-empty list" in e for e in errors_for(suite))


def test_evals_not_a_list(suite):
    suite["evals"] = {"id": 1}
    assert any("non-empty list" in e for e in errors_for(suite))


def test_duplicate_id(suite):
    suite["evals"][1]["id"] = suite["evals"][0]["id"]
    assert any("duplicate id" in e for e in errors_for(suite))


def test_missing_required_field(suite):
    del suite["evals"][0]["expected_output"]
    assert any("expected_output" in e for e in errors_for(suite))


def test_duplicate_prompt(suite):
    suite["evals"][1]["prompt"] = suite["evals"][0]["prompt"]
    assert any("duplicate prompt" in e for e in errors_for(suite))


def test_empty_expectations(suite):
    suite["evals"][0]["expectations"] = []
    assert any("expectations" in e for e in errors_for(suite))


def test_duplicate_assertion_across_cases(suite):
    suite["evals"][1]["expectations"] = list(suite["evals"][0]["expectations"])
    assert any("assertion duplicated" in e for e in errors_for(suite))


# --- the checks skill-creator would not catch -----------------------------


def test_missing_source(suite):
    del suite["evals"][2]["source"]
    assert any("missing source" in e for e in errors_for(suite))


def test_source_not_present_in_target(suite):
    suite["evals"][2]["source"] = "A directive that was never written down."
    assert any("not found verbatim" in e for e in errors_for(suite, source_text=SKILL_MD))


def test_source_matches_across_a_line_wrap(suite):
    # The gate sentence wraps in the fixture; whitespace must not decide this.
    suite["evals"][2]["source"] = "Confirm the ledger source is   configured."
    assert errors_for(suite, source_text=SKILL_MD) == []


def test_traceability_skipped_when_no_source_given(suite):
    suite["evals"][2]["source"] = "not in the file at all"
    assert errors_for(suite, source_text=None) == []


def test_bad_category(suite):
    suite["evals"][0]["category"] = "vibes"
    assert any("category" in e for e in errors_for(suite))


def test_missing_category(suite):
    del suite["evals"][0]["category"]
    assert any("missing category" in e for e in errors_for(suite))


def test_bad_tier(suite):
    suite["evals"][0]["tier"] = "gold"
    assert any("tier" in e for e in errors_for(suite))


def test_missing_tier(suite):
    del suite["evals"][0]["tier"]
    assert any("missing tier" in e for e in errors_for(suite))


def test_core_tier_too_small(suite):
    suite["evals"] = suite["evals"][:5]
    assert any("8-12 cases" in e for e in errors_for(suite, tier="core"))


def test_core_tier_too_large(suite):
    suite["evals"] = suite["evals"] * 2
    for i, ev in enumerate(suite["evals"]):
        ev["id"] = i + 1
        ev["prompt"] = f"{ev['prompt']} (#{i})"
    assert any("8-12 cases" in e for e in errors_for(suite, tier="core"))


def test_core_size_not_enforced_without_tier(suite):
    suite["evals"] = suite["evals"][:3]
    assert errors_for(suite) == []


def test_non_dict_suite():
    errors, _, _ = validate(["not", "an", "object"])
    assert errors


# --- loading --------------------------------------------------------------


def test_load_missing_file_raises(tmp_path):
    with pytest.raises(ValueError, match="no such file"):
        load_suite(tmp_path / "absent.json")


def test_load_malformed_json_raises(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{ this is not json")
    with pytest.raises(ValueError, match="not valid JSON"):
        load_suite(bad)


def test_load_valid_roundtrips(tmp_path):
    p = tmp_path / "ok.json"
    p.write_text(json.dumps(VALID))
    assert load_suite(p) == VALID
