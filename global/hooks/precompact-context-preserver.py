#!/usr/bin/env python3
"""
PreCompact Context Preserver
Extracts and preserves important context before conversation compaction
Stores context in Mem0 for permanent availability across sessions
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def read_transcript(transcript_path):
    """Read the conversation transcript from JSONL file"""
    try:
        transcript_path = Path(transcript_path).expanduser()
        messages = []

        with open(transcript_path, 'r') as f:
            for line in f:
                if line.strip():
                    messages.append(json.loads(line))

        return messages
    except Exception as e:
        print(f"Error reading transcript: {e}", file=sys.stderr)
        return []

def extract_context_summary(messages):
    """Extract key context from conversation messages"""
    context_items = []

    # Debug: Count messages by type
    user_msgs = sum(1 for m in messages if m.get('type') == 'user')
    assistant_msgs = sum(1 for m in messages if m.get('type') == 'assistant')
    print(f"DEBUG: Found {len(messages)} total messages ({user_msgs} user, {assistant_msgs} assistant)", file=sys.stderr)

    # Extract important message types
    for msg in messages:
        msg_type = msg.get('type', '')
        content = msg.get('message', {}).get('content', '')

        # Capture user requests, filtering out system messages
        if msg_type == 'user':
            # Only capture string content (ignore complex structures)
            if isinstance(content, str) and len(content.strip()) > 10:
                content_lower = content.lower()
                # Skip system messages and command outputs
                if not any(skip in content for skip in [
                    'Caveat:', 'This session is being', '<command-name>',
                    '<local-command-stdout>', 'system-reminder'
                ]):
                    context_items.append({
                        'type': 'user_request',
                        'content': content,
                        'timestamp': msg.get('timestamp', '')
                    })

        # Capture assistant confirmations of important actions
        elif msg_type == 'assistant':
            # Look for tool uses that modified files
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'tool_use':
                        tool_name = item.get('name', '')
                        if tool_name in ['Write', 'Edit', 'Bash']:
                            context_items.append({
                                'type': 'tool_action',
                                'tool': tool_name,
                                'input': item.get('input', {}),
                                'timestamp': msg.get('timestamp', '')
                            })

    print(f"DEBUG: Extracted {len(context_items)} context items", file=sys.stderr)
    return context_items

def format_context_for_storage(context_items, hook_data):
    """Format extracted context into a narrative summary optimized for Claude to read"""
    session_id = hook_data.get('session_id', 'unknown')
    trigger = hook_data.get('trigger', 'unknown')
    timestamp = datetime.now().isoformat()

    if not context_items:
        return f"""Session {session_id[:8]} compacted at {timestamp} (trigger: {trigger})

## Summary
No significant context items were found in this conversation segment.
"""

    # Group by type
    user_requests = [c for c in context_items if c['type'] == 'user_request']
    actions = [c for c in context_items if c['type'] == 'tool_action']

    # Analyze files that were modified
    files_modified = set()
    for action in actions:
        if action['tool'] in ['Write', 'Edit']:
            file_path = action['input'].get('file_path', '')
            if file_path:
                files_modified.add(file_path)

    # Build narrative summary
    summary_parts = [
        f"Session {session_id[:8]} compacted at {timestamp} (trigger: {trigger})",
        "",
        "## Conversation Summary",
        f"This conversation included {len(user_requests)} user requests and {len(actions)} actions taken.",
    ]

    if files_modified:
        summary_parts.append(f"Modified {len(files_modified)} file(s) during this session.")

    # Key user requests (narrative format) - reduced and truncated
    if user_requests:
        summary_parts.extend([
            "",
            "## Key User Requests",
            "Main questions/requests in this conversation:"
        ])
        # Show last 5 most recent requests with tight truncation
        for idx, item in enumerate(user_requests[-5:], 1):
            content = item['content'][:150].replace('\n', ' ')  # Tighter truncation, strip newlines
            summary_parts.append(f"{idx}. {content}")

    # File modifications (grouped)
    if files_modified:
        summary_parts.extend([
            "",
            "## Files Modified",
            "Files created or edited:"
        ])
        for file_path in sorted(files_modified)[:10]:  # Show up to 10 files
            summary_parts.append(f"• {file_path}")

        if len(files_modified) > 10:
            summary_parts.append(f"• ...and {len(files_modified) - 10} more")

    # Key bash commands (for context about what was done) - reduced
    bash_actions = [a for a in actions if a['tool'] == 'Bash']
    if bash_actions:
        summary_parts.extend([
            "",
            "## Key Commands",
            "Notable commands run:"
        ])
        # Show last 5 commands with tighter truncation
        for action in bash_actions[-5:]:
            cmd = action['input'].get('command', '')[:80].replace('\n', ' ')
            summary_parts.append(f"• {cmd}")

    summary_parts.extend([
        "",
        "---",
        f"*Context preserved from session {session_id[:8]}*"
    ])

    # Join and enforce size limit (3000 chars ≈ 750 tokens)
    summary = "\n".join(summary_parts)

    if len(summary) > 3000:
        # Truncate intelligently - keep header and first sections
        lines = summary.split('\n')
        truncated = []
        char_count = 0

        for line in lines:
            if char_count + len(line) > 2800:
                truncated.append("\n...(truncated to fit size limit - full context in .claude/preserved-context)")
                break
            truncated.append(line)
            char_count += len(line) + 1  # +1 for newline

        summary = '\n'.join(truncated)

    return summary

def store_in_mem0(context_summary, session_id, is_test=False):
    """Store context summary in Mem0 and Obsidian vault"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Skip file storage for test sessions
    if is_test:
        print("⚠ Test session detected - skipping file storage", file=sys.stderr)
        return

    # Try to use Mem0 Python client if available
    try:
        from mem0 import Memory

        # Initialize Mem0 client (uses environment variables)
        memory = Memory()

        # Store in Mem0
        memory.add(
            messages=[{"role": "user", "content": context_summary}],
            user_id=os.getenv("MEM0_USER_ID", "default_user"),
            metadata={
                "source": "precompact_hook",
                "session_id": session_id,
                "timestamp": timestamp,
                "type": "context_preservation"
            }
        )
        print(f"✓ Stored in Mem0 for session {session_id[:8]}", file=sys.stderr)

    except ImportError:
        print("Mem0 Python client not available, skipping Mem0 storage", file=sys.stderr)
    except Exception as e:
        print(f"Error storing in Mem0: {e}", file=sys.stderr)

    # Store in working directory's .claude/preserved-context folder
    try:
        # Get working directory from environment or current directory
        working_dir = Path(os.getenv('WORKING_DIR', os.getcwd()))
        context_dir = working_dir / '.claude' / 'preserved-context'
        context_dir.mkdir(parents=True, exist_ok=True)

        # Create filename with timestamp
        filename = f"compact-context-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        filepath = context_dir / filename

        # Write markdown file with frontmatter
        with open(filepath, 'w') as f:
            f.write(f"""---
session_id: {session_id}
preserved_at: {timestamp}
source: precompact_hook
---

# Context Preserved from Session

{context_summary}
""")

        print(f"✓ Saved to {context_dir}: {filename}", file=sys.stderr)

    except Exception as e:
        print(f"Error saving preserved context: {e}", file=sys.stderr)

def main():
    """Main entry point for PreCompact hook"""
    try:
        print("=== PreCompact Hook Starting ===", file=sys.stderr)

        # Read hook data from stdin
        hook_data = json.load(sys.stdin)

        transcript_path = hook_data.get('transcript_path', '')
        session_id = hook_data.get('session_id', 'unknown')
        trigger = hook_data.get('trigger', '')

        print(f"DEBUG: Session ID: {session_id}", file=sys.stderr)
        print(f"DEBUG: Transcript path: {transcript_path}", file=sys.stderr)

        # Detect test sessions to skip file storage
        is_test = session_id.startswith('test-') or 'test' in trigger.lower()

        if not transcript_path:
            print("No transcript path provided", file=sys.stderr)
            sys.exit(0)

        # Read and analyze transcript
        messages = read_transcript(transcript_path)

        if not messages:
            print("No messages found in transcript", file=sys.stderr)
            sys.exit(0)

        # Extract important context
        context_items = extract_context_summary(messages)

        # Always format and store, even if no context items
        # This helps with debugging and creates a record of compaction
        context_summary = format_context_for_storage(context_items, hook_data)
        store_in_mem0(context_summary, session_id, is_test=is_test)

        # Output summary to stderr for logging
        print("\n=== Context Preserved ===", file=sys.stderr)
        print(context_summary, file=sys.stderr)
        print("========================\n", file=sys.stderr)

        sys.exit(0)

    except Exception as e:
        print(f"Error in PreCompact hook: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block compaction on error

if __name__ == '__main__':
    main()
