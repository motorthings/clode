# /update-docs - Update AESOP Documentation

Update project documentation, help system content, and guides.

## Steps

1. Scan for changes since last documentation update:
   ```bash
   git diff --stat HEAD~5
   ```

2. Check current agent prompts for version changes:
   ```bash
   grep -r "Version:" backend/agents/prompts/
   ```

3. Verify CLAUDE.md is up to date with:
   - Current agent versions
   - API endpoints match actual routes
   - Environment variables are accurate
   - Project structure matches reality

4. Check frontend help system FAQ content in `contexts/HelpChatContext.tsx`:
   - Verify answers match current functionality
   - Add FAQ entries for any new features
   - Update contextual questions if new pages were added

5. Verify guide HTML files in `public/guides/` match current architecture

6. Report what was updated and what needs manual review
