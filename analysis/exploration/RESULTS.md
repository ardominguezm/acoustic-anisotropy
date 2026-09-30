# Exploration of the Zenodo 18501172 event table and raw waveforms (2026-09-30)

Inputs used: `Frequency series of AE signals...xlsx` (event table: time, dominant frequency, amplitude dB,
frequency class, deformation stage) and `Raw AE Waveforms.rar` (6,637 hits, 4 channels, 1 us sampling, 1023 pts).
Not available here: `Supporting data for Figure 9/13.xlsx` (hardware AE energy, load). t_f taken from manuscript Sec. 2.1.
Scripts read absolute paths of the upload folder; edit `load.py` (P) and `wf.py` (R) before running elsewhere.

## Data structure
- Table rows map 1:1, in time order, to waveform files (constant 0.25 ms offset; waveform amplitude = table amplitude + 40 dB, consistent with preamp gain).
- Each physical event is often recorded on several channels within ~0.2 ms. Merging hits with gaps <= 0.5 ms gives
  pre-peak events: 2270 (0 deg), 120 (30), 132 (45), 173 (60), 328 (90).

## A. Stage-of-maximum claim (pre-peak only)
Stage IV duration as fraction of t_f (seconds): 0 deg 0.083 (46 s); 30 deg 0.029 (10.5 s); 45 deg 0.027 (8.8 s);
60 deg 0.019 (5.2 s); 90 deg 0.076 (18 s). A 15 s window is wider than Stage IV for 30, 45 and 60 deg,
so the stage assigned to the window maximum depends on the window-to-stage assignment rule.
Stage containing the max trailing-window rate (w = 5/15/30 s), waveform energy:
0: IV/IV/IV; 30: IV/IV/IV; 45: III/III/III; 60: IV/IV/IV; 90: III/III/IV.
Amplitude-proxy energy (10^(A/10)): 0 deg becomes III at 15 and 30 s. Manuscript: IV, IV, IV, III, III.
45 and 60 deg disagree under both energy definitions; must be resolved with the Figure 9 energy column.

## B. b-value (Aki-Utsu, amplitude in dB)
Spearman trend of b with lifetime: 0: -0.25, 30: -0.39, 45: +0.67, 60: -0.66, 90: -0.70 (few windows each). Standard behaviour.

## C. Hawkes branching ratio (piecewise background K = 12, exponential kernel)
n_hat: 0.46, 0.36, 0.28, 0.65, 0.62 (parametric bootstrap CIs: [0.42,0.48], [0.22,0.47], [0.18,0.42], [0.48,0.74], [0.49,0.70]).
Surrogate test (events re-drawn uniformly within 48 lifetime bins, kernel timescale <= 1 s): surrogate n is equal or
larger than observed (excess -0.18, 0.01, -0.07, -0.02, -0.13; p >= 0.44). No evidence of self-excitation beyond slow rate variation.

## D. MF-DFA (merged events, shuffle surrogates)
Amplitude sequence: Delta h within surrogate noise for 4 of 5 specimens. Inter-event times: H = 0.8-1.1 (>1 indicates trend
from the loading ramp), so not interpretable as multifractality. Multifractal AE in shale is already covered by prior work.

## E. Model form (non-overlapping windows, 4% of t_f on tau in [0.3,1), waveform energy)
Delta AICc (power law in TTF minus exponential in t): 0: +6.0, 30: +1.1, 45: +1.8, 60: +0.5, 90: +5.7 (positive favours exponential).
Rate vs cumulative energy (cascade form): best only for 0 deg (Delta vs exponential = -2.6); exponent k = 0.92, 0.26, 0.30, 0.87, 0.83.
