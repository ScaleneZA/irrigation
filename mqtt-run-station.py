#!/usr/bin/python
# This script can be used to run all the stations for their default run-time.
import os, sys, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiprocessing import Process
from multiprocessing import Event

import paho.mqtt.client as mqtt
import program
import config

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
        globals()["pid-" +station["name"]] = event

    else:
        # Use the event to kill the process
        try:
            event = globals()["pid-" +station["name"]]
            event.set()
            del globals()["pid-" +station["name"]]
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
        globals()["pid-ALL"] = event
    else:
        stopAllStations(client)

def stopAllStations(client):
    # Use the event to kill the processes
    for key in list(globals()):
        if "pid-" not in key:
            continue

        event = globals()[key]
        event.set()
        del globals()[key]
        client.publish(config.mqttTopicStatus + "/" + key, '{"station": "' + key + '", "status": "OFF"}')
        # client.loop is needed to publish because the loop forever is too slow to acknowledge it in this loop. Pulled my hair out over this bug.
        client.loop()

def runAll(client, event):
    for station in config.stations:
        client.publish(config.mqttTopicStatus + "/" + station["name"], '{"station": "' + station["name"] + '", "status": "ON"}')
        # client.loop is needed to publish because the loop forever is too slow to acknowledge it in this loop. Pulled my hair out over this bug.
        client.loop()

        globals()["pid-" +station["name"]] = event
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
