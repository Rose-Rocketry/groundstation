# from asyncio import get_event_loop
# from mqttsn.transports import UDP_MQTTSN_Transport

# async def main():
#     get_event_loop().create_datagram_endpoint(UDP_MQTTSN_Transport, None, ("broker", ))

# loop = get_event_loop()
# loop.run_until_complete(main())
# loop.close()

import asyncio
import os

from .mqttsn.transports import create_xbee_transport_pi_zero
from .mqttsn.transports import UDP_MQTTSN_Transport
from .mqttsn.client import MQTTSNClient
from .sensors.cpu_temperature_sensor import CPUTemperatureSensor
from .sensors.psutil_sensor import PSUtilSensor

loop = asyncio.get_event_loop()


async def main():
    if "SENSORNET" in os.environ and os.environ["SENSORNET"] == "UDP":
        print("Using udp transport")
        a, transport = await loop.create_datagram_endpoint(
            UDP_MQTTSN_Transport,
            ("127.0.0.1", 10101),
            ("127.0.0.1", 10000),
        )
    else:
        print("Using XBee Transport")
        transport = await create_xbee_transport_pi_zero()

    client = MQTTSNClient(transport)

    # client.sensor_system.create_sensor(CPUTemperatureSensor(),
    #                                    "rocket/test/1/cpu_temp")
    client.sensor_system.create_sensor(PSUtilSensor(),
                                       "rocket/test/1/cpu_usage")


if __name__ == "__main__":
    loop.run_until_complete(main())
    loop.run_forever()
    loop.close()
