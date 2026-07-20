---
name: graduate-member
description: Flip a member to alumni, add placement, and draft a graduation win (PLAN.md Section 8).
---

# graduate-member

Skeleton (implemented in Phase 4). From `$ARGUMENTS`:

1. In `_people/<slug>.md`, set `role: alumni`, add `end` and `placement`.
2. Draft a `_news/` graduation win via the add-win pattern, with placement as `TODO(baskar)` if unconfirmed.

Owns: `_people/`, `_news/`.

Run `make validate`, then open a PR. Never push to main. Touch only the files this workflow owns.
