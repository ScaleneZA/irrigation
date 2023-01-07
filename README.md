# irrigation
A little Python project to run my irrigation system using a Raspberry Pi and an 8 channel relay. This project is intended to be used as an MQTT client which will subscribe and publish to topics on an MQTT Broker.

### Setup
Setup your Stations in `config.py`. You will need to name each station, specify which GPIO Pin to activate, and the run time in seconds. 

You will also need to specify the GPIO pin for your "common" channel. This gets turned on along with each other station because it is often the "negative" or "ground" for each pump. This could also be wired as the "Master Pump" channel if you have one.

Along with this, you are required to setup the MQTT broker along with which topics to subscribe and publish to.

### Irrigation client
I like to run the main script with a process manager (like [PM2](https://pm2.keymetrics.io/)) so that it can be restarted if it crashes. You can execute the main script simply by calling `python mqtt-run-station.py`. 

You can montitor the topics with another script: `python mqtt-logger.py`. This is subscribed to the topics on the broker set up in `config.py` and will print out the payload when those topics are published to, and can be used for debugging if your client is recieving the topics correctly.

### Control Panel client
Because the irrigation client listens for topics on the broker, something needs to publish to those topics in order to switch on and off your irrigation stations. I've used [Home Assistant Mosquito addon](https://www.home-assistant.io/integrations/mqtt/) for this. The main thing to keep in mind is the payload structure when publishing to each topic. It should look like this:

```json
// Turn on single station
{"station":"FRONT_GRASS", "status":"ON"}

// Turn off single station
{"station":"FRONT_GRASS", "status":"OFF"}

// Turn on all stations
{"station":"ALL", "status":"ON"}

// Turn off all stations
{"station":"ALL", "status":"OFF"}
```
