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



