---
name: add-impact-story
description: Scaffold and draft an impact story for the public or policy makers (PLAN.md Section 9).
---

# add-impact-story

Skeleton (implemented in Phase 5). From `$ARGUMENTS`:

1. Create `_impact/<slug>.md` with front matter: `title`, `hero` (image), `audience` (public, policy, or both), `related` (papers, products, themes), `order`.
2. Draft the body per Section 9 style: 150-250 words, problem then what we built then who benefits then at what scale, roughly 9th-grade reading level, one visual, ends with 2-4 links. All numbers are `TODO(baskar)` until confirmed. No em or en dashes.

Owns: `_impact/`.

Run `make validate`, then open a PR. Never push to main. Touch only the files this workflow owns.
