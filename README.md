# Acoustic anisotropy and AE-energy timing

Target journal: *Engineering Fracture Mechanics*.

## Current scientific framing

The project no longer claims a universal critical power law or a confirmed trigonometric bedding-angle law. The strongest reproducible result is stage-resolved:

- 0°, 30°, and 45° reach their maximum AE-energy rate in Stage IV.
- 60° and 90° reach their maximum AE-energy rate earlier, in Stage III.
- The earlier peak is associated with more shear/mixed fracture-mode composition.
- Power-law critical scaling is not uniquely supported; exponential alternatives are competitive or preferred in several cases.

The working mechanistic interpretation is therefore:

> bedding orientation → fracture-mode partitioning → timing of AE-energy concentration → failure.

Because the public dataset contains one physical specimen per bedding orientation, the result is treated as discovery-level evidence and not as a population-level law.

## Publication-figure notebook

Open the customizable publication-figure notebook directly in Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ardominguezm/acoustic-anisotropy/blob/main/notebooks/03_publication_figures.ipynb)

The notebook generates manuscript-ready PDF/PNG figures and exposes a single `CONFIG` block for typography, dimensions, line widths, markers, DPI, formats, titles, and output directory.

Required source files from Zenodo record 18501172:

- `Supporting data for Figure 9.xlsx`
- `Supporting data for Figure 13.xlsx`

The notebook can either upload them interactively in Colab or read them from Google Drive. Raw third-party data are not redistributed in this repository.

## Reproducibility

The analysis uses the original public dataset from Zenodo record 18501172. Raw data are not committed to this repository.

Key analysis files:

- `analysis/confirmatory_analysis.py`
- `notebooks/01_confirmatory_analysis.ipynb`
- `notebooks/03_publication_figures.ipynb`

## Manuscript target

Working title:

**Bedding anisotropy shifts the timing of acoustic-emission energy release during shale fracture**

The manuscript emphasizes mechanistic timing of AE-energy concentration rather than aggregate AE magnitude or a universal scaling law.
