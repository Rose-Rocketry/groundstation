# Rose Rocketry Telemetry System

## Subsystems
This repo is split into 3 subsystems, based on where the contained software will run.
- [Rocket](./rocket/): Will run on an SBC in the rocket
- [Receiver](./reciever/): Will run on an SBC connected to an XBee receiver
- [Groundstation](./groundstation/): Will run in docker containers, most likely on a laptop or SBC

## Overall System Architecture
![System Architecture Diagram](./doc/system_architecture.drawio.svg)
