# External Memory Specification
Store: SQLite (schema: id, key text, content, embedding blob, metadata JSON, created_at, source, score). Components: database, embeddings, retriever, ranker, controller.
Operations: write, search (top-k), rank, read-into-model (gated), forget/expire. Vector index only if SQLite scan becomes the bottleneck (documented measurement).
Evaluation: retrieval accuracy, context retention, effect on downstream tasks, latency. Memory must be ablatable (flag off = pure model).
API: `/memory/search`, `/memory/write`.
