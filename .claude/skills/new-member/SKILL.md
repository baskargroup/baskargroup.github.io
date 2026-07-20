---
name: new-member
description: Scaffold a person file and add author name variants (PLAN.md Section 8).
---

# new-member

Skeleton (implemented in Phase 4). From `$ARGUMENTS`:

1. Create `_people/<slug>.md` with front matter: `name`, `role` (pi, postdoc, phd, ms, undergrad, staff, alumni), `photo`, `start`, links, opt-in `social`, `themes`, `coadvisors`.
2. Add the member's name variants to `_data/authors.yml` with `person: <slug>`.
3. Do not guess names, photos, or placements; use `TODO(baskar)`.

Owns: `_people/`, `_data/authors.yml`.

Run `make validate`, then open a PR. Never push to main. Touch only the files this workflow owns.
