# Groundstation
This folder contains all of the software that will run on the groundstation.

## Mosquitto
[Mosquitto](https://mosquitto.org/) acts as a MQTT "Broker", receiving all of the telemetry data from the [Receiver](../reciever/), and forwarding it to it's clients (Orangebox and, in the future, the mobile app)

## Orangebox
Orangebox receives all of the telemetry data from Mosquitto and logs it to a file to later be fetched by the client through Deejay, or copied manually

## Deejay
Deejay acts as a simple server for fetching past flight logs stored by Orangebox. It's currently written using the flask devserver, but it'll
