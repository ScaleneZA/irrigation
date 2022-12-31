#!/usr/bin/python
import RPi.GPIO as GPIO
import time

stationGPIO = {
  "COMMON": 2,

  "FRONT_GRASS": 3,
  "FRONT_PLANTS": 17,
  "BACK_GRASS": 4,
  "BACK_PLANTS": 23,
  "DRIVEWAY_PLANTS": 22,
}

def init():
  GPIO.setmode(GPIO.BCM)

  for name in stationGPIO:
    pin = stationGPIO[name]

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

