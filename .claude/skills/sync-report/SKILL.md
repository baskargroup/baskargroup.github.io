---
name: sync-report
description: Summarize open automation PRs and pending TODO(baskar) markers across the repo (PLAN.md Section 12.4).
---

# sync-report

Skeleton (implemented in Phase 7). Read-only reporting workflow:

1. List open automation PRs (paper sync, coverage watch) and their status.
2. Scan the repo for `TODO(baskar)` and `needs-review` markers and group them by area.
3. Produce a short checklist for Baskar. Opens no PR unless asked; changes no content.

Owns: nothing (reporting only).

Run `make validate` if it touches any file. Never push to main.
