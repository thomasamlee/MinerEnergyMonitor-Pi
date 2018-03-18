Monitoring Home Energy with your Raspberry Pi

The software in this archive is pictured here:

https://photos.app.goo.gl/bTXtFVekzwhzKs923

The main piece of hardware pictured here is an ADC1115 analog-to-digital controller.

The software consists of three parts

A python script that measures current and saves the readings to a database

A python script that transmits measurements to a destination in the cloud

A simple sqlite3 database

Prerequisites

A Raspberry Pi.  I did my development on a Raspberry Pi Model 2 B. I suspect this will work fine on newer models.

Python 3 - This is probably already installed.  If not, use sudo apt-get install python3 

SQLite 3 - Install this using sudo apt-get install sqlite3 

The ADC-based circuit described at Hackster.io. 