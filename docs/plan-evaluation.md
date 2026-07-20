# Baskar Group Website Plan: Pre-Execution Evaluation

Date: 2026-07-19
Scope: independent review of the master spec before execution is (re)approved.
Method: read the full spec, stress-tested it for data-integrity risks, internal contradictions, sequencing traps, and scope creep. No web research; the plan is self-contained.
Status: all ten findings encoded into the spec. Both open decisions (items 6 and 7) settled on 2026-07-19. Spec is ready to execute Phase 0.

---

## Verdict

The plan is strong and safe to execute, on one condition: apply the four Tier 1 fixes below before Phase 0, because they change scripts and the validator you write early. If you skip them, the failure modes are silent data loss (missing papers, wrongly dropped duplicates) and a CI rule that fails on correct input. None are hard to fix; all are cheap now and expensive later. All four are now applied.

Recommendation: approved for execution with all Tier 1 amendments applied. The two Tier 2 decisions are settled: ship an MVP of Phases 0-4 plus a minimal homepage (item 6), and rebrand fully to "Baskar Group" hosted at `baskar-group.github.io` (item 7). The remaining Tier 2 items are encoded.

---

## What the plan gets right

Worth stating plainly, so the findings read as tuning and not alarm:

- Single-source-of-truth-per-content-type with key-based cross-linking is the correct architecture for safe agent edits. This is the load-bearing idea and it is sound.
- Clear separation between deterministic scripts (sync, watch, json, validate) and LLM prose, all PR-gated.
- Consent and curation policy for people and coverage is thoughtful: opt-in social, no live feeds, no LinkedIn scraping, immediate removal on request.
- Never-fabricate rule with TODO markers, and CODEOWNERS making the PI the publication event for news and impact.
- Phase gating with explicit acceptance criteria per phase.
- Accessibility and performance treated as non-negotiables, not afterthoughts.

---

## Tier 1 findings: fix in the spec before Phase 0

### 1. The dash rule contradicts "never alter titles" and will fail CI on real paper titles

Section 12.2 item 7 forbids U+2013 and U+2014 in any `.md`, `.yml`, or `.bib` "prose field." Imported titles and venues routinely contain real en-dashes: numeric ranges, and named methods such as Kohn-Sham or Navier-Stokes where the source uses an en-dash. Section 6.5 item 4 says never alter titles during enrichment. So a legitimately imported title with an en-dash makes CI fail, and the only way to pass is to violate the no-alter rule.

Fix: scope the dash ban to authored prose only (`summary`, `note`, `blurb`, and story, win, and impact body text) and explicitly exempt bibliographic metadata (`title`, `author`, `journal`, `booktitle`, `venue`, `abbr`). The validator needs a field allowlist, not a blanket byte scan of the file.

### 2. Pinning a single OpenAlex author ID will silently miss papers

OpenAlex frequently fragments one real person into several author IDs (different affiliations, name variants, disambiguation splits). Section 6.2 says pin "the resulting author ID," singular. For a 230-plus paper corpus this risks missing a meaningful slice of works with no error surfaced.

Fix: resolve all candidate author IDs by name plus ISU affiliation, union their works, and pin the set in `scripts/config.yml`. Treat the Google Scholar BibTeX export as the completeness oracle: any Scholar entry not matched in the OpenAlex union is flagged for review, never dropped.

### 3. Preprint and published duplicates can drop the wrong version

arXiv and the journal version of the same paper have different DOIs but near-identical normalized titles. The DOI-then-title dedup in Section 6.2 could keep the preprint and reject the journal record, or the reverse, and the outcome depends on ordering.

Fix: make dedup precedence explicit. A published record (has journal and DOI) outranks a preprint. On a title match to an existing entry, keep the more complete record and attach the other record's identifiers (for example add the arXiv id to the journal entry) rather than discarding either blindly.

### 4. The plan's core safety premise has no tests

Section 12.5 states that deterministic scripts stay reliable so nothing is ever silently missed. But there are no tests for the dedup, key-generation, `bib_to_json`, or normalization logic, which is exactly the code whose failure mode is silent data loss. `validate.py` checks output shape, not transform correctness.

Fix: write unit tests with small fixture bibs before Phase 2 output is trusted. Minimum fixtures: a preprint plus journal pair, two name variants of one author, a bibkey collision, and an entry with a null abstract. Pin script dependency versions (in particular `bibtexparser`, whose v1 and v2 APIs differ) so the transforms are reproducible.

---

## Tier 2 findings: judgment calls

### 5. Bibkey generation is unspecified (encoded)

Auto-generated stubs need a deterministic, collision-safe key rule. `<lastname><year><keyword>` collides when one author has two papers in a year with a similar first keyword. Specify the keyword source (first significant title word) and a disambiguation suffix (b, c, ...) applied in a stable order.

### 6. Launch could stall in automation-land (decided: MVP adopted)

The coverage pipeline (press, blog, social), policy briefs, impact stats sourcing, and nine workflow skills are a large surface. The value of the site is mostly Papers plus People plus a real homepage. Decision: ship an explicit MVP equal to Phases 0 through 4 plus a minimal homepage, then layer coverage, briefs, and automation. Encoded as AMEND-6 in Section 14.

### 7. URL and branding (decided: full rebrand, github.io for now)

The path is `me.iastate.edu/bglab`, then the new org URL, then optionally a custom domain later. Decision: rebrand fully to "Baskar Group" and host at `baskar-group.github.io`; retire the "ComPM Lab" / Computational Physics and Mechanics name. A custom domain stays deferred (Section 15); relative links keep that non-breaking. Encoded as AMEND-7 in Section 2. Note: this trades away the plan's original argument for a lab-named org (`compm-lab`) in favor of a PI-named group, which is a common and reasonable convention; the org (not personal account) rationale still holds.

### 8. "Zero unmapped authors" is unrealistic and unnecessary (encoded)

230 papers means hundreds of distinct coauthor strings. `validate.py` only needs person-slug mappings for lab members. Canonicalize lab members plus frequent collaborators; let the long tail render as raw strings. Chasing literal zero is busywork with no reader-facing payoff.

### 9. Pin third-party GitHub Actions to a commit SHA (encoded)

`peter-evans/create-pull-request` is pinned to "latest major release," which is a moving tag. An action that can open PRs into your repo is worth SHA-pinning (with a comment noting the version) to close a supply-chain path. Dependabot can bump the SHA under review.

### 10. Abstract availability will be low for this lab's venues (encoded)

Many Elsevier venues (JCP, CMAME) do not supply abstracts to OpenAlex, so `abstract_inverted_index` will often be null exactly where this lab publishes. Expect enrichment to lean heavily manual. Add Crossref and Semantic Scholar as fallback abstract sources, and elevate the Scholar export from optional to recommended (it doubles as the completeness oracle from finding 2).

---

## Spec amendments applied in this pass

All ten findings are applied directly to the master spec under a visible Amendments changelog near the top, each tagged inline with `[AMEND-N]`. The original approved text is preserved in git history once the repo is initialized.

## Status

Both former open decisions are settled: MVP scope (item 6) and full rebrand to Baskar Group at `baskar-group.github.io` (item 7). The plan is ready to execute Phase 0.
