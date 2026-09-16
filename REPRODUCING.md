# Reproducing figures and auditing the study

Study identifier: [10.5281/zenodo.22802165](https://doi.org/10.5281/zenodo.22802165). Manuscript version 1.1.

## 1. Reproduce the figures from archived results

The GitHub checkout includes all inputs needed for the ten current figures. No Zenodo download, ODE integration or new parameter search is needed for this step.

Use Python 3.9 (the original environment was Python 3.9.6), with the pinned NumPy, SciPy and Matplotlib versions. From the repository root:

```bash
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-reproduction.txt
python scripts/reproduce_figures.py
python scripts/check_reproduced_figures.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

The first command writes two figures to `figures/` and eight English reexports to `figures/english/`, each as PNG and SVG. These output directories are ignored by Git. The check compares the eight reexports' numerical artists with the archived audit and compares all ten PNG files with the original release hashes. SVG byte identity is not expected because generated IDs and metadata can vary. PNG differences can arise from platform, font or renderer differences; if numerical artists agree but PNG bytes differ, inspect the visual differences rather than treating the mismatch as scientific validation or invalidation.

The complete process was executed during repository preparation using the pinned original environment: all ten PNG files matched the frozen release byte for byte, and all eight numerical-artist fingerprints matched. This verifies reproducibility of the archived plots, not biological validity or an independent repeat of the simulations.

## Figure-to-code map

| Manuscript figure | Output | Code and frozen inputs |
|---|---|---|
| Figure 1 | `figures/fig1_hysteresis_equilibria` | `source_code/figuras_publicacao.py`; local ramp trajectories and equilibria |
| Figure 2 | `figures/fig2_identical_final_graph` | Same script; original graph and archived cases 0147/0159 |
| Figure 3 | `figures/english/fig_generalizacao_geometrias` | `source_code/render_english_figures.py`; frozen geometry, metrics and exact final voltage arrays |
| Figure 4 | `figures/english/fig_mapa_regime` | Same renderer; archived paired grid results |
| Figure 5 | `figures/english/fig_mecanismo_alternativo` | Same renderer; frozen model constants, equilibria and endpoint metrics |
| Figure S1 | `figures/english/02_memoria_recrutamento` | Same renderer; main-campaign checked metrics |
| Figure S2 | `figures/english/03_trajetorias` | Same renderer; archived compact response arrays |
| Figure S3 | `figures/english/04_reparos` | Same renderer; archived partial-repair metrics |
| Additional historical plot | `figures/english/01_histerese` | Same renderer; archived local ramp trajectories |
| Additional historical plot | `figures/english/05_estados_espaciais` | Same renderer; original graph and archived cases 0147/0159 |

## 2. What is included in GitHub

- `study/`: the 19 original scientific Python files, frozen protocols, scientific reports, metrics, numerical-check records and selected binary inputs. These are byte-identical to the existing sanitized public archive, as recorded in `CODE_PROVENANCE.json`.
- `source_code/figuras_publicacao.py`: the original two-figure publication script, unmodified.
- `source_code/archived/render_english_figures_v1.1.py`: the unmodified English-label renderer from the release.
- `source_code/render_english_figures.py`: that same renderer with an explicitly documented optional endpoint-cache argument for the lightweight GitHub checkout. It reuses the original scientific plotting blocks and changes no plotted values.
- `figure_data/validation_final_voltages.npz`: exactly `y[:226,-1]` from each of the 136 effective validation trajectories. No interpolation or rounding. The adjacent provenance JSON identifies each full source file, its SHA-256 and its exact output-array hash.
- `requirements-reproduction.txt`: the original pinned scientific dependencies. Packages themselves are not bundled.

The endpoint cache is a derived plotting input. It is **not** a replacement for complete trajectories when auditing transients, integration errors or solver agreement. The two full main-campaign trajectories used in Figure 2 are included. The bulk of the main/validation trajectory archive is intentionally absent from GitHub.

Historical manifests inside `study/` describe the complete scientific archive and therefore refer to files omitted from this lightweight checkout. Use `GITHUB_MANIFEST_SHA256.txt` to verify this checkout; use the full archive's own manifest to verify the complete archive. Historical Portuguese reports and original plotting scripts are preserved for provenance; the current English manuscript provides the current interpretation.

## 3. Audit complete numerical results without new simulations

Obtain `History_Dependent_State_Selection_Reproducibility_v1.1.zip` from the corresponding Zenodo deposit and extract it into a separate directory. The DOI's public availability was not independently confirmed during preparation; if the record is not yet accessible, a full trajectory audit cannot be completed from this GitHub subset alone.

From the extracted archive root, using the scientific environment:

```bash
python verify_bundle.py
python verify_existing_metrics.py
```

The first verifies all archived payload hashes. The second reads all 136 effective validation trajectories, recounts receiver endpoints and peaks, and checks 87 paired endpoint comparisons. It performs no ODE integration. The archived numerical-check records retain the original failures, subsequent corrections, refinement comparisons and independent-solver checks.

To regenerate the lightweight final-voltage cache independently, run this repository's helper against the extracted archive's `study/` directory:

```bash
python scripts/prepare_plot_cache.py --study-root /path/to/extracted/archive/study --output /path/to/new_cache/validation_final_voltages.npz
```

Compare per-case array hashes and source-file hashes with `figure_data/validation_final_voltages.provenance.json`; compressed NPZ container timestamps can differ even when every array is identical.

## 4. Repeat the frozen simulations

The original scientific code is under:

- `study/transmissao_memoria_histerese/core.py`: conductance-model equations and integrator.
- `study/transmissao_memoria_histerese/experimento.py`: main frozen experiment and checks.
- `study/validacao_generalizacao_2026-09/modelo.py`: validation network adapter and scalar cubic model.
- `study/validacao_generalizacao_2026-09/executar.py`: isolated/network protocols and numerical checks.

Use the **complete extracted archive** as the starting point for the full campaign and its audits. From its root:

```bash
python study/transmissao_memoria_histerese/reproduzir.py main_rerun --run
python study/validacao_generalizacao_2026-09/reproduzir_validacao.py validation_rerun --run
```

These create new sibling output directories and refuse to overwrite existing ones. Omit `--run` to prepare the output folders only. These long scientific reruns were not executed for this GitHub update. Main reproduction covers the 487-case experiment, refinement and correction, not every historical exploratory or isolated supplementary procedure. Validation reproduction covers 136 networks, six isolated protocols and associated checks. Existing original scripts and retained outputs document the additional procedures. No new parameter selection or expansion of the closed campaign is required.

Do not run the original analysis scripts directly in the archived scientific folders if preserving their hashes: some rewrite derived outputs. The figure-only entry point above writes only to `figures/`.

## Licenses

Original source code is MIT licensed. Original data, figures and scientific text are CC BY 4.0. Third-party dependencies retain their own licenses. Numerical verification is not biological validation; the synthetic model's limitations and negative cubic result remain part of the study.
