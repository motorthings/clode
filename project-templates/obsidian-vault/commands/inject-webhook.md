Inject synthetic interview data for Charlie Motor directly into the SuperAssistant database.

**This command injects the synthetic interview transcript and triggers the full extraction workflow:**
- Stores transcript in interview_extractions table
- Runs Solomon Stage 1 (TRIPS/LTEM extraction)
- Extracts pain points, values, frameworks, team structure
- Generates extraction_data JSON

Execute this command:
```bash
cd ~/Documents/GitHub/superassistant-mvp/backend && set -a && source .env && set +a && ./venv/bin/python inject_synthetic_interview.py
```

After running, provide a summary of:
- Whether the script executed successfully
- Extraction ID and session details
- Number of messages parsed
- Solomon processing status
- Any errors or warnings

**Requirements:**
- Must have a scheduled interview session in the database
- Uses environment variables from `.env` file
- Connects directly to Supabase (no webhook authentication needed)
