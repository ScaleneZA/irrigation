#!/usr/bin/python
# This script can be used to run all the stations for their default run-time.
import os, sys, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import paho.mqtt.client as mqtt
import program
import config

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe(config.mqttTopicRunStation)

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, message):
    try:
        decoded_message=str(message.payload.decode("utf-8"))
        msg=json.loads(decoded_message)

        if msg["station"] == "ALL":
            # TODO (put the loop here, publish status for each station)
            for st in config.stations:
                runStation(client, st)
            return

        runStation(client, config.lookupStation(msg["station"]))
    except Exception as e:
        # Don't kill the script when an exception happens
        print(e)

def runStation(client, station):
    client.publish(config.mqttTopicStatus, payload='{"station": "' + station["name"] + '", "status": "ON"}', qos=0, retain=False)
    try:
        program.runOne(station)
    finally:
        client.publish(config.mqttTopicStatus, payload='{"station": "' + station["name"] + '", "status": "OFF"}', qos=0, retain=False)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set(config.mqttTopicCritical, '{"status": "OFF"}')

client.username_pw_set(config.mqttUser, config.mqttPassword)

# create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect(config.mqttHost, 1883, 60)

# set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
