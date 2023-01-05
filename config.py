# The common pin is turned on alongside any station being turned on.
commonPin = 2

stations = [
    {
        "name": "FRONT_GRASS",
        "gpiopin": 3,
        "runtime": 10 * 60
    }, {
        "name": "FRONT_PLANTS",
        "gpiopin": 17,
        "runtime": 10 * 60
    }, {
        "name": "BACK_GRASS",
        "gpiopin": 4,
        "runtime": 7 * 60
    }, {
        "name": "BACK_PLANTS",
        "gpiopin": 23,
        "runtime": 10 * 60
    }, {
        "name": "DRIVEWAY_PLANTS",
        "gpiopin": 22,
        "runtime": 7 * 60
    },
]

# The following is details for an MQTT Broker if you have one.
mqttHost = "192.168.0.116"
mqttUser = "mqtt"
mqttPassword = "mqttT0nquani"

mqttTopicRunStation = "irrigation/run"
mqttTopicStatus = "irrigation/status"
mqttTopicCritical = "irrigation/critical"

def lookupStation(station):
    for st in stations:
        if st.name == station:
            return st

    raise Exception("Invalid station")