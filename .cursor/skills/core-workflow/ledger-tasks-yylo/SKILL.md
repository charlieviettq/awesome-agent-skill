---
name: ledger-tasks-yylo
description: >
  Run a persistent, dependency-aware task board for coding agents with YYLO
  Ledger: create, list, search, update, and mark tasks, manage blockers, and
  derive safe execution order from the command line.
  Triggers: "kanban", "task board", "YYLO", "ledger tasks", "blocked by",
  "task dependencies", "run tasks".
---

# YYLO Ledger Tasks

Use this skill when a coding agent needs durable task tracking with dependencies instead of an ad-hoc todo list. YYLO Ledger stores tasks in the repository, so board state survives across sessions, agents, and worktrees.

## When to use

- Plan multi-step work as tracked tasks with statuses, tags, and dependencies.
- Pick the next safe task from blockers instead of guessing.
- Record progress and outcomes on each task with explicit responses.
- Search or review the board when context is lost.

## When not to use

- One-shot questions with no persisted workflow state.
- Team-hosted trackers (Jira, Linear) that are already the source of truth.
- Archive maintenance or production mutations; those require separate explicit authorization.

## Workflow

1. Install the YYLO CLI once, then inspect the board:

```bash
npm install --global @yylo/cli@latest
yy ledger list --limit 10
```

2. Create small, completable tasks with optional tags and blockers:

```bash
yy ledger create "Add retry to upload client" --status todo --tags backend,reliability
yy ledger deps add --id TASK_ID --blocked-by BLOCKER_ID
```

3. Pick work that is actually unblocked:

```bash
yy ledger ready
yy ledger order --scores
```

4. Work one task at a time and mark progress with a response:

```bash
yy ledger mark in_progress --id TASK_ID --response "Starting: isolating flaky test"
yy ledger mark done --id TASK_ID --response "Done: retried with backoff, tests green" --commit abc123
```

5. Search and inspect when resuming:

```bash
yy ledger search --status todo --tag backend --limit 10
yy ledger get TASK_ID
```

Status flow: `backlog -> todo -> in_progress -> done` (or `archive` for abandoned tasks). Dependencies can also be declared inline in task bodies with `[blocked_by]ID[/blocked_by]` and `[task_id]ID[/task_id]` markup, parsed on create and update.

## Output

A repository-backed task board whose state (statuses, responses, commits, dependency graph) is queryable by any agent session; unblocked sets via `ready` and safe parallel execution order via `order`.

## Related skills

- `planning-and-task-breakdown` — break a spec into tasks before tracking them here.
- `verify-before-done` — verify results before marking tasks done.
