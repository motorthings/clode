# QA Command

Execute QA tests for SuperAssistant MVP. Ask the user which type of test to run if not specified.

## Test Options

Present these options to the user:

```
Which QA tests would you like to run?

1. 🚀 Quick Tests (~5 seconds)
   Fast smoke tests for rapid validation

2. 🧪 Full Suite (~30 seconds)
   Complete unit + QA tests with coverage

3. ⚡ Performance Tests
   Load testing with Locust (requires running backend)

4. 🔒 Security Tests (~10 seconds)
   Security vulnerability scanning

5. 📊 Status Report (instant)
   Show test infrastructure status without running tests

6. 🎯 Everything
   Run all tests (full + security + performance)
```

## Based on User Choice

### Option 1: Quick Tests

```bash
cd backend
source venv/bin/activate
echo "Running quick smoke tests..."
python -m pytest tests/unit/test_demo_readiness.py tests/unit/test_kpi_calculation.py tests/unit/test_kpi_with_user_param.py -v --tb=line
```

**Report**:
```
## Quick Test Results ⚡
- Tests run: X
- Passed: Y ✅
- Failed: Z ❌
- Duration: ~5 seconds

[List any failures with file:line]

✅ Use for: Quick validation after changes
```

---

### Option 2: Full Suite

```bash
cd backend
source venv/bin/activate

echo "=== Running Unit Tests with Coverage ==="
python -m pytest tests/unit/ --ignore=tests/unit/test_rag.py -v --cov=. --cov-report=html --cov-report=term --tb=short 2>&1 | tail -150

echo ""
echo "=== Running QA Functional Tests ==="
python -m pytest tests/qa/test_auth_flows.py -v --tb=short 2>&1 | tail -50
```

**Report**:
```
## Full Test Suite Results 🧪

### Unit Tests
- Total: X tests
- Passed: Y (Z%)
- Failed: N
- Coverage: W%

### QA Functional Tests
- Total: A tests
- Passed: B (C%)
- Failed: D

### Reports Generated
- 📊 Coverage: backend/htmlcov/index.html
- 📝 Summary: backend/PYTEST_EXECUTION_SUMMARY.md

### Issues Found
[List failures with file:line references]

### Next Steps
[Suggest fixes if issues, or ✅ if all passing]
```

---

### Option 3: Performance Tests

**First check backend is running**:
```bash
curl -s http://localhost:8000/health > /dev/null 2>&1 && echo "✅ Backend running" || echo "❌ Start backend: cd backend && uvicorn main:app --port 8000"
```

**If running, execute**:
```bash
cd backend
source venv/bin/activate

# Quick 30-second load test
locust -f tests/performance/locustfile.py \
  --host=http://localhost:8000 \
  --users 10 \
  --spawn-rate 2 \
  --run-time 30s \
  --headless \
  --only-summary
```

**Report**:
```
## Performance Test Results ⚡

### Load Test (10 users, 30 seconds)
- Total Requests: X
- Requests/sec: Y
- Response Time (median): Zms
- Response Time (95th percentile): Ams
- Failed Requests: N (X%)

### Performance Targets
- Chat response: < 3s ✅/❌
- RAG search: < 500ms ✅/❌
- Document upload: < 5s ✅/❌
- KPI calculation: < 2s ✅/❌

[Flag any metrics exceeding targets]
```

---

### Option 4: Security Tests

```bash
cd backend
source venv/bin/activate
echo "Running security test suite..."
python -m pytest tests/security/test_security_suite.py -v --tb=short
```

**Report**:
```
## Security Test Results 🔒

### Tests Run
- JWT Security: X/Y passed
- Authorization: A/B passed
- Input Validation: C/D passed
- Rate Limiting: E/F passed
- File Upload: G/H passed
- Secure Headers: I/J passed

### Overall
- Total: X tests
- Passed: Y ✅
- Failed: Z ❌

### Vulnerabilities Found
[List any security issues with severity]

### OWASP Coverage
✅ SQL Injection protection
✅ XSS prevention
✅ Path traversal protection
[etc.]
```

---

### Option 5: Status Report

**No tests run, just report current state**:

```bash
cd backend

# Count test files
echo "Test files:"
find tests -name "test_*.py" -type f | wc -l

# Check coverage report age
ls -lh htmlcov/index.html 2>/dev/null || echo "No coverage report"

# Check test data
ls -lh test_data/*.json 2>/dev/null || echo "No test data"
```

**Read and summarize**:
- [PYTEST_EXECUTION_SUMMARY.md](backend/PYTEST_EXECUTION_SUMMARY.md)
- [QA_IMPLEMENTATION_STATUS.md](QA_IMPLEMENTATION_STATUS.md)

**Report**:
```
## QA Infrastructure Status 📊

### Test Suite Overview
- Unit Tests: X files
- QA Tests: Y files
- Security Tests: Z files
- Performance Tests: N files
- Total Test Files: W

### Last Test Run
- Date: [timestamp from files]
- Pass Rate: X%
- Coverage: Y%
- Status: ✅ Passing / ⚠️ Needs Attention

### Available Reports
- 📊 [Coverage Report](backend/htmlcov/index.html)
- 📝 [Pytest Summary](backend/PYTEST_EXECUTION_SUMMARY.md)
- 📋 [QA Status](QA_IMPLEMENTATION_STATUS.md)
- 🧪 [Test Cases](docs/testing/test-cases/)

### Recommendations
[Suggest running tests if old, or ✅ if recent]
```

---

### Option 6: Everything

Run all tests sequentially:

```bash
cd backend
source venv/bin/activate

echo "🚀 Running Quick Tests..."
python -m pytest tests/unit/test_demo_readiness.py tests/unit/test_kpi_calculation.py -v --tb=line

echo ""
echo "🧪 Running Full Unit Tests..."
python -m pytest tests/unit/ --ignore=tests/unit/test_rag.py -v --cov=. --cov-report=html --tb=short 2>&1 | tail -100

echo ""
echo "🔒 Running Security Tests..."
python -m pytest tests/security/test_security_suite.py -v --tb=short

echo ""
echo "⚡ Checking Backend for Performance Tests..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
  echo "Running Performance Tests..."
  locust -f tests/performance/locustfile.py --host=http://localhost:8000 --users 10 --spawn-rate 2 --run-time 30s --headless --only-summary
else
  echo "⚠️ Backend not running, skipping performance tests"
fi
```

**Report**: Comprehensive summary of all test results

---

## Important Notes

- **Don't install dependencies** - assume pytest, locust already installed
- **Update reports** after running tests
- **Compare to previous runs** when possible
- **Highlight regressions** (new failures, coverage drops)
- **Suggest fixes** with time estimates for any issues

## CI/CD Reminder

Remind user these tests also run automatically:
- On every push to `main` or `develop`
- On every pull request
- Via GitHub Actions: `.github/workflows/ci-cd.yml`
