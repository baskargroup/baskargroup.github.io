# Baskar Group website — status & resume note

**Last updated:** 2026-07-21 · **Last commit:** `003c034` · **Branch:** `main` (local only, not pushed anywhere)

This is the clean resume point. Read this first, then `CLAUDE.md`, then `docs/PLAN.md`
for the full spec. The site is built and reviewed **locally and privately** — nothing
is on GitHub yet, and it stays that way until Baskar says go live.

---

## TL;DR — where we are

- **MVP build in progress, local + private.** Phases 0-4 plus a minimal homepage are in place.
- **Design is FROZEN** (tag `design-freeze-2026-07-20`): amber/gold primary + cyan highlight,
  color-blind-safe (Baskar is red color blind). **Do not change colors, fonts, or the wordmark
  without an explicit request.** See memory `baskar-group-site-design-freeze`.
- **Publications pipeline is essentially done:** 344 publications (deduped from 374),
  **215 enriched** with plain-language summaries + theme tags.

---

## ⏳ In flight — waiting on Baskar / group members

1. **Member photos — first batch processed 2026-07-25** (branch `member-photos-links`). 11 new/updated
   photos landed (6 filled empty slots, 5 replaced low-res scraped versions). **Current members still
   without a photo (2):** meherpal-singh-bhatti, nicole-hayungs. When more
   arrive, follow **"Photo intake workflow"** below. (Ravi P Singh and Raja Kataru were removed on
   2026-07-25 pending their official Aug 2026 start; re-add them then.)
2. **Personal links — now rendered.** The People page shows small LinkedIn / Google Scholar / website
   icons under each member, only for links a member provided (`_pages/people.md`; data in each
   `_people/<slug>.md` under `social.linkedin`, `links.scholar`, `links.site`).
3. **Bios held.** Hossein, Hasan, and James sent short bios / research-interest blurbs. Not rendered
   (the grid has no bio slot); saved in the `member-photos-links` PR notes for a future member-profile
   decision. Ritwesh Kumar (alumni) sent a photo + site; kept as alumni, so his photo is unused and
   his site link is held until/unless alumni links render.

---

## Photo intake workflow (for Claude, when photos arrive)

For each member photo Baskar forwards:

1. Identify the member's slug: `ls _people/ | grep -i <name>` (files are `_people/<slug>.md`).
2. Convert + square-crop to the site standard: **500×500 WebP**, face centered, ~20-35 KB.
   Existing photos live in `assets/img/people/<slug>.webp`. Use `cwebp`/ImageMagick:
   `magick input.jpg -resize 500x500^ -gravity center -extent 500x500 assets/img/people/<slug>.webp`
   (verify a real face-centered crop; adjust `-gravity`/offset if the face is off-center).
3. Set the frontmatter in `_people/<slug>.md`: `photo: /assets/img/people/<slug>.webp`
   (see `_people/zaki-jubery.md` for the exact pattern).
4. If a personal link was included, add it under `links:` (scholar/github/site) or `social:`.
5. `make validate`, rebuild, confirm the tile renders (not the silhouette fallback), commit.
6. Photos render as a **square** (CSS `aspect-ratio: 1/1`, `object-fit: cover`, rounded corners)
   in a grid of ~140px tiles — so head-and-shoulders framing is what looks right.

Current members are the priority; many of the 91 people files are alumni who may not need photos.

---

## ✅ Done (do not redo)

- **Enrichment sweep (abstracts-only) complete across all years 2009-2026.** 215/344 papers have
  `summary` + `themes` fields, drafted only from real fetched abstracts (OpenAlex/Crossref), plain
  language, present tense, no em/en dashes, no fabrication. Un-enriched remainder is abstract-less.
- **Deduplication done:** `scripts/dedup.py` removed 30 preprint/repo/conf-abstract copies
  (374 → 344), merging arXiv `eprint` pointers into 11 kept published entries. Record in
  `docs/duplicate-papers.md` (marked RECONCILED).
- **Author normalization:** `scripts/build_authors.py` → `_data/authors.yml`; `norm_key()` matching
  in `bib_to_json.py`. People → publications links work via `?member=<slug>` (fixed the PI-shows-0
  and Zaki/Talukder Jubery cases; other members' name variants checked).
- **Products:** 15 project pages in `_products/` from the `baskargroup` GitHub org.
- **Impact:** call-out inviting policymakers/philanthropists to reach out, using Baskar's direct
  email `baskarg@iastate.edu` **obfuscated** (also on the Join page). Never expose it in plaintext.
- **Homepage:** old-site text, selected works, hero from Proteus repo, Baskar's photo removed.
- **PI details:** Distinguished Professor; connected to AIIRA (aiira.iastate.edu) and
  TrAC (trac-ai.iastate.edu); "Staff" (not "Research Staff"); "societal" (not "national") challenges.
- **Launch-readiness cleanup (2026-07-25):** removed all al-folio demo debris that would have shipped
  publicly: the demo CV page (`/cv/` John Doe + `_data/cv.yml` + rendercv assets incl. Einstein PDF +
  `.github/workflows/render-cv.yml`), `assets/plotly/demo.html`, `assets/html/relativity.html`, demo
  images (`assets/img/1-12.jpg`, `prof_pic*`), demo audio/video (`pexels`, `tutorial_al_folio`), demo
  JSON (`resume.json`, `table_data.json`), demo bib preview GIFs, and blanked demo `_data/coauthors.yml`
  / `repositories.yml`. Excluded the theme `test/` dir from the build. Replaced 4 visible `TODO(baskar)`
  page notes (homepage contact note, People/Impact/Products notes) with real text; dropped the
  inaccurate "Photos from Unsplash" footer credit and set real SEO keywords. **Verified: 0 rendered
  TODO/placeholder text, 0 plaintext email, build + validate clean.**

---

## 📋 Open TODOs — suggested next steps (priority order)

1. **Member photos + personal links** (in flight — see above).
2. **News / wins** — add recent group wins to `_news/YYYY-MM-DD-<slug>.md`.
3. **Impact stories + reach numbers** — `_impact/<slug>.md` and `_data/stats.yml`. Baskar has news
   articles with real numbers; use only real, sourced figures (never invent). Also relevant:
   AAAS-Fellow nomination docs.
4. **Hiring** (for the Join page): looking to hire **1-2 PhD students next year** and a
   **back-end HPC/GPU engineer**.
5. **Go-live** — GitHub org + Pages at `baskar-group.github.io`. Needs Baskar's manual steps
   (org access, decision on the `BaskarGroup.github.io` root repo, add the git remote and push).
   Content is launch-ready after the 2026-07-25 cleanup. Remaining pre-public considerations (not
   blockers): (a) ~20 al-folio CI workflows will activate on GitHub (docker image builds,
   lighthouse-badger, visual-regression, codeql, etc.) -- prune to just deploy/validate if unwanted;
   (b) `/news/` renders an empty page (no `_news` items yet, unlinked from nav); (c) impact stat
   "Open tools and datasets released: 12" vs 16 product pages -- reconcile if desired.
6. **Optional — 122 abstract-less papers:** currently pending (no OpenAlex/Crossref abstract). Could
   source abstracts another way (publisher pages / Semantic Scholar / manual) for fuller coverage,
   or leave them un-enriched. 7 more are pending as no-theme/junk (DEI/education, tribology,
   extended-abstract boilerplate) and are intentionally skipped.

---

## Key facts, files, commands

- **Build/validate:** `make serve` (local private review), `make build`, `make validate`,
  `make json`. Ruby is Homebrew keg-only — Makefile handles the PATH; direct calls need
  `export PATH="/opt/homebrew/opt/ruby/bin:$PATH"`.
- **Tests:** `.venv/bin/python -m pytest tests/ -q -p no:cacheprovider` (10 tests). Scoped to
  `tests/` because Jekyll used to copy them into `_site/`; `tests/`, `scripts/`, `.venv/` are now
  excluded in `_config.yml`.
- **Scripts:** `bib_to_json.py` (emits `assets/json/papers.json` + `_data/theme_counts.yml`),
  `validate.py`, `build_authors.py`, `dedup.py`, `openalex_sync.py`.
- **Enrichment state:** `scripts/enrichment_pending.txt` = 129 un-enriched bibkeys (122 abstract-less
  + 7 no-theme). `validate.py` skips these for the summary/theme requirement.
- **Source-of-truth files:** see the table in `CLAUDE.md` (papers.bib, themes.yml, authors.yml,
  `_people/`, `_products/`, `_impact/`, `_news/`, coverage.yml, stats.yml, briefs.yml).
- **Theme distribution (enriched):** cyberag ~86, phenotyping ~80, sciml ~57, numerics ~47,
  energymat ~38, design-opt ~26, microfluidics ~26, hpc ~19, built-env ~12.

## Standing constraints (recap)

- **PR only; never push to `main`.** Feature branch → PR for every change.
- **Never fabricate.** No invented papers, numbers, quotes, or URLs; use `TODO(baskar)` markers and
  list them in PR descriptions.
- **Private until go-live.** Keep everything local; GitHub only when Baskar says so.
- **Design frozen.** No visual-system changes without an explicit ask.
- **Email obfuscated.** `baskarg@iastate.edu` never appears in plaintext.
- **Dash rule.** No em/en dashes in authored prose fields (imported bib metadata is exempt).
