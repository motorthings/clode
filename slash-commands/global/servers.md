Start local development servers. Ask which app to launch, then start all its services.

## Apps and Port Assignments

| App | Frontend | Backend | Other | Directory |
|-----|----------|---------|-------|-----------|
| contract-review | 3001 | 8001 | Flower: 5556, Redis: 6379 | ~/Documents/GitHub/contentful-contract-review |
| aesop | 3002 | 8002 | — | ~/Documents/GitHub/aesop-app |
| agent-factory | 3003 | 8003 | SQLite (no server) | ~/glean-agent-factory-app |

## Interaction

Ask the user which app they want to start: contract-review, aesop, or agent-factory. Then follow the steps for that app.

---

## contract-review

1. Check Redis is running: `redis-cli ping`
   - If not: `brew services start redis`
2. Kill existing processes: `lsof -ti:3001 | xargs kill -9 2>/dev/null; lsof -ti:8001 | xargs kill -9 2>/dev/null`
3. Start backend:
   ```
   cd ~/Documents/GitHub/contentful-contract-review/backend
   source venv/bin/activate
   uvicorn main:app --reload --port 8001 &
   ```
4. Start Celery worker (same venv):
   ```
   celery -A celery_app worker --loglevel=info --concurrency=3 -Q default,urgent,batch --pool=solo &
   ```
5. Start Flower (same venv):
   ```
   celery -A celery_app flower --port=5556 --basic_auth=admin:admin &
   ```
6. Start frontend:
   ```
   cd ~/Documents/GitHub/contentful-contract-review/frontend
   rm -rf .next
   npm run dev
   ```
7. Verify: curl backend health endpoint, report status.

---

## aesop

1. Kill existing processes: `lsof -ti:3002 | xargs kill -9 2>/dev/null; lsof -ti:8002 | xargs kill -9 2>/dev/null`
2. Start backend:
   ```
   cd ~/Documents/GitHub/aesop-app/backend
   source venv/bin/activate
   uvicorn main:app --reload --port 8002 &
   ```
3. Start frontend:
   ```
   cd ~/Documents/GitHub/aesop-app/frontend
   rm -rf .next
   npm run dev
   ```
4. Verify: curl backend health endpoint, report status.

---

## agent-factory

1. Kill existing processes: `lsof -ti:3003 | xargs kill -9 2>/dev/null; lsof -ti:8003 | xargs kill -9 2>/dev/null`
2. Start all services (Electron + Next.js + FastAPI):
   ```
   cd ~/glean-agent-factory-app
   npm run dev
   ```
   This launches all three via concurrently.
3. The Electron window opens automatically when ready.

---

## Important
- Never start two apps that share ports
- Backend must start before frontend (except agent-factory which handles ordering itself)
- Report which URLs are available when done
