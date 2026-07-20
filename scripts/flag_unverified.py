#!/usr/bin/env python3
"""Flag bib entries that are NOT a published journal/conference and NOT on arXiv.

An entry passes when it is either:
  - on arXiv (has an `eprint` arxiv id, or a DOI under 10.48550/arxiv), or
  - published (has a DOI whose prefix is NOT a known non-arXiv preprint server).

Everything else is flagged for human review: no identifier at all, or only a
preprint-server DOI (bioRxiv, Research Square, SSRN, Authorea, ChemRxiv, OSF,
TechRxiv, Preprints.org). Writes a review report and prints a summary.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "_bibliography" / "papers.bib"
REPORT = ROOT / "docs" / "publications-review.md"

# DOI prefixes that are preprint servers other than arXiv.
PREPRINT_DOI = {
    "10.1101": "bioRxiv/medRxiv",
    "10.21203": "Research Square",
    "10.2139": "SSRN",
    "10.22541": "Authorea",
    "10.26434": "ChemRxiv",
    "10.31219": "OSF",
    "10.31234": "OSF",
    "10.36227": "TechRxiv",
    "10.20944": "Preprints.org",
}


def classify(entry):
    doi = (entry.get("doi") or "").lower()
    arxiv = entry.get("eprint") or ""
    venue = entry.get("journal") or entry.get("booktitle") or ""
    is_arxiv = bool(arxiv) or doi.startswith("10.48550/arxiv")
    prefix = doi.split("/")[0] if doi else ""
    if is_arxiv:
        return "arxiv", venue
    if doi and prefix not in PREPRINT_DOI:
        return "published", venue
    if prefix in PREPRINT_DOI:
        return f"preprint-only ({PREPRINT_DOI[prefix]})", venue
    return "no-identifier", venue


def main():
    import bibtexparser
    with open(BIB) as fh:
        entries = bibtexparser.load(fh).entries
    flagged = []
    counts = {"arxiv": 0, "published": 0}
    for e in entries:
        status, venue = classify(e)
        if status in ("arxiv", "published"):
            counts[status] += 1
        else:
            flagged.append((e.get("ID", ""), status, e.get("year", ""),
                            e.get("title", "").strip("{} "), venue))
    flagged.sort(key=lambda r: (r[1], -int(r[2]) if str(r[2]).isdigit() else 0))

    lines = ["# Publications to review",
             "",
             f"Total entries: {len(entries)}. On arXiv: {counts['arxiv']}. "
             f"Published (journal/conference DOI): {counts['published']}. "
             f"Flagged: {len(flagged)}.",
             "",
             "These are neither on arXiv nor backed by a journal/conference DOI. "
             "Review each: keep, add a DOI/arXiv id, or remove.",
             "",
             "| bibkey | status | year | title | venue |",
             "| --- | --- | --- | --- | --- |"]
    for key, status, year, title, venue in flagged:
        t = (title[:80] + "...") if len(title) > 80 else title
        lines.append(f"| `{key}` | {status} | {year} | {t} | {venue} |")
    REPORT.write_text("\n".join(lines) + "\n")

    print(f"total={len(entries)} arxiv={counts['arxiv']} "
          f"published={counts['published']} flagged={len(flagged)}")
    by_status = {}
    for _, status, *_ in flagged:
        by_status[status] = by_status.get(status, 0) + 1
    for status, n in sorted(by_status.items()):
        print(f"  {status}: {n}")
    print(f"wrote {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
