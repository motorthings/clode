Update AESOP help documentation to match current app state.

## Steps

1. **Read recent changes** — run `git log --oneline -20` and `git diff --stat HEAD~10` to understand what has changed recently.

2. **Scan current app state:**
   - Sidebar navigation from `frontend/components/Sidebar.tsx` (nav items, labels, routes)
   - Page routes from `frontend/app/(app)/*/page.tsx` (glob for all page files)
   - Agent versions from `backend/agents/prompts/*.txt` (look for version strings)
   - API endpoints from `backend/api/routes/*.py` (router prefixes and endpoint paths)
   - Scoring formula from `backend/helpers/score_extractor.py` and `backend/services/evaluation_service.py`

3. **Compare against help docs** — read all files in `docs/help/**/*.md` and check for:
   - Outdated navigation paths or sidebar items
   - Wrong agent versions
   - Missing new features or evaluation modes
   - Incorrect scoring formula or certification thresholds
   - Missing or renamed API endpoints

4. **Update help docs** — modify any docs that are out of date to match the current app state. Use exact UI element names (bold for buttons/links).

5. **Update contextual questions** — check `CONTEXTUAL_QUESTIONS` in `frontend/components/HelpPanel.tsx` and add entries for any new routes that exist but don't have suggested questions.

6. **Reindex help docs** — run: `cd backend && source venv/bin/activate && python scripts/index_help_docs.py --force`

7. **Report summary** — list all files modified and what changed.
