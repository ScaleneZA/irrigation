#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import config

def runOne(event, station):
    GPIO.setmode(GPIO.BCM)

    try:
        GPIO.setup(config.commonPin, GPIO.OUT)
        GPIO.output(config.commonPin, GPIO.HIGH)
        GPIO.output(config.commonPin, GPIO.LOW)

        GPIO.setup(station["gpiopin"], GPIO.OUT)
        GPIO.output(station["gpiopin"], GPIO.HIGH)
        GPIO.output(station["gpiopin"], GPIO.LOW)

        sleepCount = 0
        while sleepCount <= station["runtime"]:
            time.sleep(1)
            sleepCount+=1

            if event.is_set():
                break

    finally:
        GPIO.output(config.commonPin, GPIO.HIGH)
        GPIO.output(station["gpiopin"], GPIO.HIGH)

        GPIO.cleanup()