#!/usr/bin/python
import sys

import config

name = sys.argv[1]

for station in config.stations:
  if station.name != name:
    continue

  station.start(config.commonPin)