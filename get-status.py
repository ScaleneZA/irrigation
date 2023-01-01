# This script can be used to run all the stations for their default run-time.
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import RPi.GPIO as GPIO
import config

# TODO: Extract common code. 
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.commonPin, GPIO.OUT)

print (GPIO.input(config.commonPin))