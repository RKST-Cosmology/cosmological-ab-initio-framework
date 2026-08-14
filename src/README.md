"""
RKST vs. Lambda-CDM: Galactic Rotation Curve Analysis (SPARC)

This script tests the ab-initio cosmological framework of the RKST 
(Relativistic contraction-shrinkage theory) against the standard model (Lambda-CDM/NFW).
It generates individual rotation curves and a global residual histogram 
for the galaxies in the SPARC database.

Key feature: The RKST does not use individual fitting parameters per galaxy, 
but derives galactic dynamics directly from the topological vacuum cutoff 
(proton radius) and a universal scalar field coupling.
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# =====================================================================
# 1. SYSTEM PATHS & DIRECTORY STRUCTURE
# =====================================================================
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()

DATA_DIR = os.path.join(BASE_DIR, "sparc_data")
OUTPUT_PLOTS = os.path.join(BASE_DIR, "rkst_plots_showdown")

if not os.path.exists(OUTPUT_PLOTS): 
    os.makedirs(OUTPUT_PLOTS)
    print(f"[SYSTEM] Output directory created: {OUTPUT_PLOTS}")

# =====================================================================
# 2. FUNDAMENTAL PHYSICAL CONSTANTS
# =====================================================================
C = 299792458.0           # Speed of light [m/s]
H_BAR = 1.054571817e-34   # Reduced Planck constant [J*s]
G_ASTRO = 4.302e-6        # Gravitational constant [(kpc * (km/s)^2) / M_sun]
KPC_TO_M = 3.086e19       # Conversion factor kiloparsecs to meters

# =====================================================================
# 3. RKST AB-INITIO PARAMETERS (Core Innovation)
# =====================================================================
# The topological cutoff (Axiom II: Proton radius resonance)
R_P = 2.44e-15            # [m]

# The cosmological scaling number (Dirac number N)
N_DIRAC = 2.28e40         

# Derivation of the critical vacuum acceleration A_CRIT.
# Scales via the cosmic horizon (R_H = R_P * N_DIRAC) 
# incl. geometric factor (0.0745) for vacuum polarization.
A_CRIT = (C**2 / (R_P * N_DIRAC)) * 0.0745  # Results in ~1.2e-10 m/s^2

# Scalar field coupling parameter (Empirical working value, analytical derivation in progress)
BETA = 0.1                

# =====================================================================
# 4. LAMBDA-CDM (NFW) REFERENCE PARAMETERS (Unfitted)
# =====================================================================
NFW_R_SCALE = 15.0        # Scale radius of the halo [kpc]
NFW_RHO_SCALE = 2e-3      # Characteristic density
UPS_DISK = 0.25           # Mass-to-light ratio (Disk)
UPS_BULGE = 0.90          # Mass-to-light ratio (Bulge)

# =====================================================================
# 5. DYNAMICAL MODELS
# =====================================================================
def calculate_rkst_velocity(rad_kpc, v_bar):
    """
    Calculates the rotation velocity according to the RKST framework.
    Utilizes Chameleon screening to map the transition between Newtonian 
    dynamics (center) and modified dynamics (vacuum).
    """
    rad_m = rad_kpc * KPC_TO_M
    
    # Base acceleration from baryonic (visible) matter
    a_newton = (v_bar * 1000.0)**2 / rad_m
    a_newton_safe = np.maximum(1e-15, a_newton)
    
    # Chameleon screening: The scalar field decouples in dense regions (GR limit)
    screening_factor = np.exp(-a_newton_safe / A_CRIT)
    
    # Emergent acceleration from the scalar field
    a_phi = np.sqrt(a_newton_safe * A_CRIT) * screening_factor * (1.0 + BETA)
    
    # Total dynamics in the Einstein frame
    a_tot = a_newton_safe + a_phi
    
    return np.sqrt(a_tot * rad_m) / 1000.0

def v_nfw_global_profile(r, total_baryonic_mass):
    """
    Calculates the theoretical halo velocity according to Navarro-Frenk-White.
    Applied here as a strictly global model without individual fitting.
    """
    R_s = NFW_R_SCALE * (total_baryonic_mass / 1e10)**0.33
    rho_s = NFW_RHO_SCALE / (total_baryonic_mass / 1e10)**0.1
    x = r / np.maximum(1e-5, R_s)
    term = np.log(1.0 + x) - x / (1.0 + x)
    M_enc = 4.0 * np.pi * rho_s * R_s**3 * term
    return np.sqrt(np.maximum(0, G_ASTRO * M_enc / r))

# =====================================================================
# 6. DATA PROCESSING AND EVALUATION
# =====================================================================
if not os.path.exists(DATA_DIR):
    print(f"[ERROR] Data directory missing: {DATA_DIR}")
    files = []
else:
    files = glob.glob(os.path.join(DATA_DIR, "*.txt")) + glob.glob(os.path.join(DATA_DIR, "*.dat"))

if files:
    print(f"[START] Analyzing {len(files)} SPARC galaxies...")

all_res_rkst = []
all_res_nfw_global = []

for f_path in files:
    gal_name = os.path.basename(f_path)
    for suffix in ["_rotmod.txt", ".txt", "_rotmod.dat", ".dat"]:
        gal_name = gal_name.replace(suffix, "")
        
    try:
        # Fault-tolerant reading of SPARC files
        data = np.loadtxt(f_path, comments='#')
        if data.ndim == 1 or data.shape[1] < 6:
            data = np.loadtxt(f_path, skiprows=2)
            
        if data.shape[1] < 6: continue
            
        r_kpc, v_obs, e_v = data[:, 0], data[:, 1], data[:, 2]
        v_gas, v_disk, v_bul = data[:, 3], data[:, 4], data[:, 5]
        
        # Removal of invalid radii
        valid = r_kpc > 0
        r_kpc, v_obs, e_v = r_kpc[valid], v_obs[valid], e_v[valid]
        v_gas, v_disk, v_bul = v_gas[valid], v_disk[valid], v_bul[valid]
        
        if len(r_kpc) == 0: continue
        
        # Calculation of the combined baryonic velocity
        v_bar_sq = v_gas**2 + UPS_DISK * v_disk**2 + UPS_BULGE * v_bul**2
        v_bar = np.sqrt(np.maximum(0, v_bar_sq))
        
        # Estimation of total mass for the NFW profile
        outer_idx = -1
        total_baryonic_mass = (v_bar[outer_idx]**2 * r_kpc[outer_idx]) / G_ASTRO
        
        # Predictions
        v_pred_rkst = np.array([calculate_rkst_velocity(r_kpc[i], v_bar[i]) for i in range(len(r_kpc))])
        v_pred_nfw = np.sqrt(np.maximum(0, v_bar_sq + v_nfw_global_profile(r_kpc, total_baryonic_mass)**2))
        
        # Collect residuals for global statistics
        all_res_rkst.extend(v_obs - v_pred_rkst)
        all_res_nfw_global.extend(v_obs - v_pred_nfw)
        
        # Generate plot for individual galaxy
        plt.figure(figsize=(8, 5))
        plt.errorbar(r_kpc, v_obs, yerr=e_v, fmt='ko', markersize=3, alpha=0.5, label='SPARC Observation')
        plt.plot(r_kpc, v_pred_rkst, 'b-', lw=2, label='RKST (Ab-Initio Cutoff)')
        plt.plot(r_kpc, v_pred_nfw, 'r--', lw=2, label='NFW (Global, Unfitted)')
        plt.title(f"Galactic Kinematics: {gal_name}")
        plt.xlabel("Radius [kpc]")
        plt.ylabel("V [km/s]")
        plt.legend(loc='lower right')
        plt.grid(True, alpha=0.15)
        
        plt.savefig(os.path.join(OUTPUT_PLOTS, f"{gal_name}_showdown.png"), dpi=150)
        plt.close()
        
    except Exception as e:
        print(f"-> Skipping {gal_name} (Invalid dataset)")

# =====================================================================
# 7. GLOBAL STATISTICAL ANALYSIS (HISTOGRAM)
# =====================================================================
if all_res_rkst and all_res_nfw_global:
    plt.figure(figsize=(11, 6))
    
    # Histograms of deviations
    plt.hist(all_res_rkst, bins=50, alpha=0.4, label='RKST Residuals (Universal)', color='blue', density=True, edgecolor='blue')
    plt.hist(all_res_nfw_global, bins=50, alpha=0.4, label='NFW Residuals (Global)', color='red', density=True, edgecolor='red')
    
    # Fit normal distributions (Gaussian curves)
    mu_r, sigma_r = np.mean(all_res_rkst), np.std(all_res_rkst)
    x_r = np.linspace(mu_r - 3*sigma_r, mu_r + 3*sigma_r, 200)
    plt.plot(x_r, norm.pdf(x_r, mu_r, sigma_r), 'b-', lw=2, label=f'RKST (mu={mu_r:.2f}, sigma={sigma_r:.2f})')
    
    mu_n, sigma_n = np.mean(all_res_nfw_global), np.std(all_res_nfw_global)
    x_n = np.linspace(mu_n - 3*sigma_n, mu_n + 3*sigma_n, 200)
    plt.plot(x_n, norm.pdf(x_n, mu_n, sigma_n), 'r-', lw=2, label=f'NFW (mu={mu_n:.2f}, sigma={sigma_n:.2f})')
    
    # Ideal line (No deviation between model and observation)
    plt.axvline(0, color='black', linestyle=':', alpha=0.7, label='Ideal Line (0 km/s)')
    
    plt.xlabel('Residual (Observation - Prediction) [km/s]')
    plt.ylabel('Probability Density')
    plt.title('RKST vs. Lambda-CDM: Global Residual Comparison (SPARC)')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.15)
    
    hist_path = os.path.join(BASE_DIR, 'rkst_vs_nfw_histogram.png')
    plt.savefig(hist_path, dpi=200)
    
    print("\n[SUCCESS] Analysis complete!")
    print(f"-> RKST Mean Error: {mu_r:.2f} km/s (Std Dev: {sigma_r:.2f})")
    print(f"-> NFW  Mean Error: {mu_n:.2f} km/s (Std Dev: {sigma_n:.2f})")
