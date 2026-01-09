# Folder Organization Skill

**Skill Type:** File Management & Organization
**Created:** 2025-10-23
**Use Case:** Automatically sort files from a messy folder into organized subfolders based on naming patterns and content

---

## Overview

This skill enables automated file organization by:
1. Identifying patterns in filenames (keywords, participants, dates, topics)
2. Creating appropriate subfolders
3. Moving files to correct destinations
4. Handling duplicates intelligently
5. Flagging ambiguous files for manual review

---

## When to Use This Skill

- **Messy download/export folders** (like Granola notes dump)
- **Meeting notes scattered across one folder**
- **Project files that need categorization**
- **Any bulk file organization task** with identifiable patterns

---

## The Process: Step-by-Step

### Phase 1: Discovery & Analysis

**Goal:** Understand what you have and where it should go

1. **List all files in the source folder**
   ```bash
   ls -la "/path/to/messy/folder"
   ```

2. **Identify available destination folders**
   ```bash
   ls -la "/path/to/vault" | grep "^d"
   ```

3. **Analyze filename patterns**
   - Look for keywords (e.g., "Team_Meeting", "Homework_Huddle", "Mentors")
   - Identify participant patterns (e.g., "Name_Name" format = networking)
   - Note project/client names
   - Spot date patterns
   - Recognize topic indicators

4. **Create categorization rules**
   Based on patterns, define:
   - **Clear matches** → Auto-move
   - **Ambiguous files** → Flag for manual review
   - **Duplicates** → Compare and handle

### Phase 2: Create Destination Structure

**Goal:** Ensure all destination folders exist

```bash
# Create subfolders if they don't exist
mkdir -p "/path/to/destination/Subfolder1"
mkdir -p "/path/to/destination/Subfolder2"
mkdir -p "/path/to/destination/Subfolder3"
```

**Key principle:** Create folders based on natural groupings in the content

### Phase 3: Automated Sorting

**Goal:** Move files with clear destinations

**Strategy:** Be conservative - only move files where destination is obvious

```bash
# Example: Move files with specific keywords
cd "/path/to/source/folder"
mv *Keyword*.md "../Destination_Folder/"

# Example: Move using glob patterns
mv AI_Build_Lab_Team_Meeting*.md "Team_Meetings/"
```

**Sorting Categories (from our example):**

1. **By Meeting Type:**
   - Homework Huddle files → `Homework_Huddle/`
   - Team Meeting files → `Team_Meetings/`
   - Mentor Meeting files → `Mentors_Meeting/`

2. **By Project/Client:**
   - Glean-related → `Glean/`
   - SuperAssistant → `SuperAssistant/`
   - Minal/Ineffable → `Minal Mehta - Ineffable/`

3. **By Participants:**
   - One-on-one meetings (Name_Name format) → `Networking/`

4. **By Topic:**
   - Health-related → `Health/`
   - Family-related → `Family/`
   - Course-related → `AI BuildLab/`

### Phase 4: Duplicate Detection

**Goal:** Identify and handle duplicate files

```bash
# Check for duplicates in source vs. destination
diff -q "/path/to/source/file.md" "/path/to/destination/file.md"
```

**Decision Matrix:**
- **Identical content** → Delete source, keep destination
- **Different content** → Flag for manual review (might be updated versions)
- **Different timestamps** → Check which is newer/more complete

**Important:** Don't auto-delete if files differ - user should decide which to keep

### Phase 5: Manual Review Report

**Goal:** Document files that need human judgment

Create a report with:

```markdown
# Files Requiring Manual Review

## Category 1: Unclear Destination
- File name
- Reason it's unclear
- Recommendation

## Category 2: Potential Duplicates
- Both file paths
- Size comparison
- Recommendation

## Category 3: Untitled/Ambiguous
- File name
- Need content review
```

---

## Implementation Example: Granola Notes Sort

### What We Did

**Source:** `/Granola/` folder with 90+ mixed files
**Task:** Sort into existing vault structure

**Step 1: Identified Patterns**
- AI BuildLab keywords: "Foundations", "Homework_Huddle", "Team_Meeting", "Cohort"
- Networking pattern: "Name_Name,_Date" format
- Project names: "Glean", "SuperAssistant", "Ineffable"
- Special categories: Health, Family

**Step 2: Created Categorization Rules**

Clear matches (auto-move):
- `*Homework*.md` → AI BuildLab/
- `*Team_Meeting*.md` → AI BuildLab/
- `*Glean*.md` → Glean/
- `Name_Name*.md` → Networking/

Ambiguous (manual review):
- Untitled notes
- General strategy sessions
- Files with unclear project ownership

**Step 3: Executed Sorting**
- Moved 68 files automatically
- Left 16 files for manual review
- Identified 2 duplicate pairs

**Step 4: Created Report**
- `MANUAL_REVIEW_NEEDED.md` with detailed analysis
- Categorized remaining files
- Provided recommendations for each

### Results

**Files Sorted:**
- AI BuildLab: ~40 files
- Networking: ~18 files
- Glean: 4 files
- SuperAssistant: 2 files
- Minal Mehta - Ineffable: 2 files
- Health: 1 file
- Family: 1 file

**Success Rate:** 81% automated (68/84 files)

---

## Making This Into a Reusable Skill

### Option 1: Custom Slash Command

Create `.claude/commands/organize-folder.md`:

```markdown
You are organizing files from a messy folder into a structured vault.

PROCESS:
1. Ask user for source folder path
2. List all files in source folder
3. Identify patterns in filenames
4. Ask user to confirm destination mapping
5. Create necessary subfolders
6. Move files with clear destinations
7. Check for duplicates
8. Create manual review report for ambiguous files

Be conservative - only auto-move files where destination is obvious.
```

### Option 2: Specialized Agent

Create `.claude/agents/folder-organizer.md`:

```markdown
# Folder Organizer Agent

You are a specialized agent for organizing messy file collections.

## Your Process

1. **Discovery Phase**
   - Analyze filename patterns
   - Identify natural groupings
   - Map to existing folder structure

2. **Planning Phase**
   - Present sorting plan to user
   - Get confirmation before moving
   - Explain reasoning for each category

3. **Execution Phase**
   - Create subfolders if needed
   - Move files systematically
   - Track progress with TodoWrite

4. **Reporting Phase**
   - Report files moved
   - Flag ambiguous files
   - Identify duplicates
   - Create manual review document

## Your Principles

- **Conservative:** Only move files with obvious destinations
- **Transparent:** Explain your categorization logic
- **Safe:** Never delete without explicit permission
- **Helpful:** Provide clear recommendations for manual review
```

### Option 3: Python Script (for recurring tasks)

For repeated organizational patterns, create a script:

```python
#!/usr/bin/env python3
"""
Folder Organization Script
Automatically sorts files based on naming patterns
"""

import os
import shutil
from pathlib import Path

PATTERNS = {
    'homework': ['Homework', 'homework'],
    'team_meeting': ['Team_Meeting', 'team_meeting'],
    'mentors': ['Mentors_Meeting', 'mentors'],
}

def organize_folder(source_path, dest_path):
    """Sort files from source into destination subfolders"""
    # Implementation here
    pass

if __name__ == "__main__":
    # Run organization
    pass
```

---

## Best Practices

### 1. Always Create Backup First
```bash
# Before bulk operations
cp -r "/path/to/folder" "/path/to/folder_backup"
```

### 2. Use TodoWrite for Progress Tracking
```
1. Analyze files
2. Create subfolders
3. Sort by category A
4. Sort by category B
5. Check duplicates
6. Create report
```

### 3. Be Conservative with Auto-Moving
**DO auto-move:**
- Files with clear keyword matches
- Consistent naming patterns
- Obvious project/client indicators

**DON'T auto-move:**
- Untitled files
- Ambiguous context
- Unclear ownership
- Potential duplicates (until verified)

### 4. Document Your Decisions
Create reports showing:
- What was moved and why
- What needs manual review and why
- Recommendations for each ambiguous file

### 5. Verify Before Deleting
For duplicates:
1. Compare file sizes
2. Check timestamps
3. Diff content if same size
4. If ANY difference → flag for manual review
5. Only delete true identical duplicates

---

## Pattern Recognition Tips

### Common Filename Patterns

1. **Meeting Notes:**
   - `Topic_with_Participants,_Date.md`
   - `Project_Team_Meeting,_Date.md`
   - `Name_Name,_Date.md` (1:1 meetings)

2. **Project Files:**
   - `Project_Name_Description.md`
   - `Client_Name_Meeting_Type,_Date.md`

3. **Course/Training:**
   - `Course_Week_Session,_Date.md`
   - `Homework_Huddle_Date.md`
   - `Cohort_Number_Topic,_Date.md`

4. **Export Patterns:**
   - `Untitled_App_Note,_Date.md` (needs review)
   - `App_ID_random_string.md` (needs title extraction)

### Keywords to Look For

**Meeting Types:**
- Huddle, Meeting, Session, Office Hours, Q&A, Sync

**Project Indicators:**
- Client names, Product names, Project codes

**Content Types:**
- Strategy, Planning, Review, Feedback, Brainstorm

**Participant Patterns:**
- Two names separated by underscore/comma
- Team/Group indicators
- Role descriptions

---

## Troubleshooting

### Problem: Too many files in one category

**Solution:** Create sub-subfolders
```bash
# Example: AI BuildLab has 40+ files
mkdir "AI BuildLab/Homework_Huddle"
mkdir "AI BuildLab/Team_Meetings"
mkdir "AI BuildLab/Mentors_Meeting"
# Then sort within category
```

### Problem: Can't determine pattern

**Solution:** Read first few lines of file
```bash
head -20 "filename.md"
```
Look for:
- Title in frontmatter
- Participants mentioned
- Topic/project references

### Problem: Duplicate with different content

**Solution:** DON'T delete - create comparison report
```markdown
## Duplicate Comparison

**File 1:** /path/to/v1.md (Sept 19, 45K)
**File 2:** /path/to/v2.md (Oct 23, 45K)

**Status:** Content differs
**Recommendation:** Compare manually - v2 may be updated version
```

---

## Skill Evolution

As you use this skill, you'll:

1. **Build Pattern Library**
   - Document filename patterns you encounter
   - Note organizational structures that work
   - Create reusable categorization rules

2. **Refine Auto-Move Criteria**
   - Learn which patterns are reliable
   - Identify edge cases
   - Adjust confidence thresholds

3. **Create Project-Specific Rules**
   - Each vault/project has unique patterns
   - Build custom rules for recurring structures
   - Automate common operations

---

## Summary: The Folder Organization Skill

**What It Is:**
A systematic approach to automatically sorting files from messy folders into organized structures based on naming patterns and content.

**When to Use:**
Anytime you have bulk files that need categorization and existing folder structures to sort them into.

**Key Principles:**
1. Analyze before acting
2. Be conservative (only auto-move obvious files)
3. Create safety nets (reports, backups)
4. Track progress systematically
5. Document decisions for learning

**Success Metrics:**
- 70-90% of files auto-sorted
- 10-30% flagged for manual review (with recommendations)
- Zero accidental data loss
- Clear documentation of all actions

**Make It Reusable:**
- Create slash commands for common patterns
- Build specialized agents for specific vaults
- Write scripts for recurring organizational tasks
- Document patterns you discover

---

**Remember:** The goal is to reduce manual work while maintaining accuracy. Always err on the side of caution - it's better to flag something for manual review than to mis-categorize it.
