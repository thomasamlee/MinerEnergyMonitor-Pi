import time
import math
import datetime
import array
import json
import sqlite3
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


# ----
# main routine here
# ----

# timestamp for start
dt = datetime.datetime.now()
print("===== sampler.py starting at ", dt.isoformat())

# Read configuration
# try:
#     with open('/home/pi/homeenergy-pi/HomeEnergy.json') as json_data:
#         config = json.load(json_data)
#         print("Configuration read")
# except IOError as e:
#     print("Unable to open configuration file:", e)
#     exit()


# Create the I2C bus

i2c = busio.I2C(board.SCL, board.SDA)

# , ADC object
ads = ADS.ADS1115(i2c)

channel = AnalogIn(ads, ADS.P0)

# open database connection
# try:
#     conn = sqlite3.connect(config["Database"])
#     print('Connected to database.')
# except Exception as e:
#     print("Unable to open database: ", e)
#     exit()

# Read channels 0 and 1 from ADC
amps0 = readAmps(adc, 0, config)
amps1 = readAmps(adc, 1, config)

# Save to database
try:
    c = conn.cursor()
    dt = datetime.datetime.now()
    sql = "INSERT INTO currentreading VALUES ( '{0}', '{1}', '{2}', NULL )".format(
        dt.isoformat(), amps0, amps1)
    print("Saving to database")
    c.execute(sql)
    conn.commit()
except sqlite3.Error as e:
    print("Error writing to database: ", e)
    exit()

# close database connection
conn.close()
print("Database closed")

# timestamp for done
dt = datetime.datetime.now()
print("===== sampler.py exiting at ", dt.isoformat())

# Helper function below. Should become module or class


# Read and compute the amperage on the specified channel
def readAmps(adc, chan, config):

    # Channel A
    chanid = "A{}".format(chan)
    print("Sampling " + chanid)
    GAIN = config["Sampler"][chanid]["gain"]
    A = config["Sampler"][chanid]["A"]
    B = config["Sampler"][chanid]["B"]
    C = config["Sampler"][chanid]["C"]

    n = 0
    sum = 0.0
    ssq = 0
    rms = 0
    max = 0
    min = 0
    amps = 0
    values = []

    # The inductive sensor returns an AC voltage. Sample at the
    # maximum rate for 1 second.  Then calculate the RMS of
    # the sampled readings
    # what is the max rate?
    print("Sampling started.")

    try:
        values = readChannel(adc, chan, GAIN)
        n = len(values)
        print("Sampling stopped")
    except ValueError as e:
        print("ADC configuration error: ", e)
        exit()
    except Exception as e:
        print("Unexpected ADC error: ", e)
        exit()

    # Calculate basic stats on the raw data
    avg = average(values)
    ssq = sumsquares(values)
    bias = -avg
    print("ssq ", ssq)
    print("avg", avg)
    print("bias", bias)

    variance = float(ssq)/n - avg*avg
    print("variance", variance)
    stddev = math.sqrt(variance)
    print("stddev", stddev)

    # Calculate the RMS
    rms = rootmeansquare(values, avg, stddev, bias)

    # Polynomial regression to estimate amps
    # Based on experiments from 0 to 13 amps
    # Constants stored in config file.
    temp = A + B*rms + C*rms*rms
    print("A", A)
    print("B", B)
    print("C", C)

    # Round to 2 decimal places
    amps = round(temp, 2)
    if amps < 0:
        amps = 0.00
    print('Average Reading in Amps: {0}'.format(amps))

    return amps


# Calculate RMS excluding noisey values more than 3x std dev
def rootmeansquare(values, avg, stddev, bias):
    ssq = 0.0
    sum = 0.0
    n = 0

    for value in values:
        newValue = value + bias
        # Skip values more that 3x stddev
        if abs(value) < avg + 3*stddev:
            ssq = ssq + newValue * newValue
            sum = sum + newValue
            n = n + 1

    # Figure the RMS, which is the square root of the average of the
    # sum of squares figured above
    if n == 0:
        rms = 0.00
    else:
        rms = math.sqrt(float(ssq)/n)
    print('RMS: {0}'.format(rms))
    return rms


# # Calculate the average value
def average(values):
    sum = 0
    for value in values:
        sum = sum + value
    avg = sum/len(values)
    return avg


# # Calculate sum of squares
def sumsquares(values):
    ssq = 0
    for value in values:
        ssq = ssq + value * value

    return ssq


# Read an ADC channel with the specified gain at max rate for 1 second
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
