#!/usr/bin/env python3
"""
UserPromptSubmit Context Injector
Runs when user submits a message to check for preserved context.
If a new preserved context file is found (not yet injected), injects it into the conversation.
This ensures Claude has access to important context after compaction.
Uses state tracking to inject each file only once.
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

def check_already_injected(context_file, working_dir):
    """Check if this context file has already been injected"""
    try:
        state_file = working_dir / '.claude' / 'preserved-context' / '.last-injected'

        if not state_file.exists():
            return False

        with open(state_file, 'r') as f:
            last_injected = f.read().strip()

        return last_injected == context_file.name

    except Exception as e:
        print(f"Error checking injection state: {e}", file=sys.stderr)
        return False

def mark_as_injected(context_file, working_dir):
    """Mark this context file as injected"""
    try:
        state_file = working_dir / '.claude' / 'preserved-context' / '.last-injected'

        with open(state_file, 'w') as f:
            f.write(context_file.name)

        print(f"✓ Marked {context_file.name} as injected", file=sys.stderr)

    except Exception as e:
        print(f"Error marking injection state: {e}", file=sys.stderr)

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
    """Main entry point for UserPromptSubmit hook"""
    try:
        # Read hook data from stdin
        hook_data = {}
        try:
            hook_data = json.load(sys.stdin)
        except:
            pass

        # Get working directory
        working_dir = Path(os.getenv('WORKING_DIR', os.getcwd()))

        # Find the latest preserved context file
        context_file = find_latest_preserved_context()

        if not context_file:
            # No context file found - exit silently
            sys.exit(0)

        # Check if we've already injected this file
        if check_already_injected(context_file, working_dir):
            # Already injected this file - skip
            sys.exit(0)

        file_age_seconds = datetime.now().timestamp() - context_file.stat().st_mtime
        print(f"DEBUG: Found preserved context ({int(file_age_seconds)}s old): {context_file.name}", file=sys.stderr)

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

        # Output to stdout (this gets injected into the conversation)
        print(digest)

        print(f"✓ Context digest injected ({len(digest)} chars)", file=sys.stderr)

        # Mark this file as injected to prevent re-injection
        mark_as_injected(context_file, working_dir)

        sys.exit(0)

    except Exception as e:
        print(f"Error in UserPromptSubmit hook: {e}", file=sys.stderr)
        # Don't fail - just skip context injection
        sys.exit(0)

if __name__ == '__main__':
    main()
