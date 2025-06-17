""" Sources:

***This is to simulate a F119 Turbofan Engine used in the F22-Raptor
***Not all of the data is available (obviously), so a lot of guesses and approximations are used
***Justifications will be given for them

 - John D. Anderson, Modern Compressible Flow: With Historical Perspective, 
3rd ed., McGraw-Hill, 2002. (1)
- https://www.forecastinternational.com/archive/disp_pdf.cfm?DACH_RECNO=901 (2)
- https://ntrs.nasa.gov/api/citations/20110020830/downloads/20110020830.pdf (3)
- https://soaneemrana.com/onewebmedia/MECHANICS%20AND%20THERMODYNAMICS1.pdf (4)
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
        self.Tt0 = self.stagnationTemperatureInlet(self.mach, self.temp, self.gamma)
        self.Pt0 = self.stagnationPressureInlet(self.mach, self.press, self.gamma)
        self.massflow = self.massFlowCalc(self.mach, self.Tt0, self.Pt0, self.inletArea, self.gamma, self.R)


class fan:
    # three-stage fan
    def __init__(self, stagpress, stagtemp, massflow):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.pressure_ratio = 4  # (2) page 2
        self.efficiency = 0.857 # (3) page 6 table 1
        self.massflow = massflow
        self.gamma = 1.4
        self.specificheat = 1004.5

        # stagtemp change equation from (4) page 184, equation 5.49
    def stagnationTemperatureFan(self):
        gammaexpo = (self.gamma -1) / self.gamma
        stagtempFan = self.stagtemp * (1 + (1/self.efficiency) * (self.pressure_ratio**gammaexpo - 1))
        return stagtempFan

    def stagnationPressureFan(self):
        stagPressFan = self.stagpress * self.pressure_ratio
        return stagPressFan
    
    def enthalpyRiseFan(self):
        Tt_out = self.stagnationTemperatureFan()
        delta_h = self.specificheat * (Tt_out - self.stagtemp)
        return delta_h  # [J/kg]
    
    def workRequiredFan(self):
        deltaH = self.enthalpyRiseFan()
        power_done = self.massflow * deltaH 
        return power_done


class bypassSplit:
    def __init__(self, bypaRatio, stagpress, massflow, stagtemp):
        self.bypaRatio = 0.45
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.massflow = massflow


class highPressureCompressor:
    def __init__(self, stagpress, stagtemp, hpcPressRatio, hpcEfficiency, massflow):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.hpcPressRatio = hpcPressRatio
        self.hpcEfficiency = hpcEfficiency
        self.massflow = massflow


class combuster:
    def __init__(self, stagpress, stagtemp, titemp, massflow, combEfficiency, hPR):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.titemp = titemp
        self.massflow = massflow
        self.combEfficiency = combEfficiency
        self.hPR = hPR


class highPressureTurbine:
    def __init__(self, temp, press, massflow, requiredWork, efficiency):
        self.temp = temp
        self.press = press
        self.massflow = massflow
        self.requiredWork = requiredWork
        self.efficiency = efficiency
        self.specificheat = 1004.5


class lowPressTurbine:
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


