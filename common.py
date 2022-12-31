#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import config

def init():
  GPIO.setmode(GPIO.BCM)

  for name in config.stationGPIO:
    pin = config.stationGPIO[name]

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

