# Groundstation
This folder contains all of the software that will run on the groundstation.

## Mosquitto
[Mosquitto](https://mosquitto.org/) acts as a MQTT "Broker", receiving all of the telemetry data from the [Receiver](../reciever/), and forwarding it to it's clients (Orangebox and, in the future, the mobile app)

## Orangebox
Orangebox receives all of the telemetry data from Mosquitto and logs it to a file to later be fetched by the client through Deejay, or copied manually

## Deejay
Deejay acts as a simple server for fetching past flight logs stored by Orangebox. It's currently written using the flask devserver, but it'll

## Gateway
Acts as a bridge between Mosquitto and XBee. Uses eclipse's [MQTTSNGateway](https://github.com/eclipse/paho.mqtt-sn.embedded-c/tree/master/MQTTSNGateway).

I'm not sure if we are planning on running this on the same computer as the rest of the telemetry stack, but running it all on one pi is convenient for testing rn.

### XBee MAC Adresses:
    Gateway: 0013A20041CEFBD3
    Rocket:  0013A20041CEFC0D
