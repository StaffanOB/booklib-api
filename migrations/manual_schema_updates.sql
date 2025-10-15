-- Manual schema updates to align with current Book model
-- Run this on test/prod databases that have old schema

-- Add missing columns to books table
ALTER TABLE books ADD COLUMN IF NOT EXISTS publish_year INTEGER;

ALTER TABLE books ADD COLUMN IF NOT EXISTS series VARCHAR(255);

-- Verify columns exist
-- \d books