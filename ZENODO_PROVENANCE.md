# Provenance — Version 1.1 — 16 September 2026

## Editorial revision

The author supplied 10.5281/zenodo.22802165 as the replacement study identifier and reported removal of the preceding record. All current public-facing files use this DOI. A read-only request to the Zenodo public records API returned HTTP 404 during this revision, so the new record's publication state and remote files were not independently confirmed. The superseded identifier is retained only in private local revision backups. All original scientific data and local historical releases are preserved.

Eight existing Portuguese-language plots were reexported with English labels from archived data. Two existing English publication figures were retained byte for byte. No ODE integration, parameter search, new scientific condition or new data panel was performed. Numeric plotted artists and axis/color limits were hashed before and after label translation, with equality required for each figure. Minor font-size adjustments accommodate English text. The local-dynamics title was narrowed to describe loops and coexisting resting states, avoiding an overstatement of network memory. “Original threshold” was clarified as the archived reference stimulus, and the excitable recruitment label now explicitly says threshold crossing. These clarify the existing interpretation without changing any measured values.

The current English derivatives are under figures/english/; historical Portuguese plots remain unchanged under study/ to retain scientific provenance. ENGLISH_FIGURE_AUDIT.json records the translations and numeric-artist hashes. The reexport script uses only the plotting portions of archived scripts, frozen equilibrium values and the same algebraic current law. It does not import or execute their simulation routines. PNG output is 240 dpi; SVG output is also supplied. The PDF captions no longer need Portuguese-to-English glosses.

The ResearchGate PDF combines the same current manuscript and supplement, with eight embedded figures, separate supplement pagination and bookmarks. It is explicitly an unreviewed preprint. The two additional translated historical figures are distributed in the reproducibility archive. No upload or publication was performed by this preparation.

The author originated the idea and conceived the study. Codex assisted with calculations and figures as already declared, and performed this requested translation, document formatting and archive preparation. It is not an author. Funding, competing interests and license declarations are unchanged.

## Scientific declarations revision

On 16 September 2026, at the author's request, the manuscript availability and declarations section was rewritten in scientific style. Administrative confirmation notes, machine-path handling details and instructions about obtaining a DOI were removed from the manuscript; provenance records retain those details. The public GitHub repository https://github.com/danikratz/bioelectric-history-dependent-state-selection was verified through the GitHub API: at inspection it contained the version 1.0 manuscript and supplement PDFs and project documentation, not the complete reproducibility archive. The manuscript therefore describes GitHub as hosting manuscripts and documentation and identifies Zenodo separately. The declaration of AI assistance includes computational implementation, calculations, figures and manuscript editing; conceptualization remains attributed to Daniela Barbosa Kratz. No new contributorship roles were inferred. Scientific results, figures and numerical data were unchanged. No repository content or publication status was modified remotely.

## Literature, contributorship and change-history revision

On 16 September 2026, the author identified Pezzulo et al. (2021), DOI 10.1098/rstb.2019.0765, as an omitted reference. Bibliographic metadata, the abstract and indexed section 3 excerpts were checked; direct full-text retrieval failed and no supplemental/code review is claimed. The reference was added to the manuscript, bibliography verification and novelty/claim audits, explicitly acknowledging close conceptual precedent. The manuscript now describes the literature assessment as targeted and non-exhaustive. Novelty classification C, numerical results and conclusions remain unchanged.

The version notice now covers English figure labels, revised author declarations, the study Zenodo DOI, the GitHub link and the expanded literature discussion. It does not claim that the remotely deposited v1.0 contained unresolved author declarations: the last preserved local v1.0 already had confirmed declarations, and the remote files were not independently retrieved. “Writing - review and editing” was added based on the author's documented critical review and requests for substantive manuscript corrections. Methodology, formal analysis, investigation, supervision and original-draft authorship were not assigned without evidence of those roles. The AI-assistance disclosure remains unchanged. No new scientific simulations or remote publication actions were performed.

## DOI replacement and distribution

The current Zenodo identifier is 10.5281/zenodo.22802165. This update corrects PDFs, manuscript sources, metadata, citation files and package manifests. The public GitHub companion is updated separately with the current manuscripts and identifier; the full trajectory archive is provided as a Zenodo upload payload rather than committed to GitHub. No scientific data or numerical endpoints were altered. Administrative statements in the historical baseline below refer to their original dates, not to the current DOI status.

## Historical baseline: version 1.0 preparation

The following dated account describes the preceding preparation, before the current editorial and DOI revisions. References to publication being pending or figures not being reexported refer only to that earlier stage.

# Provenance — Version 1.0 — 15 September 2026

## Chronology

Earlier work established a synthetic graph and reduced membrane implementation. Original-network development selected stimulus anchors and repair rankings before the main campaign. Main protocol freeze: 2026-09-14T21:09:27.908685+00:00. Main analyses, additional controls and six numerical corrections were completed and retained. Final validation freeze: 2026-09-15T13:58:30.658348+00:00. The validation's three bounded blocks were completed, including the negative cubic result, before editorial preparation. Both campaigns were closed before this deposit preparation. Manuscript version freeze: 15 September 2026.

These are local protocol freezes, not earlier public preregistrations. Prior knowledge of the original network informed the final validation. No new scientific simulations were executed during Zenodo preparation. Read-only checks of existing outputs, numeric recounting, editorial changes, PDF rendering and packaging are not additional scientific conditions.

## Protocol identities

Original main protocol SHA-256: 5cbb0be57d3d0a06bf0f8ff971c9db2ded15500a959596ed44f1eb7db40680ba.

Original validation protocol SHA-256: a9d5d8078bfef94c02864a6c7753946882259e0846e44b8541cadb715deac4fb.

Public validation copy SHA-256: 25357a76b1e211c2fb90c331ed8f7736ce4db6278c613b63170a97df68ffebef.

The public main protocol has the original bytes. In the public validation protocol only environment.executable was replaced by python3. Four private-path-bearing scientific records (two initial-failure logs, execution metadata, validation protocol) were redacted in the previously prepared public copy. Five dependent integrity records were updated. Nine changed public-copy files are mapped to original hashes in SOURCE_PROVENANCE.json. Original 959 scientific files remain unchanged locally; all scientific NPZ arrays are byte-identical. The public protocol hash must not be represented as the original pre-execution hash. Historical timestamps are preserved as historical evidence, not retroactively assigned to public copies.

## Environment and enumeration

Scientific execution: Python 3.9.6; NumPy 1.26.4; SciPy 1.13.1; Matplotlib 3.7.5; macOS arm64. Numerical requirements are supplied without bundling third-party binaries. PDF preparation uses Python 3.12 and ReportLab; this does not change the scientific execution environment.

Main: 487 labels (144 temporal, 144 memory, 60 sensitivity, 126 repair, nine no-stimulus, four never-restored). Additional main controls and checks retain their separate historical status. Validation: 136 unique network conditions, six isolated protocols, 138 block memberships (65/49/24) with two overlaps. Validation numerical runs: 316 network and 18 isolated. No claim of independent biological replication.

## Verification and retained negatives

Six initial main refinement failures remain alongside accepted higher-precision replacements. Largest initial discrepancy 0.0317561 mV; corrected discrepancy 0.000210172 mV. Validation refinement maximum 0.000214893 mV; 44 Radau comparisons, maximum 1.115049 × 10−11 V, no classification changes. A read-only recount of all 136 existing effective validation trajectories and all 87 paired endpoint comparisons agreed with stored metrics. All 959 original scientific hashes were checked again.

Retained negatives: graded finite-rate lag, absent cubic network recruitment despite isolated bistability/hysteresis, stronger-stimulus and higher-gD loss of the history contrast, random-weakening recruitment in four configurations, a never-restored geometry that recruits, and endpoint-dependent repair ordering. Current novelty classification is C; dated historical wording does not supersede the final manuscript's conservative scope.

## Public selection and integrity

The reproducibility ZIP contains complete scientific campaign trees plus two required earlier inputs, code, relevant figures, environment specification, source/public-copy mapping, current manuscript sources and audit documents. Full arrays are retained once to audit transient behavior, solver comparisons and corrected failures without new simulations. Temporary caches, environments, external full texts, authenticated data, duplicate display folders and journal-planning files are excluded. The archive's per-file manifest is generated before ZIP creation; the outer ZENODO_MANIFEST_SHA256.txt is generated last and covers every upload payload except itself. Any subsequent DOI insertion requires replacing affected documents and regenerating the entire outer manifest.

## Authorship and rights

Daniela Barbosa Kratz confirmed her name, affiliation Univali, ORCID 0000-0001-8364-0246 and public contact dbkratz@gmail.com in this preparation session. She authorized CC BY 4.0 for original text/data/figures and MIT for original code and explicitly confirmed no funding and no competing interests. She subsequently clarified that the research idea and conception were hers, with Codex providing assistance with calculations and figures. The contribution statement was corrected to her explicit account; the earlier inferred list of project-administration and writing-review roles is superseded. Codex is a tool, not an author or the originator of the research idea. For preparation provenance, Codex also assisted in assembling, editing and formatting the manuscript and deposit documentation, checking files and packaging the archive, as recorded in the preparation workflow. This technical assistance is distinct from ownership of the research idea. No additional human contributors are assigned. These administrative corrections do not change scientific results or the manuscript version date; the PDF, ZIP and final hashes are rebuilt.
