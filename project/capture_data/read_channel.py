import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


def read_channel(adc, chan, g):
    values = []
    adc.start_adc(chan, gain=g, data_rate=860)

    # Sample for one second

    # does this need to be made?
    start = time.time()
    while (time.time() - start) <= 1.0:
        # Read the last ADC conversion value and print it out.
        value = float(adc.get_last_result())
        values.append(value)
        # print('Channel {0}: {1}'.format(chan,value))

    # Stop continuous conversion.
    adc.stop_adc()

    return values


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    time.sleep(0.5)
