#!/usr/bin/python
# This script can be used to run all the stations for their default run-time.
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import paho.mqtt.client as mqtt
import program
import config

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe(config.mqttRunAllTopic)

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    program.run()
    client.publish(config.mqttStatusTopic, payload='{"status": "ON"}', qos=0, retain=False)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set(config.mqttStatusTopic, '{"status": "OFF"}')

client.username_pw_set(config.mqttUser, config.mqttPassword)

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect(config.mqttHost, 1883, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
