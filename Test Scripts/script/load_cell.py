#!/usr/bin/env python3
import time 
import PyNAU7802
from smbus2 import SMBus
 
i2c_address = 0x2A

bus = SMBus(6)
scale = PyNAU7802.NAU7802()
scale.begin(bus)

scale.setSampleRate(PyNAU7802.NAU7802_SPS_320) 
scale.setGain(PyNAU7802.NAU7802_GAIN_64)
scale.calibrateAFE() 

# Zero Offset
scale.calculateZeroOffset(100)

# Calibrating
# print("Put known mass on load cell")
# cal = float(input("Mass in kg: "))
# scale.calculateCalibrationFactor(cal) 
# print("Calibration factor: {0}".format(scale.getCalibrationFactor()))

# while(True):
#    print("Thrust: {0:0.4f}" .format(scale.getWeight()))     
#    print("Reading: {0:0.4f}" .format(scale.getReading()))
#    time.sleep(0.5)

# Set Calibration Factor
scale.setCalibrationFactor(-105210.9504)
    
def take_thrust():
    while(True):
        return ("{0:0.4f}" .format(scale.getWeight()))
        time.sleep(0.1)
