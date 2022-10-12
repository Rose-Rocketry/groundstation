from .sensor import PollingSensor
from .sensor_meta import SensorDescriptor, SensorReading, SensorUnit
import psutil

DESCRIPTOR = SensorDescriptor(SensorReading.TIMESTAMP_NS,
                              SensorReading("H", SensorUnit.NONE, 0.1))


class PSUtilSensor(PollingSensor):

    def __init__(self, poll_delay: float = 1) -> None:
        super().__init__(DESCRIPTOR, poll_delay, 1)

    async def poll(self) -> tuple:
        return (
          int(psutil.cpu_percent() * 10),
        )
