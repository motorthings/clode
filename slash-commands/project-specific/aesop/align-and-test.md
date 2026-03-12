# Align AESOP Backend Schema & Unlock Remaining E2E Tests

## Context

We have 27/31 Playwright e2e tests passing. 4 evaluation wizard Step 2 tests are skipped because the AESOP backend can't serve agents — the backend code expects tables (`agents`, `users`, `evaluations`, `organizations`) that don't exist in the actual Supabase project.

## The Problem: Schema Mismatch

**AESOP backend code** (in `/Users/motorthings/Documents/GitHub/aesop/backend/`) expects:
- `users` table with columns: `id`, `email`, `role`, `organization_id`, `team_id`, `full_name`
- `agents` table with columns: `id`, `name`, `agent_type`, `endpoint_url`, `endpoint_config`, `instructions`, `organization_id`, `created_by`
- `evaluations` table with eval data
- `organizations` table

**Actual AESOP_Updated Supabase project** (`cyniveygdsiyrzjzjedv`) has different tables:
- `profiles` (id, user_id, nda_accepted, etc.)
- `projects` (id, user_id, project_name, status)
- `rubrics`, `live_evaluations`, `flat_cave_runs`, `evaluation_scenarios`, etc.

The migration files exist at `/Users/motorthings/Documents/GitHub/aesop/supabase/migrations/001-006` but were never applied. They conflict with the existing tables.

## Supabase Credentials

- **Project ref**: `cyniveygdsiyrzjzjedv`
- **URL**: `https://cyniveygdsiyrzjzjedv.supabase.co`
- **Anon key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN5bml2ZXlnZHNpeXJ6anpqZWR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MDM2NjQsImV4cCI6MjA3NzE3OTY2NH0.xYopNzz0nULZ0OpLNHIBk0_JxOYHtBLCCE3qnDe7bOw`
- **Service role key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN5bml2ZXlnZHNpeXJ6anpqZWR2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTYwMzY2NCwiZXhwIjoyMDc3MTc5NjY0fQ.QPW94EdqF8A4UYpMUycOmcBVUMbZl2h6ABAt8U-AaWw`
- **JWT secret**: `wqCdP0rIdMndu6SjK3uaRM/GAplk9iYzmCKhfbg42Ny1ErzprGv7QaMgIvp3NkCsTBR/Iq7ukvrUYTq7MqxeyQ==`
- **Test user**: `motorthings@gmail.com` / `ButtButt` (GoTrue user ID: `d5385e36-79f0-4a7b-aa36-0b5518457226`)

**IMPORTANT**: The Supabase MCP tool is connected to a DIFFERENT project (`iyugbpnxfbhqjxrvmnij`). To run SQL against the correct project, use the REST API or Supabase Dashboard directly.

## MockBot Agent Data

- **Name**: MockBot (Helpful Hannah - Customer Service Assistant)
- **Endpoint**: `https://n8n.waifinder.org/webhook/MockBot`
- **Protocol**: REST (POST with `{"message": "..."}`, returns `{"reply": "..."}`)
- **Full workflow**: `/Users/motorthings/Downloads/MockBot.json`

## Tasks

1. **Decide approach**: Either adapt the backend routes to use the existing Supabase tables (`profiles`, `projects`, etc.), OR apply the migrations to create the expected tables alongside the existing ones.

2. **Align the schema**: Make the backend's `GET /api/agents` endpoint return data from whichever table holds agent/project data.

3. **Seed MockBot**: Ensure the MockBot agent exists in the database with endpoint URL and instructions so the evaluation wizard can select it.

4. **Start the backend** on port 8003:
   ```bash
   cd /Users/motorthings/Documents/GitHub/aesop/backend
   # .env already exists with correct credentials
   python3 -m uvicorn main:app --host 127.0.0.1 --port 8003
   ```

5. **Update frontend** to point at the backend:
   ```
   # in /Users/motorthings/Documents/GitHub/aesop/frontend/.env.local
   NEXT_PUBLIC_API_URL=http://localhost:8003
   ```

6. **Run the full test suite**:
   ```bash
   cd /Users/motorthings/Documents/GitHub/aesop/frontend
   rm -rf .next e2e/.auth/user.json
   E2E_AUTH=true npx playwright test --reporter=list
   ```

7. **Target**: All 31 tests pass (27 currently passing + 4 skipped evaluation wizard Step 2 tests).

## Existing Tables in AESOP_Updated (via PostgREST)

```
profiles, projects, rubrics, live_evaluations, flat_cave_runs,
flat_cave_test_cases, evaluation_scenarios, evaluation_personas,
instructions, ethos, report_requests, user_guides, nda_versions,
nda_email_log, beta_registrations, analysis_iterations,
analysis_iteration_changes, orchestrated_analysis,
analysis_orchestrator, analysis_orchestrator_iterative, ideation,
ideation_examples, ideation_instructions,
ideation_agent_instructions_examples, cave_of_shadows_runs,
interview, interview_agent, interview_storage, interview_test
```

## Key Files

- Backend routes: `/Users/motorthings/Documents/GitHub/aesop/backend/api/routes/agents.py`
- Backend auth: `/Users/motorthings/Documents/GitHub/aesop/backend/auth.py`
- Backend config: `/Users/motorthings/Documents/GitHub/aesop/backend/.env`
- Frontend env: `/Users/motorthings/Documents/GitHub/aesop/frontend/.env.local`
- Playwright config: `/Users/motorthings/Documents/GitHub/aesop/frontend/playwright.config.ts`
- Auth setup: `/Users/motorthings/Documents/GitHub/aesop/frontend/e2e/auth.setup.ts`
- Skipped tests: `/Users/motorthings/Documents/GitHub/aesop/frontend/e2e/evaluation-wizard.spec.ts` (lines 42, 63, 82, 99)
- Migrations (unapplied): `/Users/motorthings/Documents/GitHub/aesop/supabase/migrations/`
