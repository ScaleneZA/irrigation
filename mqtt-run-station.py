#!/usr/bin/python
# This script can be used to run all the stations for their default run-time.
import os, sys, json, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multiprocessing import Process
from multiprocessing import Event

import paho.mqtt.client as mqtt
import program
import config

pids = {}

# on_connect is the callback for MQTT when it connects to the Broker.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(config.mqttTopicRunStation)

# on_message is the callback for MQTT when it recieves a message from a topic that was subscribed to in on_connect.
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

# runStation will stop all stations and then run a single station asyncronously.
def runStation(client, station, status):
    stopAllStations(client)

    client.publish(config.mqttTopicStatus + "/" + station["name"], '{"station": "' + station["name"] + '", "status": "'+ status +'"}')

    if status == "ON":
        event = Event()
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

# runOne is intended to be run asynchronously. It will run a single station for the given runtime.
def runOne(client, event, station):
    time.sleep(2)
    try:
        program.runOne(event, station)
    finally:
        client.publish(config.mqttTopicStatus + "/" + station["name"], '{"station": "' + station["name"] + '", "status": "OFF"}')

# runAllStations will stop all stations and then asynchronously call runAll
def runAllStations(client, status):
    stopAllStations(client)

    if status == "ON":
        event = Event()
        process = Process(target=runAll, args=(client, event))
        process.start()
        pids["ALL"] = event

# stopAllStations will stop all running asynconous processes.
def stopAllStations(client):
    try:
        event = pids["ALL"]
        event.set()
        del pids["ALL"]
    except:
        pass

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

# runAll is intended to be run asyncronously. It loops over each station waiting for the run time to expire before calling the next station.
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
