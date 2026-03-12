# /supabase - Interact with Supabase Database

Query and interact with the Supabase database securely using environment credentials.

## Usage
```
/supabase tables          # List all tables
/supabase query <table>   # Query a table
/supabase count <table>   # Count rows in a table
/supabase schema <table>  # Show table schema
/supabase migrations      # Show migration status
```

## How to Execute

### Use the Python Helper Script
All operations should be done via Python scripts that use environment variables. Never hardcode credentials.

### List Tables
```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
dotenvx run -- python3 -c "
from scripts.lib.credentials import get_supabase_client
sb = get_supabase_client()
# List tables using Supabase API
result = sb.table('conversations').select('id', count='exact').limit(0).execute()
print('Tables accessible via Supabase client')
"
```

### Query a Table (Example: conversations)
```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
dotenvx run -- python3 -c "
from scripts.lib.credentials import get_supabase_client
sb = get_supabase_client()
result = sb.table('conversations').select('*').limit(5).execute()
for row in result.data:
    print(row)
"
```

### Count Rows
```bash
cd /Users/charlie.fuller/vaults/Contentful/GitHub/thesis/backend
dotenvx run -- python3 -c "
from scripts.lib.credentials import get_supabase_client
sb = get_supabase_client()
result = sb.table('TABLENAME').select('*', count='exact').limit(0).execute()
print(f'Count: {result.count}')
"
```

## Common Tables

| Table | Description |
|-------|-------------|
| `conversations` | Chat conversations |
| `messages` | Chat messages |
| `documents` | Knowledge base documents |
| `document_chunks` | Document chunks for RAG |
| `opportunities` | AI implementation opportunities |
| `tasks` | Kanban task items |
| `stakeholders` | Stakeholder profiles |
| `agents` | Agent configurations |
| `users` | User accounts |

## Security Notes

- NEVER hardcode credentials in scripts
- Use `dotenvx run --` to decrypt environment variables
- Use `scripts/lib/credentials.py` for Python scripts
- Credentials are read from `.env` which is gitignored
- For production, set `DOTENV_PRIVATE_KEY` in the deployment platform

## Direct Database Access (Admin Only)

For direct SQL access, use Supabase Dashboard or:
```bash
# Get connection string from Supabase Dashboard > Settings > Database
psql "postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres"
```
