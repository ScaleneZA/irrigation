#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import config

def run():
    GPIO.setmode(GPIO.BCM)

    try:
        # Initialize each GPIO pin
        for st in config.stations:
            GPIO.setup(st["gpiopin"], GPIO.OUT)
            GPIO.output(st["gpiopin"], GPIO.HIGH)

        # Common needs to be run with every station
        GPIO.setup(config.commonPin, GPIO.OUT)
        GPIO.output(config.commonPin, GPIO.LOW)

        for st in config.stations:
            # TURN ON
            GPIO.output(st["gpiopin"], GPIO.LOW)

            print (st["name"])
            print ("GPIO pin:" + str(st["gpiopin"]))
            print ("Going to run for " + str(st["runtime"] / 60) + " minutes")

            time.sleep(st["runtime"])

            # TURN OFF
            GPIO.output(st["gpiopin"], GPIO.HIGH)

            print ("Done")
            print ("")

    finally:
        # Final attempt at Turn everything off
        GPIO.output(config.commonPin, GPIO.HIGH)
        for st in config.stations:
            GPIO.setup(st["gpiopin"], GPIO.OUT)
            GPIO.output(st["gpiopin"], GPIO.HIGH)

        GPIO.cleanup()