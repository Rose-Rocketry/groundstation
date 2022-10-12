from asyncio import create_task
from .system import System
from ...sensors.sensor import Sensor

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..client import MQTTSNClient

DESCRIPTOR_SUFFIX = "/meta"


class SensorSystem(System):

    def __init__(self, client: "MQTTSNClient") -> None:
        super().__init__(client)

    def create_sensor(self, sensor: Sensor, topic: str, qos: int = 0):
        create_task(sensor.run())
        create_task(self._sensor_task(sensor, topic, qos))

    async def _sensor_task(self, sensor: Sensor, topic: str, qos: int):
        await self.client.publish_system.publish(
            topic + DESCRIPTOR_SUFFIX,
            0, # TODO: Make this at least 1
            sensor.descriptor.encode_descriptor().encode(),
            retain=True,
        )

        while True:
            packet = await sensor.packet_queue.get()
            await self.client.publish_system.publish(
                topic,
                qos,
                packet,
                retain=True,
            )
