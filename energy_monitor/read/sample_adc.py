import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


# 
def sample_adc(chan, g):
    values = []

    # Create single-ended input on channel 0
    chan = AnalogIn(ads, ADS.P0)
    print(f"Raw:{chan.value}\tVoltage:{chan.voltage}V")

    # Sample for 1 second
    # use threading.Timer() instead
    start = time.time()
    while (time.time() - start) <= 1.0:
        values.append(chan.value)
        
    return values

