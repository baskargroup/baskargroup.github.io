---
name: add-product
description: Scaffold a product file (software, app, dataset, model, service) and validate its keys (PLAN.md Section 7).
---

# add-product

Skeleton (implemented in Phase 4). From `$ARGUMENTS`:

1. Create `_products/<slug>.md` with front matter: `title`, `type`, `status`, `blurb` (<= 160 chars), `links`, `image`, `themes`, `papers` (bibkeys), `people` (slugs), `metrics`.
2. Validate that every theme, bibkey, and person key resolves. Use `TODO(baskar)` for unknown links; never invent URLs.

Owns: `_products/`.

Run `make validate`, then open a PR. Never push to main. Touch only the files this workflow owns.
