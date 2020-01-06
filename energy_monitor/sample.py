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

from calculate.rootmeansquare import rootmeansquare
from calculate.sumsquares import sumsquares
from read.read_amps import read_amps
from read.read_channel import read_channel

# put this stuff here
dt = datetime.datetime.now()
print("===== sampler.py starting at ", dt.isoformat())

sample()

dt = datetime.datetime.now()
print("===== sampler.py exiting at ", dt.isoformat())



# main routine
def sample():
    # Create the I2C bus
    channels = []
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    channels[0] = AnalogIn(ads, ADS.P0)

    # get config values
    try:
        config = get_config('/home/pi/homeenergy-pi/HomeEnergy.json')
    except OSError as e:
        print("Unable to open configuration file:", e)
        exit()
        
    # Conect to database
    try:
        conn = sqlite3.connect(config["database"])
        print('Connected to database.')
    except Exception as e:
        print("Unable to open database: ", e)
        exit()

    # should: Read channels 0 and 1 from ADC
    # input = ADC, output = raw data
    # what are the parameters?
    amps0 = read_amps(adc, 0, config)

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

    
# Helper function
def get_config(file_path):
    with open(file_path) as json_data:
        config = json.load(json_data)
        print("Configuration read")
  
    return config