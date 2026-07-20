---
name: enrich-papers
description: Batch-enrich bib entries missing summary or themes (PLAN.md Section 6.5). Draft plain-language summaries and assign 1-3 taxonomy themes, 25 entries per PR.
---

# enrich-papers

Skeleton (implemented in Phase 3). For every `_bibliography/papers.bib` entry missing `summary` or `themes`:

1. Fetch the abstract via OpenAlex, then Crossref by DOI, then Semantic Scholar (AMEND-10). Many Elsevier venues lack abstracts; expect manual work.
2. Draft the summary per PLAN.md Section 4 style rules (1-2 sentences, plain language, present tense, no citations, no em or en dashes).
3. Assign 1-3 themes from `_data/themes.yml` only. If none fit, flag for review. Never invent a theme.
4. Do not alter titles, authors, venues, or years.

Batching: 25 entries per branch and PR. List each bibkey with its drafted summary and themes in the PR body. Wait for merge before the next batch.

Owns: `_bibliography/papers.bib`, `scripts/enrichment_pending.txt`, `assets/img/papers/`.

Run `make validate`, then open a PR. Never push to main. Touch only the files this workflow owns.
