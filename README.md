# An Ab-Initio Cosmological Framework (RKST)

This repository contains the source code and formal mathematical verification for the **RKST Cosmological Framework**. This ab-initio theory derives global cosmological phenomena directly from topological vacuum cutoff scales, effectively resolving the missing mass problem and cosmic acceleration without the need for **Dark Matter** or **Dark Energy**.

## Key Features & Scientific Anchors

* **Zero Free Parameters:** Unlike empirical models (e.g., MOND or $\Lambda$CDM), the critical acceleration threshold $a_{\text{crit}}$ and the Hubble constant $H_0$ emerge naturally from a harmonic binary octave scaling ($2^{137}$) of the fundamental proton radius resonance scale ($r_p$).
* **SPARC Galaxies Verification:** The Python implementation demonstrates a statistically superior fit to the SPARC (Spitzer Photometry and Accurate Rotation Curves) data compared to the standard $\Lambda$CDM model utilizing Navarro-Frenk-White (NFW) dark matter profiles.
* **Hubble Tension Resolution:** Explains the localized Hubble tension naturally as an environmental density illusion within the KBC Void.

## Repository Structure

* [`/src`](./src): Contains the optimized **Python implementation** for galactic rotation curve profiles and screening parameter sweeps.
* [`/verification`](./verification): Features the formal mathematical verification of the core postulates using the **LEAN 4 theorem prover** (`RKST_Core.lean`).
* [`/paper`](./paper): Reserved for the LaTeX manuscripts, preprints, and cosmological derivation sheets.

## Data & Replication

To keep this repository lightweight and respect the original licensing, the 176 SPARC galaxy data files are not hosted inside this repository. Instead, they can be obtained directly from the official academic source.

### 1. Download the Data
1. Visit the official SPARC database website: [SPARC Data Access](https://astroweb.case.edu/SPARC/)
2. Download the galaxy sample data files (the raw `.txt` files containing the rotation curves).

### 2. Local Setup
1. Click the green **"Code"** button at the top of this GitHub page and select **"Download ZIP"** (or clone the repository) and extract it on your computer.
2. Inside the extracted main directory, create a folder named `data`.
3. Inside that `data` folder, create another folder named `sparc_data`.
4. Place all 176 downloaded galaxy `.txt` files directly into the `data/sparc_data/` directory.

### 3. Execution
Open `src/sparc_galaxies.py` in your Python environment (e.g., Thonny) and run it. The script will automatically read the data from the relative path and reproduce the cosmological plots.


## Formal Verification via LEAN 4

To ensure absolute mathematical consistency and eliminate any potential derivation errors, the foundational algebraic coupling between the vacuum cutoff $r_p$, the particle horizon $R_H$, and the global expansion rate $H_0$ has been verified using LEAN 4:

```lean
theorem hubble_horizon_relation : H_0 = (Real.pi * c) / R_H
```
The successful compilation of this theorem guarantees that our mathematical framework is strictly logically sound.

## Citation & Preprint
The full scientific paper is available on **Harvard Dataverse** https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/MAYBW5. If you use this framework or the rotation curve code in your research, please cite our preprint as outlined in the repository documentation.
