""" Sources:

***This is to simulate a F119 Turbofan Engine used in the F22-Raptor
***Not all of the data is available (obviously), so a lot of guesses and approximations are used
***Justifications will be given for them

 - John D. Anderson, Modern Compressible Flow: With Historical Perspective, 
3rd ed., McGraw-Hill, 2002.
- https://www.forecastinternational.com/archive/disp_pdf.cfm?DACH_RECNO=901
- https://ntrs.nasa.gov/api/citations/20110020830/downloads/20110020830.pdf
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
    def stagnationTemperature(self):
        return self.temp * (1 + (self.gamma - 1)/2 * self.mach**2)

    def stagnationPressure(self):
        return self.press * (1 + (self.gamma - 1)/2 * self.mach**2)**(self.gamma / (self.gamma - 1))

    
    def massFlowCalc(self, mach, stagtemp, stagpress, inletArea, gamma, R):
        factor = stagpress * inletArea / math.sqrt(stagtemp)
        mach_term = mach * math.sqrt(gamma)
        temp_term = (1 + ((gamma - 1) / 2) * mach**2) ** (-((gamma + 1) / (2 * (gamma - 1))))

        mass_flow = factor * mach_term * temp_term
        return mass_flow  # [kg/s]
    
    def compute(self):
        self.Tt0 = self.stagnationTemperature(self.mach, self.temp, self.gamma)
        self.Pt0 = self.stagnationPressure(self.mach, self.press, self.gamma)
        self.massflow = self.massFlowCalc(self.mach, self.Tt0, self.Pt0, self.inletArea, self.gamma, self.R)


class fan:
    # three-stage fan
    def __init__(self, stagpress, stagtemp, massflow, pressure_ratio, efficiency):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.pressure_ratio = 4  # Forecast International (PAT130A1) — full 3-stage F119 fan
        self.efficiency = 0.857 # NASA TM-2011-216769 — experimental high-efficiency fan stage
        self.massflow = massflow


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


