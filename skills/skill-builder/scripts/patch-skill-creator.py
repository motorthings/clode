#!/usr/bin/env python3
"""Repair skill-creator's trigger measurement, and verify the repair is in place.

skill-creator's `run_eval.py` scores 0% for every skill on this CLI, for three
compounding reasons. All three had to be fixed before the description optimiser
could see anything:

  1. STAGING    It wrote its test skill to `<root>/.claude/commands/`, which
                loads as a slash command only — the model's auto-trigger list
                never sees it. Now staged to `.claude/skills/<name>/SKILL.md`.
  2. DETECTOR   It bailed with `return False` on the first tool call that wasn't
                `Skill` or `Read`. Now scans the whole stream for a fire.
  3. ISOLATION  Each run got a unique staged name but every run shared one
                project root, so concurrent runs staged identically-described
                skills side by side and the model invoked a sibling. Now each
                run gets its own root.

Evidence: identical queries and staging scored 1/3 and 0/3 before, 3/3 and 2/3-3/3
after, with near-misses correctly at 0/3.

**Run this after every `claude plugin update`** — the cache is replaced wholesale
and all three fixes are lost silently. Idempotent.

Usage:
    python3 patch-skill-creator.py            # apply, then verify
    python3 patch-skill-creator.py --check    # report only, change nothing

Exit codes: 0 healthy or repaired, 1 cannot repair (upstream changed shape),
2 skill-creator is not installed.
"""

import argparse
import glob
import pathlib
import sys

OLD_STAGE = '''    project_commands_dir = Path(project_root) / ".claude" / "commands"
    command_file = project_commands_dir / f"{clean_name}.md"

    try:
        project_commands_dir.mkdir(parents=True, exist_ok=True)
        # Use YAML block scalar to avoid breaking on quotes in description
        indented_desc = "\\n  ".join(skill_description.split("\\n"))
        command_content = (
            f"---\\n"
            f"description: |\\n"
            f"  {indented_desc}\\n"
            f"---\\n\\n"
            f"# {skill_name}\\n\\n"
            f"This skill handles: {skill_description}\\n"
        )
        command_file.write_text(command_content)'''

NEW_STAGE = '''    # Claude Code exposes model-invocable skills from .claude/skills/<name>/SKILL.md.
    # Entries in .claude/commands/ load as slash commands only and never appear in
    # the model's available_skills list, so staging there yields a silent 0% trigger.
    project_skills_dir = Path(project_root) / ".claude" / "skills"
    skill_dir = project_skills_dir / clean_name
    command_file = skill_dir / "SKILL.md"

    try:
        skill_dir.mkdir(parents=True, exist_ok=True)
        indented_desc = "\\n  ".join(skill_description.split("\\n"))
        command_content = (
            f"---\\n"
            f"name: {clean_name}\\n"
            f"description: |\\n"
            f"  {indented_desc}\\n"
            f"---\\n\\n"
            f"# {skill_name}\\n\\n"
            f"This skill handles: {skill_description}\\n"
        )
        command_file.write_text(command_content)'''

OLD_CLEAN = '''    finally:
        if command_file.exists():
            command_file.unlink()'''

NEW_CLEAN = '''    finally:
        shutil.rmtree(skill_dir, ignore_errors=True)'''

# Detector fix. The original bailed with `return False` on the first tool call
# that was not Skill or Read, and returned on the first content_block_stop
# regardless of which block it belonged to. In a bare `claude -p` the model
# routinely does something else first, so real fires were discarded and the
# trigger rate read 0 however good the description was.
#
# Measured 2026-10-13, same queries and same staging, only the detector
# differing: the skill's own literal triggers scored 3/3 under this scan and
# 0/3-1/3 under the original. That null result is what made the description
# optimiser appear to find nothing across three iterations.
OLD_DETECT = '''                    if event.get("type") == "stream_event":
                        se = event.get("event", {})
                        se_type = se.get("type", "")

                        if se_type == "content_block_start":
                            cb = se.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                tool_name = cb.get("name", "")
                                if tool_name in ("Skill", "Read"):
                                    pending_tool_name = tool_name
                                    accumulated_json = ""
                                else:
                                    return False

                        elif se_type == "content_block_delta" and pending_tool_name:
                            delta = se.get("delta", {})
                            if delta.get("type") == "input_json_delta":
                                accumulated_json += delta.get("partial_json", "")
                                if clean_name in accumulated_json:
                                    return True

                        elif se_type in ("content_block_stop", "message_stop"):
                            if pending_tool_name:
                                return clean_name in accumulated_json
                            if se_type == "message_stop":
                                return False

                    # Fallback: full assistant message
                    elif event.get("type") == "assistant":
                        message = event.get("message", {})
                        for content_item in message.get("content", []):
                            if content_item.get("type") != "tool_use":
                                continue
                            tool_name = content_item.get("name", "")
                            tool_input = content_item.get("input", {})
                            if tool_name == "Skill" and clean_name in tool_input.get("skill", ""):
                                triggered = True
                            elif tool_name == "Read" and clean_name in tool_input.get("file_path", ""):
                                triggered = True
                            return triggered

                    elif event.get("type") == "result":
                        return triggered'''

NEW_DETECT = '''                    # Scan the whole stream. A fire is any Skill invocation
                    # naming the staged skill, wherever it appears.
                    if event.get("type") == "assistant":
                        for content_item in event.get("message", {}).get("content", []):
                            if content_item.get("type") != "tool_use":
                                continue
                            tool_name = content_item.get("name", "")
                            tool_input = content_item.get("input", {}) or {}
                            if tool_name == "Skill" and clean_name in str(tool_input.get("skill", "")):
                                return True
                            if tool_name == "Read" and clean_name in str(tool_input.get("file_path", "")):
                                return True

                    elif event.get("type") == "result":
                        return triggered'''

MARKER = "project_skills_dir"
DETECT_MARKER = "Scan the whole stream"
ROOT_MARKER = "run_root"
TIDY_MARKER = "Stages the skill in"

# Tidy-up: the docstring still describes the pre-fix behaviour, and the cleanup
# removed only the skill dir, leaving one `.run-<name>/` directory behind per
# run. Both are small; the docstring is the one that misleads, because it now
# states the opposite of what the code does.
OLD_DOC = '''    Creates a command file in .claude/commands/ so it appears in Claude's
    available_skills list, then runs `claude -p` with the raw query.'''
NEW_DOC = '''    Stages the skill in .claude/skills/ so it appears in Claude's
    available_skills list, then runs `claude -p` with the raw query.'''

OLD_LEFTOVER = '''        shutil.rmtree(skill_dir, ignore_errors=True)'''
NEW_LEFTOVER = '''        shutil.rmtree(run_root, ignore_errors=True)'''

# Isolation fix — the real cause of the 0% trigger rates.
#
# Each run is given a UNIQUE staged name (`<skill>-skill-<uuid>`) but every run
# shares one project root. With `--num-workers 5`, up to five identically
# described skills are staged at once under different names; the model invokes
# whichever sibling it encounters first, and the detector — which accepts only
# this run's own name — sees nothing. Detection fails even though the skill
# fired.
#
# Measured 2026-10-13: identical queries against identical staging scored 1/3
# and 0/3 under a shared root, and 3/3 under a per-run root. This, not the
# bail-out in the stream scanner, is what made the description optimiser look
# like it was finding nothing.
OLD_ROOT = '''    project_skills_dir = Path(project_root) / ".claude" / "skills"
    skill_dir = project_skills_dir / clean_name
    command_file = skill_dir / "SKILL.md"'''

NEW_ROOT = '''    # Per-run project root. A shared root stages every concurrent run's skill
    # side by side; identical descriptions under different names mean the model
    # invokes a sibling and this run's name never appears.
    run_root = Path(project_root) / f".run-{clean_name}"
    project_skills_dir = run_root / ".claude" / "skills"
    skill_dir = project_skills_dir / clean_name
    command_file = skill_dir / "SKILL.md"'''

OLD_CWD = '''            cwd=project_root,'''
NEW_CWD = '''            cwd=str(run_root),'''


FIXES = (
    ("staging", MARKER, (OLD_STAGE, OLD_CLEAN)),
    ("detector", DETECT_MARKER, (OLD_DETECT,)),
    ("isolation", ROOT_MARKER, (OLD_ROOT, OLD_CWD)),
    ("tidy", TIDY_MARKER, (OLD_DOC, OLD_LEFTOVER)),
)


def find_targets() -> list[pathlib.Path]:
    """Locate run_eval.py in the plugin cache, whatever version dir it sits under."""
    pattern = (
        pathlib.Path.home()
        / ".claude/plugins/cache/claude-plugins-official/skill-creator/*/skills/skill-creator/scripts/run_eval.py"
    )
    return sorted(pathlib.Path(p) for p in glob.glob(str(pattern)))


def status(src: str) -> tuple[list[str], list[str]]:
    """Return (fixes already applied, fixes that cannot be applied here).

    The patches are chained — the isolation fix anchors on text the staging fix
    produces — so anchors cannot be checked against the original file alone.
    A fix counts as unrepairable only if it is absent AND still absent after a
    full apply. Reporting a repairable file as unrepairable would send someone
    chasing an upstream change that never happened.
    """
    present = [name for name, marker, _ in FIXES if marker in src]
    if len(present) == len(FIXES):
        return present, []

    patched = apply(src)
    unrepairable = [
        name for name, marker, _ in FIXES
        if marker not in src and marker not in patched
    ]
    return present, unrepairable


def apply(src: str) -> str:
    """Apply every fix whose anchor is still present. Returns the new source."""
    if MARKER not in src:
        src = src.replace(OLD_STAGE, NEW_STAGE).replace(OLD_CLEAN, NEW_CLEAN)
        if "import shutil" not in src:
            src = src.replace(
                "import select\nimport subprocess",
                "import select\nimport shutil\nimport subprocess", 1,
            )
    if DETECT_MARKER not in src:
        src = src.replace(OLD_DETECT, NEW_DETECT)
    if ROOT_MARKER not in src:
        src = src.replace(OLD_ROOT, NEW_ROOT).replace(OLD_CWD, NEW_CWD, 1)
    if TIDY_MARKER not in src:
        src = src.replace(OLD_DOC, NEW_DOC).replace(OLD_LEFTOVER, NEW_LEFTOVER, 1)
    return src


def check_only(path: pathlib.Path, verbose: bool) -> int:
    """Report state without touching anything. 0 healthy, 1 needs attention."""
    src = path.read_text()
    present, unrepairable = status(src)
    if unrepairable:
        print(
            f"skill-creator's run_eval.py has changed shape since this patch was written.\n"
            f"  unrepairable: {', '.join(unrepairable)}\n"
            f"  Trigger measurement is very likely broken — it will report 0% for every\n"
            f"  skill. Fix: {sys.argv[0]}",
            file=sys.stderr,
        )
        return 1
    if len(present) < len(FIXES):
        missing = [n for n, _, _ in FIXES if n not in present]
        print(
            f"skill-creator is not patched (missing: {', '.join(missing)}).\n"
            f"  Trigger measurement will report 0% for every skill until this is applied.\n"
            f"  Fix: python3 {sys.argv[0]}",
            file=sys.stderr,
        )
        return 1
    if verbose:
        print("skill-creator trigger measurement: healthy (all 4 fixes present)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="report state and exit; change nothing")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress the success line (for scripting)")
    args = ap.parse_args()

    targets = find_targets()
    if not targets:
        print(
            "skill-creator is not installed, so there is nothing to patch.\n"
            "  claude plugin marketplace update claude-plugins-official\n"
            "  claude plugin install skill-creator@claude-plugins-official\n"
            "  (then run this again — the eval machinery needs it)",
            file=sys.stderr,
        )
        return 2

    rc = 0
    for path in targets:
        if args.check:
            rc = max(rc, check_only(path, verbose=not args.quiet))
            continue

        before = path.read_text()
        present, unrepairable = status(before)
        if unrepairable:
            print(
                f"cannot repair {path}: {', '.join(unrepairable)} no longer match.\n"
                f"  Upstream reshaped the code. Trigger measurement is likely broken.",
                file=sys.stderr,
            )
            rc = 1
            continue

        if len(present) == len(FIXES):
            if not args.quiet:
                print("skill-creator trigger measurement: already healthy")
            continue

        path.write_text(apply(before))

        after_present, after_broken = status(path.read_text())
        if after_broken or len(after_present) < len(FIXES):
            print(f"repair incomplete for {path} — please report this", file=sys.stderr)
            rc = 1
            continue
        if not args.quiet:
            print(f"skill-creator trigger measurement: repaired ({', '.join(after_present)})")

    return rc


if __name__ == "__main__":
    sys.exit(main())
