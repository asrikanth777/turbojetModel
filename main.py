from setup import runEngine
import numpy as np
import matplotlib.pyplot as plt

# Mach range
mach_values = np.linspace(0, 2.25, 40)  # Mach 0 to 2 in 0.1 steps
thrust_vals = []
tsfc_vals = []
spec_thrust_vals = []

# Run engine model for each Mach
for M in mach_values:
    res = runEngine(M, mode="wet")  # or "dry" for non-afterburning
    thrust_vals.append(res["Net Thrust"])
    tsfc_vals.append(res["TSFC"])
    spec_thrust_vals.append(res["Specific Thrust"])

# --- Plot Net Thrust ---
plt.figure()
plt.plot(mach_values, thrust_vals, marker='o')
plt.xlabel("Mach Number")
plt.ylabel("Net Thrust (N)")
plt.title("F119 Engine Thrust vs Mach")
plt.grid(True)
plt.show()

# --- Plot TSFC ---
plt.figure()
plt.plot(mach_values, tsfc_vals, marker='o', color='orange')
plt.xlabel("Mach Number")
plt.ylabel("TSFC (kg fuel / N·s)")
plt.title("F119 Engine TSFC vs Mach")
plt.grid(True)
plt.show()

# --- Plot Specific Thrust ---
plt.figure()
plt.plot(mach_values, spec_thrust_vals, marker='o', color='green')
plt.xlabel("Mach Number")
plt.ylabel("Specific Thrust (N per kg/s air)")
plt.title("F119 Engine Specific Thrust vs Mach")
plt.grid(True)
plt.show()
