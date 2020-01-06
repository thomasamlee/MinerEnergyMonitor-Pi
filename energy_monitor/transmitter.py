# -------------------------------------------------------------------------
# Program: Transmits current readings from a SQLite db to a rest service
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
import sys
import time
import math
import sqlite3
import datetime
import array
import requests
import json
from datetime import datetime
from config.get_config import get_config

print("===== transmitter.py starting at ", datetime.now().isoformat())

#Read configuration
try:
  config = get_config('/home/pi/homeenergy-pi/HomeEnergy.json')
except IOError as e:
  print("Unable to open configuration file:", e)
  exit()

  
url_login = config["transmitter"]["loginURL"]
url_reading = config["transmitter"]["currentURL"]

# Open the database
try:
  conn = sqlite3.connect(config["Database"])
except Exception as e:
  print("Unable to open database: ", e)
  exit()
        

# Get a session cookie from the server
login_data = {
  'username' : config["transmitter"]["userName"],
  'password' : config["transmitter"]["password"]
}

try:
  print("Getting access token")
  response = requests.post(url_login, login_data)
  if not response.ok:
    print("Error getting token: ", response.text)
    sys.exit(99)
except requests.exceptions.RequestException as e:  #
    print("Unable to get token: ", e)
    sys.exit()

json_data = json.loads(response.text)
tok = json_data["token"]
print( "Token Recieved" )

# Put the token into a cookie dictionary to use in later posts
myCookieDict = {'token': tok}

# Select readings that have not been transmitted yet
try:
  c = conn.cursor()
  rowIDs = []

  c.execute("SELECT rowid, * FROM currentreading LIMIT 20")

  # Loop over the readings, transmit then delete it from the database
  for row in c:
    printableRow = '{0}, {1}, {2}, {3}'.format(row[0], row[1], row[2], row[3])
    reading = {
      'readingdate' : row[1],
      'current1' : row[2],
      'current2' : row[3]
    }
    print( "Posting: " + printableRow)

    #post this row to the cloud service
    r = requests.post(url_reading, data=reading, cookies=myCookieDict)
    if not r.ok:
      print("Error posting data to the server: ", r.text)
      sys.exit(99)

    rowIDs.append( row[0] )

  # Delete these rows
  for rowid in rowIDs:
    sql = "DELETE FROM currentreading WHERE ROWID = '{0}'".format( rowid )
    print(sql)
    c.execute(sql)
    conn.commit()

except Exception as e:
  print("Error processing readings:", e)
  exit()    
  conn.rollback()
finally:
  conn.close()

print('===== transmitter.py exiting at ', datetime.now().isoformat())


