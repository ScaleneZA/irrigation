#!/usr/bin/python
# This script can be used to run all the stations for their default run-time.
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import paho.mqtt.client as mqtt
import config

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(config.mqttTopicStatus)
    client.subscribe(config.mqttTopicRunStation)
    client.subscribe(config.mqttTopicCritical)

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    # Intended to be piped into a file.
    decoded_message=str(msg.payload.decode("utf-8"))
    print(decoded_message)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(config.mqttUser, config.mqttPassword)

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect(config.mqttHost, 1883, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
