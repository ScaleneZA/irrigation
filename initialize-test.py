#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import config

GPIO.setmode(GPIO.BCM)

try:
    GPIO.setup(config.commonPin, GPIO.OUT)
    GPIO.output(config.commonPin, GPIO.HIGH)
    GPIO.output(config.commonPin, GPIO.LOW)
    GPIO.output(config.commonPin, GPIO.HIGH)

    # Initialize each GPIO pin
    for st in config.stations:
        GPIO.setup(st["gpiopin"], GPIO.OUT)
        GPIO.output(st["gpiopin"], GPIO.HIGH)
        GPIO.output(st["gpiopin"], GPIO.LOW)
        GPIO.output(st["gpiopin"], GPIO.HIGH)

finally:
    GPIO.cleanup()