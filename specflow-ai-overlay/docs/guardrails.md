# SpecFlow AI — Commercial Guardrails

Rules to sell confidently without over-promising or leaking tenant data.

## Data privacy

| Rule | Detail |
|------|--------|
| No tenant RFQ in git | Store under `tenants/<codename>/` — gitignored |
| No PII in trace exports shared externally | Hash or redact identifiers |
| KB stays in tenant boundary | Customer VPC or isolated storage option |
| Demo RFQs must be redacted | See [demo-rfq-playbook.md](sales/demo-rfq-playbook.md) |

Add to private repo `.gitignore`:

```gitignore
tenants/
*.rfq.pdf
samples/private/
```

## SLA & support (SaaS)

| Included | Not included |
|----------|--------------|
| Hosting + trace retention 90d | 24/7 on-call |
| KB quota per plan | Unlimited KB |
| Email support 48h business | Custom feature sprints in SaaS fee |
| Monthly health report | Guaranteed extraction % in contract without pilot data |

## Integration boundaries

| Phase | Scope |
|-------|-------|
| Phase 1 | Email forward, manual Zalo paste, human approval on all sends |
| Phase 2 | Zalo OA webhook, CRM read — separate SOW |
| Phase 3 | ERP sync — enterprise quote only |

Never promise Phase 2/3 at Phase 1 pricing.

## License / open-core

| Asset | License |
|-------|---------|
| Skills from awesome-agent-skill | MIT (upstream) |
| SpecFlow docs, playbooks, templates | Proprietary — private repo |
| Custom tenant skills | Customer owns content; SpecFlow retains playbook patterns |
| Pro bundle metadata | Commercial — distribute via invoice/release tarball only |

## Public/private boundary checklist

Before merging **private → public**:

- [ ] No pricing tables
- [ ] No sales scripts or outreach templates
- [ ] No tenant names, RFQ samples, or KB excerpts
- [ ] No commercial bundle definitions (`dataagent-pro`, `specbot-demo`, etc.)
- [ ] Only `dataagent-free` and demo-safe CTAs
- [ ] Reviewed by delivery lead

## Security review triggers

Run supply-chain / security checklist when:

- Adding MCP or webhook integrations
- Shipping new custom skills with scripts
- Onboarding tenant with VPC deploy

Use upstream [skill-supply-chain-audit](https://github.com/charlieviettq/awesome-agent-skill/tree/main/.cursor/skills/security-appsec/skill-supply-chain-audit) skill.

## Contract exclusions (standard)

- SpecFlow not liable for auto-sent messages without human review
- Customer responsible for accuracy of KB source documents
- AI outputs are drafts, not legal or binding quotes unless approved
- Data processing addendum required if PII processed in cloud

## Escalation

| Issue | Action |
|-------|--------|
| Wrong quote sent to customer | Pause automation; postmortem within 48h |
| KB leak suspicion | Rotate credentials; notify customer |
| Extraction <50% on pilot | Re-scope dictionary before SaaS go-live |
