#!/usr/bin/python
import RPi.GPIO as GPIO
import time

pinList = [2, 3, 4, 17, 22, 23, 10, 9]

stationMap = {
  "COMMON": 2,

  "FRONT_GRASS": 3,
  "FRONT_PLANTS": 17,
  "BACK_GRASS": 4,
  "BACK_PLANTS": 23,
  "DRIVEWAY_PLANTS": 22,
}

def init():
  GPIO.setmode(GPIO.BCM)

  # loop through pins and set mode and state to 'low'
  for i in pinList:
      GPIO.setup(i, GPIO.OUT)
      GPIO.output(i, GPIO.HIGH)

