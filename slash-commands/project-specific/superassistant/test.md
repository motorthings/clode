# SuperAssistant QA Test Suite

Execute the comprehensive QA testing process for SuperAssistant MVP. This command runs the full testing protocol defined in `docs/QA-TESTING-PROMPT.md`.

## Usage
- `/test` — run the full QA testing prompt (all sections)
- `/test quick` — run unit tests only (frontend Jest + backend pytest)
- `/test e2e` — run Playwright E2E spec only (no manual sections)
- `/test section <N>` — run a specific section (1-20) from the QA prompt
- `/test api` — run API endpoint tests only (Section 16)
- `/test security` — run security checks only (Section 18)
- `/test regression` — run known bug regression tests only

## Credentials

- **Admin:** `charlie@waifinder.org` / `ButtButt`
- **User:** `charlie@sickofancy.ai` / `ButtButt`
- **Frontend:** `https://superassistant-mvp.vercel.app`
- **Backend:** `https://superassistant-mvp-production.up.railway.app`

## Full QA Process

When running the full suite (no arguments or `/test`), follow this exact process:

### Step 1: Read the QA Testing Prompt
```
Read docs/QA-TESTING-PROMPT.md
```
This is the canonical testing document. Follow every instruction in it.

### Step 2: Determine the Round Number
```
Look in docs/testing/ for the highest QA_TEST_PROTOCOL_ROUND*.md number.
Increment by 1 for this run. Example: if ROUND6 exists, create ROUND7.
```

### Step 3: Setup Playwright
```bash
cd /Users/motorthings/Documents/GitHub/superassistant-mvp/frontend
npx playwright install chromium --with-deps
```

### Step 4: Create or Update E2E Spec
Create `frontend/e2e/qa-round{N}.spec.ts` using the Playwright test code from the QA prompt (Section 17). Update the round number in the filename.

### Step 5: Run E2E Tests
```bash
cd /Users/motorthings/Documents/GitHub/superassistant-mvp/frontend
npx playwright test e2e/qa-round{N}.spec.ts --headed --project=chromium
```

### Step 6: Run API Endpoint Tests (Section 16)
Execute each curl command from Section 16 of the QA prompt against the Railway backend. Document pass/fail for each.

### Step 7: Manual UI Verification
For any tests that cannot be automated (Sections 1-15, 18-20), use Playwright MCP browser tools to:
- Navigate to each page
- Take screenshots
- Verify UI elements
- Document results

### Step 8: Grade Each Test
For every test in the QA prompt, record:
- ✅ PASS | 🐛 BUG | ⚠ UX ISSUE | ⏭ SKIPPED (with reason)
- Exact error messages and unexpected behavior
- Screenshots where relevant

### Step 9: Write the Report
Write full findings to `docs/testing/QA_TEST_PROTOCOL_ROUND{N}.md` using this format per test:

```markdown
### {TEST-ID} — {Test Name}
**Result:** ✅ PASS | 🐛 BUG | ⚠ UX ISSUE | ⏭ SKIPPED
**Notes:** [What was observed]
**Bug details (if bug):**
- Page: [URL]
- Steps to repro: [numbered]
- Expected: [what should happen]
- Actual: [what actually happens]
- Priority: High / Medium / Low
```

At the end include:
1. **Summary table** of all tests with Pass/Fail/Skip
2. **New bugs found this round** (ranked High → Medium → Low)
3. **Ranked UX issues** (High → Medium → Low)
4. **5-minute pre-demo checklist** (critical happy-path checks only)
5. **Backend test command** with expected output: `pytest tests/unit -v`

### Step 10: Update Bug Tracker
- Read `docs/BUG_TRACKER.md` first
- Append any NEW bugs (do NOT duplicate existing entries)
- Mark previously open bugs confirmed fixed with ✅ FIXED + date
- Use the exact format from existing entries

## Quick Tests Mode (`/test quick`)

Run unit tests only — no Playwright, no QA prompt:

### Frontend Unit Tests
```bash
cd /Users/motorthings/Documents/GitHub/superassistant-mvp/frontend && npm test
```

### Backend Tests
```bash
cd /Users/motorthings/Documents/GitHub/superassistant-mvp/backend && pytest tests/unit -v
```

Summarize pass/fail counts. Highlight failures with file:line references.

## E2E Only Mode (`/test e2e`)

```bash
cd /Users/motorthings/Documents/GitHub/superassistant-mvp/frontend && npx playwright test --headed --project=chromium
```

## Section Mode (`/test section <N>`)

Run only the specified section number from the QA prompt:
- 1: Auth Flows
- 2: Admin Dashboard
- 3: Admin Users
- 4: Admin Solomon Review
- 5: Admin Conversations
- 6: Admin Documents
- 7: Admin System Instructions
- 8: Admin Theme
- 9: Admin Core Documents
- 10: Admin Index Help
- 11: Admin Help Panel
- 12: User Chat
- 13: User Documents
- 14: User Profile
- 15: User Interview
- 16: API Endpoint Tests
- 17: Playwright E2E Tests
- 18: Security Checks
- 19: Performance Checks
- 20: Mobile / Responsive

Read `docs/QA-TESTING-PROMPT.md`, find the specified section, and execute only those tests. Still document results and update bug tracker.

## API Tests Mode (`/test api`)

Run Section 16 from the QA prompt — all curl-based API endpoint tests against the Railway backend.

## Security Tests Mode (`/test security`)

Run Section 18 from the QA prompt — XSS, SQL injection, IDOR, and access control checks.

## Regression Mode (`/test regression`)

Run only the "Known Bug Regression" tests from the Playwright spec (Section 17). These verify previously reported bugs are fixed.

$ARGUMENTS
