---
name: system-mapping
description: "Map systems with diagrams—components, data flows, feedback loops, and causal relationships. Use for architecture understanding or stakeholder communication."
allowed-tools: Read, Glob, Grep
---

# System Mapping

Lightweight system mapping before deep implementation or refactor. Produces diagrams and narrative that clarify boundaries and dependencies.

## When to use

- Onboarding to unfamiliar codebase or pipeline
- Planning integration between services
- Explaining credit/ML/data flows to stakeholders

## When not to use

- Formal ADR decision (use `architecture-decision-records`)
- Auto-generating code from diagram

## Workflow

1. **Scope** — system boundary; actors; in/out of scope
2. **Components** — services, stores, queues, humans, external APIs
3. **Flows** — primary happy path; note sync vs async
4. **Feedback** — loops, retries, batch vs realtime
5. **Risks** — single points of failure, PII paths, manual steps
6. **Diagram** — Mermaid or C4-style; keep readable in markdown

## Diagram tips

- Start context/container level; drill to component only where needed
- Label data classifications on flows with sensitive data
- Version diagram with date in doc title or footer

## Output template

```markdown
## System map: [name]
- **Purpose:**
- **Actors:**
- **Components:** (table: name, role, owner)
- **Primary flows:**
- **Diagram:** (mermaid block)
- **Open questions:**
```
