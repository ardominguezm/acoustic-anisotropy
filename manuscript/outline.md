# Manuscript outline — Engineering Fracture Mechanics

## Working title
**Bedding anisotropy shifts the timing of acoustic-emission energy acceleration during shale fracture**

## Central question
Does bedding anisotropy alter the approach to macroscopic failure by shifting the stage at which acoustic-emission (AE) energy release becomes concentrated?

## Main claim
Across five bedding orientations, the timing of peak AE-energy release is not invariant. More shear-rich orientations (60° and 90°) concentrate AE-energy release earlier, in Stage III, whereas the more tensile-dominated 0°, 30°, and 45° orientations peak in Stage IV. The data support anisotropy-dependent acceleration of AE activity, but not a universal critical power-law.

## Introduction
1. AE tracks microcracking and impending failure in brittle and quasi-brittle materials.
2. Layered shale is strongly anisotropic; bedding controls strength, crack path, tensile/shear partitioning, and AE response.
3. Existing work commonly compares aggregate AE counts, energy, b-value, or frequency across orientations.
4. Less attention has been paid to when AE-energy release becomes concentrated along the damage trajectory and whether this timing is linked to fracture mode.
5. Objectives:
   - H1: temporal concentration of AE energy differs by bedding orientation;
   - H2: earlier concentration is associated with greater shear/mixed fracture contribution;
   - exploratory: acceleration exponents vary across orientations, with no universal scaling form assumed.

## Materials and data
- Public dataset: Zenodo 18501172.
- Five bedding orientations: 0°, 30°, 45°, 60°, 90°.
- Mechanical load-time histories, AE energy, frequency/amplitude descriptors, crack-size/stage annotations, tensile/shear classifications.
- One physical specimen per orientation: principal design limitation.

## Methods
### Failure alignment
Define failure time as peak-load time t_f; normalize time by tau=t/t_f.

### AE-energy rate
Compute causal/non-overlapping windowed energy rate for widths 10, 15, 20, 30, 45 s.

### Damage stages
Use source stage labels to identify the stage containing maximum AE-energy rate.

### Acceleration analysis
Fit log(rate) versus log(TTF) descriptively; use block bootstrap for uncertainty.

### Model-form check
Compare power-law and exponential acceleration by AICc. Do not claim critical scaling unless power law is clearly favored.

### Fracture-mode association
Compare peak-energy stage and descriptive exponent estimates with tensile/shear event composition.

### Sensitivity
Repeat across temporal windows and report all orientations individually.

## Results
### 3.1 Mechanical and AE trajectories depend strongly on bedding orientation
Figure 1.

### 3.2 Peak AE-energy release occurs at different damage stages
Figure 2: 0°, 30°, 45° peak in Stage IV; 60°, 90° peak in Stage III.

### 3.3 Acceleration strength is heterogeneous rather than universal
Figure 3 and Table 1.

### 3.4 A universal critical power law is not supported
Table 4: power law is never preferred by ΔAICc > 2; exponential alternatives are sometimes favored.

### 3.5 Timing of peak AE-energy release tracks fracture-mode composition
Figure 4 and Table 2. More shear-rich orientations show earlier concentration. Present as mechanistic evidence, not a universal law.

## Discussion
1. Earlier Stage-III energy concentration at 60°/90° is consistent with bedding-assisted shear/mixed localization.
2. Later Stage-IV concentration at 0°/30°/45° is consistent with delayed tensile-dominated coalescence.
3. Anisotropy affects the timing/pathway of damage accumulation, not merely total AE output.
4. Universal critical scaling is too strong for these data.
5. Limitations: one specimen per angle; source-derived stage/mode labels; no external experimental validation; AE energy is instrumentation-dependent.
6. Future validation: replicated specimens per angle and an independent AE system.

## Conclusion
Bedding orientation shifts the stage at which AE energy release becomes concentrated during failure. The timing differences align with tensile/shear fracture-mode composition, suggesting that anisotropy modifies the pathway to failure through its control of fracture localization. The dataset does not support a universal critical power-law; the stronger conclusion is mechanistic and stage-resolved.
