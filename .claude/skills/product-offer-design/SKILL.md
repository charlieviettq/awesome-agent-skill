---
name: product-offer-design
description: "Package workflows and capabilities into clear product offers—audience, outcome, scope, and delivery format. Neutral framing without fixed pricing dogma."
allowed-tools: Read, Glob, Grep
---

# Product Offer Design

Turn repeatable agent or engineering workflows into describable offers for clients, internal teams, or open-source products. Distinct from `product-analytics-experiments` (metrics) and `idea-refine` (early brainstorming).

## When to use

- Packaging a skill bundle or service line
- Defining MVP scope for a tool or template
- Clarifying what is in/out of a deliverable

## When not to use

- Detailed financial modeling or legal contracts
- Running growth experiments (use `product-analytics-experiments`)

## Workflow

1. **Audience** — who benefits; job-to-be-done in their words
2. **Outcome** — measurable result (time saved, error reduced, artifact produced)
3. **Scope** — included workflows, support level, exclusions
4. **Format** — template, repo, managed service, workshop
5. **Proof** — demo, case snippet, or checklist showing delivery
6. **Risks** — dependencies, maintenance burden, support load

## Offer canvas

```markdown
## Offer: [name]
- **For:** 
- **Problem:**
- **Promise:** (one sentence)
- **Includes:**
- **Excludes:**
- **Delivery:**
- **Success signal:**
- **Maintenance owner:**
```

## Principles

- One primary outcome per offer; upsells are separate
- Scope exclusions prevent scope creep
- Prefer assets that compound (docs, skills, templates) over one-off labor
