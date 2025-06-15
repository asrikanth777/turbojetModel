""" Sources:
 - John D. Anderson, Modern Compressible Flow: With Historical Perspective, 
3rd ed., McGraw-Hill, 2002.

"""


class inlet:
    def __init__(self, mach, press, temp):
        self.mach = mach
        self.press = press
        self.temp = temp
        self.gamma = 1.4
        self.R = 287

        # Defining stagnation temp and pressure (ref: ae312 module 1 notes)
    def stagnationTemperature(self, mach, temp, gamma):
        stagtemp = temp * (1 + (gamma - 1)/2 * mach**2)
        return stagtemp

    def stagnationPressure(self, mach, press, gamma):
        stagpress = press * (1 + (gamma - 1)/2 * mach**2)**(gamma/(gamma-1))
        return stagpress 

class fan:
    def __init__(self, stagpress, stagtemp, massflow, pressure_ratio, efficiency):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.pressure_ratio = pressure_ratio
        self.efficiency = efficiency 
        self.massflow = massflow

class bypassSplit:
    def __init__(self, bypaRatio, stagpress, massflow, stagtemp):
        self.bypaRatio = bypaRatio
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.massflow = massflow

class lowPressureCompressor:
    def __init__(self, stagpress, stagtemp, lpcPressRatio, lpcEfficiency, massflow):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.lpcPressRatio = lpcPressRatio
        self.lpcEfficiency = lpcEfficiency
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


