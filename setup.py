from classes import *
import numpy as np

# initial flight conditions
mach = 0
initialPress = 101325 # pa
initialTemp = 293 # K, 20deg Celsius
P_ambient = 101325 # pa, outside pressure

wet = "afterburner"
dry = "dry"

# inlet 
inlet_obj = inlet(mach, initialPress, initialTemp)
inlet_results = inlet_obj.compute()

inletMassflow = inlet_results["Mass Flow"]
inletStagTemp = inlet_results["Stagnation Temp (Tt0)"]
inletStagPress = inlet_results["Stagnation Press (Pt0)"]

# fan 
fan_obj = fan(inletStagPress, inletStagTemp, inletMassflow)
fan_results = fan_obj.compute()

fanStagTemp = fan_results["Stagnation Temp (out)"]
fanStagPress = fan_results["Stagnation Press (out)"]
fan_deltaH = fan_results["Enthalpy Rise"]
fan_powerReq = fan_results["Fan Work (W)"]

# bypass split
byp_obj = bypassSplit(fanStagPress, inletMassflow, fanStagTemp)
byp_results = byp_obj.compute()

coreMassFlow = byp_results["Core Mass Flow"]
bypMassFlow = byp_results["Bypass Mass Flow"]
bypassRatio = byp_results["Bypass Ratio"]

# high pressure compressor
hpc_obj = highPressureCompressor(fanStagPress, fanStagTemp, coreMassFlow)
hpc_results = hpc_obj.compute()

hpcStagTemp = hpc_results["Stagnation Temp (out)"]
hpcStagPress = hpc_results["Stagnation Press (out)"]
hpc_deltaH = hpc_results["Enthalpy Rise"]
hpc_powerReq = hpc_results["HPC Work (W)"]

# combustor
combustor_obj = combustor(hpcStagPress, hpcStagTemp, coreMassFlow)
combustor_results = combustor_obj.compute()

combustorStagTemp = combustor_results["Stagnation Temp (out)"]
combustorStagPress = combustor_results["Stagnation Press (out)"]
combustorQ_added = combustor_results["Heat Added"]
combustorFuelflow = combustor_results["Mass flow of fuel"]
combustorMassFlow = combustor_results["Total Mass Flow"]


# hpt
hpt_obj = highPressureTurbine(combustorStagTemp, combustorStagPress, combustorMassFlow, hpc_powerReq)
hpt_results = hpt_obj.compute()

hptStagTemp = hpt_results["Stagnation Temp (out)"]
hptStagPress = hpt_results["Stagnation Press (out)"]
hptWorkGenerated = hpt_results["Work Generated (equal to HPC required)"]

# lpt
lpt_obj = lowPressureTurbine(hptStagTemp, hptStagPress, combustorMassFlow, fan_powerReq)
lpt_results = lpt_obj.compute()



