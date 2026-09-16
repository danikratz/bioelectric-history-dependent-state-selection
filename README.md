# History-dependent state selection after transient coupling loss in a conductance-based bioelectric network

Daniela Barbosa Kratz — Univali  
ORCID: https://orcid.org/0000-0001-8364-0246  
Correspondence: dbkratz@gmail.com

**Version 1.1. Scientific preprint; not peer reviewed.**  
**Zenodo identifier: [10.5281/zenodo.22802165](https://doi.org/10.5281/zenodo.22802165)**

## Manuscripts

- [Complete preprint with supplement and eight embedded figures](History_Dependent_State_Selection_Preprint_v1.1.pdf) — 25 pages, suitable for ResearchGate.
- [Main manuscript](History_Dependent_State_Selection_v1.1.pdf) — 17 pages.
- [Supplementary material](History_Dependent_State_Selection_Supplement_v1.1.pdf) — 8 pages.

## Study

A synthetic conductance-based network of 226 nodes and 622 edges compares uninterrupted coupling with transient weakening followed by exact restoration. The lower-stimulus contrast persisted across five specified source/geometry configurations and occurred in 24 of 42 sampled conductance–restoration comparisons. An alternative cubic mechanism showed isolated bistability and hysteresis but no receiver recruitment or history-dependent network endpoint under the fixed protocol.

The contribution is a controlled extension of established bioelectric-memory phenomena. Physiological generality and priority of the exact comparison remain unresolved. The manuscript explicitly discusses Pezzulo et al. (2021), DOI 10.1098/rstb.2019.0765, as prior literature. Numerical results and scientific figures are unchanged in this editorial revision.

## Code and reproducibility

The repository includes the original scientific source code, pinned dependencies, frozen protocols, numerical results and enough archived data to regenerate all ten figures without running new simulations. Start with [REPRODUCING.md](REPRODUCING.md).

```bash
python -m pip install -r requirements-reproduction.txt
python scripts/reproduce_figures.py
python scripts/check_reproduced_figures.py
```

Use a Python 3.9 virtual environment as detailed in the guide. The figures were regenerated and all ten PNGs matched the frozen release byte for byte. This checks figure reproduction, not biological validation or a new simulation campaign.

The [original model and experiment code](study/) is preserved byte for byte. The [plotting scripts](source_code/) and [figure-to-code map](REPRODUCING.md#figure-to-code-map) show how each panel was generated. An exact endpoint cache supplies the validation figure values, with per-source hashes in [figure_data/validation_final_voltages.provenance.json](figure_data/validation_final_voltages.provenance.json).

Complete transient trajectories and full numerical rerun/audit inputs are in the approximately 2.67 GB reproducibility ZIP for the corresponding Zenodo deposit. They are not all included in this lightweight checkout. See the guide for complete-archive verification and simulation commands. The scientific campaign remains closed; no new simulations were performed for this repository update.

`GITHUB_MANIFEST_SHA256.txt` verifies files in this checkout. `ZENODO_MANIFEST_SHA256.txt` describes the separately distributed full Zenodo package, including its large ZIP. Historical manifests in `study/` also refer to the full scientific archive, not just the GitHub subset.

## Citation and license

Kratz, D. B. (2026). History-dependent state selection after transient coupling loss in a conductance-based bioelectric network. Version 1.1. Zenodo identifier: https://doi.org/10.5281/zenodo.22802165.

Original text, data and figures: [CC BY 4.0](LICENSE_DATA.md). Original code: [MIT](LICENSE_CODE.txt). The root MIT LICENSE applies to original software, not to manuscript text or figures. Third-party dependencies retain their own licenses.

## Revision

Version 1.1 includes English figure labels, revised author declarations, repository links and an expanded prior-literature discussion. The author supplied the current DOI as the replacement for the removed record. The current branch contains the corrected PDFs and identifier; earlier files remain in Git history. Uploads to Zenodo and ResearchGate are separate from this repository update.
