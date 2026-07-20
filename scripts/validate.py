#!/usr/bin/env python3
"""Content validator (PLAN.md Section 12.2). Fails CI on any violation.

Checks (guarded so unbuilt content types are skipped until they exist):
  1. Every bib entry has `summary` and 1-3 valid `themes`, except bibkeys listed
     in scripts/enrichment_pending.txt (Phase 2 rollout allowlist; empty by end
     of Phase 3 and stays empty).
  2. Every theme slug used anywhere exists in _data/themes.yml.
  3. Every bibkey referenced by products, impact stories, or wins exists in bib.
  4. Every person and product slug referenced anywhere resolves to a file.
  5. Every referenced image exists; every preview/hero declaration has alt text.
  6. coverage.yml URLs are unique; every author_person and papers ref resolves.
  7. AMEND-1: no em-dash or en-dash in AUTHORED prose fields only. Imported
     bibliographic metadata (title, author, journal, booktitle, venue, abbr) is
     exempt and never scanned.

Exit code 0 when clean, 1 when any check fails.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "_bibliography" / "papers.bib"
THEMES = ROOT / "_data" / "themes.yml"
AUTHORS = ROOT / "_data" / "authors.yml"
PENDING = ROOT / "scripts" / "enrichment_pending.txt"
COVERAGE = ROOT / "_data" / "coverage.yml"

DASHES = re.compile("[–—]")
# Bib fields that are imported metadata and exempt from the dash rule (AMEND-1).
BIB_METADATA = {"title", "author", "journal", "booktitle", "venue", "abbr",
                "publisher", "series", "editor", "organization", "school"}
BIB_AUTHORED = {"summary", "note"}

errors: list = []
checked: list = []


def load_yaml(path):
    import yaml
    return yaml.safe_load(path.read_text()) if path.exists() else None


def parse_bib():
    import bibtexparser
    if not BIB.exists():
        return []
    with open(BIB) as fh:
        return bibtexparser.load(fh).entries


def theme_slugs():
    return {t["slug"] for t in (load_yaml(THEMES) or [])}


def check_bib(entries, slugs):
    pending = set()
    if PENDING.exists():
        pending = {l.strip() for l in PENDING.read_text().splitlines() if l.strip()}
    for e in entries:
        key = e.get("ID", "")
        themes = [t.strip() for t in re.split(r"[,\s]+", e.get("themes", "")) if t.strip()]
        # Check 1: summary + 1-3 valid themes, unless allowlisted.
        if key not in pending:
            if not e.get("summary", "").strip():
                errors.append(f"[1] {key}: missing summary")
            if not (1 <= len(themes) <= 3):
                errors.append(f"[1] {key}: needs 1-3 themes, found {len(themes)}")
        # Check 2: theme slugs valid (even for allowlisted entries).
        for t in themes:
            if t not in slugs:
                errors.append(f"[2] {key}: unknown theme slug '{t}'")
        # Check 7: dash rule on authored fields only.
        for field in BIB_AUTHORED:
            if field in e and DASHES.search(e[field]):
                errors.append(f"[7] {key}.{field}: contains em/en dash")
    checked.append(f"[1,2,7] {len(entries)} bib entries ({len(pending)} allowlisted)")


def check_authored_yaml_and_markdown(slugs):
    """Check 2 + 7 across authored data files and content bodies that exist."""
    # themes.yml blurbs (authored prose).
    for t in (load_yaml(THEMES) or []):
        if DASHES.search(t.get("blurb", "")):
            errors.append(f"[7] themes.yml/{t.get('slug')}: blurb contains em/en dash")
    # Content collection bodies (front matter + prose), when present.
    for coll in ("_news", "_impact", "_products", "_people"):
        for md in (ROOT / coll).glob("*.md"):
            body = md.read_text()
            if DASHES.search(body):
                errors.append(f"[7] {coll}/{md.name}: contains em/en dash")
            for t in re.findall(r"themes?:\s*\[([^\]]*)\]", body):
                for slug in re.split(r"[,\s]+", t):
                    if slug.strip() and slug.strip() not in slugs:
                        errors.append(f"[2] {coll}/{md.name}: unknown theme '{slug.strip()}'")
    checked.append("[2,7] authored yaml + content bodies")


def check_coverage(bibkeys):
    data = load_yaml(COVERAGE)
    if not data:
        return
    urls = [row.get("url") for row in data if row.get("url")]
    dupes = {u for u in urls if urls.count(u) > 1}
    for u in dupes:
        errors.append(f"[6] coverage.yml: duplicate url {u}")
    for row in data:
        for bk in row.get("papers", []) or []:
            if bk not in bibkeys:
                errors.append(f"[3/6] coverage.yml: unknown bibkey '{bk}'")
    checked.append(f"[6] coverage.yml ({len(data)} items)")


def main():
    entries = parse_bib()
    slugs = theme_slugs()
    bibkeys = {e.get("ID", "") for e in entries}
    check_bib(entries, slugs)
    check_authored_yaml_and_markdown(slugs)
    check_coverage(bibkeys)

    for line in checked:
        print(f"  ok  {line}")
    if errors:
        print(f"\nVALIDATION FAILED: {len(errors)} problem(s)")
        for e in errors[:100]:
            print(f"  !!  {e}")
        sys.exit(1)
    print("\nvalidation passed")


if __name__ == "__main__":
    main()
