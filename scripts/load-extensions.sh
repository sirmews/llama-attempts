#!/bin/sh

# You could probably do this fancier and have an array of extensions
# to create, but this is mostly an illustration of what can be done

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<EOF
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS pgvector;

-- Create a sample table for Llama Index
CREATE TABLE IF NOT EXISTS data (
    id SERIAL PRIMARY KEY,
    document_text TEXT,
    document_vector pgvector
);

SELECT * FROM pg_extension;
EOF
