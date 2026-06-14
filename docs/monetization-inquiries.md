# SpecFlow AI — Handling commercial inquiries (lite)

Lightweight process for the first 3–5 customers. No billing product required yet.

## Intake channels

| Product | Public intake | Private follow-up |
|---------|---------------|-------------------|
| SpecBot demo | [SpecBot demo issue](https://github.com/charlieviettq/awesome-agent-skill/issues/new?template=specbot-demo-request.yml) | SOW + invoice in specflow-ai private repo |
| DataAgent Pro | [Pro access issue](https://github.com/charlieviettq/awesome-agent-skill/issues/new?template=dataagent-pro-request.yml) | Manual tarball or Gumroad link |
| DocFlow / Ops add-on | DM after tenant kickoff | Quote from module packs |

## Response SLA (founder)

- **Issue opened:** acknowledge within 1 business day
- **SpecBot qualified:** offer 2 demo slots within 3 days
- **Pro inquiry:** send pricing + payment options within 2 days

## SpecBot — after demo

1. Send one-pager (no private repo link)
2. Pilot SOW: scope KB, RFQ volume, success metrics (see private `docs/offers/specbot.md`)
3. Payment: bank transfer / invoice PDF — 50% kickoff, 50% go-live
4. Kickoff: `docs/specbot/tenant-onboarding.md` in private repo

## DataAgent Pro — fulfillment

1. Confirm seats and use case
2. Payment option (pick one):
   - **Invoice** (VN teams): one-time USD/VND quote, email tarball + update channel
   - **Gumroad / Lemon Squeezy** (when live): link in issue reply
3. Deliver: `skillhub install-bundle dataagent-pro . --format cursor` from private specflow-ai checkout (license key / org allowlist TBD)

## Issue hygiene

- Label: `specflow-ai`, `specbot` or `dataagent`
- Close with reason: `won`, `lost`, `nurture`, `spam`
- Log weekly metrics in private `docs/gtm/weekly-board.md`

## Do not publish in public repo

- Exact VND/USD pricing tables
- Customer names, RFQ samples, tenant configs
- Gumroad product URLs until payment page is live (placeholder OK in private docs)
