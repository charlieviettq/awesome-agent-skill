# SpecBot — Tenant Onboarding

Checklist for new SpecBot tenant after signed SOW. **Do not commit tenant data to git.**

## Prerequisites

- [ ] SOW signed (setup fee + SaaS terms)
- [ ] Tenant codename assigned (e.g. `tenant-npp-alpha`)
- [ ] `tenants/<codename>/` created locally — **gitignored**
- [ ] SpecBot demo completed; pilot RFQs identified (≥3)

## Week 1 — Discovery & KB

| Task | Owner | Artifact |
|------|-------|----------|
| Kickoff call | Delivery | Meeting notes in `tenants/<codename>/notes/` |
| Collect KB exports | Customer | PDF/DOCX/Confluence → `samples/kb/` |
| Collect 3–5 sample RFQs | Customer | Redacted → `samples/rfq/` |
| Spec field workshop | Delivery | `spec-dictionary.csv` |
| Integration choice | Both | Email forward / Zalo manual / webhook (phase 2) |

## Week 2 — Mapping & integration

| Task | Owner | Artifact |
|------|-------|----------|
| Build spec dictionary | Delivery | Fields: name, type, required, KB source |
| Map KB chunks to fields | Delivery | `kb-mapping.json` |
| Configure trace format | Delivery | JSONL schema + summary template |
| Phase 1 integration | Delivery | Forward address or paste workflow doc |
| Internal QA | Delivery | 2 RFQs processed end-to-end |

## Week 3 — Pilot

| Task | Owner | Artifact |
|------|-------|----------|
| Train reviewers (2h) | Delivery | Slide deck + checklist |
| Process 3–5 live RFQs | Customer + agent | Trace logs per RFQ |
| Measure turnaround | Delivery | Baseline vs pilot table |
| Extraction accuracy review | Both | Field-level scorecard |

## Week 4 — Go-live

| Task | Owner | Artifact |
|------|-------|----------|
| Go/no-go meeting | Both | Pilot report |
| SaaS billing start | Ops | Invoice |
| KB update quota documented | Delivery | 50 docs/mo default |
| Escalation contact | Both | Shared doc |

---

## Integration contracts (phase 1)

### Email

- Customer forwards RFQ to `rfq+<codename>@specflow.local` (or shared inbox)
- Agent processes from attachment; draft returned to reviewer inbox
- **No auto-send** without human approval

### Zalo (semi-automated)

- Reviewer pastes RFQ text or PDF extract into Cursor session
- Agent outputs draft; reviewer copies to Zalo manually
- Phase 2: official OA webhook — separate SOW

---

## Trace requirements

Each RFQ run must log:

1. Input hash (not raw PII in shared logs)
2. Fields extracted + source doc/page
3. Assumptions and gaps
4. Draft version + reviewer edits
5. Final approval timestamp + approver initials

Template: `tenants/_templates/trace-entry.json`

---

## KB update quota (SaaS)

| Tier | Docs/month | Overage |
|------|------------|---------|
| Standard | 50 | Quote per 10 docs |
| Growth | 150 | Quote per 25 docs |

---

## Handoff to DocFlow (optional upsell)

If customer needs SOP for reviewers → propose [DocFlow Pack](../offers/docflow-pack.md).
