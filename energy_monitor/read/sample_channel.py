import time
import board
import busio
from threading import Timer
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


# 
def sample_channel(chan, g):
    values = []

    # Create single-ended input on channel 0
    chan = AnalogIn(ads, ADS.P0)
    print(f"Raw:{chan.value}\tVoltage:{chan.voltage}V")

    # Sample for 1 second
    # use threading.Timer() instead
    start = time.time()
    while (time.time() - start) <= 1.0:
        # # Read the last ADC conversion value and print it out.
        # value = float(adc.get_last_result())
        # values.append(value)
        # print('Channel {0}: {1}'.format(chan,value))
        values.append(chan.value)
        
    return values

