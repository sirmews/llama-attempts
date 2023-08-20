CREATE TABLE IF NOT EXISTS data (
    id SERIAL PRIMARY KEY,
    document_text TEXT,
    embedding vector(384)
);
