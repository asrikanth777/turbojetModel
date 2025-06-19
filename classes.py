""" Sources:

***This is to simulate a F119 Turbofan Engine used in the F22-Raptor
***Not all of the data is available (obviously), so a lot of guesses and approximations are used
***Justifications will be given for them

 - John D. Anderson, Modern Compressible Flow: With Historical Perspective, 
3rd ed., McGraw-Hill, 2002. (1)
- https://www.forecastinternational.com/archive/disp_pdf.cfm?DACH_RECNO=901 (2)
- https://easychair.org/publications/preprint/CnsW/download? (3)
- https://soaneemrana.com/onewebmedia/MECHANICS%20AND%20THERMODYNAMICS1.pdf (4)
- https://www.sciencedirect.com/science/article/pii/S2666790825000424? (5)
"""
import math
import numpy as np
import sympy as sp

class inlet:
    def __init__(self, mach, press, temp):
        self.mach = mach
        self.press = press
        self.temp = temp
        self.gamma = 1.4
        self.R = 287

        # inlet info comes from http://wikiwand.com/en/articles/Pratt_&_Whitney_F119
        # an approximation of a 40in diameter at inlet
        # 48in general diameter, 50in largest (no clue how to use these ones ngl)
        self.inletArea = 0.811

        # Defining stagnation temp and pressure (ref: ae312 module 1 notes)
    def stagnationTemperatureInlet(self):
        return self.temp * (1 + (self.gamma - 1)/2 * self.mach**2)

    def stagnationPressureInlet(self):
        return self.press * (1 + (self.gamma - 1)/2 * self.mach**2)**(self.gamma / (self.gamma - 1))

    
    def massFlowCalc(self, mach, stagtemp, stagpress, inletArea, gamma, R):
        factor = stagpress * inletArea / math.sqrt(stagtemp)
        mach_term = mach * math.sqrt(gamma)
        temp_term = (1 + ((gamma - 1) / 2) * mach**2) ** (-((gamma + 1) / (2 * (gamma - 1))))

        mass_flow = factor * mach_term * temp_term
        return mass_flow  # [kg/s]
    
    def compute(self):
        self.Tt0 = self.stagnationTemperatureInlet()
        self.Pt0 = self.stagnationPressureInlet()
        self.massflow = self.massFlowCalc()
        return {
        "Stagnation Temp (Tt0)": self.Tt0,
        "Stagnation Press (Pt0)": self.Pt0,
        "Mass Flow": self.massflow,
    }


class fan:
    # three-stage axial flow fan
    def __init__(self, stagpress, stagtemp, massflow):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.pressure_ratioFan = 4  # (2) page 2
        self.efficiencyFan = 0.91 # (3) table 3, isentropic flow
        self.massflow = massflow
        self.gamma = 1.4
        self.specificheat = 1004.5

        # stagtemp change equation from (4) page 184, equation 5.49
    def stagnationTemperatureFan(self):
        gammaexpo = (self.gamma -1) / self.gamma
        stagtempFan = self.stagtemp * (1 + (1/self.efficiencyFan) * (self.pressure_ratioFan**gammaexpo - 1))
        return stagtempFan

    def stagnationPressureFan(self):
        stagPressFan = self.stagpress * self.pressure_ratioFan
        return stagPressFan
    
    def enthalpyRiseFan(self):
        Tt_out = self.stagnationTemperatureFan()
        delta_h = self.specificheat * (Tt_out - self.stagtemp)
        return delta_h  # [J/kg]
    
    def workRequiredFan(self):
        deltaH = self.enthalpyRiseFan()
        power_done = self.massflow * deltaH 
        return power_done
    
    def compute(self):
        return {
            "Stagnation Temp (out)": self.stagnationTemperatureFan(),
            "Stagnation Press (out)": self.stagnationPressureFan(),
            "Enthalpy Rise": self.enthalpyRiseFan(),
            "Fan Work (W)": self.workRequiredFan(),
        }


class bypassSplit:
    def __init__(self, stagpress, massflow, stagtemp):
        self.bypaRatio = 0.45 # (3) table 3
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.massflow = massflow


    # stag temp and pressure dont change across
    def massflowCore(self):
        coreMF = self.massflow * (1 -self.bypaRatio)
        return coreMF
    
    def massflowBypass(self):
        bypaMF = self.massflow * self.bypaRatio
        return bypaMF
    
    def compute(self):
        return {
            "Core Mass Flow": self.massflowCore(),
            "Bypass Mass Flow": self.massflowBypass(),
            "Bypass Ratio": self.bypaRatio,
        }


class highPressureCompressor:
# six stage axial flow compressor
    def __init__(self, stagpress, stagtemp, massflow):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.hpcPressRatio = 8.75 # (1) total pressure ratio / fan pressure ratio = hpc ratio
        self.hpcEfficiency = 0.91 # (3) table 3, isentropic flow
        self.massflow = massflow
        self.gamma = 1.4
        self.specificheat = 1004.5

    # stagtemp change equation from (4) page 184, equation 5.49
    def stagnationTemperatureHPC(self):
        gammaexpo = (self.gamma -1) / self.gamma
        stagtempFan = self.stagtemp * (1 + (1/self.hpcEfficiency) * (self.hpcPressRatio**gammaexpo - 1))
        return stagtempFan

    def stagnationPressureHPC(self):
        stagPressFan = self.stagpress * self.hpcPressRatio
        return stagPressFan
    
    def enthalpyRiseHPC(self):
        Tt_out = self.stagnationTemperatureHPC()
        delta_h = self.specificheat * (Tt_out - self.stagtemp)
        return delta_h  
    
    def workRequiredHPC(self):
        deltaH = self.enthalpyRiseHPC()
        power_done = self.massflow * deltaH 
        return power_done
    
    def compute(self):
        return {
            "Stagnation Temp (out)": self.stagnationTemperatureHPC(),
            "Stagnation Press (out)": self.stagnationPressureHPC(),
            "Enthalpy Rise": self.enthalpyRiseHPC(),
            "HPC Work (W)": self.workRequiredHPC(),
        }


class combuster:
# annual combustion chamber
    def __init__(self, stagpress, stagtemp, massflow):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.titemp = 1922 # Kelvin (5) table 3
        self.massflow = massflow
        self.combustFHV = 43e6 # (3) table 4, only given JP4 and JP10, so roughly guess 43MJ/kg
        self.combEfficiency = 0.90 # (3) introduction, last sentence, citing source about general turbofan engines
        self.p_drop = 0.05 # common design ratio used, hangs around 0.04-0.07
        self.specificheat = 1004.5

    def heatAdded_combustor(self):
        Q = self.massflow * self.specificheat * (self.titemp - self.stagtemp)
        return Q
    
    def combustorfuel_flowrate(self):
        Q = self.heatAdded_combustor()
        mfuel = Q / self.combustFHV / self.combEfficiency 
        return mfuel



class highPressureTurbine:
# one stage high pressure turbine
    def __init__(self, temp, press, massflow, requiredWork, efficiency):
        self.temp = temp
        self.press = press
        self.massflow = massflow
        self.requiredWork = requiredWork
        self.efficiency = efficiency
        self.specificheat = 1004.5


class lowPressTurbine:
# one stage low pressure turbine
    def __init__(self, temp, press, massflow, requiredWork, efficiency):
        self.temp = temp
        self.press = press
        self.massflow = massflow
        self.requiredWork = requiredWork
        self.efficiency = efficiency
        self.specificheat = 1004.5


class nozzle:
    def __init__(self, stagtemp, stagpress, ambpress, massflow, nozzleEff):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.ambpress = ambpress
        self.massflow = massflow
        self.nozzleEff = nozzleEff
        self.specificheat = 1004.5
        self.gamma = 1.4
        self.R = 287


class exhaust:
    def __init__(self, noz_exitV, byp_exitV, freestrmV, massflow, bypaRatio, fuel_flow, fuel_heatingval):
        self.noz_exitV = noz_exitV
        self.byp_exitV = byp_exitV
        self.freestrmV = freestrmV
        self.massflow = massflow
        self.bypaRatio = bypaRatio
        self.fuel_flow = fuel_flow
        self.fuel_heatingval = fuel_heatingval


