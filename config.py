#!/usr/bin/python
import station

# The common pin is turned on alongside any station being turned on.
commonPin = 2

# Station class takes a name, GPIO pin and run-time (in seconds) as parameters
stations = [
  station.Station("FRONT_GRASS", 3, 10 * 60),
  station.Station("FRONT_PLANTS", 17, 10 * 60),
  station.Station("BACK_GRASS", 4, 7 * 60),
  station.Station("BACK_PLANTS", 23, 10 * 60),
  station.Station("DRIVEWAY_PLANTS", 23, 7 * 60),
]