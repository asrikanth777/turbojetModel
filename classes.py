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
https://www.researchgate.net/publication/352295971_Efficiencies_and_losses_comparison_of_various_turbofan_engines_for_aircraft_propulsion (6)
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
        # an approximation of a 100cm diameter at inlet
        # 120cm general diameter, 130cm largest (no clue how to use these ones ngl)
        self.inletArea = 0.7854 # m^2

        # Defining stagnation temp and pressure (ref: ae312 module 1 notes)
    def stagnationTemperatureInlet(self):
        self.stagTempInlet = self.temp * (1 + (self.gamma - 1)/2 * self.mach**2)
        return self.stagTempInlet

    def stagnationPressureInlet(self):
        self.stagPressInlet = self.press * (1 + (self.gamma - 1)/2 * self.mach**2)**(self.gamma / (self.gamma - 1))
        return self.stagPressInlet
    
    def massFlowCalc(self):

        factor = self.stagPressInlet * self.inletArea / math.sqrt(self.stagTempInlet)
        mach_term = self.mach * math.sqrt(self.gamma)
        temp_term = (1 + ((self.gamma - 1) / 2) * self.mach**2) ** (-((self.gamma + 1) / (2 * (self.gamma - 1))))
        self.mass_flow = factor * mach_term * temp_term
        return self.mass_flow  # [kg/s]
    
    def compute(self):
        self.stagnationTemperatureInlet()
        self.stagnationPressureInlet()
        self.massFlowCalc()
        return {
        "Stagnation Temp (Tt0)": self.stagTempInlet,
        "Stagnation Press (Pt0)": self.stagPressInlet,
        "Mass Flow": self.mass_flow,
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
        self.stagtempFan = self.stagtemp * (1 + (1/self.efficiencyFan) * (self.pressure_ratioFan**gammaexpo - 1))
        return self.stagtempFan

    def stagnationPressureFan(self):
        self.stagPressFan = self.stagpress * self.pressure_ratioFan
        return self.stagPressFan
    
    def enthalpyRiseFan(self):
        Tt_out = self.stagnationTemperatureFan()
        self.deltaH_fan = self.specificheat * (Tt_out - self.stagtemp)
        return self.deltaH_fan # [J/kg]
    
    def workRequiredFan(self):
        deltaH = self.enthalpyRiseFan()
        self.powerReq_fan = self.massflow * deltaH 
        return self.powerReq_fan
    
    def compute(self):
        self.stagnationTemperatureFan()
        self.stagnationPressureFan()
        self.enthalpyRiseFan()
        self.workRequiredFan()
        return {
            "Stagnation Temp (out)": self.stagtempFan,
            "Stagnation Press (out)": self.stagPressFan,
            "Enthalpy Rise": self.deltaH_fan,
            "Fan Work (W)": self.powerReq_fan,
        }


class bypassSplit:
    def __init__(self, stagpress, massflow, stagtemp):
        self.bypaRatio = 0.45 # (3) table 3
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.massflow = massflow

    # stag temp and pressure dont change across
    def massflowCore(self):
        self.coreMF = self.massflow / (1 + self.bypaRatio)
        return self.coreMF
    
    def massflowBypass(self):
        self.bypaMF = self.massflow - self.coreMF
        return self.bypaMF
    
    def compute(self):
        self.massflowCore()
        self.massflowBypass()
        return {
            "Core Mass Flow": self.coreMF,
            "Bypass Mass Flow": self.bypaMF,
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
        # work generated by turbine equals work required for compressor/fan

    # stagtemp change equation from (4) page 184, equation 5.49
    def stagnationTemperatureHPC(self):
        gammaexpo = (self.gamma -1) / self.gamma
        self.stagtempHPC = self.stagtemp * (1 + (1/self.hpcEfficiency) * (self.hpcPressRatio**gammaexpo - 1))
        return self.stagtempHPC

    def stagnationPressureHPC(self):
        self.stagPressHPC = self.stagpress * self.hpcPressRatio
        return self.stagPressHPC
    
    def enthalpyRiseHPC(self):
        Tt_out = self.stagnationTemperatureHPC()
        self.deltaH_HPC = self.specificheat * (Tt_out - self.stagtemp)
        return self.deltaH_HPC  
    
    def workRequiredHPC(self):
        deltaH = self.enthalpyRiseHPC()
        self.powerReq_HPC = self.massflow * deltaH 
        return self.powerReq_HPC
    
    def compute(self):
        self.stagnationTemperatureHPC()
        self.stagnationPressureHPC()
        self.enthalpyRiseHPC()
        self.workRequiredHPC()
        return {
            "Stagnation Temp (out)": self.stagtempHPC,
            "Stagnation Press (out)": self.stagPressHPC,
            "Enthalpy Rise": self.deltaH_HPC,
            "HPC Work (W)": self.powerReq_HPC,
        }


class combustor:
# annual combustion chamber
    def __init__(self, stagpress, stagtemp, massflow):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.titemp = 1922 # Kelvin (5) table 3
        self.massflow = massflow
        self.combustFHV = 43e6 # (3) table 4, only given JP4 and JP10, so roughly guess 43MJ/kg
        self.combEfficiency = 0.95 # (6) Figure 4, for Engine 4
        # Engine 4 layout: fan -> hpc -> cc -> hpt -> lpt -> nozzle
        self.p_drop = 0.05 # common design ratio used, hangs around 0.04-0.07
        self.specificheat = 1004.5

    def heatAdded_combustor(self):
        self.Q = self.massflow * self.specificheat * (self.titemp - self.stagtemp)
        return self.Q
    
    def combustorfuel_flowrate(self): # (4) page 243
        self.mfuel = self.heatAdded_combustor() / (self.combustFHV * self.combEfficiency) 
        return self.mfuel
    
    def stagnationTemperatureCombust(self):
        self.stagTempComb = self.titemp # exit stag temp is turbine inlet temperature
        return self.stagTempComb

    def stagnationPressureCombust(self):
        self.stagPressComb = self.stagpress * (1 - self.p_drop)
        return self.stagPressComb

    
    def compute(self):
        self.heatAdded_combustor()
        self.combustorfuel_flowrate()
        self.stagnationTemperatureCombust()
        self.stagnationPressureCombust()
        self.massFlowTotal = self.mfuel + self.massflow
        return {
            "Stagnation Temp (out)": self.stagTempComb,
            "Stagnation Press (out)": self.stagPressComb,
            "Heat Added": self.Q,
            "Mass flow of fuel": self.mfuel,
            "Total Mass Flow": self.massFlowTotal
        }



class highPressureTurbine:
# one stage high pressure turbine
    def __init__(self, stagtemp, stagpress, massflow, HPCrequiredWork):
        self.stagtemp = stagtemp
        self.stagpress = stagpress
        self.massflow = massflow
        self.HPCrequiredWork = HPCrequiredWork
        self.efficiency = 0.9291 # (6) Figure 4, for Engine 4
        # Engine 4 layout: fan -> hpc -> cc -> hpt -> lpt -> nozzle
        # doesnt include afterburner but we can work around that
        self.specificheat = 1004.5
        self.gamma = 1.4
        # work generated by HPturbine equals work required for HPC

    def stagnationTemperatureHPT(self):
        delta_h = self.HPCrequiredWork / (self.massflow * self.efficiency)
        self.stagTempHPT = self.stagtemp - (delta_h / self.specificheat)
        return self.stagTempHPT

    def stagnationPressureHPT(self):
        T_out = self.stagTempHPT
        T_ratio = T_out / self.stagtemp
        exponent = self.gamma / (self.gamma - 1)
        pressureRatio = (1 - (1/self.efficiency) * (1 - T_ratio)) ** exponent
        self.stagPressHPT = pressureRatio * self.stagpress
        return self.stagPressHPT
    
    def compute(self):
        self.stagnationTemperatureHPT()
        self.stagnationPressureHPT()
        return {
            "Stagnation Temp (out)": self.stagTempHPT,
            "Stagnation Press (out)": self.stagPressHPT,
            "Work Generated (equal to HPC required)": self.HPCrequiredWork
        }

class lowPressureTurbine:
# one stage low pressure turbine
    def __init__(self, stagtemp, stagpress, massflow, fanRequiredWork):
        self.stagtemp = stagtemp
        self.stagpress = stagpress
        self.massflow = massflow
        self.fanRequiredWork = fanRequiredWork
        self.efficiency =  0.9035 # (6) Figure 4, Engine 3
        self.specificheat = 1004.5
        self.gamma = 1.4
        # work generated by LPturbine equals work required for fan

    def stagnationTemperatureLPT(self):
        delta_h = self.fanRequiredWork / (self.massflow * self.efficiency)
        self.stagTempLPT = self.stagtemp - (delta_h / self.specificheat)
        return self.stagTempLPT

    def stagnationPressureLPT(self):
        T_out = self.stagTempLPT
        T_ratio = T_out / self.stagtemp
        exponent = self.gamma / (self.gamma - 1)
        pressureRatio = (1 - (1/self.efficiency) * (1 - T_ratio)) ** exponent
        self.stagPressLPT = pressureRatio * self.stagpress
        return self.stagPressLPT

    def compute(self):
        self.stagnationTemperatureLPT()
        self.stagnationPressureLPT()
        return {
            "Stagnation Temp (out)": self.stagTempLPT,
            "Stagnation Press (out)": self.stagPressLPT,
            "Work Generated (equal to fan required)": self.fanRequiredWork
        }
    
class mixer:
    def __init__(self, coremassflow, lptstagtemp, lptstagpress, bypassmassflow, fanstagtemp, fanstagpress):
        self.coremassflow = coremassflow
        self.lptstagtemp = lptstagtemp
        self.lptstagpress = lptstagpress
        self.bypassmassflow = bypassmassflow
        self.fanstagtemp = fanstagtemp
        self.fanstagpress = fanstagpress
        self.specificheat = 1004.5
        self.gamma = 1.4
        self.p_drop = 0.01 # (7) page 9 on mixer performance, between 0.9-1.2 mach 8 and 0.8-1.1 mach 1.4

    def mixedMassFlow(self):
        self.mixedMF = self.coremassflow + self.bypassmassflow
        return self.mixedMF
    
    def mixedStagnationTemperature(self):
        self.stagTempMixed = (self.coremassflow * self.lptstagtemp + \
            self.bypassmassflow * self.fanstagtemp) / self.mixedMF
        return self.stagTempMixed

    def mixedStagnationPressure(self): # simplification, assuming lower stagpress to not risk having higher pressure
        self.stagPressMixed = min(self.fanstagpress, self.lptstagpress) * (1 - self.p_drop)
        return self.stagPressMixed
    
    def compute(self):
        self.mixedMassFlow()
        self.mixedStagnationTemperature()
        self.mixedStagnationPressure()
        return {
            "Mixed Mass Flow": self.mixedMF,
            "Stagnation Temp (out)": self.stagTempMixed,
            "Stagnation Press (out)": self.stagPressMixed
        }

class afterBurner:
    def __init__(self, stagtemp, stagpress, massflow):
    # military information, so a lot of these are ballpark estimations i made
    # not complete guess tho, just based on what i saw online
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.massflow = massflow
        self.afterburnertemp = 2450 # K
        self.p_drop = 0.05
        self.afterburnerEfficiency = 0.95 
        self.afterburnerFHV = 43e6
        self.specificheat = 1004.5

    def heatAdded_afterburner(self):
        self.Q = self.massflow * self.specificheat * (self.afterburnertemp - self.stagtemp)
        return self.Q
    
    def afterburnerfuel_flowrate(self): # (4) page 243
        self.mfuel = self.heatAdded_afterburner() / (self.afterburnerFHV * self.afterburnerEfficiency) 
        return self.mfuel
    
    def stagnationTemperatureAfterburner(self):
        self.stagTempAF = self.afterburnertemp # exit stag temp is turbine inlet temperature
        return self.stagTempAF

    def stagnationPressureAfterburner(self):
        self.stagPressAF = self.stagpress * (1 - self.p_drop)
        return self.stagPressAF
    
    def compute(self):
        self.stagnationTemperatureAfterburner()
        self.stagnationPressureAfterburner()
        self.heatAdded_afterburner()
        self.afterburnerfuel_flowrate()
        return {
            "Stagnation Temp (out)": self.stagTempAF,
            "Stagnation Press (out)": self.stagPressAF,
            "Heat Added": self.Q,
            "Mass flow of fuel": self.mfuel,
        }
    


class nozzle:
    def __init__(self, stagtemp, stagpress, ambpress, massflow, desiredMach):
        self.stagpress = stagpress
        self.stagtemp = stagtemp
        self.ambpress = ambpress
        self.massflow = massflow
        self.nozzleEff = 0.97 # approximation
        self.specificheat = 1004.5
        self.gamma = 1.4
        self.R = 287

        # max mach of 2.25, using 130cm max diameter, calculating nozzle throat area
        # finding throat, i can change nozzle exit area using isentropic relations and desired mach number
        self.nozzleExitMax = 1.327 # m^2
        self.topMach = 2.25
        self.nozzleThroat = 0.463 # m^2
        self.desiredMach = desiredMach

    def nozzleExitSize(self):
        M = self.desiredMach
        gamma = self.gamma
        area_ratio = (1 / M) * ((2 / (gamma + 1)) * (1 + (gamma - 1)/2 * M**2)) ** ((gamma + 1) / (2 * (gamma - 1)))
        self.nozzleExit = self.nozzleThroat * area_ratio
        return self.nozzleExit
    
    def staticTemperatureNozzle(self):
        self.tempNozzle = self.stagtemp / (1 + (self.gamma - 1)/2 * self.desiredMach**2)
        return self.tempNozzle

    def staticPressureNozzle(self):
        self.pressNozzle = self.stagpress / (1 + (self.gamma - 1)/2 * self.desiredMach**2)**(self.gamma / (self.gamma - 1))
        return self.pressNozzle

    def nozzleExitVelocity(self):
        a = math.sqrt(self.gamma * self.R * self.tempNozzle)
        self.nozzleVelocity = a * self.desiredMach
        return self.nozzleVelocity
    
    def compute(self):
        self.nozzleExitSize()
        self.staticTemperatureNozzle()
        self.staticPressureNozzle()
        self.nozzleExitVelocity()

        return {
            "Nozzle Exit Size": self.nozzleExit,
            "Nozzle Exit Velocity": self.nozzleVelocity,
            "Static Temp (out)": self.tempNozzle,
            "Static Press (out)": self.pressNozzle,
        }



class exhaust:
    def __init__(self, noz_exitV, byp_exitV, freestrmV, massflow, bypaRatio, fuel_flow, fuel_heatingval):
        self.noz_exitV = noz_exitV
        self.byp_exitV = byp_exitV
        self.freestrmV = freestrmV
        self.massflow = massflow
        self.bypaRatio = bypaRatio
        self.fuel_flow = fuel_flow
        self.fuel_heatingval = fuel_heatingval


