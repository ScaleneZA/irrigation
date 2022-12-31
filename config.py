#!/usr/bin/python

# Station class takes a name, GPIO pin and run-time (in seconds) as parameters
stations = [
  # COMMON will be turned on along with each other station. 
  # Must always be set as the first item in the array.
  Station("COMMON", 2, 0),

  Station("FRONT_GRASS", 3, 10 * 60),
  Station("FRONT_PLANTS", 17, 10 * 60),
  Station("BACK_GRASS", 4, 7 * 60),
  Station("BACK_PLANTS", 23, 10 * 60),
  Station("DRIVEWAY_PLANTS", 23, 7 * 60),
]