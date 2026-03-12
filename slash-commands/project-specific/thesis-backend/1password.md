# /1password - Secure Credential Access

Access Thesis credentials securely via 1Password CLI.

## Thesis Credentials Location

- **Vault**: Employee
- **Item**: Thesis Backend
- **Item ID**: `bqvwidzwtlswzndi5wjq33gon4`

## Available Credentials

| Field | Description |
|-------|-------------|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase admin key |
| `SUPABASE_JWT_SECRET` | JWT signing secret |
| `ANTHROPIC_API_KEY` | Claude API key |
| `VOYAGE_API_KEY` | Voyage embeddings API |
| `NEO4J_URI` | Neo4j connection string |
| `NEO4J_USERNAME` | Neo4j username |
| `NEO4J_PASSWORD` | Neo4j password |
| `MEM0_API_KEY` | Mem0 memory API key |

## How to Retrieve Credentials

### Get a specific field
```bash
op item get bqvwidzwtlswzndi5wjq33gon4 --field SUPABASE_URL --reveal
```

### Get all fields (JSON)
```bash
op item get bqvwidzwtlswzndi5wjq33gon4 --format json
```

### Use in scripts
The `scripts/lib/credentials.py` module automatically retrieves from 1Password when:
```bash
USE_1PASSWORD=1 python scripts/your_script.py
```

## Python Usage

```python
from scripts.lib.credentials import get_credentials, get_supabase_client

# Get all credentials (uses env vars, falls back to 1Password if USE_1PASSWORD=1)
creds = get_credentials()

# Get a configured Supabase client
supabase = get_supabase_client()
```

## Security Notes

- 1Password CLI requires Touch ID or system authentication
- Credentials are never stored in plaintext outside 1Password
- The `.env` file can be deleted once 1Password is primary
- Set `USE_1PASSWORD=1` in your shell profile for automatic retrieval
