---
name: agent-tool-contracts
description: "Design agent tools and CLI surfaces—schemas, naming, errors, idempotency, and discoverability for LLM callers. Use when defining tools for agents, SDKs, or AI-native CLIs."
allowed-tools: Read, Glob, Grep
---

# Agent tool contracts

## Tool design rules

1. **Verb-noun names** — `search_issues`, `create_draft_pr` (not `doStuff`).
2. **Minimal parameters** — fewer required fields; sensible defaults in description.
3. **Explicit side effects** — "Creates...", "Deletes...", "Read-only" in description.
4. **Bounded output** — paginate or truncate; return summary + pointer for large data.
5. **Stable errors** — `{ "code": "NOT_FOUND", "message": "..." }`.

## Schema quality

- Types and enums for categorical fields.
- Examples in parameter descriptions.
- Reject unknown enums at validation layer.

## Idempotency and safety

| Operation | Pattern |
|-----------|---------|
| Read | Safe to retry |
| Create | Idempotency key or dedupe by natural key |
| Update | Version or ETag when concurrent edits possible |
| Delete | Soft delete or two-step confirm in description |

## AI-native CLI (when applicable)

- `--json` for machine output; stable field names.
- Exit codes: 0 success, non-zero with stderr message.
- `--dry-run` for mutating commands.

## Review checklist

- [ ] Description tells the model when NOT to use the tool
- [ ] Errors actionable (what to fix, not internal codes only)
- [ ] No overlapping tools with ambiguous choice
- [ ] Integration test with representative agent prompts

## Related

`mcp-builder` for MCP-specific packaging; `agent-evaluation` for measuring tool accuracy.
