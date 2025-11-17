-- Add formatted_output_eli5 column to analyses table
-- This migration adds the ELI5 (Explain Like I'm 5) simplified version storage

-- Add the column
ALTER TABLE analyses
ADD COLUMN IF NOT EXISTS formatted_output_eli5 JSON;

-- Verify the migration
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'analyses' AND column_name = 'formatted_output_eli5';
