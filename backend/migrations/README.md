# Database Migrations

## fix_json_columns.sql

**Purpose**: Convert TEXT columns to JSON type in the `analyses` table.

**Issue**: The SQLAlchemy model defines `formatted_output`, `preparation_result`, and `analysis_result` as JSON columns, but the actual database table has them as TEXT. This causes issues when the API tries to return these fields.

**Solution**: Use PostgreSQL's `ALTER COLUMN ... TYPE JSON USING` to safely convert existing TEXT data to JSON type.

### How to Run

```bash
# Run the migration
docker compose exec postgres psql -U postgres -d legally_ai -f /migrations/fix_json_columns.sql

# Or manually:
docker compose exec postgres psql -U postgres -d legally_ai << 'SQL'
ALTER TABLE analyses
ALTER COLUMN formatted_output TYPE JSON
USING CASE
    WHEN formatted_output IS NULL THEN NULL
    WHEN formatted_output::text = '' THEN NULL
    ELSE formatted_output::json
END;

ALTER TABLE analyses
ALTER COLUMN preparation_result TYPE JSON
USING CASE
    WHEN preparation_result IS NULL THEN NULL
    WHEN preparation_result::text = '' THEN NULL
    ELSE preparation_result::json
END;

ALTER TABLE analyses
ALTER COLUMN analysis_result TYPE JSON
USING CASE
    WHEN analysis_result IS NULL THEN NULL
    WHEN analysis_result::text = '' THEN NULL
    ELSE analysis_result::json
END;
SQL
```

### Verification

After running the migration, verify the column types:

```bash
docker compose exec postgres psql -U postgres -d legally_ai -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'analyses' AND column_name IN ('formatted_output', 'preparation_result', 'analysis_result');"
```

Expected output:
```
     column_name     | data_type
---------------------+-----------
 formatted_output    | json
 preparation_result  | json
 analysis_result     | json
```
