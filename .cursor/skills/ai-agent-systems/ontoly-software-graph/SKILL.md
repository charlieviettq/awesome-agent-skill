---
name: ontoly-software-graph
description: >
  Use Ontoly's deterministic Software Graph and MCP capabilities for repository
  architecture, request tracing, dependency analysis, and impact analysis before
  falling back to direct source search. Triggers: "Ontoly", "Software Graph",
  "trace request", "impact analysis", "dependency graph".
---

# Ontoly Software Graph

Use this skill when a coding agent needs graph-backed software understanding from Ontoly before searching repository files directly.

Ontoly builds a deterministic Software Graph for TypeScript repositories and exposes the result through CLI queries, MCP capabilities, validation reports, and agent skills. This skill teaches workflow only; Ontoly is the source of truth.

## When to use

- Explain repository architecture, packages, modules, services, routes, controllers, or ownership.
- Trace a request, route, controller, service, provider, dependency, or call chain.
- Estimate impact for removing, renaming, or refactoring a symbol, module, package, route, or service.
- Review graph diagnostics, unresolved imports, circular dependencies, dead code, configuration usage, or environment variable usage.

## When not to use

- The repository has no Ontoly installation and the user does not want local graph artifacts.
- The user explicitly asks for a manual source review without graph assistance.
- The graph is stale, untrusted, or missing the semantic concept needed for the answer and cannot be rebuilt.

## Workflow

1. Check for Ontoly artifacts such as `.ontoly/`, `SoftwareGraph.json`, graph reports, validation output, or documented Ontoly scripts.
2. If the graph is missing and local output is acceptable, run `ontoly build .`.
3. Review diagnostics, trust, semantic coverage, framework detection, graph hash, and validation status before making claims.
4. Prefer Ontoly CLI or MCP capabilities for architecture summaries, request tracing, dependency analysis, configuration lookup, framework reports, and impact analysis.
5. Inspect source files only when Ontoly cannot answer, the graph is incomplete, or the user asks for source-level verification.
6. Rebuild the graph after meaningful repository changes before answering current-state questions.

## Output

Answer with:

- The relevant graph nodes, edges, packages, routes, diagnostics, or query outputs.
- A clear split between measured graph facts and inference.
- Confidence based on graph evidence, diagnostics, and coverage.
- A narrow fallback explanation when direct file inspection was needed.

## Related skills

- `mcp-builder` - when designing or validating MCP server capabilities.
- `agent-tool-contracts` - when reviewing agent-facing CLI or tool schemas.
- `agent-evaluation` - when measuring whether graph-backed answers improve agent behavior.
