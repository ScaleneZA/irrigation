#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import common

def run():
  common.init()

  # Common needs to be run with every station
  GPIO.output(common.stationGPIO["COMMON"], GPIO.LOW)

  try:  
    for name in common.stationGPIO:
      if name == "COMMON":
        continue

      seconds = common.stationRunSeconds[name]
      pin = common.stationGPIO[name]

      # TURN ON
      GPIO.output(pin, GPIO.LOW)

      print (name)
      print ("GPIO pin:" + str(pin))
      print ("Going to run for " + str(seconds / 60) + " minutes")

      time.sleep(seconds);

      # TURN OFF
      GPIO.output(pin, GPIO.HIGH)

      print ("Done")
      print ("")

  finally:
    GPIO.cleanup()
