#!/usr/bin/python
import RPi.GPIO as GPIO
import time

import config

GPIO.setmode(GPIO.BCM)

try:
    GPIO.setup(config.commonPin, GPIO.OUT)
    GPIO.output(config.commonPin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(config.commonPin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(config.commonPin, GPIO.HIGH)
    time.sleep(1)

    # Initialize each GPIO pin
    for st in config.stations:
        print(st["gpiopin"])
        GPIO.setup(st["gpiopin"], GPIO.OUT)
        GPIO.output(st["gpiopin"], GPIO.HIGH)
        time.sleep(1)
        GPIO.output(st["gpiopin"], GPIO.LOW)
        time.sleep(1)
        GPIO.output(st["gpiopin"], GPIO.HIGH)
        time.sleep(1)

finally:
    GPIO.cleanup()