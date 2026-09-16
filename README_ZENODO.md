# Title

History-dependent state selection after transient coupling loss in a conductance-based bioelectric network

# Version

Version 1.1 — 16 September 2026. Author: Daniela Barbosa Kratz, Univali. ORCID: https://orcid.org/0000-0001-8364-0246. Scientific preprint; Zenodo deposit does not constitute peer review.

# Scientific question

Can transient perturbation of intercellular coupling alter stable electrical state selection even after exact restoration of the original weighted network connectivity?

# Main result

In the tested synthetic conductance-based network, transient perturbation of intercellular coupling altered stable state selection even after exact restoration of the original weighted connectivity. Networks with identical final weighted adjacency, identical membrane equations and zero final external input reached distinct stable electrical states depending on their preceding coupling history. The lower-stimulus contrast occurred in five specified configurations and 24/42 sampled conductance–restoration comparisons.

# Negative cubic control

The cubic model had two stable equilibria, an intermediate unstable equilibrium and hysteretic switching, yet no receiver recruitment or history-dependent network endpoint under the fixed protocol. Bistability and hysteresis alone were insufficient to produce network-level history dependence under the fixed stimulation protocol.

# Scope

Synthetic reduced conductance-based ODE networks, 226 nodes and 622 undirected edges; 487 main labeled cases plus 136 final-validation networks and six isolated protocols. Existing calibrated biological tissue dynamics, morphogenesis and anatomical memory were not established. No new scientific simulations were performed for this release.

# Limitations

Synthetic regenerative current, approximate potassium kinetics, correlated geometries, earlier original-network selection of anchors, unmatched cubic excitation strength, operational recruitment thresholds and local rather than global stability evidence. Numerical runs are not biological replicates. Priority of the exact restoration comparison remains unresolved; novelty classification C is conservative.

# Files in this deposit

- History_Dependent_State_Selection_v1.1.pdf: scientific manuscript and five reused figures.
- History_Dependent_State_Selection_Supplement_v1.1.pdf: methods, controls, verification and three reused figures.
- History_Dependent_State_Selection_Reproducibility_v1.1.zip: scientific source trees, trajectories, metrics, protocols, code, figure sources, licenses and audit records.
- README_ZENODO.md: this guide.
- ZENODO_PROVENANCE.md: chronology, source/public-copy hashes and preparation scope.
- ZENODO_MANIFEST_SHA256.txt: SHA-256 of the five upload payload files, excluding the manifest itself.

# Reproducibility

Extract the ZIP into a new directory. Run `python3 verify_bundle.py` there to verify its per-file hashes without any simulation. The script prints one compact PASS/FAIL summary and exits nonzero on mismatch. The outer manifest can be checked with `shasum -a 256 -c ZENODO_MANIFEST_SHA256.txt` from the upload directory.

For optional independent reruns, first install the pinned scientific dependencies in a separate Python 3.9 environment. The following archived commands create new sibling output directories and refuse overwriting. They are supplied for readers; they were not executed during deposit preparation.

`python study/transmissao_memoria_histerese/reproduzir.py main_rerun --run`

`python study/validacao_generalizacao_2026-09/reproduzir_validacao.py validation_rerun --run`

Omit --run to prepare only. Main reproduction covers the 487-case experiment, refinement and six-case correction; it does not automatically repeat every historical exploratory, isolated-ramp, additional-control or spatial perturbation procedure. Those original scripts and existing outputs remain in the main tree. Validation reproduction covers its 136 networks, six isolated protocols, analysis and audits. Report generation and visual inspection are not automatically certified by execution success. Never run analysis scripts in the archived folders if you intend to preserve byte identity; use a working copy.

`python source_code/figuras_publicacao.py` reexports the two existing English figures from archived arrays only into figures/. This changes output files and therefore invalidates the internal manifest unless it is regenerated. It does not integrate the model. Other original figure routines are in each scientific tree and may also rewrite derived files; inspect and run only in a copy.

Effective main records: metricas_conferidas.csv and resultados_conferidos.jsonl, with six replacements under precisao_corrigida. Effective validation records: resultados_conferidos_validacao.jsonl and each record's effective_source trajectory, currently refinadas. Historical initial failures are intentionally retained. Current interpretation is the v1.1 manuscript, not superseded exploratory wording.

# Software environment

Scientific execution: Python 3.9.6, NumPy 1.26.4, SciPy 1.13.1, Matplotlib 3.7.5 on macOS arm64. requirements-reproduction.txt specifies the three Python packages. It is a version specification, not a fully locked operating-system or BLAS image; cross-platform roundoff is possible. Libraries are not redistributed. Original text/data/figures use CC BY 4.0; original code uses MIT. See LICENSE_DATA.md, LICENSE_CODE.txt and THIRD_PARTY_NOTICES.md inside the ZIP.

# Frozen protocols

Main local freeze: 14 September 2026, 21:09:27.908685 UTC. SHA-256: 5cbb0be57d3d0a06bf0f8ff971c9db2ded15500a959596ed44f1eb7db40680ba.

Validation local freeze: 15 September 2026, 13:58:30.658348 UTC. Original SHA-256: a9d5d8078bfef94c02864a6c7753946882259e0846e44b8541cadb715deac4fb. Public redacted copy SHA-256: 25357a76b1e211c2fb90c331ed8f7736ce4db6278c613b63170a97df68ffebef. Only the private executable path was changed in this protocol. The source/public mapping and dependent manifest changes are documented; these local freezes were not prior public preregistrations.

# Numerical verification

Six initial main refinement failures were preserved and corrected without relaxing tolerance or changing classification. All 136 final-validation networks passed refinement; 44 Radau comparisons retained classifications. Existing validation trajectories and 87 endpoint pairs were independently recounted during preparation; original scientific hashes remained unchanged. See audits/ZENODO_NUMERIC_AUDIT.md and the original numerical records in the ZIP.

# Citation

Kratz, Daniela Barbosa (2026). History-dependent state selection after transient coupling loss in a conductance-based bioelectric network. Version 1.1. Scientific preprint and reproducibility materials. Zenodo identifier: https://doi.org/10.5281/zenodo.22802165.

# Contact

Daniela Barbosa Kratz — Univali. dbkratz@gmail.com. ORCID: https://orcid.org/0000-0001-8364-0246.

# Version 1.1 revision

Version 1.1 translates figure labels into English, updates author declarations, updates the Zenodo DOI and GitHub link, and expands the prior-literature discussion. Numerical results and conclusions are unchanged. Revision date: 16 September 2026. Use figures/english/ for current figures; Portuguese images in study/ are preserved historical outputs. The archive supplies all ten current PNG figures, ten SVGs, the eight-figure translation audit and source_code/render_english_figures.py. Run the latter with `--study-root study --output english_reexport` to write derivatives to a separate directory, without integrating any model. See ZENODO_PROVENANCE.md for the revision history and limits of verification.

The current main PDF contains Figures 1–5; the supplement contains Figures S1–S3. A separate ResearchGate PDF combines those two documents. None has been peer reviewed. The current study identifier is 10.5281/zenodo.22802165.

# Project repository

Manuscripts and project documentation: https://github.com/danikratz/bioelectric-history-dependent-state-selection. The repository is public and is maintained as the manuscript and documentation companion. The full computational archive is distributed with the Zenodo deposit; do not assume that all trajectories or source files are mirrored on GitHub. The local version 1.1 manuscript also replaces preparation notes with standard data-availability and scientific declarations.

The prior-literature discussion now cites Pezzulo et al. (2021), DOI 10.1098/rstb.2019.0765. Literature coverage remains targeted and non-exhaustive. Author contributions state conceptualization and writing review/editing, supported by the documented contribution and manuscript revision history.

# DOI replacement

The author supplied 10.5281/zenodo.22802165 as the replacement study identifier after reporting removal of the preceding record. All current manuscript links and citation metadata use this identifier. The Zenodo public API returned HTTP 404 during preparation, so public availability was not independently confirmed. Earlier local releases are retained only as historical backups; they are not the upload package for this identifier.
