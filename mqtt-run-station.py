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

        runStation(client, config.lookupStation(msg["station"]), msg["status"], False)
    except Exception as e:
        # Don't kill the script when an exception happens
        print(e)

def runStation(client, station, status, wait):
    publish(client, config.mqttTopicStatus + "/" + station["name"], '{"station": "' + station["name"] + '", "status": "'+ status +'"}')

    event = Event()
    if status == "ON":
        process = Process(target=runOne, args=(client, event, station))
        process.start()
        pids[station["name"]] = event

        if wait:
            process.join()
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
        publish(client, config.mqttTopicStatus + "/" + station["name"], '{"station": "' + station["name"] + '", "status": "OFF"}')

def runAllStations(client, status):
    if status == "ON":
        event = Event()
        process = Process(target=runAll, args=(client, event))
        process.start()
        pids["ALL"] = event
    else:
        # Use the event to kill the processes
        for key in list(pids):
            event = pids[key]
            event.set()
            del pids[key]
            publish(client, config.mqttTopicStatus + "/" + key, '{"station": "' + key + '", "status": "OFF"}')

def runAll(client, event):
    for st in config.stations:
        runStation(client, st, "ON", True)

        if event.is_set():
            break

def publish(client, topic, message):
    process = Process(target=client.publish, args=(topic, message))
    process.start()

#############################

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.will_set(config.mqttTopicCritical, '{"status": "OFF"}')
client.username_pw_set(config.mqttUser, config.mqttPassword)
client.connect(config.mqttHost, 1883, 60)

client.loop_forever()
