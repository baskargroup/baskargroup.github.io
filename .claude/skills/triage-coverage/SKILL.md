---
name: triage-coverage
description: Triage coverage inbox candidates (press, blog, social) into the rendered coverage list (PLAN.md Section 10.2).
---

# triage-coverage

Skeleton (implemented in Phase 7). For each item in `_data/coverage_inbox.yml`:

1. Fetch the item and keep only those genuinely about the group.
2. Set `kind` (press, blog, social), `author_person`, and `papers`; write a one-line `note`.
3. Move keepers to `_data/coverage.yml`; clear the inbox.
4. PR body lists keepers and dropped items, one line each, for a quick mobile skim.

Owns: `_data/coverage.yml`, `_data/coverage_inbox.yml`.

Run `make validate`, then open a PR. Never push to main. Touch only the files this workflow owns.
