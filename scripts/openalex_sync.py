#!/usr/bin/env python3
"""Sync Baskar Group publications from OpenAlex into BibTeX.

PLAN.md Section 6.2, with amendments:
  AMEND-2: resolve the author across ALL candidate IDs (OpenAlex fragments a
           person), union their works. Scholar export is the completeness oracle.
  AMEND-3: explicit dedup precedence (published outranks preprint; merge
           identifiers; log every drop or merge, never silently discard).
  AMEND-5: deterministic, collision-safe bibkey generation.

Modes:
  --full   pull all works and write stubs to data-import/openalex.bib
  --sync   append only genuinely new entries to _bibliography/papers.bib
  --dry-run  with --sync, report what would change without writing

The metadata transform (normalize_title, make_bibkey, dedup_records) is pure and
covered by tests/test_openalex_sync.py.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "config.yml"
FULL_OUT = ROOT / "data-import" / "openalex.bib"
PAPERS_BIB = ROOT / "_bibliography" / "papers.bib"

OPENALEX_WORKS = "https://api.openalex.org/works"

# Words never used as the bibkey keyword.
STOPWORDS = {
    "a", "an", "the", "on", "of", "for", "and", "in", "to", "with", "using",
    "via", "based", "from", "by", "at", "as", "is", "are", "toward", "towards",
    "into", "over", "under", "new", "novel", "study", "analysis",
}


# --------------------------------------------------------------------------- #
# Pure helpers (unit-tested)
# --------------------------------------------------------------------------- #
def ascii_fold(text: str) -> str:
    """Lowercase, strip accents, keep alphanumerics only."""
    nfkd = unicodedata.normalize("NFKD", text or "")
    stripped = "".join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", stripped.lower())


def normalize_title(title: str) -> str:
    """Casefold, drop punctuation, collapse whitespace (for dedup matching)."""
    nfkd = unicodedata.normalize("NFKD", title or "")
    stripped = "".join(c for c in nfkd if not unicodedata.combining(c))
    cleaned = re.sub(r"[^a-z0-9]+", " ", stripped.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def first_keyword(title: str) -> str:
    """First significant title word, ascii-folded; 'paper' if none."""
    for word in normalize_title(title).split():
        if word not in STOPWORDS and len(word) > 1:
            folded = ascii_fold(word)
            if folded:
                return folded
    return "paper"


def last_name(author_display: str) -> str:
    """Best-effort surname from an OpenAlex 'First Last' display name."""
    if not author_display:
        return "anon"
    if "," in author_display:  # already 'Last, First'
        surname = author_display.split(",")[0]
    else:
        surname = author_display.split()[-1]
    return ascii_fold(surname) or "anon"


def base_bibkey(record: dict) -> str:
    first_author = record["authors"][0] if record.get("authors") else ""
    year = record.get("year") or "nd"
    return f"{last_name(first_author)}{year}{first_keyword(record.get('title', ''))}"


def assign_bibkeys(records: list) -> None:
    """AMEND-5: assign collision-safe keys in a stable order (base key, then DOI).

    Mutates each record with record['bibkey']. Deterministic: colliding keys get
    suffixes b, c, ... ordered by DOI then OpenAlex id, so keys never depend on
    fetch order.
    """
    groups: dict = {}
    for rec in records:
        groups.setdefault(base_bibkey(rec), []).append(rec)
    for base, group in groups.items():
        group.sort(key=lambda r: (r.get("doi") or "~", r.get("openalex_id") or "~"))
        for i, rec in enumerate(group):
            rec["bibkey"] = base if i == 0 else f"{base}{chr(ord('a') + i)}"


def completeness(record: dict) -> int:
    """Higher is more complete; used to pick the survivor in a dedup group."""
    score = 0
    if record.get("doi"):
        score += 10
    for field in ("venue", "volume", "number", "pages", "year"):
        if record.get(field):
            score += 1
    score += min(len(record.get("authors", [])), 20)
    return score


def merge_identifiers(winner: dict, loser: dict) -> None:
    """Attach the loser's identifiers to the winner without overwriting."""
    for field in ("doi", "arxiv", "url", "venue", "volume", "number", "pages"):
        if not winner.get(field) and loser.get(field):
            winner[field] = loser[field]


def dedup_records(records: list):
    """AMEND-3: dedup with published-over-preprint precedence.

    Returns (kept, log). `kept` is the deduped list; `log` is a list of human
    readable strings describing every merge and drop (nothing is silent).
    """
    log = []
    published = [r for r in records if not r.get("is_preprint")]
    preprints = [r for r in records if r.get("is_preprint")]

    # 1) Dedup published among themselves (by DOI, then normalized title).
    kept_pub: list = []
    by_doi: dict = {}
    by_title: dict = {}
    for rec in published:
        doi = (rec.get("doi") or "").lower()
        ntitle = normalize_title(rec.get("title", ""))
        existing = by_doi.get(doi) if doi else None
        if existing is None:
            existing = by_title.get(ntitle) if ntitle else None
        if existing is None:
            kept_pub.append(rec)
            if doi:
                by_doi[doi] = rec
            if ntitle:
                by_title[ntitle] = rec
        else:
            # Keep the more complete record; merge the other's identifiers.
            if completeness(rec) > completeness(existing):
                merge_identifiers(rec, existing)
                kept_pub[kept_pub.index(existing)] = rec
                for k, v in list(by_doi.items()):
                    if v is existing:
                        by_doi[k] = rec
                for k, v in list(by_title.items()):
                    if v is existing:
                        by_title[k] = rec
                existing, rec = rec, existing
            else:
                merge_identifiers(existing, rec)
            log.append(f"dup-published: kept {existing.get('openalex_id')} "
                       f"dropped {rec.get('openalex_id')} :: {rec.get('title','')[:70]}")

    # 2) Preprints: drop when a published version shares the title (attach arxiv).
    kept_pre: list = []
    pre_by_title: dict = {}
    for rec in preprints:
        ntitle = normalize_title(rec.get("title", ""))
        pub = by_title.get(ntitle)
        if pub is not None:
            if rec.get("arxiv") and not pub.get("arxiv"):
                pub["arxiv"] = rec["arxiv"]
            log.append(f"preprint-merged into {pub.get('bibkey') or pub.get('openalex_id')} "
                       f":: {rec.get('title','')[:70]}")
            continue
        if ntitle in pre_by_title:
            log.append(f"dup-preprint dropped {rec.get('openalex_id')} "
                       f":: {rec.get('title','')[:70]}")
            continue
        kept_pre.append(rec)
        pre_by_title[ntitle] = rec

    return kept_pub + kept_pre, log


# --------------------------------------------------------------------------- #
# OpenAlex fetch + record extraction
# --------------------------------------------------------------------------- #
def load_config():
    import yaml
    with open(CONFIG_PATH) as fh:
        return yaml.safe_load(fh)


def openalex_works(author_ids, mailto):
    """Yield raw work dicts for the OR-union of author_ids, via cursor paging."""
    import requests
    filt = "author.id:" + "|".join(author_ids)
    cursor = "*"
    while cursor:
        params = {"filter": filt, "per-page": 200, "cursor": cursor, "mailto": mailto}
        resp = requests.get(OPENALEX_WORKS, params=params, timeout=60)
        resp.raise_for_status()
        payload = resp.json()
        for work in payload["results"]:
            yield work
        cursor = payload["meta"].get("next_cursor")
        time.sleep(0.2)


def bare_doi(doi_url):
    if not doi_url:
        return ""
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", doi_url, flags=re.I)


def extract_arxiv(work):
    for loc in work.get("locations", []) or []:
        src = (loc.get("source") or {}).get("display_name", "") or ""
        url = loc.get("landing_page_url", "") or ""
        if "arxiv" in src.lower() or "arxiv.org" in url.lower():
            m = re.search(r"(\d{4}\.\d{4,5})", url)
            if m:
                return m.group(1)
    return ""


# Supplementary-material and file-artifact titles that are not publications.
JUNK_TITLE = re.compile(r"^\s*(MOESM\d*|Additional file|Supplementary (file|material|information)|Data (from|for)\b)", re.I)


def is_junk_title(title):
    return bool(JUNK_TITLE.match(title or ""))


def work_to_record(work, include_types, preprint_types):
    wtype = work.get("type", "")
    if wtype not in include_types and wtype not in preprint_types:
        return None
    if is_junk_title(work.get("title", "")):
        return None
    authors = [(a.get("author") or {}).get("display_name", "").strip()
               for a in work.get("authorships", [])]
    authors = [a for a in authors if a]
    loc = work.get("primary_location") or {}
    source = loc.get("source") or {}
    biblio = work.get("biblio") or {}
    pages = ""
    if biblio.get("first_page"):
        pages = biblio["first_page"]
        if biblio.get("last_page"):
            pages += f"--{biblio['last_page']}"
    return {
        "openalex_id": (work.get("id") or "").split("/")[-1],
        "type": wtype,
        "is_preprint": wtype in preprint_types,
        "title": (work.get("title") or "").strip(),
        "authors": authors,
        "year": work.get("publication_year"),
        "venue": (source.get("display_name") or "").strip(),
        "doi": bare_doi(work.get("doi")),
        "arxiv": extract_arxiv(work),
        "volume": biblio.get("volume") or "",
        "number": biblio.get("issue") or "",
        "pages": pages,
        "url": work.get("doi") or (loc.get("landing_page_url") or ""),
    }


BIBTYPE = {"article": "article", "book-chapter": "incollection",
           "conference-paper": "inproceedings", "preprint": "article"}


def bibtex_escape(value):
    return str(value).replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")


def record_to_bibtex(rec):
    entrytype = BIBTYPE.get(rec["type"], "misc")
    lines = [f"@{entrytype}{{{rec['bibkey']},"]
    fields = [("title", rec["title"]),
              ("author", " and ".join(rec["authors"])),
              ("year", rec.get("year")),
              ("journal" if entrytype == "article" else "booktitle", rec.get("venue")),
              ("volume", rec.get("volume")),
              ("number", rec.get("number")),
              ("pages", rec.get("pages")),
              ("doi", rec.get("doi")),
              ("eprint", rec.get("arxiv"))]
    for key, val in fields:
        if val:
            lines.append(f"  {key:8}= {{{bibtex_escape(val)}}},")
    if rec.get("is_preprint"):
        lines.append("  note    = {Preprint},")
    lines.append("  openalex= {%s}," % rec["openalex_id"])
    lines.append("}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #
def gather_records(cfg):
    core_ids = cfg["author"]["openalex_ids"]
    cand_ids = cfg["author"].get("candidate_ids", [])
    include = set(cfg["include_types"])
    preprint = set(cfg["preprint_types"])
    mailto = cfg["mailto"]

    core_raw = {w["id"]: w for w in openalex_works(core_ids, mailto)}
    cand_raw = {}
    if cand_ids:
        for w in openalex_works(cand_ids, mailto):
            if w["id"] not in core_raw:
                cand_raw[w["id"]] = w

    records, candidate_only = [], []
    for wid, work in {**core_raw, **cand_raw}.items():
        rec = work_to_record(work, include, preprint)
        if rec is None:
            continue
        if wid in cand_raw:
            candidate_only.append(rec)
        records.append(rec)
    return records, candidate_only


def run_full(cfg):
    records, candidate_only = gather_records(cfg)
    kept, log = dedup_records(records)
    assign_bibkeys(kept)
    kept.sort(key=lambda r: (-(r.get("year") or 0), r["bibkey"]))
    FULL_OUT.parent.mkdir(parents=True, exist_ok=True)
    header = ("% Generated by scripts/openalex_sync.py --full\n"
              "% Stubs only: summary and themes are added by /enrich-papers (Phase 3).\n\n")
    FULL_OUT.write_text(header + "\n\n".join(record_to_bibtex(r) for r in kept) + "\n")

    print(f"fetched records (papers types): {len(records)}")
    print(f"after dedup:                    {len(kept)}")
    print(f"  merges/drops logged:          {len(log)}")
    print(f"candidate-id-only works:        {len(candidate_only)}")
    for rec in candidate_only:
        note = "IN final set" if rec in kept else "dropped in dedup"
        print(f"    [{note}] {rec.get('openalex_id')} {rec.get('year')} "
              f"{rec.get('title','')[:70]}")
    print(f"wrote {FULL_OUT.relative_to(ROOT)}")


def parse_existing_keys(path):
    """Return (dois, normalized_titles) already present in a bib file."""
    if not path.exists():
        return set(), set()
    import bibtexparser
    with open(path) as fh:
        db = bibtexparser.load(fh)
    dois = {(e.get("doi") or "").lower() for e in db.entries if e.get("doi")}
    titles = {normalize_title(e.get("title", "")) for e in db.entries if e.get("title")}
    return dois, titles


def run_sync(cfg, dry_run):
    records, _ = gather_records(cfg)
    kept, _ = dedup_records(records)
    assign_bibkeys(kept)
    dois, titles = parse_existing_keys(PAPERS_BIB)
    new = [r for r in kept
           if (r.get("doi", "").lower() not in dois)
           and (normalize_title(r.get("title", "")) not in titles)]
    new.sort(key=lambda r: (-(r.get("year") or 0), r["bibkey"]))
    print(f"existing entries: dois={len(dois)} titles={len(titles)}")
    print(f"genuinely new:    {len(new)}")
    for r in new[:50]:
        print(f"    + {r['bibkey']}  {r.get('year')}  {r.get('title','')[:70]}")
    if dry_run:
        print("dry-run: no files written.")
        return
    with open(PAPERS_BIB, "a") as fh:
        for r in new:
            fh.write("\n" + record_to_bibtex(r) + "\n")
    print(f"appended {len(new)} entries to {PAPERS_BIB.relative_to(ROOT)}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sync publications from OpenAlex.")
    ap.add_argument("--full", action="store_true", help="write all stubs to data-import/openalex.bib")
    ap.add_argument("--sync", action="store_true", help="append new entries to _bibliography/papers.bib")
    ap.add_argument("--dry-run", action="store_true", help="with --sync, report only")
    args = ap.parse_args(argv)
    cfg = load_config()
    if args.full:
        run_full(cfg)
    elif args.sync:
        run_sync(cfg, args.dry_run)
    else:
        ap.error("choose --full or --sync")


if __name__ == "__main__":
    main()
