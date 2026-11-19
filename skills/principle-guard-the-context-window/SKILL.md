---
name: principle-guard-the-context-window
description: "Use when handling large outputs, planning fan-out, or choosing delegate history. Delegate bulk reading, keep summaries in the main thread, and limit delegate history to the assignment."
---

# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Bound delegate history.** Follow [Delegation](../mode/references/delegation.md#choose-whether-to-resume-a-delegate) when deciding which conversation a delegate needs.
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
