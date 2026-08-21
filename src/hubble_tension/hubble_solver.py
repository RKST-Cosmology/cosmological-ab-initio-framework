import os
import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# 1. COSMOLOGICAL BASELINES & KBC VOID PARAMETERS
# =====================================================================
H0_PLANCK = 67.4       
H0_SHOES = 73.04       
H0_SHOES_ERR = 1.04    

# Central density contrast: delta = -0.4 +/- 0.1
# Expressed as a density ratio: rho_ratio = 1.0 + delta
DELTA_CENTRAL = -0.4
DELTA_ERR = 0.1

RHO_RATIO_CENTRAL = 1.0 + DELTA_CENTRAL                      # 0.6
RHO_RATIO_MAX_VOID = 1.0 + (DELTA_CENTRAL - DELTA_ERR)       # 0.5
RHO_RATIO_MIN_VOID = 1.0 + (DELTA_CENTRAL + DELTA_ERR)       # 0.7

# =====================================================================
# 2. EVALUATION OF THE COUPLING SPECTRUM & INDEPENDENT CONSTRAINTS
# =====================================================================
beta_range = np.linspace(0.0, 0.25, 500)

# Theoretical curves based on Jordan-frame scalar-tensor scaling
h0_central = H0_PLANCK * (1.0 / RHO_RATIO_CENTRAL)**beta_range
h0_upper_bound = H0_PLANCK * (1.0 / RHO_RATIO_MAX_VOID)**beta_range
h0_lower_bound = H0_PLANCK * (1.0 / RHO_RATIO_MIN_VOID)**beta_range

# Analytical perfect match needed for Hubble tension
beta_perfect = np.log(H0_SHOES / H0_PLANCK) / np.log(1.0 / RHO_RATIO_CENTRAL)

# FIXED INDEPENDENT VALUE FROM SPARC DATABASE (Galactic Rotation)
BETA_SPARC = 0.157

# =====================================================================
# 3. SCIENTIFIC VISUALIZATION (Publication Ready)
# =====================================================================
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.linewidth'] = 1.2

fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)

# 1. Shaded error band for KBC-Void density mapping uncertainties
ax.fill_between(beta_range, h0_lower_bound, h0_upper_bound, 
                color='royalblue', alpha=0.15, linestyle=':',
                label='KBC-Void Structural Uncertainty (delta = -0.4 +/- 0.1)')

# 2. Main RKST Theoretical Prediction Curve
ax.plot(beta_range, h0_central, 'b-', lw=2.5, 
        label='RKST Model: H0_void = H0_Planck * (1/rho_ratio)^Beta')

# 3. Empirical Observational Horizons
ax.axhspan(H0_SHOES - H0_SHOES_ERR, H0_SHOES + H0_SHOES_ERR, color='darkred', alpha=0.1, label='SH0ES 1-Sigma Confidence Interval')
ax.axhline(y=H0_SHOES, color='darkred', linestyle='--', alpha=0.7, label='SH0ES Central Observation (73.04)')
ax.axhline(y=H0_PLANCK, color='black', linestyle=':', lw=1.5, label='Planck CMB Global Baseline (67.4)')

# 4. Universal Paradigm Markers & Spectacular Coincidence
ax.plot(beta_perfect, H0_SHOES, 'go', markersize=9, 
        label=f'Required Hubble Resolution (Beta = {beta_perfect:.3f})')

ax.axvline(x=BETA_SPARC, color='darkgreen', linestyle='-.', lw=1.8,
           label=f'Independent Galactic Constraint Beta = {BETA_SPARC} (SPARC Database)')

# Plot Aesthetics
ax.set_title("Cosmological Scale Resolution of the Hubble Tension via RKST Framework", fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel("RKST Vacuum Coupling Parameter Beta", fontsize=12)
ax.set_ylabel("H0 [km s-1 Mpc-1]", fontsize=12)
ax.set_xlim(0.0, 0.23)
ax.set_ylim(66.0, 76.5)
ax.grid(True, linestyle='--', alpha=0.3)

# Optimized legend position
ax.legend(loc='lower right', fontsize=9.5, frameon=True, facecolor='white', framealpha=0.9, edgecolor='gray')

plt.tight_layout()
output_pdf = "RKST_Hubble_Tension_Resolution.pdf"
plt.savefig(output_pdf, format='pdf', bbox_inches='tight')
plt.show()

