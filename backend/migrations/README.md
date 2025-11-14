# Database Migrations

This directory contains SQL migration scripts for the Legally_AI database.

## Available Migrations

### fix_json_columns.sql
**Purpose**: Convert the `formatted_output` column from TEXT to JSON type.

**Why needed**: The SQLAlchemy model expects `formatted_output` to be JSON, but the database column may be TEXT. This causes type mismatches and prevents proper storage/retrieval of structured analysis results.

**How to apply**:

```bash
# Option 1: Using docker compose
docker compose exec postgres psql -U postgres -d legally_ai -f /app/migrations/fix_json_columns.sql

# Option 2: Direct psql connection
psql -U postgres -d legally_ai -f backend/migrations/fix_json_columns.sql
```

**Important**: If you have existing TEXT data in `formatted_output` that isn't valid JSON, you'll need to clear it first:

```sql
-- Clear existing non-JSON data
UPDATE analyses SET formatted_output = NULL WHERE formatted_output IS NOT NULL;
```

## Future Improvements

Consider using Alembic for proper migration management:
1. Initialize Alembic: `alembic init alembic`
2. Configure alembic.ini with database connection
3. Generate migrations automatically from model changes
4. Apply migrations with version tracking
