#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import common

class Station:
  def __init__(self, name: str, gpioPin: int, runTime: int):
    self.name = name
    self.gpioPin = gpioPin
    self.runTime = runTime  

  def run(self, commonPin: int):
    common.init()

    # Common needs to be run with every station
    GPIO.output(commonPin, GPIO.LOW)

    try:  
      # TURN ON
      GPIO.output(self.gpioPin, GPIO.LOW)
      
      time.sleep(self.runTime);

      # TURN OFF
      GPIO.output(gpioPin, GPIO.HIGH)
    finally:
      GPIO.cleanup()

