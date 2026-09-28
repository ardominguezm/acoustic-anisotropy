# Acoustic anisotropy and critical AE acceleration

Target journal: *Engineering Fracture Mechanics*.

## Current status

A clean confirmatory rerun was performed from the original Zenodo 18501172 data.

The originally proposed predictive angular law
```
log(AE energy rate) = a(beta) - p_eff(beta) log(TTF)
p_eff(beta) = p0 + p1 cos(2 beta) + p2 cos(4 beta)
```
does **not** pass the prespecified confirmatory gate.

Primary 30 s causal window:
- anisotropic model better than universal model in 8/15 held-out angle × horizon tests;
- exact 5! bedding-angle permutation test: p = 0.167;
- removing the 60° trajectory eliminates the mean advantage.

Sensitivity:
- 15 s window: 10/15 wins;
- 30 s window: 8/15 wins;
- 45 s window: 13/15 wins.

Therefore the trigonometric angular law should **not** be presented as a confirmed predictive law.

## Exploratory mechanism

A secondary analysis suggests that the orientation-specific critical-acceleration exponent is inversely related to the tensile-event fraction reported in Figure 13. This points to a potentially more defensible mechanism:

> the acceleration of acoustic-emission activity toward failure may depend on fracture-mode composition (tensile vs shear/mixed), with bedding orientation acting through the failure mechanism rather than through a universal angular scaling law.

This result is exploratory and requires independent specimens or external validation before being used as the paper's principal claim.

## Reproducibility

The analysis uses the original Zenodo deposit 18501172. Raw data are not committed to this private repository. Place the downloaded ZIP under `data/raw/18501172.zip` or set the environment variable `DATA_ZIP`.

The confirmatory notebook is maintained under `notebooks/01_confirmatory_analysis.ipynb`.

## Next decision

Before drafting for *Engineering Fracture Mechanics*, test whether the fracture-mode interpretation is robust using:
1. block/bootstrap uncertainty for orientation-specific exponents;
2. alternative non-overlapping rate windows;
3. stage-resolved tensile/shear composition where timestamps permit;
4. influence diagnostics excluding each orientation;
5. a comparison of power-law critical acceleration against exponential/log-linear alternatives.

No further black-box ML or Neural ODE development is planned for this dataset.
