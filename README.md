# Rose Rocketry Telemetry System

## Subsystems
This repo is split into 3 subsystems, based on where the contained software will run.
- [Rocket](./rocket/): Will run on an SBC in the rocket
- [Groundstation](./groundstation/): Will run in docker containers, most likely on a laptop or SBC. Currently also connected to the XBee receiver.

## Overall System Architecture
![System Architecture Diagram](./doc/system_architecture.drawio.svg)
