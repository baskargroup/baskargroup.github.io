"""Unit tests for the author-name normalizer (AMEND-4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import bib_to_json as b  # noqa: E402


def test_norm_key_ignores_middle_names_and_order():
    # middle initial, plain, and "Last, First" all collapse to first+last
    assert b.norm_key("Makrand A. Khanwale") == "makrand khanwale"
    assert b.norm_key("Makrand Khanwale") == "makrand khanwale"
    assert b.norm_key("Khanwale, Makrand") == "makrand khanwale"


def test_norm_key_keeps_initial_forms_distinct():
    # an initial-only first name is a different key (avoids homonym over-matching)
    assert b.norm_key("B. Ganapathysubramanian") == "b ganapathysubramanian"


def test_norm_key_strips_accents_and_punctuation():
    assert b.norm_key("José Peña") == "jose pena"
