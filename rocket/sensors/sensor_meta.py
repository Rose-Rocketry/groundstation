import enum
from datetime import datetime
from struct import Struct
from typing import Any, Callable
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from typing_extensions import Self


class SensorUnit(enum.Enum):
    _formatter: Callable[[Any], str]

    NONE = (lambda x: str(x), )
    TIMESTAMP = (lambda x: datetime.utcfromtimestamp(x).isoformat(), )
    DEGREES_C = (lambda x: f"{x:.02f}\u00B0C", )

    def __init__(self, formatter) -> None:
        self._formatter = formatter

    def __repr__(self) -> str:
        return f"<{str(self)}>"

    def format(self, x: Any) -> str:
        return self._formatter(x)


class SensorReading:
    TIMESTAMP_NS: "Self"

    data_type: str
    unit: SensorUnit
    scale: float

    def __init__(self,
                 data_type: str = "d",
                 unit=SensorUnit.NONE,
                 scale=1.0) -> None:
        self.data_type = data_type
        self.unit = unit
        self.scale = scale

    def encode(self) -> str:
        return f"{self.data_type}:{self.unit.name}:{self.scale}"

    @staticmethod
    def decode(data: str):
        data_type, unit, scale = data.split(":")
        unit = SensorUnit[unit]
        scale = float(scale)

        return SensorReading(data_type, unit, scale)


SensorReading.TIMESTAMP_NS = SensorReading("Q", SensorUnit.TIMESTAMP, 1e-9)


class SensorDescriptor:
    DESCRIPTOR_TOPIC_SUFFIX = "/descriptor"

    readings: "tuple[SensorReading]"
    format: Struct

    def __init__(self, *readings: SensorReading) -> None:
        self.readings = readings

        struct_format = "!" + "".join(reading.data_type
                                      for reading in readings)

        self.format = Struct(struct_format)

    def encode_descriptor(self) -> str:
        return ",".join(reading.encode() for reading in self.readings)

    @staticmethod
    def decode_descriptor(data: str):
        readings = data.split(",")
        readings = (SensorReading.decode(data) for data in readings)
        return SensorDescriptor(*readings)

    def encode_packet(self, *values: Any) -> bytes:
        return self.format.pack(*values)

    def decode_packet(self, data: bytes) -> "list[tuple[float, SensorUnit]]":
        return [
            (value * reading.scale, reading.unit)
            for value, reading in zip(self.format.unpack(data), self.readings)
        ]
