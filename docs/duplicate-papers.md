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
| `saurabh2023cyrsoxs` (J. Appl. Cryst.) | `saurabh2022cyrsoxs` (arXiv) | CyRSoXS GPU virtual instrument for P-RSoXS |
| `chiteri2022dissecting` (Frontiers Plant Sci.) | `chiteri2021dissecting` (ISU repo) | Root phenotypic/genotypic variability of Iowa mung bean |
| `rairdin2022deep` (Frontiers Plant Sci.) | `rairdin2022nappn` (NAPPN conf. abstract) | Deep-learning phenotyping + GWAS of soybean sudden death syndrome |
| `cho2021differentiableb` (NeurIPS) | `cho2021differentiable` (ISU repo, "Piecewise Polynomial Functions") | Differentiable spline approximations |

| `riera2021deep` (Plant Phenomics) | `riera2020deep`, `riera2020deepb` (both arXiv) | Deep multiview image fusion for soybean yield estimation |
| `botelho2020deepb` (arXiv) | `botelho2020deep` (ISU repo) | Deep generative models that solve PDEs (distributed training) |

Also note: `chiteri2022nappn` (NAPPN conf. abstract, already enriched) is the conference-abstract precursor of `chiteri2023dissecting` (leaf morphology GWAS) and is a dedup candidate too.

Note: a fuller dedup pass over the whole bibliography (fuzzy-title, arXiv-vs-DOI)
would likely find more; this list is only what enrichment happened to surface.
