# SpecBot — Offer Sheet

**Product:** SpecBot (SpecFlow AI P1)  
**Status:** Pilot-ready

## One-liner

AI-assisted RFQ/spec workflow: ingest PDF → extract requirements → map to your KB → draft response with full trace for human approval.

## Pricing

| Component | Range (VND) |
|-----------|-------------|
| Setup (one-time) | 30–80M / tenant |
| SaaS (monthly) | 5–15M / tenant |
| DocFlow Pack upsell | +10–25M setup |

Setup scales with: KB size, number of spec templates, integration complexity (Zalo vs email-only).

## Setup scope (included)

1. **KB ingest** — up to 500 documents (PDF, DOCX, Confluence export)
2. **Spec mapping** — field dictionary aligned to your RFQ format
3. **Integration phase 1** — email forward + Zalo webhook or manual paste workflow
4. **Trace** — log of agent steps, sources cited, human edit diff
5. **Training** — 2h session for sales/ops reviewers

## SaaS scope (included)

- Hosted agent runtime (or customer VPC option — quote separately)
- Trace retention 90 days
- KB update quota: 50 documents/month
- Monthly health report (extraction accuracy, turnaround time)

## Exclusions (quote separately)

- ERP/CRM bi-directional sync
- Unlimited KB without quota
- 24/7 on-call
- Custom model fine-tuning
- Storing customer PII in SpecFlow repos

## Pilot success criteria

| Metric | Target |
|--------|--------|
| RFQ turnaround | ≥30% faster vs baseline |
| Field extraction | ≥80% on pilot set (≥5 RFQs) |
| Reviewer satisfaction | ≥4/5 on trace clarity |

## Delivery timeline

| Week | Milestone |
|------|-----------|
| 0 | Signed SOW, redacted sample RFQs |
| 1 | KB ingest + spec map draft |
| 2 | Integration + internal demo |
| 3 | Pilot with 3–5 live RFQs |
| 4 | Go/no-go for SaaS |

## Artifacts delivered

- Spec field dictionary (CSV/JSON)
- Review checklist
- Trace export template
- Runbook for sales reviewers

## Sales assets

- [Demo RFQ playbook](../sales/demo-rfq-playbook.md)
- [Tenant onboarding](../specbot/tenant-onboarding.md)
