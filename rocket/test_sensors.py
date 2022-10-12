import asyncio
import os
from mqttsn.transports.constructs.mqttsn import MQTTSNPacket, MsgType, TopicIdType
from mqttsn.transports.constructs.xbee import APIFrame
from sensors.sensor_meta import SensorDescriptor
from sensors.cpu_temperature_sensor import CPUTemperatureSensor


async def main():
    sensor = CPUTemperatureSensor()
    asyncio.create_task(sensor.run())

    encoded_descriptor = sensor.descriptor.encode_descriptor()
    encoded_packet = await sensor.packet_queue.get()

    descriptor = SensorDescriptor.decode_descriptor(encoded_descriptor)
    packet = descriptor.decode_packet(encoded_packet)
    print(packet)
    for (value, unit) in packet:
        print(unit.format(value))

asyncio.get_event_loop().run_until_complete(main())
