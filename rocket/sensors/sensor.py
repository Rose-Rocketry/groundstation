from asyncio import Queue
from time import sleep
import time
from .sensor_meta import SensorDescriptor


class Sensor:
    packet_queue: "Queue[bytes]"
    descriptor: SensorDescriptor

    def __init__(self,
                 descriptor: SensorDescriptor,
                 queue_depth=1) -> None:
        self.descriptor = descriptor

        self.packet_queue = Queue(queue_depth)

    async def run(self):
        raise NotImplementedError()


class PollingSensor(Sensor):
    poll_delay: float

    def __init__(self, descriptor: SensorDescriptor, poll_delay: float, queue_depth=1) -> None:
        super().__init__(descriptor, queue_depth)

        self.poll_delay = poll_delay

    async def run(self):
        while True:
            now = time.time_ns()
            reading = await self.poll()

            packet = self.descriptor.encode_packet(now, *reading)
            await self.packet_queue.put(packet)

            sleep(self.poll_delay)

    async def poll(self) -> tuple:
        raise NotImplementedError()
