---
name: add-win
description: Draft a news win (paper, preprint, grant, award, graduation, defense, milestone) from arguments and resolve entity links (PLAN.md Section 10.1).
---

# add-win

Skeleton (implemented in Phase 6). From `$ARGUMENTS` (type plus details):

1. Create `_news/YYYY-MM-DD-<slug>.md` with front matter: `date`, `type`, `title`, `people` (slugs), `links` (`bibkey`, `product`, `url`, any subset), optional `image`.
2. Resolve people slugs, bibkeys, and product slugs to existing files.
3. Keep prose plain and free of em and en dashes.

Owns: `_news/`.

Run `make validate`, then open a PR. Never push to main. Touch only the files this workflow owns.
