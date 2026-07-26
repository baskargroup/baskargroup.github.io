# Baskar Group website — status & resume log

**Last updated:** 2026-07-25 · **Branch:** `main` · **Status: LIVE and PUBLIC.**

This is the clean resume point for the next session. Read this first, then `CLAUDE.md`,
then `docs/PLAN.md` for the original spec. **The site is now published** at
**https://baskargroup.github.io/** — every push to `main` that touches site content
auto-deploys to the public web (see "How to ship an edit" below). This is no longer a
private local project; treat edits as going live.

---

## TL;DR — where we are

- **LIVE** at **https://baskargroup.github.io/** (public, GitHub Pages, went live 2026-07-25).
- **Repo:** `github.com/baskargroup/baskargroup.github.io` — the org-root site under the existing
  `baskargroup` GitHub org, sharing the domain with the project pages
  (`baskargroup.github.io/HS-3D-NeRF/`, `/BioTrove/`, etc.). Local `origin` remote already points here.
- **Design is FROZEN** (tag `design-freeze-2026-07-20`): amber/gold primary + cyan highlight,
  color-blind-safe (Baskar is red color blind). **Do not change colors, fonts, or the wordmark
  without an explicit ask.** See memory `baskar-group-site-design-freeze`.
- **Content is launch-clean:** 344 publications (215 enriched), all al-folio demo debris removed,
  zero placeholder/TODO text renders on the site, PI email obfuscated everywhere.

---

## How to ship an edit (READ THIS before making changes)

The publishing pipeline is: **push `main` → "Deploy site" Action builds al-folio → pushes static
HTML to the `gh-pages` branch → GitHub Pages serves `gh-pages`.** GitHub's own Jekyll CANNOT build
al-folio (custom plugins), which is why Pages serves the pre-built `gh-pages`, not `main`.

1. **Branch off `main`**, make the change. One concern per branch (that has been the working rhythm).
2. **Validate + build locally:**
   - `.venv/bin/python scripts/validate.py` (the `Makefile`'s `make validate` uses system python and
     lacks the deps — always use the venv).
   - `rm -rf .jekyll-cache && export PATH="/opt/homebrew/opt/ruby/bin:$PATH" && bundle exec jekyll build`
     — **clear `.jekyll-cache` first**; config/`_data` changes are otherwise served stale locally.
   - Preview: `cd _site && python3 -m http.server 8900` then load it (or `make serve`).
3. **Commit** (end message with the `Co-Authored-By: Claude Opus 4.8` footer), **merge to `main`**
   fast-forward, delete the branch. (PR-only rule: never edit `main` directly; use a branch.)
4. **Push:** `git push origin main`.
   - GOTCHA: the agent's auto-mode classifier BLOCKS `git push`. Ask Baskar to run it himself via the
     `! git push origin main` prefix in the session, or in his terminal. (First launch used
     `--force` to overwrite the repo's initial README commit; normal pushes do NOT need `--force`.)
5. **Deploy:** the push auto-triggers "Deploy site" (path filters cover `assets/**`, `**.md`, `**.yml`,
   `**.bib`, `**.html`, etc.). Live in ~1-2 min. If a push doesn't auto-run it (path filters can skip
   some), go to **Actions → Deploy site → Run workflow → main** (it has a `workflow_dispatch` trigger).
   Watch the run at github.com/baskargroup/baskargroup.github.io/actions.

**Take the site offline** (all reversible): repo Settings → Pages → "Unpublish site", or set Source to
None, or make the repo private. Note: nothing erases search-engine/Wayback caches instantly.

**GitHub Pages config that must stay put:** Source = "Deploy from a branch", Branch = **`gh-pages` /
(root)**; Settings → Actions → General → Workflow permissions = "Read and write". If the site ever
shows a bare README again, Pages got flipped back to building `main` — set it to `gh-pages`.

---

## ⏳ In flight / the only open member item

- **Member photos:** 26 of ~27 current members now have a 500x500 WebP headshot. **Only one lacks a
  photo: `meherpal-singh-bhatti`.** When it arrives, follow the Photo intake workflow below.
  (Ravi P Singh and Raja Kataru were removed 2026-07-25 pending their official Aug 2026 start —
  re-add them then.)

---

## Photo intake workflow (for the next Claude, when a photo arrives)

1. Identify the slug: `ls _people/ | grep -i <name>`.
2. Convert + square-crop to the site standard (**500x500 WebP**, face centered):
   `magick input.jpg -auto-orient -resize 500x500^ -gravity center -extent 500x500 -quality 82 assets/img/people/<slug>.webp`
   (use `-gravity north` when the face sits high; **Read the output image to verify the crop** before committing).
3. Set frontmatter in `_people/<slug>.md`: `photo: /assets/img/people/<slug>.webp`. Add any personal
   links under `links:` (`scholar`/`github`/`site`) or `social:` (`linkedin`). The People page renders
   small LinkedIn / Scholar / website icons per member, only for links actually provided.
4. Validate, build, confirm the tile renders, commit, merge, push, let it deploy.
- Bot-protected sources (e.g. TrAC `trac-ai.iastate.edu`) block curl/WebFetch — use the Chrome browser
  tools to load the page in the real session, read the image URL from the DOM, then curl that direct
  file URL (the image asset itself is usually not WAF-protected).

---

## ✅ Done (do not redo)

- **Go-live (2026-07-25):** pushed to `baskargroup/baskargroup.github.io`, ran Deploy site → `gh-pages`,
  set Pages to serve `gh-pages`. Site verified live. Site `url`/`og_image`/JSON-LD point at
  `baskargroup.github.io`.
- **Launch-readiness cleanup (2026-07-25):** removed ALL al-folio demo debris (John Doe `/cv/` page +
  `_data/cv.yml` + rendercv/Einstein-PDF assets + `render-cv.yml`; `plotly/demo.html`;
  `html/relativity.html`; demo images `1-12.jpg` + `prof_pic*`; demo audio/video; `resume.json` +
  `table_data.json` + the `jekyll_get_json`/`jsonresume` config; demo bib-preview GIFs; blanked demo
  `_data/coauthors.yml` + `repositories.yml`); excluded the theme `test/` dir from the build; replaced
  4 visible `TODO(baskar)` page notes with real copy; dropped the "Photos from Unsplash" footer; set
  real SEO keywords. Verified: 0 rendered TODO/placeholder, 0 plaintext email.
- **CI pruned to 4 essentials:** `deploy.yml`, `unit-tests.yml`, `broken-links.yml`,
  `broken-links-site.yml`. Removed 14 template workflows (docker builds, lighthouse-badger,
  visual-regression, codeql, prettier x3, axe, update-citations, update-tocs, upgrade-check,
  copilot-setup-steps). The two broken-link checkers may occasionally go red on external-link flakiness
  (cosmetic; deploy is independent) — drop them if that annoys.
- **Member photos + personal-link icons:** 13 photos processed across the session (zip batch + Antriksh
  from his Google site + Prashant, Harish, Nicole from source/TrAC). LinkedIn/Scholar/website icons
  render under each member (inline SVG, cyan on hover). Name fixes: "Md Mohammadul" -> "Md Mahmudul
  Hasan Mollah"; "Antriksh Srivatsava" -> "Srivastava" (slug + authors.yml, old spelling kept as a
  matching variant).
- **Products:** added `flowbench.md` (dataset; bitbucket + arXiv); repointed HS-3D-NeRF repo to
  `github.com/kibonku/HSI-SC-NeRF`. 16 product pages total.
- **Impact page "Funding and support" section:** grouped funder name chips (Federal / State and farmer
  groups / Institutional / Industry & public-private partnerships), sourced from the July 2026 CV, in
  `_data/funding.yml`, placed BELOW the "Let's build what comes next" CTA (CTA emphasized). Template
  supports an optional per-funder `logo:` for a future logo wall (deferred — company/state logos need
  official brand assets; they are trademarks not freely available on Wikimedia).
- **Publications pipeline (earlier):** 344 papers after dedup, 215 enriched (summaries + themes).
  Author normalization via `_data/authors.yml` + `norm_key()`. People->publications links via
  `?member=<slug>`.

---

## 📋 Open TODOs — suggested next steps

1. **`meherpal-singh-bhatti` photo** (only member missing one).
2. **News / wins** — `_news/YYYY-MM-DD-<slug>.md` (dir does not exist yet; `/news/` currently renders an
   empty page, unlinked from nav). Use the `add-win` skill.
3. **Impact stories + reach numbers** — `_impact/<slug>.md`, `_data/stats.yml`. Real figures only.
4. **Funder logo wall** — upgrade the funding chips to logos once Baskar supplies company/state brand
   assets (drop into `assets/img/funding/`, add `logo:` to each funder in `_data/funding.yml`).
5. **Hiring (Join page):** 1-2 PhD students next year + a back-end HPC/GPU engineer.
6. **Custom domain (optional):** can be layered on either later via CNAME (Settings -> Pages).
7. **Minor:** impact stat "Open tools and datasets released: 12" vs 16 product pages — reconcile if
   desired (stat is CV-sourced). 122 abstract-less papers remain un-enriched (no fabrication).

---

## Key files, commands, gotchas

- **Source of truth:** see the table in `CLAUDE.md` (papers.bib, themes.yml, authors.yml, `_people/`,
  `_products/`, `_impact/`, `_news/`, coverage.yml, stats.yml, briefs.yml, and now `_data/funding.yml`).
- **Scripts:** `bib_to_json.py` (-> `assets/json/papers.json` + `_data/theme_counts.yml`),
  `validate.py`, `build_authors.py`, `dedup.py`, `openalex_sync.py`. Run via `.venv/bin/python`.
- **Tests:** `.venv/bin/python -m pytest tests/ -q -p no:cacheprovider` (`tests/`, `test/`, `scripts/`,
  `.venv/` are all excluded from the Jekyll build in `_config.yml`).
- **Gotchas learned this session:** (a) clear `.jekyll-cache` before rebuilding after config/`_data`
  edits or you see stale output; (b) GitHub Pages can't build al-folio — must serve `gh-pages`;
  (c) the agent can't `git push` (classifier blocks it) — Baskar runs it; (d) `make validate` uses the
  wrong python — use the venv; (e) some external sites (TrAC) need the browser, not curl.
- **Workflow skills available:** `enrich-papers`, `add-win`, `triage-coverage`, `add-mention`,
  `add-product`, `add-impact-story`, `new-member`, `graduate-member`, `sync-report`.

## Standing constraints (recap)

- **LIVE now** — pushes to `main` publish to the public site. Double-check before pushing.
- **PR only; never edit `main` directly.** Branch -> validate -> merge -> push.
- **Never fabricate.** No invented papers, numbers, quotes, or URLs; use `TODO(baskar)` markers only in
  places that DO NOT render (never in page body text now that the site is public).
- **Design frozen.** No visual-system changes without an explicit ask.
- **Email obfuscated.** `baskarg@iastate.edu` never appears in plaintext (use the `encode_email` filter).
- **Dash rule.** No em/en dashes in authored prose fields (imported bib metadata is exempt).
- **Private, not committed:** `docs/source/` (CV, Scholar export, nomination letters, member-photo
  originals) is gitignored — never publish or commit its contents.
