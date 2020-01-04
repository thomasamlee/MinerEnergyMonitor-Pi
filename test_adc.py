import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c, gain=1, data_rate=860)

print(f"ads rates:{ads.rates}")
print(f"ads rate_config:{ads.rate_config}")
print(f"ads bits:{ads.bits}")

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
print(f"Raw:{chan.value}\tVoltage:{chan.voltage}V")


# print("{:>5}\t{:>5}".format('raw', 'v'))

# while True:
#     # print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
#     time.sleep(0.5)
