---
name: add-mention
description: File a single coverage item from a URL or pasted text (PLAN.md Section 12.4). Handles login-walled items like LinkedIn posts.
---

# add-mention

Skeleton (implemented in Phase 7). From `$ARGUMENTS` (a URL, or pasted text plus a URL when the item is login-walled):

1. Fetch metadata when possible.
2. Set `kind`, `outlet` or author, `author_person` (if a member), `papers`, and a one-line `note`.
3. Append to `_data/coverage.yml`. LinkedIn is never scraped; social items enter only through this workflow.

Owns: `_data/coverage.yml`.

Run `make validate`, then open a PR. Never push to main. Touch only the files this workflow owns.
