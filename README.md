# What dis?

I tinker with AI to build a second brain because my first isn't so great.

Tools being used:
- [Chainlit](https://docs.chainlit.io/overview)  
- [Llama Index](https://www.llamaindex.ai/)  


# Problems
## pgvector

Possibly because I'm using a postgres image, installing the `pgvector` extension isn't immediately recognized on first run.
Running `docker-compose up` the second time will not throw an `extension not found` error. This means my extension and table setup scripts aren't working.

Run this manually:
```sql
CREATE EXTENSION vector;

CREATE TABLE IF NOT EXISTS data (
    id SERIAL PRIMARY KEY,
    document_text TEXT,
    embedding vector(384)
);

```