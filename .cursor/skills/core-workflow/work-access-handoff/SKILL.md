---
name: work-access-handoff
description: Explain and document work access layers—repo permissions, local vs cloud environments, handoff packages for collaborators. Triggers: "handoff", "access", "onboard collaborator", "share project", "where is the work".
---

# Work Access Handoff

Generic guide for transferring project context and access without platform lock-in. Helps collaborators find code, data boundaries, and environment setup.

## When to use

- Handing work to another developer or agent session
- Documenting where artifacts live (git, cloud, local)
- Reducing "where do I start?" friction

## When not to use

- Security access reviews (use team IAM process)
- Partner data agreements (use `ds-partner-boundaries` if available)

## Handoff checklist

### Code

- [ ] Repo URL and default branch
- [ ] Open PRs or WIP branches named
- [ ] How to run tests and dev server

### Access

- [ ] Required accounts (CI, cloud, analytics) listed by name
- [ ] Who grants access; no credentials in chat or repo
- [ ] `.env.example` documents required vars

### Artifacts

- [ ] Spec, ADR, or ticket links
- [ ] Model artifacts location (if ML)
- [ ] Design/mockup links

### State

- [ ] What is done vs in progress vs blocked
- [ ] Known risks and decisions already made
- [ ] Next recommended action

## Handoff note template

```markdown
## Handoff: [project/feature]
- **Repo:**
- **Branch/PR:**
- **Run locally:**
- **Access needed:** (request from X)
- **Key paths:**
- **Status:**
- **Next steps:**
```

## Safety

- Never paste tokens, passwords, or private URLs with embedded secrets
- Use team secret managers for credential transfer

## Related skills

- `interview-me` — clarify recipient needs
- `dynamic-config-management` — env documentation
- `verify-before-done` — confirm handoff recipient can run project

*Clean-room generic handoff workflow.*
