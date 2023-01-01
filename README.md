# irrigation
A little Python project to run my irrigation system using a Raspberry Pi and an 8 channel relay. 

### Setup
Setup your Stations in `config.py`. You will need to name each station, specify which GPIO Pin to activate, and the run time in seconds. 

You will also need to specify the GPIO pin for your "common" channel. This gets turned on along with each other station because it is often the "negative" or "ground" for each pump. This could also be wired as the "Master Pump" channel if you have one.

### Running
You can run the program by executing `python run-all.py`. It will activate each station in sequence for the run time specified (They do not run in parallel).

You can check the status of the program by executing `python get-status.py`. It will print out either `ON` or `OFF`.
