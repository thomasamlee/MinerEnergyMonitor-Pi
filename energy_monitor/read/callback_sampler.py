#!/usr/bin/env python2.7
# -------------------------------------------------------------------------
# Program: Reads current from ADS115 ADC computes RMS then saves to DB
#
# Copyright (C) 2019 Michael T. Nigbor
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

# Put ADS1115 in continous, comparative sampling
# Enable RDY pin so it pulses when each sample is ready
# Setup GPIO so that it calls a function with each pulse

import time
import math
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
# import adafruit_ads1x15.ads1015 as ADS
import Queue
from threading import Thread
import sqlite3
import datetime
import array
import json

# 
dt = datetime.datetime.now()
print("===== callback_sampler.py starting at ", dt.isoformat())

# Read configuration
try:
    with open('/home/pi/HomeEnergy/HomeEnergy.json') as json_data:
        config = json.load(json_data)
        print("Configuration read")
except IOError as e:
    print("Unable to open configuration file:", e)
    exit()

keep_going = True

# Create instance of ADS1115
adc = Adafruit_ADS1x15.ADS1115()

# Initialize the GPIO
GPIO.setmode(GPIO.BCM)

# Queue to hold values
q = Queue.Queue(maxsize=860)

# Set up the ADC
GAIN = 1

# This function is called when the ADC says there's a value to read


def queue_sample(channel):
    value = adc.get_last_result()
    if q.full():
        q.get()
    q.put(value)

# This function runs in a thread (or maybe a separate process)
# It wakes up once per second, pulls a second's worth of values
# from the queue, computes and stores an RMS value.


def compute_rms():

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

    while keep_going:
        time.sleep(1)

        if keep_going == False:
            return

        n = 0
        sum = 0.0
        ssq = 0
        rms = 0
        max = 0
        min = 0
        amps = 0

        # Pull up to 860 values from the queue
        print "Reading %d values from queue" % q.qsize()
        for value in iter(q.get, None):
            n = n + 1
            if n > 860:
                break
            sum = sum + value
            ssq = ssq + (value*value)

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

        # Save to the database
        try:
            c = conn.cursor()
            dt = datetime.datetime.now()
            sql = "INSERT INTO currentreading VALUES ( '{0}', '{1}', 0, NULL )".format(
                dt.isoformat(), amps)
            print("Saving to database")
            c.execute(sql)
            conn.commit()
        except sqlite3.Error as e:
            print("Error writing to database: ", e)

    conn.close()
    print("Database closed")


# ADS1115 RDY connected to GPIO 24 results in call to my_callback
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=queue_sample)

try:
    print "Starting sampling"

    # To enable the RDY pin,
    # Set the MSB of the HI_Thresh register to 1
    # Set the MSB of the LO_Thresh register to 0
    adc.start_adc_comparator(0,  # Channel number
                             32768, 0,  # High threshold value, low threshold value
                             data_rate=860,
                             active_low=False, traditional=True, latching=False,
                             num_readings=1, gain=GAIN)

    # Start the RMS thread
    t = Thread(target=compute_rms)
    t.start()

    # Put the main thread to sleep
    # TODO: Run until you stop collecting data.
    time.sleep(10)

except KeyboardInterrupt:
    keep_going = False
    adc.stop_adc()

keep_going = False
GPIO.cleanup()
adc.stop_adc()
time.sleep(2)

dt = datetime.datetime.now()
print("===== sampler.py exiting at ", dt.isoformat())
