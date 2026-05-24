---
name: postmortem-writing
description: >
  Write blameless incident postmortems—timeline, impact, root cause, contributing
  factors, and actionable follow-ups. Use after outages, SEV incidents, or
  significant near-misses.
  Triggers: "postmortem", "incident review", "RCA", "blameless", "SEV".
---

# Postmortem writing

## Principles

- **Blameless** — focus on systems and process, not individuals.
- **Accurate** — timeline in UTC with evidence (logs, deploys, tickets).
- **Actionable** — every finding maps to owner + due date or ticket.

## Required sections

1. **Summary** — what happened, duration, user/business impact
2. **Timeline** — detection, escalation, mitigation, recovery
3. **Root cause** — technical chain; distinguish trigger vs underlying gap
4. **Contributing factors** — process, monitoring, dependency, change management
5. **What went well**
6. **Action items** — prevent recurrence, improve detection, reduce blast radius

## Timeline table

| Time (UTC) | Event |
|------------|-------|
| ... | Alert fired |
| ... | Mitigation applied |
| ... | Service restored |

## Action item quality

| Weak | Strong |
|------|--------|
| "Be more careful" | "Add alert on queue depth > X with runbook" |
| "Improve testing" | "Integration test for failover path in service Y" |

## Severity-appropriate depth

- SEV1/2: full postmortem + review meeting.
- SEV3/4: lightweight doc still with timeline and actions.

## Template

See [reference.md](reference.md) for full markdown template.

## Follow-up

Track action items to closure; link superseding ADRs or runbook updates.
