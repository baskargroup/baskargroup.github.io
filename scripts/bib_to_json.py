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
        })
    papers.sort(key=lambda p: (-(p["year"] or 0), p["bibkey"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(papers, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} with {len(papers)} entries")


if __name__ == "__main__":
    build()
