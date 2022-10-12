from .sensor import PollingSensor
from .sensor_meta import SensorDescriptor, SensorReading, SensorUnit

DESCRIPTOR = SensorDescriptor(SensorReading.TIMESTAMP_NS,
                              SensorReading("H", SensorUnit.DEGREES_C, 1e-2))
SENSOR_PATH = "/sys/class/thermal/thermal_zone0/temp"


class CPUTemperatureSensor(PollingSensor):

    def __init__(self, poll_delay: float = 1) -> None:
        super().__init__(DESCRIPTOR, poll_delay, 1)

    async def poll(self) -> tuple:
        # Store in centidegrees celcius
        value = int(open(SENSOR_PATH).read()) // 10
        return (value, )
