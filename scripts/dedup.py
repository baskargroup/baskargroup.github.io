#!/usr/bin/env python3
"""Reconcile the duplicate sets logged in docs/duplicate-papers.md.

For each set: keep the published (or canonical arXiv) entry, merge the arXiv
`eprint` identifier from a removed copy into the kept entry if it lacks one
(preserving the preprint pointer), then delete the duplicate entries. Also
drops the removed keys from the enrichment allowlist.
"""
import re
from pathlib import Path

ROOT = Path("/Users/baskarg/Dropbox/work/Projects/ClaudeCode/BaskarGroupWebsite")
BIB = ROOT / "_bibliography" / "papers.bib"
PENDING = ROOT / "scripts" / "enrichment_pending.txt"

KEEP_DUPS = {
 "arshad2024evaluating": ["arshad2024evaluatingb", "arbab2024evaluating"],
 "duke2024mix": ["duke2024mixb"],
 "gamdha2025gratev2": ["gamdha2024gratev2"],
 "kim2025soybean": ["kim2024soybean"],
 "rabeh2025benchmarking": ["rabeh2024geometry"],
 "jignasu2024stitch": ["jignasu2024sdfconnect"],
 "chiteri2023dissecting": ["chiteri2023dissectingb", "chiteri2022nappn"],
 "berzina2023electrokinetic": ["berzina2022electrokinetic"],
 "saurabh2023cyrsoxs": ["saurabh2022cyrsoxs"],
 "chiteri2022dissecting": ["chiteri2021dissecting"],
 "rairdin2022deep": ["rairdin2022nappn"],
 "cho2021differentiableb": ["cho2021differentiable"],
 "riera2021deep": ["riera2020deep", "riera2020deepb"],
 "botelho2020deepb": ["botelho2020deep"],
 "kommajosula2019high": ["kommajosula2019highb"],
 "gao2018multirobotb": ["gao2018multirobot"],
 "pokuri2022algorithm": ["pokuri2018paryopt", "pokuri2018paryoptb"],
 "pokuri2019interpretable": ["pokuri2018interpretable"],
 "sharma2018transferb": ["sharma2018transfer"],
 "nagasubramanian2019plant": ["nagasubramanian2018explaining"],
 "shook2021crop": ["shook2018integrating"],
 "nagasubramanian2018hyperspectral": ["nagasubramanian2017hyperspectral", "nagasubramanian2017hyperspectralb"],
 "dyja2018parallel": ["dyja2016massively"],
 "busch2011near": ["busch2011rapid"],
 "wodo2011graph": ["wodo2011graphb"],
}

text = BIB.read_text()

def find_block(key):
    """Return (start, end, block_text) for @type{key, ... \n}"""
    m = re.search(r"@\w+\{" + re.escape(key) + r",", text)
    if not m:
        return None
    start = m.start()
    # find the closing "\n}" that ends this entry
    end = text.index("\n}", start) + 2
    return start, end, text[start:end]

def get_field(block, field):
    m = re.search(r"\n\s*" + field + r"\s*=\s*\{([^}]*)\}", block)
    return m.group(1) if m else None

missing, removed, merged = [], [], []

# 1) merge eprint into keeps that lack one
for keep, dups in KEEP_DUPS.items():
    kb = find_block(keep)
    if not kb:
        missing.append(("KEEP", keep)); continue
    ks, ke, kblock = kb
    if get_field(kblock, "eprint") is None:
        eprint = None
        for d in dups:
            db = find_block(d)
            if db and get_field(db[2], "eprint"):
                eprint = get_field(db[2], "eprint"); break
        if eprint:
            # insert eprint line before the closing brace of the keep block
            new_kblock = kblock[:-2] + f"  eprint  = {{{eprint}}},\n}}"
            text = text[:ks] + new_kblock + text[ke:]
            merged.append((keep, eprint))

# 2) delete duplicate blocks (recompute positions each time since text mutates)
for keep, dups in KEEP_DUPS.items():
    for d in dups:
        db = find_block(d)
        if not db:
            missing.append(("DUP", d)); continue
        s, e, _ = db
        # swallow the blank line that follows the entry, if any
        tail = text[e:e+2]
        cut = e + (1 if tail.startswith("\n") else 0)
        text = text[:s] + text[cut:]
        removed.append(d)

BIB.write_text(text)

# 3) drop removed keys from the enrichment allowlist
rem = set(removed)
keep_lines = [l for l in PENDING.read_text().splitlines() if l.strip() and l.strip() not in rem]
PENDING.write_text("\n".join(keep_lines) + "\n")

print(f"merged eprint into {len(merged)} kept entries:")
for k, e in merged:
    print(f"   {k}  <- arXiv:{e}")
print(f"removed {len(removed)} duplicate entries")
if missing:
    print("MISSING (not found):")
    for kind, k in missing:
        print(f"   {kind} {k}")
