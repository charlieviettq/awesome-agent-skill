# SpecFlow AI

**Private commercial workbench — not public distribution.**

Local path: `~/Documents/OtherProject/personal-research/specflow-ai`

SpecFlow AI packages agent skill workflows for B2B teams: RFQ/spec automation (SpecBot), DS/ops skill bundles (DataAgent Kit), and document ops add-ons (DocFlow Pack).

Built on the open-source [awesome-agent-skill](https://github.com/charlieviettq/awesome-agent-skill) skill library.

## Brand

| Product | Role |
|---------|------|
| **SpecFlow AI** | Master brand |
| **SpecBot** | P1 — RFQ/spec PDF → structured response + trace |
| **DataAgent Kit** | P2 — Cursor skill bundles for data teams |
| **DocFlow Pack** | P3/P4 — SOP, Confluence, sales training |

## Quick links

- [Business model](docs/business-model.md)
- [SpecBot offer](docs/offers/specbot.md)
- [DataAgent Kit offer](docs/offers/dataagent-kit.md)
- [DocFlow Pack](docs/offers/docflow-pack.md)
- [Module packs pricing](docs/offers/module-packs.md)
- [RFQ demo playbook](docs/sales/demo-rfq-playbook.md)
- [Outreach playbook](docs/sales/outreach-playbook.md)
- [Tenant onboarding](docs/specbot/tenant-onboarding.md)
- [GTM weekly board](docs/gtm/weekly-board.md)
- [Guardrails & boundaries](docs/guardrails.md)

## Sync from public upstream

```bash
bash scripts/sync-from-upstream.sh
python3 scripts/skillhub.py sync
```

## Install commercial bundles

```bash
skillhub install-bundle specbot-demo . --format cursor
skillhub install-bundle dataagent-pro . --format cursor
skillhub install-bundle docflow-pack . --format cursor
```

## License

- Open-source skills inherited from upstream: MIT
- Commercial docs, playbooks, and tenant templates: proprietary — do not redistribute
