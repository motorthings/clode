Start the contract-review app locally. All services run on dedicated ports to avoid conflicts with other projects.

## Port Assignments
- Frontend (Next.js): 3001
- Backend API (FastAPI): 8001
- Celery Flower: 5556
- Redis: 6379

## Steps

1. Check prerequisites:
   - Node.js installed (check with `node --version`)
   - Python 3.11+ installed (check with `python3 --version`)
   - Redis running (check with `redis-cli ping`)
   - If Redis not running, start it: `brew services start redis` (macOS) or `docker run -d -p 6379:6379 redis:7-alpine`

2. Kill any existing processes on ports 3001 and 8001:
   - `lsof -ti:3001 | xargs kill -9 2>/dev/null; lsof -ti:8001 | xargs kill -9 2>/dev/null`

3. Start the backend (from `backend/` directory):
   - Activate venv: `source venv/bin/activate`
   - Run: `uvicorn main:app --reload --port 8001 &`
   - Wait 3 seconds for startup

4. Start the Celery worker (from `backend/` directory, same venv):
   - Run: `celery -A celery_app worker --loglevel=info --concurrency=3 -Q default,urgent,batch --pool=solo &`

5. Start Flower monitoring (from `backend/` directory, same venv):
   - Run: `celery -A celery_app flower --port=5556 --basic_auth=admin:admin &`

6. Clear Next.js cache and start frontend (from `frontend/` directory):
   - `rm -rf .next`
   - `npm run dev`

7. Wait 5 seconds, then verify all services:
   - Backend: `curl -s http://localhost:8001/health || curl -s http://localhost:8001/docs`
   - Frontend: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3001`
   - Report status of each service

## Important
- Backend must start BEFORE frontend (frontend calls backend API)
- The backend `.env` file must exist with valid API keys (Supabase, Anthropic, Voyage AI)
- The frontend `.env.local` must have `NEXT_PUBLIC_API_URL="http://localhost:8001"`
- All backend processes run in background; frontend runs in foreground for log visibility
