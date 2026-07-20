# Baskar Group Website Rebuild: Instruction Set for Claude Code

Owner: Baskar Ganapathysubramanian (Baskar Group, Iowa State University)
Purpose: Replace https://www.me.iastate.edu/bglab/ with a modern, agent-updatable GitHub Pages site.
Status: Approved plan. Execute phase by phase.

---

## Amendments (2026-07-19, pre-execution evaluation)

These edits resolve findings from `docs/plan-evaluation.md`. Each amendment is marked inline with `[AMEND-N]`. All ten findings are now encoded; the two former open decisions were settled on 2026-07-19 (MVP scoping and branding/URL, below).

- [AMEND-1] Section 12.2: the dash ban applies to authored prose fields only, not imported bibliographic metadata.
- [AMEND-2] Section 6.2: resolve all OpenAlex author IDs (profiles fragment), union their works; Scholar export is the completeness oracle.
- [AMEND-3] Section 6.2: explicit dedup precedence (published outranks preprint; merge identifiers, never blind-drop).
- [AMEND-4] Sections 6 and 12.5: unit tests with fixtures for the deterministic scripts; pin dependency versions.
- [AMEND-5] Section 6.2: deterministic, collision-safe bibkey generation.
- [AMEND-6] Section 14: approved MVP launch target of Phases 0-4 plus a minimal homepage, then layer the rest.
- [AMEND-7] Section 2: full rebrand to "Baskar Group" hosted at `baskar-group.github.io`; the "ComPM Lab" / Computational Physics and Mechanics identity is retired.
- [AMEND-8] Section 6.3: canonicalize members and frequent collaborators, not literally every author string.
- [AMEND-9] Section 12.1: SHA-pin third-party GitHub Actions.
- [AMEND-10] Sections 6.2 and 6.5: Scholar export recommended; Crossref and Semantic Scholar as abstract fallbacks.

---

## 0. How to use this document

- This file is the master spec. In Phase 0, commit it into the repo as `docs/PLAN.md`.
- Work strictly phase by phase (Section 14). Do not start a phase until the previous phase's acceptance criteria pass.
- All changes go through a feature branch and a pull request into `main`. Never push directly to `main`. This applies to humans, scripts, and Claude Code alike.
- Discover, do not assume. The al-folio theme evolves; file names below (bib layout, workflow names) reflect intent, not guaranteed paths. Inspect the cloned theme and adapt.
- Never fabricate content. No invented paper claims, statistics, quotes, names, or URLs. When information is missing, insert a `TODO(baskar)` marker and list all such markers in the PR description.
- Hard style rule: no em-dashes and no en-dashes in authored prose, code comments, or authored data-file values. Use commas, colons, parentheses, or separate sentences. Hyphens in compound words and numeric ranges (e.g., 1-2) are fine. [AMEND-1] This rule does not apply to imported bibliographic metadata (`title`, `author`, `journal`, `booktitle`, `venue`, `abbr`), which must never be altered (Section 6.5) and may legitimately contain en-dashes. This rule is enforced by CI on authored fields only (Section 12.2).
- Kickoff prompt for the first session, verbatim:
  "Read docs/PLAN.md and CLAUDE.md. Execute Phase 0 only. Open a PR when the Phase 0 acceptance criteria pass, and list any deviations from the plan in the PR description."

---

## 1. Goals and constraints

Goals:
1. Modern, fast, mobile-friendly lab site reflecting current research (SciML, HPC/FEM, cyber-agriculture, energy, buildings), not the 2014-era WordPress content.
2. Papers section: searchable and filterable by year, author, and theme; every paper carries a 1-2 line plain-language summary; selected papers get a hero figure or video.
3. Products page: software, apps, datasets, and models, cross-linked to papers, themes, and people.
4. Impact page written for the general public and policy makers.
5. News that celebrates wins (papers, grants, awards, defenses, graduations) plus prominent press and community coverage (media stories, member blog posts, LinkedIn posts).
6. Everything updatable by editing one file per content type, so agent-driven updates are safe and reviewable.
7. Automation is PR-gated: scripts and Claude Code propose, Baskar approves.

Constraints:
- Hosting: GitHub Pages at the org github.io URL for now. A custom domain is a later, non-breaking change (Section 15).
- No servers, no databases, no paid services. Client-side search only.
- Minimal JavaScript, vanilla only, and every page must degrade gracefully without JS.
- Accessible (WCAG AA contrast, alt text, keyboard focus) and fast (Lighthouse mobile >= 90).

---

## 2. Stack and repository

- Theme: al-folio (Jekyll), created via "Use this template" from `alshedivat/al-folio`. It provides publications from BibTeX (jekyll-scholar), light/dark mode, math and code support, and a stock GitHub Actions deploy workflow.
- [AMEND-7] GitHub org: create `baskar-group` (confirm availability first; fallback if taken: `baskar-group-isu`). Repo name: `baskar-group.github.io`, which serves the site at the org root URL. Rationale for an org rather than a personal account: the group identity outlives any one account, students can be granted scoped access, and the personal `BaskarGS` account stays free for a personal homepage.
- GitHub Pages: repo Settings -> Pages -> Source: GitHub Actions. Keep the theme's stock deploy workflow; extend it only as specified in Section 12.1.
- Local development: use the theme's Docker setup (Ruby/Jekyll installs are brittle otherwise). Add a `Makefile` with targets: `serve`, `build`, `json` (runs `scripts/bib_to_json.py`), `validate` (runs `scripts/validate.py`), `sync` (runs the OpenAlex sync in dry-run).
- [AMEND-7] `_config.yml`: site title "Baskar Group", subtitle "Iowa State University" with a fuller descriptive tagline marked TODO(baskar) for final wording (do not reuse "Computational Physics and Mechanics Laboratory"; that identity is retired), correct `url` (`https://baskar-group.github.io`), empty `baseurl`, links to Google Scholar (user R1JIs4cAAAAJ), ORCID (TODO(baskar)), and the GitHub org.

Phase 0 acceptance:
- [ ] Org and repo exist; stock theme deploys green; site loads at the org URL.
- [ ] `docs/PLAN.md`, `CLAUDE.md` (Section 12.3), and `Makefile` committed.
- [ ] `make build` succeeds locally in Docker.

---

## 3. Information architecture

Top navigation: Home, Research (themes), Publications, Products, People, Impact, News, Join.

Single source of truth per content type:

| Content | Source of truth |
|---|---|
| Papers | `_bibliography/papers.bib` |
| Theme taxonomy | `_data/themes.yml` |
| Author name map | `_data/authors.yml` |
| People | `_people/<slug>.md` |
| Products | `_products/<slug>.md` |
| Impact stories | `_impact/<slug>.md` |
| Wins | `_news/YYYY-MM-DD-<slug>.md` |
| Coverage: press, blogs, member posts | `_data/coverage.yml` (candidates in `_data/coverage_inbox.yml`, never rendered) |
| Impact statistics | `_data/stats.yml` |
| Policy briefs | `_data/briefs.yml` + PDFs in `assets/pdf/briefs/` |

Cross-linking keys: theme slug, bib key, person slug, product slug. Rule: pages never restate linked facts in free text; they reference keys and let templates resolve them. This is what keeps agent edits localized and safe.

---

## 4. Conventions

- Slugs: lowercase, hyphenated, stable once created.
- Bib keys: `<firstauthorlastname><year><keyword>`, e.g., `khanwale2023twophase`.
- Images: WebP preferred. Paper previews at 16:9, max width 1200px, target <= 250 KB, stored in `assets/img/papers/<bibkey>.webp`. Alt text is mandatory and validated.
- Video: never committed to the repo. Use YouTube (unlisted is fine) with a poster image in the repo and a click-to-load embed. No autoplay.
- Paper summary style: 1-2 sentences, plain language, present tense, states what was done and why it matters. No citations inside the summary, no jargon that a senior undergraduate outside the field would stumble on, and no em/en dashes. Fictional tone examples (for style only, do not reuse):
  - "We develop a solver that captures how droplets break up and merge at resolutions previous methods could not reach. This makes it practical to simulate industrial mixing processes on ordinary GPU clusters."
  - "We train a model that identifies crop pests from a phone photo and explain when its answers can be trusted. Extension educators use it to give growers same-day guidance."
- Impact story style: 150-250 words, structure of problem -> what we built -> who benefits -> at what scale, roughly 9th-grade reading level, one visual, ends with 2-4 links (project, product, papers).
- Author canonicalization: `_data/authors.yml` maps every observed name variant to one canonical display form; lab members additionally carry `person: <slug>` to link their person page. Example:

```yaml
- canonical: "B. Ganapathysubramanian"
  person: baskar
  variants: ["Baskar Ganapathysubramanian", "B Ganapathysubramanian", "Ganapathysubramanian, B."]
```

---

## 5. Theme taxonomy (approved)

Create `_data/themes.yml` exactly as below (colors are placeholders; finalize in Phase 6 design pass). Taxonomy changes happen only by editing this file; the validator rejects unknown slugs everywhere else.

```yaml
- slug: sciml
  name: Scientific machine learning
  blurb: Neural surrogates, operator learning, and physics-informed models for scientific prediction and design.
- slug: numerics
  name: Numerical methods and FEM
  blurb: Finite element methods, variational multiscale approaches, and solvers for coupled PDE systems.
- slug: hpc
  name: HPC and GPU computing
  blurb: Scalable, GPU-accelerated simulation software for leadership-class and departmental clusters.
- slug: cyberag
  name: Cyber-agricultural systems
  blurb: AI, sensing, and decision tools for resilient crop production.
- slug: phenotyping
  name: Plant phenotyping and sensing
  blurb: Imaging, computer vision, and analytics that measure plants at scale.
- slug: energymat
  name: Energy materials and devices
  blurb: Simulation and design of organic electronics, electrochemical systems, and soft matter manufacturing.
- slug: microfluidics
  name: Microfluidics and electrokinetics
  blurb: Modeling and control of droplets, charge transport, and lab-on-chip devices.
- slug: built-env
  name: Building and urban physics
  blurb: Flow, energy, and coupled food-energy-water modeling for buildings and cities.
- slug: design-opt
  name: Design, optimization, and control
  blurb: Turning simulators and data into decisions through optimization and control.
```

---

## 6. Papers system

### 6.1 Bib schema

One BibTeX entry per paper in `_bibliography/papers.bib`. Use the theme's supported fields (`abbr`, `doi`, `url`, `pdf`, `code`, `poster`, `slides`, `award`) plus these custom fields, which jekyll-scholar passes through to templates:

- `summary = {...}`: the 1-2 line plain-language summary.
- `themes = {sciml, hpc}`: 1-3 slugs from Section 5.
- `preview = {<bibkey>.webp}`: hero figure filename under `assets/img/papers/`.
- `video = {<youtube-id>}`: optional.
- `selected = {true}`: promotes the paper to hero-card treatment.

Locate the theme's bib rendering template (likely `_layouts/bib.liquid` or `_includes/bib.html`; inspect the clone) and extend it to render: summary text under the citation, clickable theme chips, an award badge, and a video button when present.

### 6.2 Initial import

Write `scripts/openalex_sync.py` (Python, `requests`; no API key needed):
- [AMEND-2] Resolve the author across all candidate IDs, not one: OpenAlex commonly fragments a single person into multiple author IDs (affiliation and name-variant splits). Query the authors endpoint by ORCID if available, else by name; collect every candidate whose affiliation history includes Iowa State; and pin the full set of author IDs in `scripts/config.yml`. Include a `mailto` parameter in all requests (polite pool). Pinning a single ID is a silent-undercount risk and is not allowed.
- `--full`: pull all works for the pinned author-ID set with cursor pagination and write BibTeX stubs (title, authors, year, venue, DOI, pages) to `data-import/openalex.bib`. [AMEND-5] Generate bibkeys deterministically and collision-safely: `<firstauthorlastname><year><keyword>`, where keyword is the first significant title word (skip articles, prepositions, and stopwords), lowercased and ASCII-folded. On collision, append a stable suffix (`b`, `c`, ...) assigned in ascending DOI order so keys never depend on run order.
- `--sync`: diff OpenAlex against `_bibliography/papers.bib` by DOI, then by normalized title (casefold, strip punctuation), and append only genuinely new entries. Never modify existing entries. [AMEND-3] Dedup precedence is explicit and deterministic: a published record (has a journal or booktitle plus a DOI) outranks a preprint (arXiv, bioRxiv, SSRN). When a candidate matches an existing entry by normalized title but not DOI (the classic preprint-versus-journal case), keep the more complete record and attach the other record's identifiers (for example, add an `arxiv` or `eprint` field to the journal entry) rather than dropping either blindly. A dropped or merged record is logged to the PR body, never silently discarded.
- [AMEND-10] Reconciliation with Google Scholar is recommended, not optional, and doubles as the completeness oracle for [AMEND-2]: if Baskar places his full Scholar export at `data-import/scholar.bib`, merge it, preferring OpenAlex metadata, flagging Scholar-only items with `note = {needs-doi}`, and listing every Scholar entry not matched in the OpenAlex union for review (flag, never drop).

Target: all 230+ publications present as at least stubs by end of Phase 2.

### 6.3 Author normalization

`scripts/normalize_authors.py` extracts every distinct author string from the bib, proposes groupings of obvious variants into `_data/authors.yml`, applies the map, and reports unmapped strings. [AMEND-8] The completeness bar is every lab member plus every frequent collaborator canonicalized, not literally zero unmapped strings: `validate.py` only requires person-slug mappings for lab members, and the long tail of one-off coauthors may render as raw strings. Chasing literal zero across hundreds of distinct coauthor strings is busywork with no reader-facing payoff. The initial map is a one-time PR that Baskar reviews carefully, since it drives all author cross-links.

### 6.4 Publications page, JSON, and search

- Keep the theme's year-grouped rendering.
- `scripts/bib_to_json.py` (use `bibtexparser`) emits `assets/json/papers.json`: bibkey, title, canonical authors, member-person slugs, year, venue, doi/url, themes, summary, selected, preview. Run it as a build step in the deploy and CI workflows and via `make json`. It is also the substrate for cross-queries on product, person, and theme pages.
- `assets/js/papers-filter.js` (vanilla JS): each rendered entry carries `data-year`, `data-authors`, `data-themes`, and searchable text. Controls: year dropdown, author autocomplete (options from papers.json), theme chips, and a free-text box over title, summary, and authors. AND semantics across facets, live result count, and filter state synced to URL params (`?year=&author=&theme=&q=`) so filtered views are shareable links. Without JS, the full list renders normally.
- Cross-links: member author names link to person pages; all author names link to `?author=` filtered views; theme chips link to `?theme=` views and theme pages.
- Selected papers render as hero cards (preview image or video poster, summary, chips) at the top of the publications page and are reused on the home and theme pages.

### 6.5 Enrichment of all entries (workflow skill `/enrich-papers`)

For every entry missing `summary` or `themes`:
1. Fetch the abstract via OpenAlex (`abstract_inverted_index`, reconstruct to text), then Crossref by DOI, then Semantic Scholar as further fallbacks. [AMEND-10] Expect low abstract coverage for this lab's core venues: several Elsevier journals (for example JCP and CMAME) do not supply abstracts to OpenAlex, so a large share of entries will have no machine-readable abstract and enrichment will lean heavily manual. Treat that as the norm, not a bug.
2. Draft the summary per the Section 4 style rules. If no abstract is available and the title is insufficient, add the bibkey to a `needs-review` list in the PR body instead of guessing.
3. Assign 1-3 themes from the taxonomy only. If none fit, flag for review; never invent a theme.
4. Do not alter titles, authors, venues, or years during enrichment.

Batching: 25 entries per branch and PR. The PR body lists each bibkey with the drafted summary and themes for fast review. Wait for merge before starting the next batch. Full coverage of 230+ papers is roughly 10 PRs; this is Phase 3.

Papers acceptance (Phases 2-3):
- [ ] [AMEND-4] Unit tests for `openalex_sync` (dedup, bibkey generation), `bib_to_json`, and `normalize_authors` pass in CI; the four minimum fixtures (Section 12.5) are present.
- [ ] `papers.json` entry count equals bib entry count; `make validate` passes.
- [ ] Filters work; URL params round-trip; page is fully readable with JS disabled.
- [ ] Spot-check 10 papers: summary, chips, and cross-links render; member names resolve to person pages.
- [ ] `scripts/enrichment_pending.txt` (Section 12.2) is empty at the end of Phase 3.

---

## 7. Products

`_products/<slug>.md` front matter:

```yaml
title: FASTEST
type: software        # software | app | dataset | model | service
status: active        # active | maintained | archived
blurb: GPU-accelerated finite element framework for multiphysics simulation.  # <= 160 chars
links:
  repo: TODO(baskar)
  docs: TODO(baskar)
  app:            # web app or app store link, if any
image: assets/img/products/fastest.webp
themes: [numerics, hpc]
papers: []            # bibkeys; template renders them from papers.json
people: []            # person slugs
metrics:
  stars: auto         # auto renders a shields.io badge from links.repo; no tokens needed
  downloads: TODO(baskar)
```

- Products page: card grid, filterable by type with the same URL-param pattern as publications. Each product's detail section lists related papers (resolved from papers.json by bibkey), themes, and team.
- Seed stubs in Phase 4 (fill links via TODO markers, do not invent URLs): FASTEST, DiffSim, InsectNet / InsectID, WeedID, PestIDBot. Leave commented placeholders for datasets and models to be added later.

Acceptance:
- [ ] Page renders and filters; every referenced bibkey, person, and theme validates; star badges resolve for products with a repo link.

---

## 8. People

`_people/<slug>.md` front matter: name, role (`pi | postdoc | phd | ms | undergrad | staff | alumni`), photo, start, end (alumni), links (scholar, github, site), social (strictly opt-in: linkedin, bluesky, x, blog; rendered as icons only when the member chooses to provide them), themes, coadvisors (free text), placement (alumni only, e.g., "Postdoc, Stanford" or "Corning Inc").

- Current members grouped by role; alumni page grouped by degree and year with placements. With 29+ PhD graduates and strong placements, the alumni wall is a first-class recruiting asset: give it real design attention.
- Each person page links to their filtered publications view (via authors.yml canonical name), their products, and wins that mention them.
- Seed with Baskar plus stub files generated from a roster Baskar pastes into a session; do not guess names or placements.

Acceptance:
- [ ] Validator passes; roles render into the correct sections; at least the PI page is complete with photo and links.

---

## 9. Impact page (public and policy makers)

Layout, top to bottom: mission paragraph, impact story cards, by-the-numbers strip, policy engagement section.

- Mission paragraph: adapt the current site's research statement into 3-4 plain sentences at roughly 9th-grade reading level. Draft it, mark `TODO(baskar)` for final wording.
- Impact stories: `_impact/<slug>.md` with front matter `title`, `hero` (image), `audience` (`public | policy | both`), `related` (papers, products, themes), `order`. Body follows the Section 4 story style. Launch with four stories (draft in Phase 5, all numbers as TODO until Baskar confirms):
  1. `putting-ai-in-farmers-hands`: pest, weed, and disease identification tools and the AIIRA ecosystem reaching growers and educators.
  2. `simulating-the-physical-world`: FASTEST and GPU-accelerated simulation compressing design cycles for engineered systems.
  3. `healthier-smarter-buildings`: building energy and urban food-energy-water modeling informing efficient, resilient communities.
  4. `training-the-ai-workforce`: 29+ PhD graduates plus K-12 and educator programs building AI capacity.
- By-the-numbers strip reads `_data/stats.yml` (PhDs graduated, publications, open tools, people reached, sponsors). Ship it with TODO placeholders; the template hides any stat without a confirmed value. Absolute rule: no fabricated numbers, ever.
- Policy section: short paragraph on advisory and briefing engagement, then a list of downloadable one-page PDF briefs from `_data/briefs.yml` and `assets/pdf/briefs/`. Staffers forward PDFs, not URLs. Create the structure with one placeholder brief entry; writing briefs is content work for later sessions.

Acceptance:
- [ ] Page renders with all four stories; every related key validates; no visible TODO text on the rendered page; hero images have alt text.

---

## 10. News: wins, press, and community voices

Approval model: nothing in this section publishes itself. Every item reaches the live site only when Baskar merges a PR into `main`, and CODEOWNERS (Section 12.1) makes his review mandatory for these paths. Inbox files are never rendered.

### 10.1 Wins

`_news/YYYY-MM-DD-<slug>.md` front matter: `date`, `type` (`paper | preprint | grant | award | graduation | defense | milestone`), `title`, `people` (slugs), `links` (`bibkey`, `product`, `url`, any subset), optional `image`.

- Rendering: a small colored type badge per win; homepage shows the latest 5; `/news/` archive is filterable by type and year with the shared URL-param pattern.
- `/add-win` workflow skill (Section 12.4) drafts a win from arguments, resolves entity links, and opens a PR.
- The weekly paper-sync PR (Section 12.1) also drafts one win per genuinely new peer-reviewed paper (skip errata and datasets), marked `TODO(confirm)` so nothing announces itself without review.

### 10.2 Press and community coverage

One pipeline covers three kinds of external attention: media stories, blog posts (often by members and collaborators), and social posts (mostly LinkedIn). `_data/coverage.yml` entries:

```yaml
- date: 2026-05-02
  kind: press            # press | blog | social
  outlet: Example Outlet # for blog and social items, the author's name
  author_person:         # optional person slug when the author is a lab member
  title: How AI is changing pest scouting in the Midwest
  url: https://example.com/story
  note: Features the lab's insect identification tools in extension use.
  papers: []             # optional bibkeys the item discusses
```

- `scripts/coverage_watch.py` plus a weekly Action:
  - Press sources: Google News RSS queries for "Baskar Ganapathysubramanian", "AI Institute for Resilient Agriculture", and "Translational AI Center" Iowa State. Additionally, inspect news.iastate.edu and the AIIRA and TrAC sites once for RSS/Atom feeds and hardcode any found.
  - Blog sources: an opt-in list of member and collaborator blog RSS feeds in `scripts/config.yml`; new posts about the group's work are filed as `kind: blog` candidates.
  - LinkedIn: never scraped. Scraping violates the platform's terms and posts often sit behind login walls, so social items enter only through `/add-mention` (Section 12.4).
  - Follow redirects to resolve final URLs; dedupe against both `coverage.yml` and `coverage_inbox.yml` by URL and normalized title; append candidates to `_data/coverage_inbox.yml` and open a PR titled "coverage: N candidates". Expect false positives; that is what triage is for.
- `/triage-coverage` workflow skill: fetch each inbox item, keep only items genuinely about the group, set `kind`, `author_person`, and `papers`, write the one-line note, move keepers to `coverage.yml`, clear the inbox, open a PR. The PR body lists keepers and dropped items one line each, so review is a quick skim and works from the GitHub mobile app.
- Rendering and prominence:
  - Homepage: the "In the news" strip stays press-only (latest 3 outlets with dates) to keep it authoritative, with one compact "From the group" line beneath it showing the latest member blog or LinkedIn post.
  - News page: the full coverage list, filterable by kind and year with the shared URL-param pattern.
  - Person pages: a "Writing and posts" section listing that member's coverage items, which also gives students visible credit for their outreach.
  - Papers: any bib entry referenced by a coverage item renders small "coverage" links, so a paper shows who is talking about it.
- Consent and curation policy (also write this into CLAUDE.md): member accounts and feeds are strictly opt-in; curate individual items, never embed live feeds, since content on the other end can change and LinkedIn embeds are unreliable; anything a member asks to remove comes down immediately; the weekly external link check (Section 12.1) catches dead links.

Acceptance:
- [ ] Watcher dry-run produces inbox candidates for press and for at least one configured blog feed; triage assigns kinds and dedupes correctly; homepage strips render; person-page and paper coverage links resolve; win badges render for every type.

---

## 11. Homepage

Order: hero (lab name, one-sentence mission, buttons for Publications, Products, Join), selected papers (3 hero cards), recent wins (5, compact with badges), In the news (3) with a "From the group" line, research themes grid (9 chips with live paper counts from papers.json), footer (ISU affiliation, contact, GitHub org).

---

## 12. Automation, CI, and Claude Code assets

### 12.1 GitHub Actions (`.github/workflows/`)

- `deploy.yml`: the theme's stock workflow, with one added step before the Jekyll build: `python scripts/bib_to_json.py`.
- `ci.yml` (on every PR): set up Ruby and Python; run `bib_to_json.py`, then `scripts/validate.py`, then the Jekyll build, then an internal link check with lychee in offline mode against `_site`. This workflow is a required status check.
- `links-external.yml` (weekly): lychee over external links with caching and an allowlist for flaky domains; opens an issue on failures rather than failing PRs.
- `papers-sync.yml` (weekly cron): run `openalex_sync.py --sync`; if new entries exist, create a branch adding bib stubs plus drafted paper wins, and open a PR (use `peter-evans/create-pull-request`). [AMEND-9] Pin every third-party action to a full commit SHA with a trailing comment naming the version (e.g. `@<sha> # v7`), not a moving tag: an action that can open PRs into the repo is a supply-chain surface. Let Dependabot bump the pinned SHAs under review.
- `coverage-watch.yml` (weekly cron): run `coverage_watch.py`; open a PR when candidates exist.
- Branch protection on `main`: PRs required, `ci.yml` required, no force pushes.
- `CODEOWNERS`: assign `_news/`, `_data/coverage.yml`, `_data/coverage_inbox.yml`, and `_impact/` to Baskar's GitHub handle, and enable "require review from Code Owners" in branch protection. This makes Baskar's explicit approval the publication event for news, social, and impact content even after students gain write access to the org; code and papers plumbing can be reviewed by any maintainer. Extend the path list if stricter coverage is wanted later.

### 12.2 `scripts/validate.py` checks (fail CI on violation)

1. Every bib entry has `summary` and 1-3 valid `themes`, except bibkeys listed in `scripts/enrichment_pending.txt` (the Phase 2 rollout allowlist, which must be empty by the end of Phase 3 and stay empty).
2. Every theme slug used anywhere exists in `themes.yml`.
3. Every bibkey referenced by products, impact stories, or wins exists in the bib.
4. Every person and product slug referenced anywhere resolves to a file.
5. Every referenced image exists on disk; every preview and hero image declaration includes alt text.
6. `coverage.yml` URLs are unique, and every `author_person` and `papers` reference in it resolves.
7. [AMEND-1] No em-dash or en-dash characters (U+2014, U+2013) in authored prose fields only: `summary`, `note`, `blurb`, front-matter `title` and `blurb` on people, products, and impact stories, win and story and impact body text, and `_data/*.yml` authored values. Imported bibliographic metadata is exempt and must not be scanned or altered: `title`, `author`, `journal`, `booktitle`, `venue`, and `abbr` in `.bib` entries. The check operates on a field allowlist, not a blanket byte scan of the file.

### 12.3 `CLAUDE.md` (write in Phase 0)

Keep it under one page: what the site is; the source-of-truth table from Section 3; the PR-only rule; the style rules from Section 4 including the dash rule; the instruction to run `make validate` before opening any PR; the never-fabricate rule; the discover-do-not-assume rule; and the list of workflow skills below. `CLAUDE.md` is project memory that Claude Code loads automatically, so anything written here shapes every future session.

### 12.4 Workflow skills (`.claude/skills/<name>/SKILL.md`)

Claude Code loads these as invocable `/name` commands (this skills format is the current recommended replacement for the legacy `.claude/commands/` directory; `$ARGUMENTS` carries whatever follows the command). Create one per workflow, each ending with "run `make validate`, then open a PR; never push to main; touch only the files this workflow owns":

- `enrich-papers`: the Section 6.5 batch procedure.
- `add-win`: draft a win from `$ARGUMENTS` (type plus details), resolve links.
- `triage-coverage`: the Section 10.2 procedure.
- `add-mention`: file a coverage item from `$ARGUMENTS` (a URL, or pasted text plus a URL when the item is login-walled); fetch metadata when possible, set kind, author_person, and papers, draft the note, open a PR.
- `add-product`: scaffold a product file from `$ARGUMENTS`, validate keys.
- `add-impact-story`: scaffold and draft a story per Section 9 style.
- `new-member`: scaffold a person file from `$ARGUMENTS`, add authors.yml variants.
- `graduate-member`: flip role to alumni, add placement, draft a graduation win.
- `sync-report`: summarize open automation PRs and pending TODO(baskar) markers.

Runtime note: these run interactively from any of Baskar's Claude Code machines; the always-on office Mac can run the recurring ones on a schedule. A fully hosted alternative (Anthropic's Claude Code GitHub Action with an API key secret) exists but is optional; verify its current setup at https://docs.claude.com/en/docs/claude-code/overview before adopting it.

### 12.5 Division of labor

Deterministic scripts (sync, watch, json, validate) stay dumb and reliable so nothing is ever silently missed. The LLM writes only prose and classifications (summaries, themes, win text, press notes, stories), always PR-gated.

[AMEND-4] "Nothing is ever silently missed" is a testable claim, so test it. Before Phase 2 output is trusted, cover `openalex_sync` (dedup and bibkey generation), `bib_to_json`, and `normalize_authors` with unit tests over small fixture bibs under `tests/fixtures/`. Minimum fixtures: a preprint-plus-journal pair (asserts published wins and identifiers merge), two name variants of one author (asserts they map to one canonical), a bibkey collision (asserts stable suffixing), and an entry with a null abstract (asserts graceful flag, not crash). Pin script dependency versions in a lockfile (`requirements.txt` with pinned versions or equivalent), in particular `bibtexparser`, whose v1 and v2 APIs differ enough to change parsing behavior silently. Run the tests in `ci.yml` as a required check.

---

## 13. Design direction

Do a real design pass in Phase 6 rather than shipping stock al-folio with a swapped logo. Process: draft a compact token system first (4-6 named palette hexes, a characterful display face paired with a workhorse body face, spacing scale), critique it against the brief below, then implement.

Brief: the subject is computation applied to the physical world: fields, meshes, flows, plants, cities. The audience is prospective students, collaborators, program officers, and policy staff. The signature element should come from that world; strong candidates are a hero built on an actual simulation visualization (a FASTEST flow field or an adaptive mesh render, supplied by Baskar as an image or short loop) or theme chips whose colors form a coherent spectral system across the whole site. Avoid the generic AI-site defaults (cream background with terracotta accent, near-black with one acid accent). A restrained nod to ISU cardinal is welcome; do not clone university branding.

Non-negotiables: dark mode retained; consistent 16:9 preview crops; lazy-loaded images; click-to-load video embeds; visible keyboard focus; reduced motion respected; Lighthouse mobile >= 90 on Home, Publications, and Impact.

---

## 14. Phase plan

Each phase is one or more PRs. A phase is done when its acceptance boxes are checked and CI is green.

[AMEND-6] MVP launch target (approved 2026-07-19): ship Phases 0 through 4 plus a minimal homepage, then launch, then layer the rest. This prevents the site stalling in automation-land before it is publicly useful.

- MVP scope: Phases 0-4 (setup, shells, papers import and filter UI, enrichment of the selected set only, Products and People) plus a minimal homepage (hero with mission and buttons, selected-papers hero cards, research-themes grid with live counts, footer). The full design pass (Section 13) and the coverage, news, impact, briefs, and cron automations are explicitly out of the MVP.
- MVP enrichment: for the MVP, enrich only the selected set from Phase 3 (the 8-12 hero papers). Full enrichment of all 230-plus papers (the rest of Phase 3) continues after the MVP launches; unenriched entries stay on the `enrichment_pending.txt` allowlist so CI passes in the interim.
- MVP launch: run the Phase 8 read-through and Lighthouse check against the MVP surface only, then announce. Post-MVP work resumes at the remainder of Phase 3 and Phases 5 through 7, ending in a second, full launch pass.

- Phase 0: Org, repo from template, Pages via Actions, Docker dev loop, Makefile, CLAUDE.md, docs/PLAN.md. (Acceptance in Section 2.)
- Phase 1: Navigation and page shells, `themes.yml`, `authors.yml` skeleton, config, workflow-skill skeletons.
  - [ ] All nav routes render; validator runs (may pass trivially); skills listed by `/help`.
- Phase 2: Papers import (`--full`), Scholar reconciliation if provided, author normalization, bib_to_json, publications page with full filter UI. (Acceptance in Section 6.)
- Phase 3: Enrichment of all papers in batched PRs; hero figures and video for an initial selected set Baskar picks (8-12 papers). (Acceptance in Section 6.)
- Phase 4: Products and People, seeded per Sections 7-8. (Acceptance in Sections 7-8.)
- Phase 5: Impact page, four stories, stats and briefs scaffolding. (Acceptance in Section 9.)
- Phase 6: News (wins and press), homepage assembly, design pass per Section 13.
  - [ ] Homepage sections all render from live data; design tokens applied site-wide; Lighthouse targets met.
- Phase 7: Automations live (all workflows, branch protection and CODEOWNERS, validator at full strictness); one full dry-run cycle of paper sync and coverage watch reviewed and merged.
  - [ ] Both cron PRs produced, triaged, merged; CI required checks enforced.
- Phase 8: Launch. Full content read-through, resolve every `TODO(baskar)` or explicitly defer to Section 15, Lighthouse re-check, then two manual items for Baskar: ask ISU IT to add a banner or redirect on the old WordPress site pointing to the new URL, and announce (mailing lists, social, AIIRA/TrAC channels).

---

## 15. Deferred backlog

Custom domain (add CNAME and update `url`; use relative links throughout so this stays non-breaking), cookie-free analytics (GoatCounter or Plausible), funded-projects pages, talks and teaching pages, RSS/JSON feed of wins, per-paper OpenGraph images, alumni placement map, hosted scheduled agent runs.

---

## Appendix A: file examples

Bib entry (fictional, format reference only):

```bibtex
@article{doe2025mixing,
  title   = {A resolved-interface method for turbulent droplet mixing},
  author  = {Doe, Jane and Ganapathysubramanian, Baskar},
  journal = {Journal of Computational Physics},
  year    = {2025},
  doi     = {10.0000/example},
  summary = {We develop a solver that captures how droplets break up and merge at resolutions previous methods could not reach. This makes it practical to simulate industrial mixing on ordinary GPU clusters.},
  themes  = {numerics, hpc},
  preview = {doe2025mixing.webp},
  selected= {true}
}
```

Win (graduation):

```yaml
---
date: 2026-08-14
type: graduation
title: Dr. Jane Doe defends her PhD and heads to a national lab
people: [jane-doe]
links:
  url: TODO(baskar)
---
Congratulations to Dr. Jane Doe on completing her PhD on GPU-accelerated
two-phase flow solvers. She joins TODO(baskar) this fall.
```

`_data/stats.yml` skeleton:

```yaml
- key: phds
  label: PhD graduates
  value: TODO(baskar)   # 29+ as of mid-2026; confirm exact count
- key: publications
  label: Peer-reviewed publications
  value: auto           # computed from papers.json at build time
- key: tools
  label: Open tools and apps
  value: auto           # computed from _products with status != archived
- key: reach
  label: People reached through extension and education
  value: TODO(baskar)
```

`_data/coverage.yml` entries (a press item and a member blog post):

```yaml
- date: 2026-05-02
  kind: press
  outlet: Example Outlet
  title: How AI is changing pest scouting in the Midwest
  url: https://example.com/story
  note: Features the lab's insect identification tools in extension use.
- date: 2026-06-11
  kind: blog
  outlet: Jane Doe
  author_person: jane-doe
  title: What we learned building a GPU two-phase flow solver
  url: https://example.com/blog/solver
  note: A student's walkthrough of the ideas behind our JCP paper.
  papers: [doe2025mixing]
```

## Appendix B: per-phase kickoff prompts

- Phase 1: "Read docs/PLAN.md Sections 3-5 and 12.4. Execute Phase 1. Open one PR."
- Phase 2: "Execute Phase 2 per Sections 6.1-6.4. I have placed my Scholar BibTeX export at data-import/scholar.bib (if present). Open PRs for import and normalization separately."
- Phase 3: "Run /enrich-papers. Continue in batches of 25 until enrichment_pending.txt is empty, pausing for my review at each PR."
- Phase 4: "Execute Phase 4. Here is the current roster: <paste>. Scaffold people and products; mark unknowns TODO(baskar)."
- Phase 5: "Execute Phase 5. Draft all four impact stories; every number is TODO until I confirm."
- Phase 6: "Execute Phase 6. Propose the design token system first and wait for my approval before implementing."
- Phase 7: "Execute Phase 7. Trigger both cron workflows manually and walk me through the resulting PRs."
- Phase 8: "Run /sync-report, then produce the launch checklist with every remaining TODO(baskar)."
