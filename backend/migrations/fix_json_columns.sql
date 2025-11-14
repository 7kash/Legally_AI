-- Fix column types from TEXT to JSON
-- This allows PostgreSQL to properly store and validate JSON data

-- Convert formatted_output from TEXT to JSON
-- Use USING clause to safely convert existing TEXT data to JSON
ALTER TABLE analyses
ALTER COLUMN formatted_output TYPE JSON
USING CASE
    WHEN formatted_output IS NULL THEN NULL
    WHEN formatted_output::text = '' THEN NULL
    ELSE formatted_output::json
END;

-- Convert preparation_result to JSON (if needed)
ALTER TABLE analyses
ALTER COLUMN preparation_result TYPE JSON
USING CASE
    WHEN preparation_result IS NULL THEN NULL
    WHEN preparation_result::text = '' THEN NULL
    ELSE preparation_result::json
END;

-- Convert analysis_result to JSON (if needed)
ALTER TABLE analyses
ALTER COLUMN analysis_result TYPE JSON
USING CASE
    WHEN analysis_result IS NULL THEN NULL
    WHEN analysis_result::text = '' THEN NULL
    ELSE analysis_result::json
END;

-- Verify the changes
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'analyses'
AND column_name IN ('formatted_output', 'preparation_result', 'analysis_result');
