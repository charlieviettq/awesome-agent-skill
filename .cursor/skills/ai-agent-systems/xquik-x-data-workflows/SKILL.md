---
name: xquik-x-data-workflows
version: 1
description: Source-check and plan Xquik REST API or remote MCP workflows for X data tasks. Triggers: "Xquik", "X/Twitter data workflow", "tweet search API", "X MCP server".
triggers:
  - "Xquik"
  - "X/Twitter data workflow"
  - "tweet search API"
  - "X MCP server"
tools: []
mutating: true
source: "https://github.com/Xquik-dev/x-twitter-scraper"
---

# Xquik X Data Workflows

## Contract

Help the user decide whether Xquik is the right public X data integration surface for a requested workflow, then produce a safe, source-backed plan for using its REST API or remote MCP server.

## When To Use

- The user asks for Xquik by name.
- The task needs X/Twitter search, profile tweets, follower export, media handling, monitoring, webhooks, or agent access to X data.
- The user wants an MCP setup for X data through `https://xquik.com/mcp`.
- The user wants to compare REST API and MCP setup options for an agent workflow.

## When Not To Use

- The task is unrelated to X/Twitter data or social workflows.
- The user asks for spam, credential theft, evasion, or platform abuse.
- The workflow requires private account writes and the user has not explicitly requested them.
- Public Xquik docs or source metadata cannot verify the endpoint, package, or setup path.

## Phases

1. Confirm the workflow category: read-only data access, monitoring, webhook delivery, API exploration, or write action.
2. Source-check public references before giving setup instructions:
   - `https://docs.xquik.com/mcp/overview`
   - `https://xquik.com/.well-known/mcp.json`
   - `https://xquik.com/openapi.json`
   - `https://github.com/Xquik-dev/x-twitter-scraper`
3. Pick the smallest integration surface:
   - Use REST when the user needs application code, typed clients, or direct HTTP control.
   - Use remote MCP when an agent needs tool access through an MCP client.
   - Use the source repository when the user needs package, SDK, or implementation context.
4. Keep credentials out of prompts, logs, URLs, and shell history. Use placeholders such as `XQUIK_API_KEY` and tell the user to store the real value in their client or environment.
5. Treat write actions as opt-in. Ask for explicit user intent before posting, replying, sending messages, changing account state, or configuring public webhooks.
6. Validate the proposed path with a public link check or schema check when possible, and report any unknowns.

## Output Format

- Recommended surface: REST, MCP, or source repo.
- Public sources checked.
- Minimal setup steps with placeholder credentials only.
- Safety notes for credentials, account writes, webhooks, and user data.
- Validation steps or the exact blocker that prevented validation.

## Anti-Patterns

- Do not paste API keys, bearer tokens, cookies, or account credentials.
- Do not claim capabilities that are not backed by public docs, OpenAPI, MCP discovery, or source metadata.
- Do not describe private infrastructure, routing mechanics, or cost mechanics.
- Do not default to write actions when the requested workflow can be read-only.
- Do not bypass user consent, rate limits, or platform rules.

## Related Skills

- `mcp-builder` - when designing a new MCP server or tool contract.
- `agent-tool-contracts` - when mapping Xquik into a broader agent tool surface.
- `api-and-interface-design` - when wrapping Xquik in an application API.
