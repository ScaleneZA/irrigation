#!/usr/bin/python
# This script can be used to run all the stations for their default run-time.

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import RPi.GPIO as GPIO

import config

for station in config.stations:
  try:
    print (station.name)
    print ("GPIO pin:" + station.gpiopin)
    print ("Going to run for " + str(station.runtime / 60) + " minutes")

    station.run(config.commonPin)

    print ("Done")
    print ("")
  except KeyboardInterrupt:
    GPIO.cleanup()

