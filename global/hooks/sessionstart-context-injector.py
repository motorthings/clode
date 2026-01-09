#!/usr/bin/env python3
"""
SessionStart Context Injector
Runs at the start of each session to check for recently preserved context.
If found (indicating a recent compaction), injects a digest into the new session.
This ensures Claude has access to important context after compaction.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def find_latest_preserved_context():
    """Find the most recent preserved context file"""
    try:
        # Get working directory from environment or current directory
        working_dir = Path(os.getenv('WORKING_DIR', os.getcwd()))
        context_dir = working_dir / '.claude' / 'preserved-context'

        if not context_dir.exists():
            return None

        # Find all preserved context files
        context_files = list(context_dir.glob('compact-context-*.md'))

        if not context_files:
            return None

        # Sort by modification time, get most recent
        latest_file = max(context_files, key=lambda p: p.stat().st_mtime)

        return latest_file

    except Exception as e:
        print(f"Error finding preserved context: {e}", file=sys.stderr)
        return None

def read_preserved_context(file_path):
    """Read and parse the preserved context file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract the main content (skip frontmatter)
        if content.startswith('---'):
            # Skip YAML frontmatter
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()

        return content

    except Exception as e:
        print(f"Error reading preserved context file: {e}", file=sys.stderr)
        return None

def create_digest(full_context):
    """Create a concise digest of the preserved context for Claude"""

    # The preserved context is already well-formatted from PreCompact
    # We just need to wrap it with instructions for Claude

    digest = f"""
## 📋 Preserved Context from Previous Session

The conversation was recently compacted. Below is important context preserved from before the compaction:

{full_context}

---

**Note to Claude:** This context was automatically preserved before compaction. Use this information to maintain continuity with the previous conversation segment. The user may reference topics, decisions, or work completed in the preserved context above.
"""

    return digest

def main():
    """Main entry point for SessionStart hook"""
    try:
        print("=== SessionStart Hook: Checking for preserved context ===", file=sys.stderr)

        # Read hook data from stdin
        hook_data = {}
        try:
            hook_data = json.load(sys.stdin)
            session_id = hook_data.get('session_id', 'unknown')
            source = hook_data.get('source', 'unknown')
            print(f"DEBUG: Session ID: {session_id}", file=sys.stderr)
            print(f"DEBUG: Source: {source}", file=sys.stderr)
        except:
            pass

        # Find the latest preserved context file
        context_file = find_latest_preserved_context()

        if not context_file:
            print("No preserved context file found - starting fresh session", file=sys.stderr)
            sys.exit(0)

        # Check file age based on source
        file_age_seconds = datetime.now().timestamp() - context_file.stat().st_mtime

        # If triggered by compaction, inject immediately (no time limit)
        # Otherwise, only inject if file is recent (within last 15 minutes)
        if hook_data.get('source') == 'compact':
            print(f"DEBUG: Triggered by compaction - injecting preserved context immediately", file=sys.stderr)
        elif file_age_seconds > 900:  # 15 minutes
            print(f"Preserved context is old ({int(file_age_seconds)}s) - skipping injection", file=sys.stderr)
            sys.exit(0)

        print(f"DEBUG: Found recent preserved context ({int(file_age_seconds)}s old): {context_file.name}", file=sys.stderr)

        # Read the preserved context
        preserved_content = read_preserved_context(context_file)

        if not preserved_content:
            print("Could not read preserved context content", file=sys.stderr)
            sys.exit(0)

        # Check if content is too large (limit to ~2000 tokens ≈ 8000 chars)
        if len(preserved_content) > 8000:
            print(f"Preserved context is large ({len(preserved_content)} chars), truncating...", file=sys.stderr)
            # Keep the summary sections, truncate the details
            lines = preserved_content.split('\n')
            truncated_lines = []
            char_count = 0

            for line in lines:
                if char_count + len(line) > 8000:
                    truncated_lines.append("\n... (additional details truncated, full context available in .claude/preserved-context)")
                    break
                truncated_lines.append(line)
                char_count += len(line)

            preserved_content = '\n'.join(truncated_lines)

        # Create digest for Claude
        digest = create_digest(preserved_content)

        # Output to stdout (this gets injected into the new session)
        print(digest)

        print(f"✓ Context digest injected ({len(digest)} chars)", file=sys.stderr)

        sys.exit(0)

    except Exception as e:
        print(f"Error in SessionStart hook: {e}", file=sys.stderr)
        # Don't fail - just skip context injection
        sys.exit(0)

if __name__ == '__main__':
    main()
