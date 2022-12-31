#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import common

stationRunSeconds = {
  "FRONT_GRASS": 10 * 60,
  "FRONT_PLANTS": 10 * 60,
  "BACK_GRASS": 7 * 60,
  "BACK_PLANTS": 10 * 60,
  "DRIVEWAY_PLANTS": 7 * 60,
}

def run():
  common.init()
  GPIO.output(common.stationMap["COMMON"], GPIO.LOW)

  try:  
    for name in common.stationMap:
      if name == "COMMON":
        continue

      seconds = stationRunSeconds[name]
      pin = common.stationMap[name]

      # Common needs to be run with every station

      GPIO.output(pin, GPIO.LOW)

      print (name)
      print ("GPIO pin:" + str(pin))
      print ("Going to run for " + str(seconds / 60) + " minutes")

      time.sleep(seconds);
      GPIO.output(pin, GPIO.HIGH)

      print ("Done")
      print ("")

  finally:
    GPIO.cleanup()
