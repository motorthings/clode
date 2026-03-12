# Run Test Suite

Run the Thesis test suite with options for quick unit tests, full pytest regimen, code quality gates, or comprehensive everything.

## STEP 0: Review Recent Changes and Update Tests

**IMPORTANT:** Before running any tests, check for recent code changes that may need new or updated tests.

1. Run `git log --oneline -10` to see recent commits
2. For each commit that modified backend source files (not docs/tests), check if corresponding test coverage exists:
   - Run `git diff HEAD~10..HEAD --name-only -- backend/api/ backend/services/ backend/agents/` to find changed source files
   - For each changed file, check if its test file covers the changed functions
   - Look for new functions, changed function signatures, new model fields, or new endpoints
3. If gaps are found:
   - Add new test cases to the appropriate test file
   - Run the new tests to verify they pass
   - Stage and commit the test updates before proceeding
4. Report what was found: "X source files changed, Y test gaps found, Z tests added" or "All recent changes have test coverage"

**Skip this step** if the user explicitly says to skip it or if running in quick mode with `--skip-review`.

## STEP 1: Ask User Which Mode to Run

**IMPORTANT:** Before running any tests, use `AskUserQuestion` to ask the user which test mode they want.

Since AskUserQuestion only supports 4 options, use TWO questions:

**Question 1:** "What type of testing do you need?"
- Header: "Test Type"
- Options:
  1. "Functional Tests (Recommended)" - "pytest unit/integration tests + basic E2E"
  2. "Code Quality" - "Type checking, linting, complexity, secret scan"
  3. "Full E2E" - "100 comprehensive browser tests on production"
  4. "Comprehensive" - "Everything: functional + quality + E2E (~1000+ checks)"

If user selects "Functional Tests", ask **Question 2:** "How thorough?"
- Header: "Test Depth"
- Options:
  1. "Quick (Recommended)" - "Unit tests only (~430 tests, fastest)"
  2. "Default" - "All pytest stages + 5 basic E2E (~860 tests)"

Based on the user's final selection:
- **Quick** → Execute "OPTION: --quick" section only
- **Default** → Execute "DEFAULT MODE" section (Stages 1-4 + basic E2E)
- **Full E2E** → Execute "OPTION: --full" section (100 E2E scenarios)
- **Quality** → Execute "OPTION: --quality" section (code quality gates)
- **Comprehensive** → Execute DEFAULT MODE + OPTION: --full + OPTION: --quality (everything)

---

## Prerequisites

### For Quick and Default modes (pytest)
1. **dotenvx** - The `.env` file is encrypted. Use `dotenvx run` to decrypt and inject environment variables.
2. **DOTENV_PRIVATE_KEY** - Required for decryption. Found in `backend/.env.keys`.

### For Full E2E mode (production)
1. **Playwright MCP** - Use the Playwright MCP server for all browser automation (not Chrome DevTools)
2. **Authentication** - You should be logged into thesis-mvp.vercel.app

### For Quality mode
1. **pre-commit** - Install with `pip install pre-commit`
2. **mypy** - Installed via pre-commit or `pip install mypy`
3. **trufflehog** - For secret scanning (optional, skipped if not installed)

**Note:** Cleanup of E2E test data runs automatically at the end of any E2E test (Default or Full modes).

---

# OPTION: --quick (Unit Tests Only)

Run ONLY Stage 1 (unit tests) and skip everything else.

---

# OPTION: --quality (Code Quality Gates)

Run code quality checks: type checking, linting, complexity analysis, and secret scanning.

## Quality Stage 1: Ruff Linting & Formatting

Check code style and formatting:

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
.venv/bin/python -m ruff check . --select=E,F,W,B,I,C90,D 2>&1 || true
.venv/bin/python -m ruff format --check . 2>&1 || true
```

Record: errors found, files checked.

## Quality Stage 2: Mypy Type Checking

Run static type analysis:

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
.venv/bin/python -m mypy . --ignore-missing-imports --no-error-summary 2>&1 || true
```

Record: type errors found, files checked.

## Quality Stage 3: Complexity Analysis

Check cyclomatic complexity (max 10):

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
.venv/bin/python -m ruff check . --select=C90 2>&1 || true
```

Record: complexity violations found.

**Known Exemptions (too risky to refactor):**
- `api/routes/chat.py::chat_stream` (complexity ~57) - Core streaming logic
- `api/routes/chat.py::get_agent_response` (complexity ~56) - Agent routing logic

**Refactored Functions (Jan 2026):**
- `agents/taskmaster.py::_get_task_context` - 26 -> ~8 (extracted helpers)
- `agents/oracle.py::_format_analysis` - 23 -> ~10 (section formatters)
- `api/routes/admin/help_docs.py::update_help_document` - 21 -> ~12 (module-level helpers)
- `services/stakeholder_extractor.py::_parse_response` - 17 -> ~8 (extraction helpers)
- `services/task_extractor.py::_extract_due_date` - 15 -> ~8 (date calculators)

Tests for these helpers: `tests/test_refactored_helpers.py` (~62 tests)

## Quality Stage 4: Docstring Coverage

Check docstring compliance (Google style):

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
.venv/bin/python -m ruff check . --select=D --ignore=D100,D104,D103 2>&1 || true
```

Record: missing/malformed docstrings.

## Quality Stage 5: Secret Scanning

Scan for accidentally committed secrets:

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis
# Check if trufflehog is installed
if command -v trufflehog &> /dev/null; then
  trufflehog filesystem . --only-verified --no-update 2>&1 || true
else
  echo "trufflehog not installed - skipping secret scan"
fi
```

Record: secrets found (should be 0).

## Quality Stage 6: Frontend Lint

Check frontend code quality:

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/frontend
npm run lint 2>&1 || true
```

Record: lint errors found.

## Quality Summary

After ALL quality stages complete, provide a summary:

```
============================================
CODE QUALITY SUMMARY
============================================
Stage 1 - Ruff Lint/Format:    XX errors, XX warnings
Stage 2 - Mypy Type Check:     XX type errors
Stage 3 - Complexity (C90):    XX violations (max complexity: 10)
Stage 4 - Docstrings (D):      XX issues
Stage 5 - Secret Scan:         XX secrets found
Stage 6 - Frontend Lint:       XX errors
--------------------------------------------
OVERALL:  [PASS/WARN/FAIL]
============================================

Notes:
- Type errors are advisory (Week 1-2 rollout)
- Complexity > 10 indicates functions needing refactor
- Any secrets found is a CRITICAL failure
```

---

# DEFAULT MODE: Full Pytest Regimen + Basic E2E

Execute ALL test stages below in order. Do NOT stop if one stage fails - continue to the next stage and report all results at the end.

## Stage 1: Unit Tests

Run core unit tests first:

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
DOTENV_PRIVATE_KEY=4980b243281755774eab2a5107d475ceecdeceb0b7aef97e014d9cfcece1c230 \
dotenvx run -f .env -- .venv/bin/python -m pytest \
  tests/test_refactored_helpers.py \
  tests/test_document_classifier.py \
  tests/test_tasks.py \
  tests/test_projects.py \
  tests/test_engagement.py \
  tests/test_agents_new.py \
  tests/test_vibe_coding_bugs.py \
  tests/test_rigorous.py \
  -v --tb=short --timeout=60 2>&1 || true
```

Record: passed, failed, skipped counts.

## Stage 2: Integration Tests

Run integration and Obsidian sync tests:

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
DOTENV_PRIVATE_KEY=4980b243281755774eab2a5107d475ceecdeceb0b7aef97e014d9cfcece1c230 \
dotenvx run -f .env -- .venv/bin/python -m pytest \
  tests/test_integration.py \
  tests/test_obsidian_sync.py \
  -v --tb=short --timeout=120 2>&1 || true
```

Record: passed, failed, skipped counts.

## Stage 3: Extended Tests

Run all remaining tests (excluding E2E):

```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
DOTENV_PRIVATE_KEY=4980b243281755774eab2a5107d475ceecdeceb0b7aef97e014d9cfcece1c230 \
dotenvx run -f .env -- .venv/bin/python -m pytest tests/ \
  --ignore=tests/e2e/ \
  --ignore=tests/e2e_browser_tests.py \
  --ignore=tests/test_refactored_helpers.py \
  --ignore=tests/test_document_classifier.py \
  --ignore=tests/test_tasks.py \
  --ignore=tests/test_projects.py \
  --ignore=tests/test_engagement.py \
  --ignore=tests/test_agents_new.py \
  --ignore=tests/test_vibe_coding_bugs.py \
  --ignore=tests/test_rigorous.py \
  --ignore=tests/test_integration.py \
  --ignore=tests/test_obsidian_sync.py \
  -v --tb=short --timeout=120 2>&1 || true
```

Record: passed, failed, skipped counts.

## Stage 4: Basic E2E Browser Tests

E2E tests use **Playwright MCP** to automate browser interactions.

### Step 4.1: Check Server Status

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null || echo "Frontend not running"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "Backend not running"
```

### Step 4.2: Start Servers (if not running)

If servers are not running, start them in background:

**Backend** (run in background):
```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
JWK=$(curl -s "https://imdavfgreeddxluslsdl.supabase.co/auth/v1/.well-known/jwks.json" | jq -c '.keys[0]')
SUPABASE_JWT_SECRET="$JWK" \
DOTENV_PRIVATE_KEY=4980b243281755774eab2a5107d475ceecdeceb0b7aef97e014d9cfcece1c230 \
dotenvx run -f .env -- .venv/bin/python -m uvicorn main:app --reload --port 8000
```

**Frontend** (run in background):
```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/frontend
npm run dev
```

Wait for both servers to be ready.

### Step 4.3: Verify Playwright MCP Connection

Use `mcp__playwright__browser_navigate` to verify Playwright is connected.

### Step 4.4: Run Basic E2E Test Scenarios

**Test 1: Auth Login Success**
1. Navigate to `http://localhost:3000`
2. Verify user is authenticated (user menu visible) or complete login flow

**Test 2: Chat Send Message**
1. Navigate to `/chat`
2. Send test message: "Hello, this is an E2E test"
3. Verify AI agent responds

**Test 3: KB Search** (optional)
1. Navigate to `/kb`
2. Search for a term
3. Verify results appear

**Test 4: Tasks Create**
1. Navigate to `/tasks`
2. Click "Add Task"
3. Create task: "E2E Test Task - Automated"
4. Verify task appears in To Do column

**Test 5: Tasks Kanban Drag**
1. Drag test task to In Progress
2. Verify task persists after refresh

### Step 4.5: Cleanup Test Data

After running E2E tests, clean up any test data created:

1. Navigate to `/tasks`
2. Delete any tasks containing "E2E Test" in the title
3. Navigate to `/chat`
4. Delete any conversations created during testing

### Step 4.6: Record E2E Results

Record pass/fail for each scenario.

---

## Default Mode Summary

After ALL stages complete, provide a summary table:

```
============================================
TEST SUMMARY
============================================
Stage 1 - Unit Tests:        XX passed, XX failed, XX skipped
Stage 2 - Integration Tests: XX passed, XX failed, XX skipped
Stage 3 - Extended Tests:    XX passed, XX failed, XX skipped
Stage 4 - E2E Browser Tests: XX passed, XX failed
--------------------------------------------
TOTAL:                       XXX passed, XXX failed, XXX skipped
============================================
```

---

# OPTION: --full (Comprehensive Production E2E)

Run comprehensive end-to-end test of ALL Thesis functionality using **Playwright MCP** on production.

**Test Configuration:**
- **Production URL**: https://thesis-mvp.vercel.app
- **Test Data Prefix**: All test data uses "E2E Test" prefix for easy cleanup
- **Total Tests**: 100 scenarios across 15 phases

Execute ALL test phases in order. After each test, record PASS/FAIL.

---

## PHASE 1: AUTHENTICATION & SESSION (4 tests)

### Test 1.1: Verify Authentication State
1. Navigate to `https://thesis-mvp.vercel.app`
2. Take snapshot
3. Verify user menu button is visible (authenticated state)

*Expected:* User is authenticated with access to all app sections

### Test 1.2: User Menu Functionality
1. Click user menu button
2. Verify dropdown shows user info and logout option
3. Close menu without logging out

### Test 1.3: Navigation Bar - All Links Present
1. Verify presence of ALL navigation links: Dashboard, Chat, Tasks, Projects, Intelligence, Agents, KB, DISCo
2. Count should be 8 main navigation items

### Test 1.4: Navigation Bar - Each Link Works
1. Click each navigation link in sequence
2. Verify each page loads without console errors
3. Verify URL changes correctly

---

## PHASE 2: DASHBOARD (5 tests)

### Test 2.1: Dashboard Initial Load
1. Navigate to `/`
2. Verify dashboard content loads
3. Check for console errors via `mcp__playwright__browser_console_messages`

### Test 2.2: Dashboard Widgets Present
1. Verify key dashboard sections are visible
2. Check for recent activity or summary widgets

### Test 2.3: Dashboard Quick Actions
1. Look for quick action buttons (if present)
2. Verify they are clickable

### Test 2.4: Dashboard Data Loading
1. Verify any data-driven widgets show content (not loading spinners indefinitely)

### Test 2.5: Dashboard Navigation from Widgets
1. Click on a widget link (e.g., "View all tasks")
2. Verify navigation to correct page

---

## PHASE 3: CHAT - BASIC FUNCTIONALITY (8 tests)

### Test 3.1: Chat Page Load
1. Navigate to `/chat`
2. Verify conversation list sidebar
3. Verify message input area

### Test 3.2: New Chat Creation
1. Click "+ New Chat" button
2. Verify fresh chat interface appears
3. Verify message input is enabled

### Test 3.3: Send Message and Receive Response
1. Type: "E2E Test: Hello, please acknowledge this automated test message."
2. Click Send (or press Enter)
3. Wait for AI response (up to 30 seconds)
4. Verify response appears with agent attribution

### Test 3.4: Conversation Auto-Naming
1. After sending message, check if conversation was auto-named
2. Verify name appears in sidebar

### Test 3.5: Conversation Rename
1. Find Rename button for test conversation
2. Click Rename
3. Enter new name: "E2E Renamed Chat"
4. Confirm rename
5. Verify new name appears in sidebar

### Test 3.6: Conversation Archive
1. Find Archive button for a conversation
2. Click Archive
3. Verify conversation moves to archived
4. Click "Show Archived" to verify it's there

### Test 3.7: Conversation Delete
1. Find Delete button for archived conversation
2. Click Delete
3. Confirm deletion
4. Verify conversation is removed

### Test 3.8: Search Conversations
1. Type in conversation search box
2. Verify conversations filter based on search term

---

## PHASE 4: CHAT - AI AGENTS & KB CONTEXT (7 tests)

### Test 4.1: Agent Selector Display
1. In chat, find Agent selector button (shows "Auto" by default)
2. Click to open agent selection

### Test 4.2: Agent Selection - Atlas
1. Select "Atlas" agent
2. Send: "E2E Agent Test: What are current AI research trends?"
3. Verify response includes Atlas attribution

### Test 4.3: Agent Selection - Capital
1. Select "Capital" agent
2. Send: "E2E Agent Test: What's a typical AI project ROI?"
3. Verify response includes Capital attribution and financial focus

### Test 4.4: Agent Selection - Auto Routing
1. Select "Auto" agent
2. Send: "E2E Test: What security considerations are there for AI?"
3. Verify system routes to appropriate agent (likely Guardian)

### Test 4.5: KB Context Chat (CRITICAL)
1. Start new chat with Auto agent
2. Send: "What are the key topics from my recent Knowledge Base documents? Please cite specific documents."
3. Wait for response (up to 30 seconds)
4. **Verify response contains:**
   - References to specific KB document names
   - Actual content from documents
   - Agent attribution

*Pass Criteria:* At least 1 document cited

### Test 4.6: Multi-Turn Conversation
1. In same chat, send follow-up: "Tell me more about the first topic you mentioned."
2. Verify response references previous context
3. Verify conversation maintains coherence

### Test 4.7: Chat Error Handling
1. Send extremely long message (if possible)
2. Verify system handles gracefully (error or truncation)

---

## PHASE 5: CHAT - MEETING ROOMS (5 tests)

### Test 5.1: Meeting Rooms Tab Access
1. Navigate to `/chat`
2. Find and click "Meeting Rooms" tab
3. Verify Meeting Rooms interface loads

### Test 5.2: Meeting Room List
1. Verify meeting rooms list displays
2. Note if there are existing rooms or empty state

### Test 5.3: Create Meeting Room (if available)
1. Look for "Create Room" or similar button
2. If present, create: "E2E Test Meeting Room"
3. Verify room appears in list

### Test 5.4: Meeting Room Entry
1. Click on a meeting room
2. Verify room interface loads with agent participants

### Test 5.5: Meeting Room Discussion (if autonomous mode available)
1. If room supports autonomous discussion, trigger it
2. Verify agents respond to each other

---

## PHASE 6: TASKS - BOARD VIEW (10 tests)

### Test 6.1: Tasks Page Load
1. Navigate to `/tasks`
2. Verify Kanban board displays
3. Verify all 4 columns: To Do, In Progress, Blocked, Done

### Test 6.2: Task Counts Display
1. Verify task count shows in header
2. Verify each column shows task count

### Test 6.3: Create Task - Basic
1. Click "Add Task" button
2. Fill title: "E2E Test Task - Basic Creation"
3. Leave other fields default
4. Click Create
5. Verify task appears in To Do column

### Test 6.4: Create Task - Full Details
1. Click "Add Task"
2. Fill title: "E2E Test Task - Full Details"
3. Fill description: "This is an automated test task with full details"
4. Set priority: High
5. Set team: Engineering
6. Set due date: tomorrow
7. Click Create
8. Verify task appears with priority indicator

### Test 6.5: Edit Task
1. Click on "E2E Test Task - Basic Creation"
2. Verify edit modal opens
3. Change title to: "E2E Test Task - Edited"
4. Click Update
5. Verify change persists

### Test 6.6: Change Task Status via Modal
1. Open task edit modal
2. Change status from To Do to In Progress
3. Save changes
4. Verify task moves to In Progress column

### Test 6.7: Delete Task
1. Open task edit modal for "E2E Test Task - Edited"
2. Click Delete
3. Confirm deletion
4. Verify task is removed from board

### Test 6.8: Task Search
1. Type in search box: "E2E"
2. Verify tasks filter to show only matching tasks
3. Clear search
4. Verify all tasks return

### Test 6.9: Task Filter - Priority
1. Click priority filter button (e.g., "High")
2. Verify only High priority tasks show
3. Click again to clear filter

### Test 6.10: Task Filter - Team
1. Select a team from Team dropdown
2. Verify tasks filter by team
3. Reset to show all

---

## PHASE 7: TASKS - ADVANCED FEATURES (6 tests)

### Test 7.1: Task Filter - Assignee
1. Select an assignee from dropdown
2. Verify tasks filter correctly

### Test 7.2: Task Filter - Due Date Range
1. Set due date range filter
2. Verify tasks filter by date

### Test 7.3: Task Filter - Source
1. Click a source filter (Transcript, Conversation, etc.)
2. Verify filtering works

### Test 7.4: Show/Hide Completed Toggle
1. Find "Show completed" checkbox
2. Toggle it off
3. Verify Done column behavior changes

### Test 7.5: Sort Tasks
1. Click sort button in a column
2. Verify tasks reorder

### Test 7.6: Refresh Tasks
1. Click Refresh button
2. Verify tasks reload without losing state

---

## PHASE 8: PROJECTS (10 tests)

### Test 8.1: Projects Page Load
1. Navigate to `/projects`
2. Verify projects list or pipeline view loads

### Test 8.2: Pipeline Columns Present
1. Verify status columns exist (Discovery, Evaluation, etc.)
2. Count columns match expected

### Test 8.3: Create Project
1. Click "Add Project" button
2. Fill name: "E2E Test Project"
3. Fill description: "Automated test project"
4. Click Create
5. Verify project appears

### Test 8.4: Project Details View
1. Click on test project
2. Verify details panel or page opens
3. Verify name, description, status display

### Test 8.5: Edit Project Name
1. In project details, find edit option
2. Change name to: "E2E Test Project - Edited"
3. Save
4. Verify name updates

### Test 8.6: Edit Project Status
1. Change project status to next stage
2. Save
3. Verify project moves to new column

### Test 8.7: Project Scoring (if available)
1. If project has scoring inputs, enter values
2. Verify score calculates
3. Verify tier updates if applicable

### Test 8.8: Project Search/Filter
1. Use search or filter if available
2. Verify projects filter correctly

### Test 8.9: Project Stakeholders (if available)
1. Look for stakeholder assignment
2. If available, assign a stakeholder
3. Verify association saves

### Test 8.10: Delete Project
1. Find delete option for test project
2. Delete project
3. Verify removal

---

## PHASE 9: KNOWLEDGE BASE - NAVIGATION (8 tests)

### Test 9.1: KB Page Load
1. Navigate to `/kb`
2. Verify main KB interface loads
3. Verify tabs: Documents, Conversations, Data Map

### Test 9.2: Documents Tab
1. Click Documents tab (if not default)
2. Verify document browser displays

### Test 9.3: Vault Structure Display
1. In document browser, verify Vault Structure heading
2. Verify folder list displays with document counts

### Test 9.4: Expand Folder
1. Click on a folder (e.g., "Granola" or "GitHub")
2. Verify folder expands or documents filter

### Test 9.5: KB Navigator Panel
1. Verify KB Navigator section displays
2. Verify document count shows

### Test 9.6: Conversations Tab
1. Click Conversations tab
2. Verify conversation list loads

### Test 9.7: Data Map Tab
1. Click Data Map tab
2. Verify data map visualization loads

### Test 9.8: Storage Usage Display
1. Verify storage usage indicator shows
2. Check format (e.g., "75 KB / 500 MB")

---

## PHASE 10: KNOWLEDGE BASE - DOCUMENTS (8 tests)

### Test 10.1: Document Selection
1. Click on a document in the navigator
2. Verify document preview loads

### Test 10.2: Document Preview Content
1. With document selected, verify:
   - Title displays
   - Content/preview shows
   - Metadata visible (date, source, etc.)

### Test 10.3: Document Agents
1. Verify associated agents display for document
2. Check agent icons/tags

### Test 10.4: Document Tags
1. Verify document tags display
2. Click a tag to filter (if available)

### Test 10.5: Document Search
1. Find search input in KB
2. Search for a term (e.g., "AI")
3. Verify results update

### Test 10.6: Tag Manager
1. Click Tag Manager button/tab
2. Verify tag management interface

### Test 10.7: Full Resync Button
1. Find Full Resync button (in Vault section)
2. Verify button is clickable (don't actually trigger full resync in test)

### Test 10.8: Multiple Document Selection
1. If supported, select multiple documents
2. Verify multi-select behavior

---

## PHASE 11: AGENTS DIRECTORY (6 tests)

### Test 11.1: Agents Page Load
1. Navigate to `/agents`
2. Verify agent cards/list loads

### Test 11.2: All 21 Agents Present
1. Scroll through agents list
2. Verify key agents present: Atlas, Compass, Capital, Guardian, Counselor, Sage, Oracle, etc.
3. Count total agents (should be ~21)

### Test 11.3: Agent Card Information
1. Verify each card shows:
   - Agent name
   - Icon/avatar
   - Brief description or role

### Test 11.4: Agent Details Expansion
1. Click on an agent card (e.g., Atlas)
2. Verify expanded details show
3. Verify capabilities/description

### Test 11.5: Agent Category Grouping
1. Verify agents are grouped by category if applicable
2. Check for category headers

### Test 11.6: Agent Search/Filter (if available)
1. If search exists, search for an agent
2. Verify filtering works

---

## PHASE 12: INTELLIGENCE DASHBOARD (5 tests)

### Test 12.1: Intelligence Page Load
1. Navigate to `/intelligence`
2. Verify page loads without errors

### Test 12.2: Charts/Visualizations Display
1. Verify charts or data visualizations render
2. Check for loading states completing

### Test 12.3: Intelligence Metrics
1. Verify key metrics display
2. Check for data in metrics (not empty)

### Test 12.4: Time Range Selection (if available)
1. If time range selector exists, change it
2. Verify data updates

### Test 12.5: Intelligence Drill-Down (if available)
1. Click on a chart element or metric
2. Verify drill-down or detail view

---

## PHASE 13: DISCo (8 tests)

### Test 13.1: DISCo Page Load
1. Navigate to `/disco`
2. Verify DISCo interface loads

### Test 13.2: DISCo Tabs/Sections
1. Verify main DISCo sections display
2. Check for Discovery, Insights, Synthesis, Convergence tabs

### Test 13.3: Initiative List
1. Verify initiatives list displays
2. Note existing initiatives or empty state

### Test 13.4: Create Initiative (if available)
1. Look for create initiative option
2. If available, create: "E2E Test Initiative"
3. Verify creation

### Test 13.5: Initiative Details
1. Click on an initiative
2. Verify details panel loads

### Test 13.6: Initiative Members (if available)
1. Check for members section
2. Verify member management UI

### Test 13.7: Initiative Documents (if available)
1. Check for associated documents
2. Verify document linking UI

### Test 13.8: Delete Test Initiative
1. Delete any test initiative created
2. Verify cleanup

---

## PHASE 14: ADMIN HELP PANEL (5 tests)

### Test 14.1: Help Panel Visibility
1. On chat page, verify Admin Help panel on right side
2. Verify "How can I help?" text

### Test 14.2: Quick Help Options
1. Verify quick help buttons display:
   - "How do I add a new user?"
   - "How do I customize the theme?"
   - "How do I export conversation history?"

### Test 14.3: Click Quick Help Option
1. Click one of the quick help buttons
2. Verify helpful response appears

### Test 14.4: Custom Help Question
1. Type in help input: "How do I create a new task?"
2. Submit question
3. Verify helpful response

### Test 14.5: Help Previous Chats
1. Click "Previous Chats" button
2. Verify help history or conversation list

---

## PHASE 15: CLEANUP & FINAL VERIFICATION (5 tests)

### Cleanup 15.1: Delete Test Conversations
1. Navigate to `/chat`
2. Search/find all conversations with "E2E" in name
3. Delete each one
4. Verify deletion

### Cleanup 15.2: Delete Test Tasks
1. Navigate to `/tasks`
2. Search for "E2E Test"
3. Delete all matching tasks
4. Verify cleanup

### Cleanup 15.3: Delete Test Projects
1. Navigate to `/projects`
2. Find any "E2E Test" projects
3. Delete them
4. Verify cleanup

### Cleanup 15.4: Verify No Test Data Remains
1. Search tasks for "E2E" - should be empty
2. Search chat for "E2E" - should be empty
3. Check projects for "E2E" - should be empty

### Cleanup 15.5: Final Console Error Check
1. Run `mcp__playwright__browser_console_messages`
2. Check for any ERROR level messages
3. Document any issues found

---

## --full Mode Summary

```
============================================
COMPREHENSIVE E2E TEST SUMMARY
============================================
Date: [CURRENT_DATE]
Environment: Production (thesis-mvp.vercel.app)
Total Tests: 100
============================================

PHASE 1: Authentication & Session (4 tests)
- Test 1.1 Verify Auth:              [PASS/FAIL]
- Test 1.2 User Menu:                [PASS/FAIL]
- Test 1.3 Nav Links Present:        [PASS/FAIL]
- Test 1.4 Nav Links Work:           [PASS/FAIL]

PHASE 2: Dashboard (5 tests)
- Test 2.1 Dashboard Load:           [PASS/FAIL]
- Test 2.2 Widgets Present:          [PASS/FAIL]
- Test 2.3 Quick Actions:            [PASS/FAIL]
- Test 2.4 Data Loading:             [PASS/FAIL]
- Test 2.5 Widget Navigation:        [PASS/FAIL]

PHASE 3: Chat - Basic (8 tests)
- Test 3.1 Page Load:                [PASS/FAIL]
- Test 3.2 New Chat:                 [PASS/FAIL]
- Test 3.3 Send/Receive:             [PASS/FAIL]
- Test 3.4 Auto-Naming:              [PASS/FAIL]
- Test 3.5 Rename:                   [PASS/FAIL]
- Test 3.6 Archive:                  [PASS/FAIL]
- Test 3.7 Delete:                   [PASS/FAIL]
- Test 3.8 Search:                   [PASS/FAIL]

PHASE 4: Chat - AI & KB (7 tests)
- Test 4.1 Agent Selector:           [PASS/FAIL]
- Test 4.2 Atlas Agent:              [PASS/FAIL]
- Test 4.3 Capital Agent:            [PASS/FAIL]
- Test 4.4 Auto Routing:             [PASS/FAIL]
- Test 4.5 KB Context (CRITICAL):    [PASS/FAIL]
- Test 4.6 Multi-Turn:               [PASS/FAIL]
- Test 4.7 Error Handling:           [PASS/FAIL]

PHASE 5: Meeting Rooms (5 tests)
- Test 5.1 Tab Access:               [PASS/FAIL]
- Test 5.2 Room List:                [PASS/FAIL]
- Test 5.3 Create Room:              [PASS/FAIL]
- Test 5.4 Room Entry:               [PASS/FAIL]
- Test 5.5 Discussion:               [PASS/FAIL]

PHASE 6: Tasks - Board (10 tests)
- Test 6.1 Page Load:                [PASS/FAIL]
- Test 6.2 Task Counts:              [PASS/FAIL]
- Test 6.3 Create Basic:             [PASS/FAIL]
- Test 6.4 Create Full:              [PASS/FAIL]
- Test 6.5 Edit Task:                [PASS/FAIL]
- Test 6.6 Change Status:            [PASS/FAIL]
- Test 6.7 Delete Task:              [PASS/FAIL]
- Test 6.8 Search:                   [PASS/FAIL]
- Test 6.9 Filter Priority:          [PASS/FAIL]
- Test 6.10 Filter Team:             [PASS/FAIL]

PHASE 7: Tasks - Advanced (6 tests)
- Test 7.1 Filter Assignee:          [PASS/FAIL]
- Test 7.2 Filter Date:              [PASS/FAIL]
- Test 7.3 Filter Source:            [PASS/FAIL]
- Test 7.4 Show Completed:           [PASS/FAIL]
- Test 7.5 Sort Tasks:               [PASS/FAIL]
- Test 7.6 Refresh:                  [PASS/FAIL]

PHASE 8: Projects (10 tests)
- Test 8.1 Page Load:                [PASS/FAIL]
- Test 8.2 Pipeline Columns:         [PASS/FAIL]
- Test 8.3 Create Project:           [PASS/FAIL]
- Test 8.4 Project Details:          [PASS/FAIL]
- Test 8.5 Edit Name:                [PASS/FAIL]
- Test 8.6 Edit Status:              [PASS/FAIL]
- Test 8.7 Scoring:                  [PASS/FAIL]
- Test 8.8 Search/Filter:            [PASS/FAIL]
- Test 8.9 Stakeholders:             [PASS/FAIL]
- Test 8.10 Delete:                  [PASS/FAIL]

PHASE 9: KB - Navigation (8 tests)
- Test 9.1 Page Load:                [PASS/FAIL]
- Test 9.2 Documents Tab:            [PASS/FAIL]
- Test 9.3 Vault Structure:          [PASS/FAIL]
- Test 9.4 Expand Folder:            [PASS/FAIL]
- Test 9.5 Navigator Panel:          [PASS/FAIL]
- Test 9.6 Conversations Tab:        [PASS/FAIL]
- Test 9.7 Data Map Tab:             [PASS/FAIL]
- Test 9.8 Storage Usage:            [PASS/FAIL]

PHASE 10: KB - Documents (8 tests)
- Test 10.1 Document Selection:      [PASS/FAIL]
- Test 10.2 Preview Content:         [PASS/FAIL]
- Test 10.3 Document Agents:         [PASS/FAIL]
- Test 10.4 Document Tags:           [PASS/FAIL]
- Test 10.5 Search:                  [PASS/FAIL]
- Test 10.6 Tag Manager:             [PASS/FAIL]
- Test 10.7 Resync Button:           [PASS/FAIL]
- Test 10.8 Multi-Select:            [PASS/FAIL]

PHASE 11: Agents (6 tests)
- Test 11.1 Page Load:               [PASS/FAIL]
- Test 11.2 All Agents Present:      [PASS/FAIL]
- Test 11.3 Card Information:        [PASS/FAIL]
- Test 11.4 Details Expansion:       [PASS/FAIL]
- Test 11.5 Category Grouping:       [PASS/FAIL]
- Test 11.6 Search/Filter:           [PASS/FAIL]

PHASE 12: Intelligence (5 tests)
- Test 12.1 Page Load:               [PASS/FAIL]
- Test 12.2 Charts Display:          [PASS/FAIL]
- Test 12.3 Metrics:                 [PASS/FAIL]
- Test 12.4 Time Range:              [PASS/FAIL]
- Test 12.5 Drill-Down:              [PASS/FAIL]

PHASE 13: DISCo (8 tests)
- Test 13.1 Page Load:               [PASS/FAIL]
- Test 13.2 Tabs/Sections:           [PASS/FAIL]
- Test 13.3 Initiative List:         [PASS/FAIL]
- Test 13.4 Create Initiative:       [PASS/FAIL]
- Test 13.5 Initiative Details:      [PASS/FAIL]
- Test 13.6 Members:                 [PASS/FAIL]
- Test 13.7 Documents:               [PASS/FAIL]
- Test 13.8 Delete Initiative:       [PASS/FAIL]

PHASE 14: Admin Help (5 tests)
- Test 14.1 Panel Visibility:        [PASS/FAIL]
- Test 14.2 Quick Options:           [PASS/FAIL]
- Test 14.3 Click Quick Help:        [PASS/FAIL]
- Test 14.4 Custom Question:         [PASS/FAIL]
- Test 14.5 Previous Chats:          [PASS/FAIL]

PHASE 15: Cleanup (5 tests)
- Test 15.1 Delete Conversations:    [DONE/PARTIAL]
- Test 15.2 Delete Tasks:            [DONE/PARTIAL]
- Test 15.3 Delete Projects:         [DONE/PARTIAL]
- Test 15.4 Verify No Test Data:     [PASS/FAIL]
- Test 15.5 Console Error Check:     [PASS/FAIL]

--------------------------------------------
TOTALS:  XX/100 tests passed
         XX/100 tests failed
         XX/100 tests skipped (feature not available)
============================================

CRITICAL TESTS:
- KB Context Chat (4.5): [PASS/FAIL]
  - Documents cited: [COUNT]
  - Response quality: [GOOD/NEEDS_IMPROVEMENT]

CONSOLE ERRORS FOUND:
[List any ERROR level console messages]
============================================
```

---

# OPTION: --comprehensive (Everything)

Run ALL tests AND all code quality gates. This is the most thorough validation for major releases.

## Execution Order

1. **Run DEFAULT MODE first** (Stages 1-4 + basic E2E)
2. **Run QUALITY MODE** (all 6 quality stages)
3. **Run FULL E2E MODE** (100 production E2E scenarios)

## Comprehensive Summary

After ALL stages complete, provide a combined summary:

```
============================================
COMPREHENSIVE TEST SUMMARY
============================================
Date: [CURRENT_DATE]
============================================

FUNCTIONAL TESTS (DEFAULT MODE)
--------------------------------------------
Stage 1 - Unit Tests:        XX passed, XX failed, XX skipped
Stage 2 - Integration Tests: XX passed, XX failed, XX skipped
Stage 3 - Extended Tests:    XX passed, XX failed, XX skipped
Stage 4 - Basic E2E Tests:   XX passed, XX failed
--------------------------------------------
Functional Total:            XXX passed, XXX failed

CODE QUALITY GATES
--------------------------------------------
Stage 1 - Ruff Lint/Format:  XX errors, XX warnings
Stage 2 - Mypy Type Check:   XX type errors
Stage 3 - Complexity (C90):  XX violations
Stage 4 - Docstrings (D):    XX issues
Stage 5 - Secret Scan:       XX secrets found
Stage 6 - Frontend Lint:     XX errors
--------------------------------------------
Quality Total:               XX issues

FULL E2E TESTS (100 SCENARIOS)
--------------------------------------------
Phase 1 - Auth & Session:    X/4 passed
Phase 2 - Dashboard:         X/5 passed
Phase 3 - Chat Basic:        X/8 passed
Phase 4 - Chat AI & KB:      X/7 passed
Phase 5 - Meeting Rooms:     X/5 passed
Phase 6 - Tasks Board:       X/10 passed
Phase 7 - Tasks Advanced:    X/6 passed
Phase 8 - Projects:          X/10 passed
Phase 9 - KB Navigation:     X/8 passed
Phase 10 - KB Documents:     X/8 passed
Phase 11 - Agents:           X/6 passed
Phase 12 - Intelligence:     X/5 passed
Phase 13 - DISCo:            X/8 passed
Phase 14 - Admin Help:       X/5 passed
Phase 15 - Cleanup:          X/5 passed
--------------------------------------------
Full E2E Total:              XX/100 passed

============================================
OVERALL RESULT: [PASS/WARN/FAIL]
============================================

Pass Criteria:
- All functional tests pass
- All E2E tests pass (or documented as N/A)
- No secrets found (critical)
- Lint errors = 0
- Type errors = advisory (Week 1-2)
- Complexity violations = warning only

Blocking Issues:
- [List any blocking failures]

Advisory Issues:
- [List non-blocking warnings]
============================================
```

---

# Failure Remediation Plan

When tests fail, create a detailed improvement plan.

## Step 1: Document Each Failure

| Field | Description |
|-------|-------------|
| **Test Name** | Full test path |
| **Stage** | Which stage/phase |
| **Error Type** | Exception or failure type |
| **Error Message** | Full error/traceback |
| **Root Cause** | Analysis of why it failed |
| **Proposed Fix** | Specific changes needed |
| **Files Affected** | Which files need modification |

## Step 2: Create Improvement Plan

```
============================================
FAILURE REMEDIATION PLAN
============================================

FAILURE 1: [Test Name]
-----------------------
Stage: [Stage/Phase]
Error: [Brief description]

Root Cause Analysis:
[Why the test failed]

Proposed Fix:
[Specific changes needed]

Files to Modify:
- [file1]: [what to change]

============================================
```

## Step 3: Generate Follow-Up Prompt

Create a ready-to-use prompt for a new Claude Code session:

````markdown
## Fix Test Failures from /test Run

### Context
The `/test` command was run on [DATE] and the following tests failed.
Working directory: `/Users/charlie.fuller/vaults/Contentful/GitHub/thesis`

### Failed Tests

#### Failure 1: `[FULL_TEST_PATH]`

**Error:**
```
[PASTE FULL ERROR/TRACEBACK]
```

**Root Cause:** [EXPLANATION]
**Proposed Fix:** [SPECIFIC CHANGES]

### Instructions
1. Read failing test file
2. Read source files being tested
3. Implement fixes
4. Re-run specific tests to verify
5. Run full suite with `/test`
6. Commit fixes
````

---

# Troubleshooting

## Pytest Issues

### "Invalid URL" Supabase Errors
**Cause:** `.env` is encrypted. Always run with `dotenvx run`.

### Lazy Supabase Initialization
Some modules need lazy `_get_db()` pattern instead of import-time initialization.

### Test Isolation Issues
Tests pass individually but fail together - module state pollution. Use `pytest-forked` or reset fixtures.

## E2E Issues

### Playwright Not Connected
- Verify Playwright MCP server is running via `/mcp`
- Use `mcp__playwright__browser_snapshot` to check page state

### Element Not Found
- Always take a fresh snapshot (`mcp__playwright__browser_snapshot`) before interacting
- Use accessibility snapshots to find interactive elements

### Authentication Issues
- Complete login flow if redirected
- Session may expire - re-login if needed

### Slow Responses
- KB context chat may take 10-15 seconds
- Use `mcp__playwright__browser_wait_for` for expected content

---

# Test Coverage Reference

| Mode | Tests | Expected |
|------|-------|----------|
| --quick | Unit tests only | ~370 tests |
| default | All pytest + 5 E2E | ~800 tests |
| --full | Production E2E | 100 scenarios |
| --quality | Code quality gates | 6 check categories |
| comprehensive | Functional + Quality + Full E2E | ~1000+ checks |

### Mode Summary

| Mode | What It Runs | Use Case |
|------|--------------|----------|
| Quick | Unit tests only | Fast feedback during development |
| Default | Pytest stages 1-4 + 5 basic E2E | Standard CI validation |
| Full E2E | 100 browser scenarios | Pre-release production validation |
| Quality | Type check, lint, complexity, secrets | Code review preparation |
| Comprehensive | Default + Quality + Full E2E | Full validation before major releases |

### Quality Gate Breakdown

| Stage | Check | Tool | Threshold |
|-------|-------|------|-----------|
| 1 | Lint & Format | Ruff | 0 errors |
| 2 | Type Checking | Mypy | Advisory (Week 1-2) |
| 3 | Complexity | Ruff C90 | Max 10 per function |
| 4 | Docstrings | Ruff D | Google style |
| 5 | Secret Scan | TruffleHog | 0 secrets (critical) |
| 6 | Frontend Lint | ESLint | 0 errors |

### E2E Scenario Summary

| Mode | Scenarios | Validates |
|------|-----------|-----------|
| default (basic) | 5 | Auth, Chat, KB page load, Tasks CRUD, Task delete |
| --full | 100 | Complete app coverage (see breakdown below) |

### --full Mode Test Breakdown

| Phase | Tests | Coverage |
|-------|-------|----------|
| 1. Auth & Session | 4 | Login state, user menu, navigation links |
| 2. Dashboard | 5 | Widgets, data loading, quick actions |
| 3. Chat - Basic | 8 | New chat, send/receive, rename, archive, delete, search |
| 4. Chat - AI & KB | 7 | Agent selection, KB context (critical), multi-turn |
| 5. Meeting Rooms | 5 | Tab access, room list, create, entry, discussion |
| 6. Tasks - Board | 10 | CRUD, search, filters (priority, team) |
| 7. Tasks - Advanced | 6 | Filters (assignee, date, source), sort, refresh |
| 8. Projects | 10 | CRUD, pipeline, scoring, stakeholders |
| 9. KB - Navigation | 8 | Tabs, vault structure, folders, storage |
| 10. KB - Documents | 8 | Selection, preview, agents, tags, search |
| 11. Agents | 6 | Directory, all 21 agents, details, categories |
| 12. Intelligence | 5 | Dashboard, charts, metrics, time range |
| 13. DISCo | 8 | Initiative CRUD, members, documents |
| 14. Admin Help | 5 | Panel, quick options, custom questions |
| 15. Cleanup | 5 | Delete test data, verify clean state |
| **TOTAL** | **100** | **Complete Thesis functionality** |
