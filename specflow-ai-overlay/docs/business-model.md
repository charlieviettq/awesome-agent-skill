# SpecFlow AI — Business Model

Source of truth for offers, pricing, and delivery scope. **Confidential — private repo only.**

## Overview

| Line | Priority | Model | Primary revenue |
|------|----------|-------|-----------------|
| P1 SpecBot | P0 | Hybrid productized service | Setup + SaaS retainer |
| P2 DataAgent Kit | P1 | Product-led growth | Pro subscription / one-time |
| P3/P4 Modules | P2 | Add-on / standalone setup | Setup fees |
| P5 Consumer | Backlog | Passion / affiliate | Slow, optional |

Public funnel: [awesome-agent-skill](https://github.com/charlieviettq/awesome-agent-skill) → free `dataagent-free` → demo/contact → private pilot.

---

## P1 SpecBot

### Offer canvas

| Field | Value |
|-------|-------|
| **For** | NPP / B2B sales & ops teams handling RFQ/spec PDFs (VN manufacturing, distribution) |
| **Problem** | RFQ response slow, inconsistent, missing trace; KB scattered across email/Zalo/Drive |
| **Promise** | Turn inbound RFQ PDF into structured spec map + draft response with human review trace in under 1 business day |
| **Includes** | KB ingest (≤500 docs initial), spec field mapping, Zalo/email connector (phase 1: semi-auto), trace log, 2h sales training |
| **Excludes** | Unlimited custom integrations, real-time ERP sync, 24/7 SLA, customer PII in repo |
| **Delivery** | 2–4 week setup + monthly SaaS |
| **Success signal** | ≥30% faster RFQ turnaround; ≥80% fields auto-extracted on pilot RFQs |
| **Maintenance owner** | SpecFlow delivery lead |

### Pricing

| Tier | Price (VND) | Notes |
|------|-------------|-------|
| Setup | 30–80M / tenant | KB ingest, spec mapping, integration |
| SaaS | 5–15M / month / tenant | Hosting, trace, KB update quota (e.g. 50 docs/mo) |
| Upsell | DocFlow Pack | See P3/P4 |

---

## P2 DataAgent Kit

### Offer canvas

| Field | Value |
|-------|-------|
| **For** | DS/analytics/ops teams using Cursor or Claude Code |
| **Problem** | Agents lack repeatable data workflows; every analysis starts from scratch |
| **Promise** | Install proven skill bundle for explore → query → analyze → validate → report in one command |
| **Includes** | Pro bundle install, update notes, optional workshop |
| **Excludes** | Custom model training, warehouse access, ongoing analysis labor |
| **Delivery** | Self-serve install + optional 1-day workshop |
| **Success signal** | Team installs bundle; ≥3 recurring workflows documented in 30 days |
| **Maintenance owner** | Product / community |

### Pricing

| Tier | Price | Notes |
|------|-------|-------|
| Free | $0 | 5 skills on GitHub (`dataagent-free`) |
| Pro | $29–99/mo or $199 one-time / team | `dataagent-pro` bundle + updates |
| Enterprise | 20–50M VND | Custom skill pack + install workshop |

---

## P3/P4 Module Packs

See [module-packs.md](offers/module-packs.md).

| Module | Standalone setup | Attach rule |
|--------|------------------|-------------|
| DocFlow Pack | 10–25M VND | Bundled discount with SpecBot |
| Custom Skill Pack | 15–30M VND | Requires discovery call |
| Ops Trace Pack | 10–20M VND | Recommended with SpecBot SaaS |
| Sales team training | 5–15M VND | Half-day workshop |

---

## P5 Consumer (backlog)

Affiliate booking, premium itinerary, local business listing — **no active GTM** until P1/P2 hit 3 paying tenants or 50 Pro seats.

---

## Revenue mix target (12 months)

| Source | Target share |
|--------|--------------|
| SpecBot setup + SaaS | 60% |
| DataAgent Pro / Enterprise | 25% |
| Module packs | 15% |

---

## ICP summary

**SpecBot:** 20–200 employee B2B, ≥10 RFQs/month, PDF/email-heavy, VN market first.

**DataAgent:** 5–50 person data/engineering team, already on Cursor, needs workflow standardization.

---

## Related docs

- [SpecBot offer](offers/specbot.md)
- [DataAgent Kit offer](offers/dataagent-kit.md)
- [DocFlow Pack](offers/docflow-pack.md)
- [Guardrails](guardrails.md)
