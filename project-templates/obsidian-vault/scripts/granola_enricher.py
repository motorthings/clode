#!/usr/bin/env python3
"""
Granola Enrichment Processor

Generates enriched meeting intelligence summaries using the Stuart Winter-Tear /
Unhyped decision-forcing framework.

Handles two Granola export formats:
  - Current: single .md file in Granola/ with summary + transcript inline
  - Legacy:  separate files in Granola/Summaries/ and Granola/Transcripts/

Run modes:
  python3 granola_enricher.py           # process any new unprocessed files
  python3 granola_enricher.py --backfill # process ALL legacy Summaries/ files

Triggered automatically by launchd when new files appear in Granola/.
"""

import os
import sys
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Paths ────────────────────────────────────────────────────────────────────

VAULT = Path(os.environ.get("OBSIDIAN_VAULT_PATH", Path.home() / "Documents" / "Vault"))
GRANOLA_DIR = VAULT / "Granola"
SUMMARIES_DIR = GRANOLA_DIR / "Summaries"
TRANSCRIPTS_DIR = GRANOLA_DIR / "Transcripts"
ENRICHED_DIR = GRANOLA_DIR / "Enriched"
ARCHIVE_DIR = GRANOLA_DIR / "Archive"

LOG_FILE = Path.home() / "Library" / "Logs" / "granola-enricher.log"

# ── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ── Prompt ───────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are processing meeting notes for Charlie Fuller, an AI strategy leader at Contentful.
Generate enriched meeting intelligence using the Stuart Winter-Tear / Unhyped decision-forcing
framework. The output must be comprehensive enough that the raw transcript never needs to be
read again — except to attribute a specific verbatim quote."""

ENRICHMENT_TEMPLATE = """Meeting: {title}
Date: {date}

Original summary:
{summary}

Transcript (first 6000 chars):
{transcript}

---

Generate an enriched meeting intelligence document in exactly this structure.
Be specific and substantive. Omit any section that has nothing meaningful — do not pad.

## Meeting Intelligence: {title}
**Date:** {date} | **Attendees:** [extract from content] | **Context:** [project/initiative]

### State in Motion
What situation, metric, outcome, or relationship is actively in play — and which direction is it moving?
Tie to strategic pillars where relevant (ENABLE / OPERATIONALIZE / GOVERN).

### Decisions Made
| Decision | Owner | What It Unlocks |
|---|---|---|

### Decisions Pending / Decision-Forcing
| Decision Needed | Owner | Forcing Function | Urgency |
|---|---|---|---|

### Initiative Connections
Which strategic initiatives does this meeting advance, block, or complicate — and how?

### Signal Worth Keeping
New information, stance shifts, risks surfaced, or anything that materially changes the picture.

### Actions
| Owner | Action | By When |
|---|---|---|

### Quotes
[1–3 verbatim quotes with speaker — only what's worth attributing. Omit if nothing stands out.]"""


# ── API key ───────────────────────────────────────────────────────────────────

def get_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key and not key.startswith("your-"):
        return key

    config_path = Path(__file__).parent / "config.py"
    if config_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        cfg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cfg)
        key = getattr(cfg, "ANTHROPIC_API_KEY", "")
        if key and not key.startswith("your-"):
            return key

    log.error("No valid ANTHROPIC_API_KEY found. Set it in config.py or as an env var.")
    sys.exit(1)


# ── File parsing ─────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_body, content) from a file with optional --- delimiters."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", text


def extract_title_date(frontmatter: str, fallback_stem: str) -> tuple[str, str]:
    title = fallback_stem
    date = ""
    for line in frontmatter.splitlines():
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"')
        if line.startswith("created_at:"):
            raw = line.split(":", 1)[1].strip()
            try:
                date = datetime.fromisoformat(raw.replace("Z", "+00:00")).strftime("%Y-%m-%d")
            except ValueError:
                date = raw[:10]
    return title, date


def parse_inline_file(path: Path) -> dict:
    """Parse a current-format Granola file (summary + transcript inline)."""
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    title, date = extract_title_date(frontmatter, path.stem)

    summary, transcript = body.strip(), ""
    if "# Transcript" in body:
        parts = body.split("# Transcript", 1)
        summary = parts[0].strip()
        transcript = parts[1].strip()

    return {"title": title, "date": date, "frontmatter": frontmatter,
            "summary": summary, "transcript": transcript, "source": path}


def find_transcript_for_summary(summary_path: Path) -> Path | None:
    """Find the matching transcript file for a legacy Summaries/ file."""
    stem = summary_path.stem

    candidates = [
        TRANSCRIPTS_DIR / f"{stem}-transcript.md",
        TRANSCRIPTS_DIR / f"{stem}.md",
        TRANSCRIPTS_DIR / (stem.replace("Summary", "Transcript") + ".md"),
        TRANSCRIPTS_DIR / (stem.replace("Meeting Summary", "Meeting Transcript") + ".md"),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def parse_legacy_files(summary_path: Path) -> dict:
    """Parse a legacy-format Granola pair (Summaries/ + optional Transcripts/)."""
    text = summary_path.read_text(encoding="utf-8")
    frontmatter, summary = parse_frontmatter(text)
    title, date = extract_title_date(frontmatter, summary_path.stem)

    transcript = ""
    transcript_path = find_transcript_for_summary(summary_path)
    if transcript_path:
        t_text = transcript_path.read_text(encoding="utf-8")
        _, transcript = parse_frontmatter(t_text)

    return {"title": title, "date": date, "frontmatter": frontmatter,
            "summary": summary.strip(), "transcript": transcript.strip(),
            "source": summary_path}


# ── Claude call ───────────────────────────────────────────────────────────────

def generate_enriched_summary(parsed: dict, api_key: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    prompt = ENRICHMENT_TEMPLATE.format(
        title=parsed["title"],
        date=parsed["date"] or "unknown",
        summary=parsed["summary"][:4000],
        transcript=parsed["transcript"][:6000],
    )

    log.info(f"  → calling API: {parsed['title']}")
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
        timeout=60.0,
    )
    return message.content[0].text


# ── Job collection ────────────────────────────────────────────────────────────

def get_enriched_stems() -> set:
    return {f.stem for f in ENRICHED_DIR.glob("*.md")} if ENRICHED_DIR.exists() else set()


def get_archived_stems() -> set:
    return {f.stem for f in ARCHIVE_DIR.glob("*.md")} if ARCHIVE_DIR.exists() else set()


def is_complete(path: Path, min_age_secs: int = 5) -> bool:
    try:
        stat = path.stat()
        return stat.st_size > 100 and (time.time() - stat.st_mtime) >= min_age_secs
    except OSError:
        return False


def collect_inline_jobs(enriched: set, archived: set) -> list[dict]:
    """Jobs from current-format files in Granola/ root."""
    jobs = []
    for f in sorted(GRANOLA_DIR.glob("*.md")):
        if f.stem not in enriched and f.stem not in archived and is_complete(f):
            jobs.append(parse_inline_file(f))
    return jobs


def collect_legacy_jobs(enriched: set) -> list[dict]:
    """Jobs from legacy Summaries/ files."""
    if not SUMMARIES_DIR.exists():
        return []
    jobs = []
    for f in sorted(SUMMARIES_DIR.glob("*.md")):
        if f.stem not in enriched:
            jobs.append(parse_legacy_files(f))
    return jobs


# ── Processing ────────────────────────────────────────────────────────────────

def process_one(parsed: dict, api_key: str) -> str:
    """Generate enriched summary and write output file. Returns status string."""
    title = parsed["title"]
    source = parsed["source"]

    enriched_text = generate_enriched_summary(parsed, api_key)

    date_field = f"date: {parsed['date']}\n" if parsed['date'] else ""
    enriched_content = (
        f"---\n{parsed['frontmatter'].strip()}\n"
        f"{date_field}"
        f"enriched_at: {datetime.now().isoformat()}\n---\n\n"
        f"{enriched_text}\n"
    )

    out_path = ENRICHED_DIR / source.name
    out_path.write_text(enriched_content, encoding="utf-8")

    # For inline files (current format), archive the original
    if source.parent == GRANOLA_DIR:
        archive_path = ARCHIVE_DIR / source.name
        source.rename(archive_path)
        return f"OK  {title} → Enriched + Archived"

    return f"OK  {title} → Enriched"


def run(jobs: list[dict], workers: int = 4):
    if not jobs:
        log.info("No new files to process.")
        return

    api_key = get_api_key()
    ENRICHED_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    log.info(f"Processing {len(jobs)} file(s) with up to {workers} parallel workers...")

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(process_one, job, api_key): job["title"] for job in jobs}
        for future in as_completed(futures):
            title = futures[future]
            try:
                result = future.result()
                log.info(f"  {result}")
            except Exception as e:
                log.error(f"  FAIL  {title}: {e}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Granola meeting enricher")
    parser.add_argument("--backfill", action="store_true",
                        help="Process all legacy Summaries/ files")
    parser.add_argument("--workers", type=int, default=4,
                        help="Parallel API workers (default: 4)")
    args = parser.parse_args()

    log.info("Granola enricher started")

    enriched = get_enriched_stems()
    archived = get_archived_stems()

    if args.backfill:
        jobs = collect_legacy_jobs(enriched)
        log.info(f"Backfill mode: {len(jobs)} legacy files to process")
    else:
        # Normal mode: process new files from Summaries/ (where Granola sync deposits them)
        jobs = collect_legacy_jobs(enriched)
        # Also catch any inline-format files dropped directly in Granola/ root
        jobs += collect_inline_jobs(enriched, archived)
        log.info(f"Watch mode: {len(jobs)} new files to process")

    run(jobs, workers=args.workers)
    log.info("Done")


if __name__ == "__main__":
    main()
