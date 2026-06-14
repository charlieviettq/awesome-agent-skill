# Public / Private Repo Split

Strategy for separating open-source lead-gen from commercial delivery under **SpecFlow AI**.

## Repositories

| Repo | Name | Role |
|------|------|------|
| Public | [`awesome-agent-skill`](https://github.com/charlieviettq/awesome-agent-skill) | Trust, SEO, marketplace, free skills, install CLI |
| Private | `specflow-ai` | Pricing, pilot kits, tenant playbooks, Pro bundles, GTM |
| Local path | `~/Documents/OtherProject/personal-research/specflow-ai` | Personal research workspace (not under CakeProjects) |

**Tagline:** SpecFlow AI — private AI workflow packs built on awesome-agent-skill.

## Brand architecture

| Brand | Type | Description |
|-------|------|-------------|
| **SpecFlow AI** | Master brand | Commercial product line |
| **SpecBot** | P1 module | RFQ/spec PDF → structured response + trace |
| **DataAgent Kit** | P2 product | Cursor skill bundles for DS/ops teams |
| **DocFlow Pack** | P3/P4 add-on | SOP, Confluence, sales training |

## What stays public

- All open-source `SKILL.md` under `.cursor/skills/` and `.claude/skills/`
- Marketplace (`catalog/`) and registry metadata
- Bundle `dataagent-free` only (lead-gen)
- Demo-safe CTAs: “Book SpecBot demo”, “Request DataAgent Pro”
- Technical docs: skillhub CLI, skill writing guide, comparison, distribution (community)

## What lives in private (`specflow-ai`)

- `docs/business-model.md` — pricing, ICP, offer canvas
- `docs/offers/*` — SpecBot, DataAgent Pro, DocFlow, module packs
- `docs/sales/*` — RFQ demo playbook, outreach templates
- `docs/specbot/*` — tenant onboarding, KB mapping, integrations
- `docs/gtm/weekly-board.md` — execution tracker
- `docs/guardrails.md` — SLA, privacy, license boundaries
- Commercial bundles: `dataagent-pro`, `specbot-demo`, `docflow-pack`, `ops-trace-pack`
- Tenant-specific KB, RFQ samples (redacted), customer notes

## Sync model

```text
awesome-agent-skill (public) ──pull upstream──► specflow-ai (private)
specflow-ai ──merge back (selective)──► awesome-agent-skill
         only: dataagent-free, public-safe docs, non-sensitive improvements
```

1. **Private pulls from public** weekly or before each release: `scripts/sync-from-upstream.sh`
2. **Public never receives** pricing, sales scripts, tenant data, or Pro bundle definitions
3. Before any public merge from private, run the [public/private boundary checklist](../specflow-ai/docs/guardrails.md#publicprivate-boundary-checklist) in the private repo

## Bootstrap private repo

From this repo:

```bash
bash scripts/bootstrap-specflow-ai.sh
```

Creates **`~/Documents/OtherProject/personal-research/specflow-ai`** (override with `PERSONAL_RESEARCH` or first argument) with full git history copy and commercial docs overlay.

Then create GitHub private repo and push:

```bash
cd ~/Documents/OtherProject/personal-research/specflow-ai
git remote add origin git@github.com:charlieviettq/specflow-ai.git
git push -u origin main
```

## Contact CTAs (public-safe)

- SpecBot demo: LinkedIn DM or email (configure in README)
- DataAgent Pro: GitHub issue template or contact form on charlieviettq.github.io

Do not publish detailed pricing on the public repo.
