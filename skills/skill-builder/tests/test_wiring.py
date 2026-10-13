"""Structural invariants for this skill.

These do not test behaviour. They test that the pieces are connected: that every
reference the SKILL.md points at exists, that no reference sits orphaned, and
that the guardrails are wired into both the build flow and the eval flow.

They exist because a rename or a delete would otherwise degrade the skill
silently — the interview would keep running and simply never read the file that
was supposed to make it safe.
"""

import pathlib
import re

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
SKILL_MD = SKILL_DIR / "SKILL.md"
REFS = SKILL_DIR / "references"
SCRIPTS = SKILL_DIR / "scripts"

# Guardrails that must be reached from both halves of the procedure.
# Build side: SKILL.md. Eval side: eval-procedure.md.
BOTH_FLOWS = ("safety.md",)


def referenced_files(text: str, folder: str, suffix: str) -> set[str]:
    return set(re.findall(rf"{folder}/([A-Za-z0-9_-]+{suffix})", text))


def _external_dirs() -> list[pathlib.Path]:
    """The skill-creator install, whose scripts and references this skill cites.

    SKILL.md legitimately points at `scripts/aggregate_benchmark.py` and
    `references/schemas.md`, which live there rather than here. A missing file
    that resolves in that tree is an external reference, not a broken link.
    """
    base = pathlib.Path.home() / ".claude/plugins/cache/claude-plugins-official/skill-creator"
    return [p for p in base.glob("*/skills/skill-creator") if p.is_dir()]


def _resolves_externally(name: str, folder: str) -> bool:
    return any((d / folder / name).exists() for d in _external_dirs())


def _broken(text: str, folder: str, suffix: str, local: pathlib.Path) -> list[str]:
    return sorted(
        n for n in referenced_files(text, folder, suffix)
        if not (local / n).exists() and not _resolves_externally(n, folder)
    )


def test_every_reference_mentioned_exists_on_disk():
    broken = _broken(SKILL_MD.read_text(), "references", r"\.md", REFS)
    assert broken == [], f"SKILL.md points at references that do not exist: {broken}"


def test_no_orphaned_reference_files():
    mentioned = referenced_files(SKILL_MD.read_text(), "references", r"\.md")
    on_disk = {p.name for p in REFS.glob("*.md")}
    orphans = sorted(on_disk - mentioned)
    assert orphans == [], f"reference files nothing points at: {orphans}"


def test_every_script_mentioned_exists_on_disk():
    broken = _broken(SKILL_MD.read_text(), "scripts", r"\.py", SCRIPTS)
    assert broken == [], f"SKILL.md points at scripts that do not exist: {broken}"


def test_guardrails_reach_both_the_build_and_the_eval():
    skill_text = SKILL_MD.read_text()
    eval_text = (REFS / "eval-procedure.md").read_text()
    unreached = [
        name for name in BOTH_FLOWS
        if name not in skill_text or name not in eval_text
    ]
    assert unreached == [], (
        f"these guardrails are not wired into both flows: {unreached}. "
        "A safety rule in the skill with no eval case is an untested claim."
    )


def test_environment_check_precedes_the_eval_step():
    # The tool-scope check is a build-time guardrail; it must be reachable from
    # the phase that designs dependencies, not only from the reference table.
    text = SKILL_MD.read_text()
    phase5 = text.split("## Phase 5", 1)
    assert len(phase5) == 2, "Phase 5 heading is gone"
    body = phase5[1].split("## Phase 6", 1)[0]
    assert "environment.md" in body, "Phase 5 no longer calls the environment check"
    assert "safety.md" in body, "Phase 5 no longer calls the safety pass"


def test_the_completion_condition_is_stated():
    # The skill must say that validation is not the end of the process.
    text = SKILL_MD.read_text()
    assert "benchmark.json" in text, (
        "the skill no longer states a completion condition for the eval step"
    )
