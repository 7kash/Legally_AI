-- Migration: Convert formatted_output column from TEXT to JSON
-- Date: 2025-11-14
-- Description: The formatted_output column needs to be JSON type to store structured analysis results

-- Step 1: Convert TEXT column to JSON type
-- Note: This will fail if there are existing TEXT values that aren't valid JSON
-- You may need to clean up data first if there are invalid JSON strings

ALTER TABLE analyses
ALTER COLUMN formatted_output TYPE JSON USING
  CASE
    WHEN formatted_output IS NULL THEN NULL
    WHEN formatted_output::text = '' THEN NULL
    ELSE formatted_output::json
  END;

-- Note: If you have existing markdown text in formatted_output,
-- you'll need to convert or clear it first:
-- UPDATE analyses SET formatted_output = NULL WHERE formatted_output IS NOT NULL;
-- Then run the ALTER TABLE command above
