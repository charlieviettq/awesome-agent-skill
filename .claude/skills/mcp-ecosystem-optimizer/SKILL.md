---
name: mcp-ecosystem-optimizer
description: "Review and optimize MCP server setup—inventory, registry hygiene, config, versioning, and observability. Use when managing multiple MCP servers in Cursor or Claude."
allowed-tools: Read, Glob, Grep
---

# MCP Ecosystem Optimizer

Operational review of Model Context Protocol servers: what is installed, what is used, and how to reduce noise and risk. Complements `mcp-builder` (authoring servers) with consumer-side hygiene.

## When to use

- Slow or cluttered agent tool lists
- Debugging MCP connection failures
- Onboarding team to shared MCP config
- Auditing third-party MCP servers before enable

## When not to use

- Building a new MCP server (use `mcp-builder`)
- General agent eval (use `agent-evaluation`)

## Workflow

1. **Inventory** — list enabled servers, tools exposed, auth method
2. **Usage** — which tools actually get called; disable unused servers
3. **Config** — single source of truth (`.cursor/mcp.json` or team template); no duplicated entries
4. **Versioning** — pin server versions; document upgrade path
5. **Observability** — log tool errors; note latency outliers
6. **Security** — run `skill-supply-chain-audit` mindset: network scope, credential storage

## Optimization checklist

- [ ] Remove duplicate servers providing same capability
- [ ] Narrow tool allowlists where client supports it
- [ ] Document required env vars in `.env.example` (names only)
- [ ] Test each server with one representative tool call
- [ ] Separate dev vs prod MCP profiles if needed

## Anti-patterns

- Enabling every server from a registry "just in case"
- Storing API keys in committed config
- Platform-specific CLI wrappers that hide what tools run
