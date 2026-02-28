import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Setup Parameters (Physically Reasonable for MRI)
# ---------------------------------------------------------
v_true = 0.5            # Constant true velocity (m/s)
venc_nominal = 1.0      # Set VENC on the scanner (m/s)
x = np.linspace(-0.2, 0.2, 500)  # 40cm Field of View (-20cm to +20cm)

# Proposing a physically reasonable model: 
# Most gradients weaken (roll-off) at the edges.
# alpha = -0.1 means a 10% drop in strength at the edge of the FOV.
alpha = -0.1 
L = 0.2  # Characteristic length (m)

# ---------------------------------------------------------
# 2. Gradient Nonlinearity Model
# ---------------------------------------------------------
# g_error represents the deviation factor G_actual / G_nominal
g_error = 1 + alpha * (x / L)**2 

# ---------------------------------------------------------
# 3. Simulation: The Effect on VENC and Velocity
# ---------------------------------------------------------
# Effective VENC: If gradient is weak, VENC effectively increases 
# (it takes more velocity to reach a 180-degree phase shift)
venc_effective = venc_nominal / g_error

# Step A: Calculate the actual Phase (phi) the scanner receives
# phi = (v_true / venc_effective) * pi
phase_actual = (v_true / venc_effective) * np.pi

# Step B: The scanner "thinks" the gradient is perfect (nominal)
# It calculates velocity using: v = (phase / pi) * venc_nominal
v_measured = (phase_actual / np.pi) * venc_nominal

# ---------------------------------------------------------
# 4. Bonus: Correction Strategy
# ---------------------------------------------------------
# If we have a calibration map of the nonlinearity (g_error),
# we can divide the measured velocity by the local error factor.
v_corrected = v_measured / g_error

# ---------------------------------------------------------
# 5. Visualization
# ---------------------------------------------------------
fig, ax = plt.subplots(2, 1, figsize=(10, 10))

# Subplot 1: Effective VENC vs Position
ax[0].plot(x * 100, [venc_nominal]*len(x), 'k--', label='Nominal VENC (1.0 m/s)')
ax[0].plot(x * 100, venc_effective, 'b', label='Effective VENC (Actual)')
ax[0].set_title("Spatially Varying Effective VENC")
ax[0].set_ylabel("VENC (m/s)")
ax[0].set_xlabel("Position from Isocenter (cm)")
ax[0].legend()
ax[0].grid(True)

# Subplot 2: Measured Velocity and Correction
ax[1].axhline(v_true, color='black', linestyle='--', label='True Velocity (0.5 m/s)')
ax[1].plot(x * 100, v_measured, 'r', label='Measured Velocity (With Nonlinearity)')
ax[1].plot(x * 100, v_corrected, 'g:', linewidth=3, label='Corrected Velocity')
ax[1].set_title("Velocity Error and Correction")
ax[1].set_ylabel("Velocity (m/s)")
ax[1].set_xlabel("Position from Isocenter (cm)")
ax[1].set_ylim(0.3, 0.7)
ax[1].legend()
ax[1].grid(True)

plt.tight_layout()
plt.show()

print(f"Max Error at edges: {np.abs(v_measured[0] - v_true):.4f} m/s")