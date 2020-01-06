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
from config.get_config import get_config
from datetime import datetime
from statistics import mean, stdev, variance
from calculate.rootmeansquare import rootmeansquare
from calculate.calc_current import calc_current


print("===== sampler.py starting at ", datetime.now().isoformat())
sample()
print("===== sampler.py exiting at ", datetime.now().isoformat())


# main routine
def sample():

    # get config values
    try:
        config = get_config('/home/pi/homeenergy-pi/HomeEnergy.json')
    except IOError as e:
        print("Unable to open configuration file:", e)
        exit()
        
    # Conect to database
    # try:
    #     conn = sqlite3.connect(config["database"])
    #     print('Connected to database.')
    # except Exception as e:
    #     print("Unable to open database: ", e)
    #     exit()

    # setup channel
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan = AnalogIn(ads, ADS.P0)


    # Read raw values
    raw_values = []

    try:
        # def read_adc(): (later)
        start = time.time()
        while (time.time() - start) <= 1.0:
            value = chan.value
            voltage = chan.voltage
            print(f"Raw:{value}\tVoltage:{voltage}V")
            raw_values.append(value)

        print("Sampling stopped")
    except ValueError as e:
        print("ADC configuration error: ", e)
        exit()
    except Exception as e:
        print("Unexpected ADC error: ", e)
        exit()

    # Calculations
    current = calc_current(raw_values, config)


    # Save to database
    # try:
    #     conn = conn.cursor()
    #     sql_string = f"INSERT INTO currentreading VALUES ('{datetime.now().isoformat()}', '{amps0}', '{amps1}', NULL )"
    #     print("Saving to database")
    #     c.execute(sql_string)
    #     conn.commit()
    # except sqlite3.Error as e:
    #     print("Error writing to database: ", e)
    #     exit()

    # close database connection
    conn.close()
    print("Database closed")