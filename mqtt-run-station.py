#!/usr/bin/python
# This script can be used to run all the stations for their default run-time.
import os, sys, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiprocessing import Process
from multiprocessing import Event

import paho.mqtt.client as mqtt
import program
import config

pids = {}

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe(config.mqttTopicRunStation)

def on_message(client, userdata, message):
    try:
        decoded_message=str(message.payload.decode("utf-8"))
        msg=json.loads(decoded_message)

        if msg["status"] != "ON" and msg["status"] != "OFF":
            print("Invalid status: " + msg["status"])
            return

        if msg["station"] == "ALL":
            runAllStations(client, msg["status"])
            return

        runStation(client, config.lookupStation(msg["station"]), msg["status"])
    except Exception as e:
        # Don't kill the script when an exception happens
        print(e)

def runStation(client, station, status):
    stopAllStations(client)

    client.publish(config.mqttTopicStatus + "/" + station["name"], '{"station": "' + station["name"] + '", "status": "'+ status +'"}')

    event = Event()
    if status == "ON":
        process = Process(target=runOne, args=(client, event, station))
        process.start()
        pids[station["name"]] = event

    else:
        # Use the event to kill the process
        try:
            event = pids[station["name"]]
            event.set()
            del pids[station["name"]]
        except:
            pass

def runOne(client, event, station):
    program.runOne(event, station)
    try:
        program.runOne(event, station)
    finally:
        client.publish(config.mqttTopicStatus + "/" + station["name"], '{"station": "' + station["name"] + '", "status": "OFF"}')

def runAllStations(client, status):
    if status == "ON":
        event = Event()
        process = Process(target=runAll, args=(client, event))
        process.start()
        pids["ALL"] = event
    else:
        stopAllStations(client)

def stopAllStations(client):
    # Use the event to kill the processes
    for station in config.stations:
        client.publish(config.mqttTopicStatus + "/" + station["name"], '{"station": "' + station["name"] + '", "status": "OFF"}')

        try:
            event = pids[station["name"]]
            event.set()
            del pids[station["name"]]
        except:
            pass

        # client.loop is needed to publish because the loop forever is too slow to acknowledge it in this loop. Pulled my hair out over this bug.
        client.loop()

def runAll(client, event):
    for station in config.stations:
        client.publish(config.mqttTopicStatus + "/" + station["name"], '{"station": "' + station["name"] + '", "status": "ON"}')
        pids[station["name"]] = event

        # client.loop is needed to publish because the loop forever is too slow to acknowledge it in this loop. Pulled my hair out over this bug.
        client.loop()

        runOne(client, event, station)

        if event.is_set():
            break

#############################

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.will_set(config.mqttTopicCritical, '{"status": "OFF"}')
client.username_pw_set(config.mqttUser, config.mqttPassword)
client.connect(config.mqttHost, 1883, 60)

client.loop_forever()
