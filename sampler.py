# -------------------------------------------------------------------------
# Program: Reads current from ADS115 ADC and saves to database
#
# Copyright (C) 2018 Michael T. Nigbor
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License at https://www.gnu.org/licenses
#    for more details.
# -------------------------------------------------------------------------
import time
import math
import Adafruit_ADS1x15
import sqlite3
import datetime
import array
import json

dt = datetime.datetime.now()
print("===== sampler.py starting at ", dt.isoformat())

#Read configuration
try:
    with open('/home/pi/HomeEnergy/HomeEnergy.json') as json_data:
        config = json.load(json_data)
        print("Configuration read")
except IOError as e:
  print("Unable to open configuration file:", e)
  exit()
    
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
GAIN = config["Sampler"]["gain"]

# Polynomial regression coefs to estimate amps
# Based on experiments from 0 to 13 amps
A = config["Sampler"]["A"]
B = config["Sampler"]["B"]
C = config["Sampler"]["C"]

try:
    conn = sqlite3.connect(config["Database"])
    print('Connected to database.')
except Exception as e:
    print("Unable to open database: ", e)
    exit()

values = array.array('l')

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
print("Sampling started.")

try:
    adc.start_adc(0, gain=GAIN, data_rate=860)
    # Sample for one second
    start = time.time()
    while (time.time() - start) <= 1.0:
        # Read the last ADC conversion value and print it out.
        value = float(adc.get_last_result())
        values.append(value)
        if value < min:
            min = value
        if value > max:
            max = value
        n = n + 1
        sum = sum + value
        ssq = ssq + (value*value)
        #print('Channel 0: {0}'.format(value))

    # Stop continuous conversion.
    adc.stop_adc()
    print("Sampling stopped")
except ValueError as e:
    print("ADC configuration error: ", e)
    exit()
except Exception as e:
    print("Unexpected ADC error: ", e)
    exit()
    
# Calculate basic stats on the raw data
avg = float(sum)/float(n)
bias = -avg

variance = float(ssq)/n - avg*avg
stddev = math.sqrt(variance)
ssq = 0.0
sum = 0.0
n = 0

# Refigure sum and sum of squares for "valid" values
# Skipping values more that 3x stddev
for value in values:
    newValue = value + bias
    if abs(value) < avg + 3*stddev:
        ssq = ssq + newValue * newValue
        sum = sum + newValue
        n = n + 1

# Figure the RMS.
if n == 0:
    rms = 0.00
else:
    rms = math.sqrt(float(ssq)/n)
    
print('RMS: {0}'.format(rms))

# Polynomial regression to estimate amps
# Based on experiments from 0 to 13 amps
temp = A + B*rms + C*rms*rms
amps = round(temp, 2)
if amps < 0:
    amps = 0.00
print('Average Reading in Amps: {0}'.format(amps))

#Save to the database
try:
    c = conn.cursor()
    dt = datetime.datetime.now()
    sql = "INSERT INTO currentreading VALUES ( '{0}', '{1}', 0, NULL )".format( dt.isoformat(), amps)
    print( "Saving to database" )
    c.execute(sql)
    conn.commit()
except sqlite3.Error as e:
    print("Error writing to database: ", e)
    exit()
    
conn.close()
print("Database closed")

dt = datetime.datetime.now()
print("===== sampler.py exiting at ", dt.isoformat())


