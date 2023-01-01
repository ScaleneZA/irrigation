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