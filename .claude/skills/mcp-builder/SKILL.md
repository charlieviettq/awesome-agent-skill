---
name: mcp-builder
description: "Design and implement MCP servers—tools, resources, prompts, schemas, and error contracts for agent clients. Use when adding MCP integration or exposing capabilities to Cursor/Claude agents."
allowed-tools: Read, Glob, Grep
---

# MCP builder

## Design principles

- **One capability per tool** — clear name, single purpose.
- **Strict schemas** — JSON Schema for inputs; document required vs optional.
- **Predictable errors** — machine-readable codes + human message; no stack traces to client by default.
- **Idempotent reads** — writes clearly labeled; confirm destructive ops in description.

## Server checklist

- [ ] `server` identity and version documented
- [ ] Tool list small and discoverable
- [ ] Input validation before side effects
- [ ] Timeouts and size limits on responses
- [ ] Auth documented (env vars, OAuth, local only)
- [ ] README: install, config, example tool calls

## Tool definition pattern

```json
{
  "name": "search_docs",
  "description": "Search internal docs by query. Read-only.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Search terms" },
      "limit": { "type": "integer", "minimum": 1, "maximum": 50 }
    },
    "required": ["query"]
  }
}
```

## Testing

- Unit test handlers with fixture inputs.
- Integration test with MCP client or inspector.
- Verify error paths (invalid args, upstream failure).

## Security

- No broad filesystem or shell unless required and scoped.
- Sanitize paths; block path traversal.
- Do not return secrets in tool results.

## Related

Use `agent-tool-contracts` for cross-platform tool design beyond MCP.
