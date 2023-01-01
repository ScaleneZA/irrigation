#!/usr/bin/python
# This script can be used to force stop all stations.
import RPi.GPIO as GPIO

for station in globals()["stations"]:
    station.stop(config.commonPin)

GPIO.cleanup()