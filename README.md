# Stage A — identifiability of a reduced L5 pyramidal model from multi-site injections (code and figures)

**Status:** Released with the preprint. The version cited by the preprint is the tag `preprint-v1`.

**Licenses:** code under the MIT License (`LICENSE`); data and figures (`code/results/`, `figures/`) under Creative Commons Attribution 4.0 International (`LICENSE-DATA`).

**Language note:** code comments and log messages are in Portuguese, and many comments cite entries of the project's internal decision record ("D1xx", "item N"). They are kept as written, so that the code matches the record it was run under.

## What this reproduces
- The reduced model (N = 32 compartments per region, 30 log-parameters) built from the Hay et al. 2011 L5 pyramidal model.
- Stage A in batches: conditioned per-point protocols, multi-site injection designs, Fisher information under four noise models (white, i.e. iid; OU 1/10/50 ms), the linear specification σ*, intrinsic curvature σ_lin (Bates & Watts), the certified level min(σ*, σ_lin), the physiological-range rule with its fixed point, and the stop rule between batches.
- The preprint figures: one script per figure (`code/preprint_fig1_morphology_designs.py` … `code/preprint_fig6_artifacts.py`, shared helpers in `code/preprint_comum.py`), all run by `code/preprint_figuras.py`.

## Requirements (as used)
- Linux x86_64. Python 3.14, NEURON 9.0.2, NumPy 2.5 and SciPy 1.18 in the simulation environment (exact versions: `requirements-simulation.txt`); matplotlib 3.11 and NumPy 2.5 in a separate environment, for the figures only (`requirements-figures.txt`).
- Hay et al. 2011 model, ModelDB accession **139653**: download it from https://modeldb.science/139653 (mirror: github.com/ModelDBRepository/139653). The archive used had sha256 `aeeb87d9ea70ddb67ebac5974211cdc7497b25b9a06d084fb9b61f67927e3555`. Unpack it to `.cache/hay/139653-master` and compile the mechanisms with `cd .cache/hay/139653-master/mod && nrnivmodl .`.

## Step by step
1. **Every simulation goes through the memory gate:** `python3 code/lancar.py <type> [--esperar] -- <command>` (the modules refuse a process not started this way). The project ran the long jobs through a queue supervisor that is NOT included (it is machine infrastructure); to reproduce, run each unit directly with the runner through the gate, e.g. `python3 code/lancar.py distal --esperar -- python3 code/etapaA_runner.py unit <dir> ...`, with the argv recorded in `code/results/supervisor/TRABALHOS.json`.
2. **Functional sensitivity G at atol 1e-8:** run `code/etapaA_runner.py G ...` with 5 sub-workers.
3. **Per-point conditioning:** `code/etapaA_condiciona.py`, then `code/etapaA_condiciona_lote.py`.
4. **θ units:** `code/etapaA_runner.py unit <dir> --only <point> --so-theta --atol 1e-8 --amplitudes ...`.
5. **Relevant directions:** `code/etapaA_piloto.py --direcoes`. Then the rests (`code/etapaA_repousos.py`), the absolute rest potentials (`code/etapaA_vrest.py`) and the direction runs (`etapaA_runner.py unit --direcoes`).
6. **Per-unit accumulations:** `code/etapaA_piloto.py --acumular` (with the physiological range).
7. **Functional along the directions beyond the range:** `etapaA_runner.py G --direcoes`, then `code/etapaA_Fdir.py`. The fixed point is iterated with `code/etapaA_ponto_fixo.py`.
8. **Analysis:** `code/etapaA_piloto.py --analise --acumulados ... --fdir ...`. Stop rule between batches: `code/etapaA_lote_aval.py`.
9. **Queue generators:** `code/cadeias/cadeia_lotes.py` and `cadeia_pf.py`.
10. **Figures:** `code/preprint_morfologia.py`, then `code/preprint_figuras.py <out>` (or any single `code/preprint_figN_….py <out>`).
11. **Sensitivity to the CaBurst_PA1 tolerance (0.2 / 0.5 / 1.0 ms):** `code/etapaA_Fdir.py ... --tol-CaBurst <ms>` for each direction round, then `code/etapaA_sens_caburst_cond.py`. Check: the 1.0-ms line reproduces the fixed point exactly.
12. **Readout density (400 / 200 / 100 / 50 µm / all) and the double-precision rest artifact:** `code/etapaA_densidade_cond.py` and `code/etapaA_repouso_double.py`.

Tests with known answers (run before use) are in `code/*_teste.py`.

## Data
- **Included:** the figure data (`code/results/...`, the 15 files the figure scripts read; ~460 KB) and the six figures (`figures/`, PDF and PNG).
- **Queue file:** `code/results/supervisor/TRABALHOS.json` is a reduced copy of the project queue, with only the Stage A jobs whose scripts are in `code/` (several scripts read the official argv of the analysis jobs from it).
- **Per-unit accumulated Fisher terms:** about 4 MB. These are enough to redo every analysis without simulation.
- **Raw traces:** the θ runs of the three designs are about 80 GB. Candidate for Zenodo, or regenerate by simulation.

## Notes for the owner before publishing
Comments are in Portuguese and cite internal decision numbers (D1xx, "item N"). See `LISTA_DE_ARQUIVOS.md` for the files that mention the wider project. An extract of the decision record (D131–D132), with the personal/operational items marked for a one-by-one decision, is kept OUTSIDE this folder (`../etapaA_publico_REGISTRO_A_DECIDIR/`), so it cannot be published by accident.

## Decision record
`record/D131_D132_extract.md` is a literal extract of the project's decision record (items D131 and D132, in Portuguese), with 8 purely operational items removed. The code comments cite these items ("D132 item N").
