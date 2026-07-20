"""Unit tests for the deterministic OpenAlex transform (AMEND-4).

Covers the failure modes that would silently lose or corrupt data:
  - preprint vs published dedup (published wins, identifiers merge)
  - collision-safe, order-independent bibkey generation
  - title normalization used for matching
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import openalex_sync as s  # noqa: E402


def test_normalize_title_ignores_case_punctuation_accents():
    assert s.normalize_title("Kohn-Sham: A Study!") == "kohn sham a study"
    assert s.normalize_title("Navier   Stokes") == "navier stokes"
    assert s.normalize_title("Crème brûlée") == "creme brulee"


def test_first_keyword_skips_stopwords():
    assert s.first_keyword("A Study on the New Solver") == "solver"
    assert s.first_keyword("The") == "paper"


def test_bibkey_is_deterministic_and_collision_safe():
    # Two papers, same first-author surname, same year, same first keyword.
    recs = [
        {"authors": ["Jane Doe"], "year": 2025, "title": "Mixing of droplets",
         "doi": "10.2/b", "openalex_id": "W2"},
        {"authors": ["John Doe"], "year": 2025, "title": "Mixing at scale",
         "doi": "10.1/a", "openalex_id": "W1"},
    ]
    s.assign_bibkeys(recs)
    keys = sorted(r["bibkey"] for r in recs)
    assert keys == ["doe2025mixing", "doe2025mixingb"]
    # Lowest DOI gets the unsuffixed key, regardless of input order.
    low = next(r for r in recs if r["doi"] == "10.1/a")
    assert low["bibkey"] == "doe2025mixing"


def test_dedup_prefers_published_and_merges_arxiv():
    preprint = {"openalex_id": "Wpre", "title": "A resolved-interface method",
                "authors": ["Jane Doe"], "year": 2025, "is_preprint": True,
                "arxiv": "2501.00001", "doi": ""}
    published = {"openalex_id": "Wpub", "title": "A Resolved-Interface Method!",
                 "authors": ["Jane Doe"], "year": 2025, "is_preprint": False,
                 "doi": "10.1016/j.jcp.2025.1", "venue": "JCP"}
    kept, log = s.dedup_records([preprint, published])
    assert len(kept) == 1
    survivor = kept[0]
    assert survivor["openalex_id"] == "Wpub"          # published wins
    assert survivor["doi"] == "10.1016/j.jcp.2025.1"
    assert survivor["arxiv"] == "2501.00001"          # preprint id attached
    assert any("preprint-merged" in line for line in log)


def test_dedup_keeps_standalone_preprint():
    preprint = {"openalex_id": "Wpre", "title": "Unpublished idea",
                "authors": ["Jane Doe"], "year": 2026, "is_preprint": True,
                "arxiv": "2601.00002", "doi": ""}
    kept, _ = s.dedup_records([preprint])
    assert len(kept) == 1
    assert kept[0]["is_preprint"] is True


def test_junk_titles_are_filtered():
    assert s.is_junk_title("MOESM1 of A real-time phenotyping framework")
    assert s.is_junk_title("Additional file 2 of Something")
    assert s.is_junk_title("Supplementary material for X")
    assert not s.is_junk_title("A resolved-interface method for droplet mixing")


def test_dedup_published_keeps_more_complete():
    sparse = {"openalex_id": "Wa", "title": "Same paper", "authors": ["A B"],
              "year": 2024, "is_preprint": False, "doi": ""}
    rich = {"openalex_id": "Wb", "title": "Same Paper", "authors": ["A B"],
            "year": 2024, "is_preprint": False, "doi": "10.5/x", "venue": "J",
            "pages": "1--10"}
    kept, log = s.dedup_records([sparse, rich])
    assert len(kept) == 1
    assert kept[0]["openalex_id"] == "Wb"
    assert any("dup-published" in line for line in log)
