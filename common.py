#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# Setup which GPIO pins control each station here.
stationGPIO = {
  # COMMON will be turned on along with each other station.
  "COMMON": 2,

  "FRONT_GRASS": 3,
  "FRONT_PLANTS": 17,
  "BACK_GRASS": 4,
  "BACK_PLANTS": 23,
  "DRIVEWAY_PLANTS": 22,
}

# Setup how long each station should run here.
stationRunSeconds = {
  "FRONT_GRASS": 10 * 60,
  "FRONT_PLANTS": 10 * 60,
  "BACK_GRASS": 7 * 60,
  "BACK_PLANTS": 10 * 60,
  "DRIVEWAY_PLANTS": 7 * 60,
}

########################
####  END OF SETUP  ####
########################

def init():
  GPIO.setmode(GPIO.BCM)

  for name in stationGPIO:
    pin = stationGPIO[name]

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

