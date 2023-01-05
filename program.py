#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import config

def runOne(station):
    GPIO.setmode(GPIO.BCM)

    try:
        GPIO.setup(config.commonPin, GPIO.OUT)
        GPIO.output(config.commonPin, GPIO.HIGH)
        GPIO.output(config.commonPin, GPIO.LOW)

        GPIO.setup(station["gpiopin"], GPIO.OUT)
        GPIO.output(station["gpiopin"], GPIO.HIGH)
        GPIO.output(station["gpiopin"], GPIO.LOW)

        time.sleep(station["runtime"])

    finally:
        GPIO.output(config.commonPin, GPIO.HIGH)
        GPIO.output(station["gpiopin"], GPIO.HIGH)

        GPIO.cleanup()