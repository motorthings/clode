**🔒 REPOSITORY FOCUS MODE**

Lock working context to a specific repository for this entire conversation.

---

**STEP 1: List all repositories**

Run this command to find all repositories:
```bash
ls -d /Users/motorthings/Documents/GitHub/*/ | nl
```

Show the user a numbered list of all repositories found.

**STEP 2: Ask user to select**

Present the numbered list and ask: "Which repository do you want to work in? (Enter the number)"

**STEP 3: Once user selects a number**

1. Change to that repository:
   ```bash
   cd /Users/motorthings/Documents/GitHub/[selected-repo]
   pwd  # Confirm location
   ```

2. Show brief repository info:
   ```bash
   git status
   ls -la | head -20
   ```

3. **ACTIVATE STRICT WORKING DIRECTORY RULES:**
   - ✅ **ONLY** make changes in this repository
   - ✅ All file paths must be within this repository
   - ✅ All bash commands run from this directory
   - ❌ **NEVER** modify files in other repositories
   - ❌ **NEVER** touch the Obsidian Vault
   - ❌ **NEVER** work outside this directory

**STEP 4: Enforce for entire conversation**

- Before EVERY file operation, verify the path is in this repository
- If user requests work outside, politely refuse and remind them of focus mode
- This lock persists until the conversation ends
- Display a reminder: "🔒 Working in: [repository-name]" at the start of each response

**Ready to list repositories and let user choose.**
