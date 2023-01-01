#!/usr/bin/python
# This script needs to be called once on startup so that all stations are setup correctly.

import config
import station

for st in config.stations:
    globals()['stations'].append(
        station.Station(st["name"], st["gpiopin"], st["runtime"])
    )