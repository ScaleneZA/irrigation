#!/usr/bin/python
import RPi.GPIO as GPIO
import time

class Station:
  def __init__(self, name, gpiopin, runtime):
    self.name = name
    self.gpiopin = gpiopin
    self.runtime = runtime

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpiopin, GPIO.OUT)
    GPIO.output(self.gpiopin, GPIO.HIGH)

  def start(self, commonpin):
    GPIO.output(commonpin, GPIO.LOW)
    GPIO.output(self.gpiopin, GPIO.LOW)

  def stop(self, commonpin):
    GPIO.output(self.gpiopin, GPIO.HIGH)
    GPIO.output(commonpin, GPIO.HIGH)

  def run(self, commonpin):
    self.start(commonpin)
    time.sleep(self.runtime)
    self.stop(commonpin)
