---
name: /reflect-yourself-queue
description: View pending learnings queue without processing.
---

# /reflect-yourself-queue - View Pending Learnings

View the queue of captured learnings without processing them.

---

## Instructions for Agent

1. Read the queue file at `~/.cursor/reflect-queue.json` (global location)
2. If the file doesn't exist or is empty, report "No pending learnings"
3. Display learnings in a **compact card-style list** (no wide tables — they cause horizontal scroll):

```markdown
## Pending Learnings Queue

**Total:** 2 pending learnings

---

### 1. [correction] Use prepared statements
**Date:** Jan 29 · **Confidence:** 0.85 · **Status:** pending

---

### 2. [preference] Prefer async/await over callbacks
**Date:** Jan 28 · **Confidence:** 0.80 · **Status:** pending

---
```

4. If there are learnings with `status: "applied"`, note that they can be cleaned up
5. Show age of oldest learning to encourage processing (e.g. "Oldest: 3 days")
6. **Ask questions (Cursor agent tool):** When items exist, use the **Ask questions** tool (message-question; Cursor docs → Agent overview → Tools): "Process queue now?" with options **Yes** (run `/reflect-yourself` to process) / **No** / **Discard all** (run `/reflect-yourself-skip`). If the tool is unavailable, present the options in text and wait for reply (e.g. yes / no / discard). Do not proceed without explicit user choice.