# P3/P4 Module Packs — Pricing Matrix

Standalone and attach pricing for SpecFlow AI modules. All prices VND unless noted.

## Matrix

| Module ID | Name | Standalone setup | Attach discount | Requires |
|-----------|------|------------------|-----------------|----------|
| `docflow-pack` | DocFlow Pack | 15–25M | 10–20M with P1/P2 | — |
| `ops-trace-pack` | Ops Trace Pack | 10–20M | 8–15M with SpecBot SaaS | SpecBot or self-hosted agent |
| `custom-skill-pack` | Custom Skill Pack | 15–30M | N/A | Enterprise discovery |
| `sales-training` | Sales team training | 5–15M | +5M with SpecBot | SpecBot pilot live |

## Custom Skill Pack

**For:** Teams needing domain-specific agent playbooks beyond public catalog.

**Includes:**
- 2h discovery (workflows, tools, constraints)
- 3–5 custom `SKILL.md` + reference files
- Validation via `validate-skills.py`
- Install handoff doc

**Excludes:** Ongoing skill maintenance (monthly retainer optional).

## Ops Trace Pack

**For:** Tenants needing audit trail, review gates, launch checklists.

**Includes:**
- `ops-trace-pack` bundle install
- Review rubric customization
- Trace log format (JSONL + human summary)

## Attach / standalone rules

1. **Standalone:** Customer has no SpecBot/DataAgent contract — full standalone price.
2. **Attach:** Active SpecBot setup or DataAgent Enterprise within 90 days — apply attach column.
3. **No stacking:** Max one attach discount per module per tenant.
4. **Scope cap:** Standalone setup ≤30M unless SOW signed for multi-module bundle.

## Upsell sequence (recommended)

```text
SpecBot pilot → DocFlow Pack → Ops Trace Pack → SaaS retainer
DataAgent Pro → Custom Skill Pack → Enterprise workshop
```

## Contract snippets

- Module SOW references master [business-model.md](../business-model.md)
- Exclusions per [guardrails.md](../guardrails.md)
- Payment: 50% start, 50% on acceptance for setup; SaaS monthly in advance
