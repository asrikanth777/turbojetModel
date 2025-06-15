"""
------------------------------------------------------------
F119 1D Turbofan Simulator – Variable Reference
------------------------------------------------------------

# GENERAL
mach             : Freestream Mach number (M₀)
press            : Freestream static pressure (P₀) [Pa]
temp             : Freestream static temperature (T₀) [K]
gamma            : Ratio of specific heats (Cp/Cv), assumed 1.4 for air
R                : Specific gas constant for air [J/kg·K], assumed 287

# STAGNATION CONDITIONS
stagpress        : Stagnation (total) pressure Pₜ at component inlet [Pa]
stagtemp         : Stagnation (total) temperature Tₜ at component inlet [K]

# MASS FLOW
massflow         : Mass flow rate of air into the component [kg/s]
bypaRatio        : Bypass ratio β = ṁ_bypass / ṁ_core (F119 ≈ 0.3)

# FAN & COMPRESSORS
pressure_ratio   : Total pressure ratio across fan or compressor stage (e.g., π_fan)
efficiency       : Polytropic/isothermal efficiency of fan or compressor
lpcPressRatio    : Pressure ratio across Low Pressure Compressor (π_LPC)
lpcEfficiency    : LPC efficiency (η_LPC)
hpcPressRatio    : Pressure ratio across High Pressure Compressor (π_HPC)
hpcEfficiency    : HPC efficiency (η_HPC)

# COMBUSTOR
titemp           : Turbine Inlet Temperature (Tₜ4) after combustor [K]
combEfficiency   : Combustor efficiency (η_b), typically ~0.98–0.99
hPR              : Fuel heating value (Jet-A), ~43e6 J/kg

# TURBINES
requiredWork     : Power required by downstream component (HPC or Fan) [J/s]
efficiency       : Isentropic efficiency of turbine (η_turbine)
specificheat     : Cp value for hot gas (post-combustion), [J/kg·K], assumed ~1004.5

# NOZZLE
ambpress         : Ambient static pressure (P₀) [Pa] at nozzle exit
nozzleEff        : Nozzle isentropic efficiency (η_n), typically ~0.98

# EXHAUST
noz_exitV        : Exhaust velocity from core nozzle [m/s]
byp_exitV        : Exhaust velocity from bypass stream [m/s]
freestrmV        : Freestream velocity (V₀) [m/s]
fuel_flow        : Fuel mass flow rate [kg/s]
fuel_heatingval  : Lower heating value of fuel, same as hPR [J/kg]

------------------------------------------------------------
"""
