Restart both frontend and backend development servers with clean caches.

Steps:
1. Kill all processes on ports 3000 (frontend) and 8000 (backend)
2. Clear Next.js cache (remove .next directory in frontend)
3. Start backend server in background (uvicorn on port 8000)
4. Wait 3 seconds for backend to initialize
5. Start frontend server in background (npm run dev on port 3000)
6. Wait 5 seconds and verify both servers are running
7. Report status to user

Important:
- Run commands from the correct directories (/Users/motorthings/Documents/GitHub/superassistant-mvp)
- Use background processes for both servers
- Provide clear feedback on success/failure
