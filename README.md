# Rose Rocketry Telemetry System

## Installation Guide
1. Install `docker-compose`
    1. Setup passwordless ssh to the pi
    2. Install docker on the pi and add the pi user to the docker group
    3. Ensure that your connection to docker works
        ```bash
        [user@devmachine]$ DOCKER_HOST="ssh://pi@hostname" docker version
        ```
    4. Install docker-compose to your local machine (docker daemon not needed)
    5. Create a `/data` directory on the pi
        ```bash
        [pi@raspberry]$ sudo mkdir -p /data
        [pi@raspberry]$ sudo chown pi:pi /data
        ```
3. Running on PC (no XBee needed)
    1. WIP
4. Run the code with `docker-compose`
    ```bash
    [user@devmachine]$ cd groundstation
    [user@devmachine]$ DOCKER_HOST="ssh://pi@hostname" docker-compose up --build
    ```

## Subsystems
This repo is split into 2 subsystems, based on where the contained software will run.
- [Rocket](./rocket/): Will run on an SBC in the rocket
- [Groundstation](./groundstation/): Will run in docker containers, most likely on a laptop or SBC. Currently also connected to the XBee receiver.

## Overall System Architecture
![System Architecture Diagram](./doc/system_architecture.drawio.svg)
