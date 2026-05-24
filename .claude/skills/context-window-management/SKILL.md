---
name: context-window-management
description: "Manage LLM context budgets—prioritization, summarization, compaction, and what to load vs reference. Use for long sessions, large repos, or multi-doc tasks."
allowed-tools: Read, Glob, Grep
---

# Context window management

## Lifecycle

| Phase | Action |
|-------|--------|
| Bootstrap | Load spec, constraints, key paths only—not whole repo |
| During task | Append deltas; replace full file reads with summaries after use |
| Before compaction | Write `Session state` block (objective, done, open, paths) |
| Session end | Drop tool noise; keep decisions and verification evidence |

## Strategy order

1. **Do not load** — use search/read targeted files only.
2. **Reference** — pointers (paths, line ranges) instead of full paste.
3. **Summarize** — compress completed work; keep decisions and open items.
4. **Drop** — remove obsolete tool output and duplicated content.

## What to keep in active context

- Current objective and acceptance criteria
- Constraints (env, versions, "do not touch")
- Recent errors and fixes
- Open questions

## What to offload

- Full file contents already summarized
- Long command outputs (keep exit code + last N lines)
- Exploratory branches that did not ship

## Compaction pattern

```text
## Session state (compacted)
Objective: ...
Done: ...
Open: ...
Key paths: ...
Do not repeat: [list already-established facts]
```

## Multi-file work

- Load one module at a time when possible.
- Prefer ripgrep/semantic search over dumping trees.
- For RAG: retrieve only top-k relevant chunks.

## Anti-patterns

- Pasting entire repos or logs into chat.
- Re-explaining architecture every turn without delta.
- Keeping failed attempts at full length after resolution.

## Session setup (context engineering)

Before long tasks, establish a minimal working set:

1. **Objective block** — one paragraph: goal, non-goals, done-when
2. **Constraint block** — versions, env, files off-limits
3. **Reference map** — paths to spec, ADR, or ticket; load on demand
4. **Tool policy** — which tools/skills apply; avoid loading unused skill bodies

Refresh the objective block after major pivots; do not re-paste full history.

## Pairing

Use with `rag-systems` for external knowledge; `clarify-underspecified` when scope grows mid-session; `interview-me` before loading large specs.
