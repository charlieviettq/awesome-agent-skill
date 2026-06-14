# SpecBot — RFQ Demo Playbook

30-minute sales demo using **one real RFQ PDF** (redacted). No custom code required before the call.

## Pre-demo checklist

- [ ] RFQ PDF redacted: customer name, prices, PII removed
- [ ] Sample KB: 3–5 product spec sheets (PDF/DOCX) in demo folder — **not committed to git**
- [ ] `specbot-demo` bundle installed locally
- [ ] Screen share: Cursor + trace panel / notes doc ready

## Demo flow (30 min)

| Min | Step | Agent prompt (example) | Expected output |
|-----|------|------------------------|-----------------|
| 0–3 | Intro | — | Problem: slow RFQ, no trace |
| 3–8 | Ingest | "Read this RFQ PDF and list required spec fields as a table" | Field list with page refs |
| 8–14 | Gap analysis | "Compare RFQ fields to our KB; flag missing or ambiguous items" | Gap table + clarifying questions |
| 14–22 | Draft response | "Draft a professional RFQ response email in Vietnamese; mark assumptions" | Draft email + assumption list |
| 22–27 | Trace review | "Summarize sources used and what a human must verify" | Trace checklist |
| 27–30 | Close | — | Pilot scope, pricing, next steps |

## Expected artifacts (show live)

1. **Spec extraction table** — field, value, source page, confidence
2. **Clarifying questions** — bullet list for customer follow-up
3. **Draft response** — email-ready, not sent automatically
4. **Trace checklist** — human sign-off items

## Redaction rules

| Remove | Keep |
|--------|------|
| Customer legal name | Product category |
| Contact phone/email | Technical requirements |
| Exact pricing | Quantity bands (ranges OK) |
| Bank / tax IDs | Delivery region |

Store demo RFQs in `tenants/<codename>/samples/` — **gitignored**.

## Objection handling

| Objection | Response |
|-----------|----------|
| "AI will hallucinate specs" | Trace + human review gate; pilot metrics on extraction accuracy |
| "We use Zalo not email" | Phase 1 semi-auto paste; Phase 2 webhook after pilot |
| "Too expensive" | ROI: hours saved × RFQ volume; start smaller KB scope |

## Post-demo

- [ ] Send one-pager + SpecBot offer sheet (PDF, no repo link)
- [ ] Schedule pilot kickoff if qualified
- [ ] Log in [GTM weekly board](../gtm/weekly-board.md)

## Skills used (bundle `specbot-demo`)

- `writing-docs/pdf` — RFQ read
- `core-workflow/spec-driven-development` — structured output
- `core-workflow/clarify-underspecified` — gap questions
- `knowledge-work/sales/draft-outreach` — response draft
- `core-workflow/verify-before-done` — trace checklist
