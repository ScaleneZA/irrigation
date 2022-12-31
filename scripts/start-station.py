#!/usr/bin/python
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

name = sys.argv[1]

for station in config.stations:
  if station.name != name:
    continue

  station.start(config.commonPin)