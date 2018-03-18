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