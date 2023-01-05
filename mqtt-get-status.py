# This script can be used to run all the stations for their default run-time.
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import config

# TODO: Extract common code. 
GPIO.setmode(GPIO.BCM)
GPIO.setup(config.commonPin, GPIO.OUT)

status = "ON" if GPIO.input(config.commonPin) == GPIO.LOW else "OFF"

GPIO.cleanup()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect

client.username_pw_set(config.mqttUser, config.mqttPassword)

client.connect(config.mqttHost, 1883, 60)

client.publish(config.mqttStatusTopic, payload='{"status":"' + status + '"}', qos=0, retain=False)
print(f"send {status} to " + config.mqttStatusTopic)

client.loop_forever()
