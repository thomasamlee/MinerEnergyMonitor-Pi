#Monitoring Home Energy with your Raspberry Pi

[The hardware in this archive is pictured here](https://photos.app.goo.gl/bTXtFVekzwhzKs923)

The centerpice of the design is an ADC1115 analog-to-digital controller, which used I2C to communicate with the RPi.

The software consists of three parts

1. A python script that measures current and saves the readings to a database

2. A python script that transmits measurements to a destination in the cloud

3. A simple sqlite3 database

##Prerequisites

A Raspberry Pi.  I did my development on a Raspberry Pi Model 2 B. I suspect this will work fine on newer models.

Python 3 - This is probably already installed.  If not, use sudo apt-get install python3 

SQLite 3 - Install this using sudo apt-get install sqlite3 

[The ADC-based circuit described at Hackster.io](https://www.hackster.io/michael-nigbor/homeenergy-pi-cecfdf)

##Configuration
Configuration is stored in the HomeEnergy.json file. There are two sections, one for the sampler and another for
transmitter.

The A, B, C and gain values are calibration values that convert the voltages read by the ADC into amps.  They
should be close, but if you use a different current sensor or your readings are off, you may need to adjust them.
The values are the coefficients for a polynomial regression.

Transmitter values have login information as well as URLs for the web destination. 

{
  "Database": "/home/pi/HomeEnergy/HomeEnergy.db",
  "Sampler": 
  {
    "A": 0.1051,
    "B": 0.00324,
    "C": 0.0000011614,
    "gain": 1
  },
  "Transmitter":
  {
      "loginURL": "DESTINATION URL HERE",
      "currentURL": "DESTINATION URL HERE",
      "userName": "USERNAME HERE",
      "password": "PASSWORD HERE"
  }
}

##Web Destination
The idea behind the web destination is that you'll want to see the values produced by the system as graphs, gauges
charts.

I'm working on a Node-based web application that will do this. It should be published in another repo soon.