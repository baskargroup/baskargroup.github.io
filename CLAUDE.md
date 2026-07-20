# CLAUDE.md: Baskar Group website

Project memory for Claude Code. Loaded automatically every session. Keep it under one page.

## What this is

The Baskar Group website (Iowa State University), built on the al-folio Jekyll theme and served at `https://baskar-group.github.io`. The master spec is `docs/PLAN.md`; the pre-execution evaluation and amendments are in `docs/plan-evaluation.md`. Work strictly phase by phase (PLAN.md Section 14). The approved launch target is an MVP: Phases 0-4 plus a minimal homepage, then layer the rest.

## Golden rules

- PR only. Never push to `main`. Every change goes through a feature branch and a pull request, for humans, scripts, and Claude Code alike.
- Never fabricate. No invented papers, statistics, quotes, names, URLs, or numbers. When information is missing, insert a `TODO(baskar)` marker and list all such markers in the PR description.
- Discover, do not assume. al-folio evolves; inspect the actual files before relying on a path or layout name.
- Run `make validate` before opening any PR.
- Workflow skills touch only the files they own, run `make validate`, then open a PR.

## Source of truth (one file per content type)

| Content | Source of truth |
|---|---|
| Papers | `_bibliography/papers.bib` |
| Theme taxonomy | `_data/themes.yml` |
| Author name map | `_data/authors.yml` |
| People | `_people/<slug>.md` |
| Products | `_products/<slug>.md` |
| Impact stories | `_impact/<slug>.md` |
| Wins | `_news/YYYY-MM-DD-<slug>.md` |
| Coverage (press, blogs, posts) | `_data/coverage.yml` (candidates in `_data/coverage_inbox.yml`, never rendered) |
| Impact statistics | `_data/stats.yml` |
| Policy briefs | `_data/briefs.yml` + PDFs in `assets/pdf/briefs/` |

Pages reference keys (theme slug, bib key, person slug, product slug) and let templates resolve them. Never restate linked facts in free text.

## Style rules

- Plain-language paper summaries, 1-2 sentences, present tense, no jargon, no citations.
- Dash rule: no em-dashes or en-dashes in authored prose fields (`summary`, `note`, `blurb`, story, win, and impact body text, and authored `_data/*.yml` values). Imported bibliographic metadata (`title`, `author`, `journal`, `booktitle`, `venue`, `abbr`) is exempt and must never be altered. Enforced by `scripts/validate.py` on an allowlist of authored fields only.
- Images: WebP, 16:9 previews, alt text mandatory. Video: YouTube click-to-load with a poster; never commit video.

## Local development

- Ruby is Homebrew keg-only: add `/opt/homebrew/opt/ruby/bin` to `PATH`, or just use the `Makefile` targets, which do it for you.
- `make serve` builds and serves locally for private review. `make build` builds `_site`.
- `make json` / `make validate` / `make sync` run the Phase 2+ scripts (added in later phases).
- Local build has no Jupyter, so al-folio's demo notebook post was removed. The `jekyll-jupyter-notebook` plugin stays; GitHub CI has Jupyter for real notebooks.

## Workflow skills (added in later phases)

`enrich-papers`, `add-win`, `triage-coverage`, `add-mention`, `add-product`, `add-impact-story`, `new-member`, `graduate-member`, `sync-report`. See PLAN.md Section 12.4.

## Private, not committed

`docs/source/` holds Baskar's CV and Scholar export. It is gitignored. Do not publish or commit its contents.
