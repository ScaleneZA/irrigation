#!/usr/bin/python
# You should be able to use this script to run a single station using the name as an arugment.

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

name = sys.argv[1]

for station in globals()["stations"]:
  if station.name != name:
    continue

  station.start(config.commonPin)