---
name: rag-systems
description: "Design retrieval-augmented generation pipelines—chunking, embeddings, retrieval, reranking, grounding, and evaluation. Use when building or improving doc Q&A, code search agents, or knowledge bases."
allowed-tools: Read, Glob, Grep
---

# RAG systems

## Pipeline stages

1. **Ingest** — parse, clean, preserve structure (headings, tables).
2. **Chunk** — size/overlap tuned to content type; keep metadata (source, section).
3. **Embed** — consistent model; version stored with index.
4. **Retrieve** — hybrid (keyword + vector) when recall matters.
5. **Rerank** — optional cross-encoder for top-k precision.
6. **Generate** — cite sources; refuse when context insufficient.

## Chunking heuristics

| Content | Guidance |
|---------|----------|
| Docs | Split on headings; 300-800 tokens typical |
| Code | Function/class level; include path in metadata |
| Tables | Row batches or markdown table blocks |

## Quality checks

- [ ] Retrieval hit rate on golden questions
- [ ] Answer grounded in retrieved chunks (no hallucinated citations)
- [ ] Latency budget per query documented
- [ ] Index refresh process defined

## Failure modes

| Issue | Mitigation |
|-------|------------|
| Missed relevant doc | Hybrid search, query expansion, metadata filters |
| Wrong chunk | Smaller chunks, reranker, parent-child retrieval |
| Stale index | Version tag, scheduled re-embed |
| Prompt overflow | Summarize chunks, dynamic top-k |

## Evaluation

- Golden Q&A set with expected source doc/section.
- Metrics: recall@k, answer correctness, citation accuracy.
- Regression when changing embed model or chunk strategy.

## Security

- Respect ACLs at retrieval time; do not leak cross-tenant data in shared indexes.
