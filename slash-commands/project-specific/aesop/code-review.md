# /code-review - AESOP Code Review

Run a systematic code review across the AESOP codebase to catch vibe-coded patterns and bring the code to production quality. Uses the checklist at `testing/CODE-REVIEW.md` as the source of truth.

## Scope

Review all backend and frontend code for:
- **Security**: Org-isolation (every Supabase query must scope by `organization_id`), credential hygiene, webhook auth, file upload validation
- **Duplication**: Shared utilities instead of copy-paste (agent runners, model pricing, file validation, SSE parsing)
- **Error handling**: Structured error responses, failure status updates with `error_message`, rate limiting on compute endpoints, frontend error boundaries
- **Type safety**: Pydantic models for request/response, score range clamping, accurate token estimation
- **Frontend polish**: Extracted shared utilities (markdown, constants, SSE), null guards, consistent error toasts
- **Test coverage**: All critical paths covered (routes, org-isolation, edge cases, pipeline failures)
- **Infrastructure**: CI workflows, pagination on list endpoints, request ID middleware

## Steps

1. Read the current checklist:
   ```bash
   cat testing/CODE-REVIEW.md
   ```

2. Identify any unchecked items (`- [ ]`) and work through them one at a time.

3. For each item:
   - Read the relevant source files before making changes
   - Make the fix
   - Run affected tests to verify

4. After completing items, run the full backend test suite:
   ```bash
   cd backend && ./venv/bin/python -m pytest tests/ -v --timeout=30
   ```

5. Run frontend build check:
   ```bash
   cd frontend && npm run build
   ```

6. Update `testing/CODE-REVIEW.md` to check off completed items with a brief note of what was done.

7. Report summary of changes, test results, and any remaining items.

## Key Files

| Area | Files |
|------|-------|
| Checklist | `testing/CODE-REVIEW.md` |
| Backend routes | `backend/api/routes/*.py` |
| Services | `backend/services/*.py` |
| Agents | `backend/agents/*.py` |
| Helpers | `backend/helpers/*.py` |
| Config | `backend/config.py` |
| Tests | `backend/tests/test_*.py` |
| Frontend components | `frontend/components/*.tsx` |
| Frontend libs | `frontend/lib/*.ts`, `frontend/lib/*.tsx` |
| CI workflows | `.github/workflows/*.yml` |

## Security Checklist (Quick Reference)

Every Supabase query that returns user/org data MUST include:
- `.eq("organization_id", current_user["organization_id"])` for org-scoped tables
- `.eq("user_id", current_user["id"])` for user-scoped legacy tables
- Ownership verification before DELETE/UPDATE operations
- `hmac.compare_digest()` for any secret comparison (never `==`)
- File upload: size limit (`MAX_FILE_SIZE`), MIME type validation (`ALLOWED_MIME_TYPES`)

## Current Status

All 7 phases complete. 95 tests passing (0 failures). Checklist is fully checked off.
