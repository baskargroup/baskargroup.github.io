#!/usr/bin/env python3
"""Emit assets/json/papers.json from the bibliography (PLAN.md Section 6.4).

papers.json is the substrate for the publications filter UI and for cross-queries
on product, person, and theme pages. Run as a build step and via `make json`.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS_BIB = ROOT / "_bibliography" / "papers.bib"
AUTHORS_YML = ROOT / "_data" / "authors.yml"
OUT = ROOT / "assets" / "json" / "papers.json"


def load_author_map():
    """Return {variant_lower: (canonical, person_slug_or_None)}."""
    import yaml
    mapping = {}
    if AUTHORS_YML.exists():
        for row in yaml.safe_load(AUTHORS_YML.read_text()) or []:
            canonical = row.get("canonical", "")
            person = row.get("person")
            for variant in [canonical, *row.get("variants", [])]:
                if variant:
                    mapping[variant.strip().lower()] = (canonical, person)
    return mapping


def split_authors(field):
    return [a.strip() for a in re.split(r"\s+and\s+", field or "") if a.strip()]


def canonicalize(authors, author_map):
    canon, members = [], []
    for name in authors:
        canonical, person = author_map.get(name.lower(), (name, None))
        canon.append(canonical)
        if person:
            members.append(person)
    return canon, members


def split_themes(field):
    return [t.strip() for t in re.split(r"[,\s]+", field or "") if t.strip()]


# Non-arXiv preprint-server DOI prefixes (mirrors scripts/flag_unverified.py).
PREPRINT_DOI = {"10.1101", "10.21203", "10.2139", "10.22541", "10.26434",
                "10.31219", "10.31234", "10.36227", "10.20944"}


def classify_status(entry):
    """published | preprint | other, for the publications status facet."""
    doi = (entry.get("doi") or "").lower()
    arxiv = entry.get("eprint") or ""
    is_preprint_note = "preprint" in (entry.get("note") or "").lower()
    if arxiv or doi.startswith("10.48550/arxiv") or is_preprint_note:
        return "preprint"
    prefix = doi.split("/")[0] if doi else ""
    if prefix in PREPRINT_DOI:
        return "preprint"
    if doi:
        return "published"
    return "other"


def build():
    import bibtexparser
    author_map = load_author_map()
    with open(PAPERS_BIB) as fh:
        db = bibtexparser.load(fh)

    papers = []
    for e in db.entries:
        authors = split_authors(e.get("author", ""))
        canon, members = canonicalize(authors, author_map)
        papers.append({
            "bibkey": e.get("ID", ""),
            "title": e.get("title", "").strip("{} "),
            "authors": canon,
            "members": sorted(set(members)),
            "year": int(e["year"]) if e.get("year", "").isdigit() else None,
            "venue": e.get("journal") or e.get("booktitle") or "",
            "doi": e.get("doi", ""),
            "url": e.get("url", ""),
            "themes": split_themes(e.get("themes", "")),
            "summary": e.get("summary", "").strip(),
            "selected": e.get("selected", "").strip().lower() == "true",
            "preview": e.get("preview", "").strip(),
            "status": classify_status(e),
        })
    papers.sort(key=lambda p: (-(p["year"] or 0), p["bibkey"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(papers, indent=2, ensure_ascii=False) + "\n")

    # Theme counts for the homepage research grid (only enriched papers count).
    counts = {}
    for p in papers:
        for t in p["themes"]:
            counts[t] = counts.get(t, 0) + 1
    tc = ROOT / "_data" / "theme_counts.yml"
    tc.write_text("".join(f"{k}: {v}\n" for k, v in sorted(counts.items())))
    print(f"wrote {OUT.relative_to(ROOT)} with {len(papers)} entries; "
          f"theme_counts for {len(counts)} themes")


if __name__ == "__main__":
    build()
