# Duplicate publications to reconcile

Surfaced during enrichment: the same paper appears under multiple bibkeys because
the preprint/repository title differs slightly from the published title, so the
AMEND-3 dedup (normalized-title match) did not catch them. Keep the published
version, merge identifiers, and remove the rest.

| Keep (published) | Duplicates to remove | Paper |
| --- | --- | --- |
| `arshad2024evaluating` (Plant Phenomics) | `arshad2024evaluatingb` (arXiv), `arbab2024evaluating` (ISU repo) | Evaluating NeRFs for 3D Plant Geometry Reconstruction |
| `duke2024mix` (J. Chem. Ed.) | `duke2024mixb` (ISU repo) | In the Mix workshop |
| `gamdha2025gratev2` (Materials Advances) | `gamdha2024gratev2` (arXiv) | GRATEv2 |
| `kim2025soybean` (Plant Phenome J.) | `kim2024soybean` (arXiv) | Soybean maturity from 2D contour plots |
| `rabeh2025benchmarking` (Comms. Eng.) | `rabeh2024geometry` (arXiv, "Geometry Matters") | Benchmarking SciML for flow around complex geometries |
| `jignasu2024stitch` (STITCH) | `jignasu2024sdfconnect` (same work: sparse point cloud + persistent homology, single connected component) | Topology-constrained neural surface reconstruction |
| `chiteri2023dissecting` (Plant Phenome J.) | `chiteri2023dissectingb` (ISU repo) | Genetic architecture of mungbean leaf morphology |
| `berzina2023electrokinetic` (ACS Sensors) | `berzina2022electrokinetic` (ChemRxiv) | Electrokinetic enrichment + electrochemical nucleic acid detection |

Note: a fuller dedup pass over the whole bibliography (fuzzy-title, arXiv-vs-DOI)
would likely find more; this list is only what enrichment happened to surface.
