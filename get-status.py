# This script can be used to run all the stations for their default run-time.
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import RPi.GPIO as GPIO
import config

# Disable warnings because we rely on the output of this script.
GPIO.setwarnings(False)

# TODO: Extract common code. 
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.commonPin, GPIO.OUT)

status = "ON" if GPIO.input(config.commonPin) == GPIO.LOW else "OFF"

print(status)

GPIO.cleanup()