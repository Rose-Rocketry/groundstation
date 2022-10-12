from inspect import signature
import time
from typing import Any, Callable
from asyncio import Event, Queue, create_task, sleep, wait_for

from .systems.advertisement_system import AdvertisementSystem
from .systems.connection_system import ConnectionSystem
from .systems.topic_system import TopicSystem
from .systems.publish_system import PublishSystem
from .systems.sensor_systen import SensorSystem
from .transports.generic import MQTTSN_Transport
from .transports.constructs.mqttsn import MQTTSNPacket, MsgType, ReturnCode

# GWInfo has no TTL, default to 60


class MQTTSNClient:
    transport: MQTTSN_Transport

    topic_registry_queue: "Queue[str]"
    topic_registry_packet_queue: "Queue[(MsgType, Any)]"

    _callbacks: "dict[MsgType, list[Callable[[MsgType, Any], Any]]]"

    advertisement_system: AdvertisementSystem
    connection_system: ConnectionSystem
    topic_system: TopicSystem
    publish_system: PublishSystem
    sensor_system: SensorSystem

    def __init__(self, transport: MQTTSN_Transport) -> None:
        self.transport = transport

        self._callbacks = dict()

        self.advertisement_system = AdvertisementSystem(self)
        self.connection_system = ConnectionSystem(self)
        self.topic_system = TopicSystem(self)
        self.publish_system = PublishSystem(self)
        self.sensor_system = SensorSystem(self)

        transport.set_receive_callback(self.on_receive)

    def register_callback(self, message_type: MsgType,
                          callback: "Callable[[MsgType, Any], Any]"):
        if message_type not in self._callbacks:
            self._callbacks[message_type] = []

        self._callbacks[message_type].append(callback)

    async def send_packet(self,
                          message_type: MsgType,
                          message: Any,
                          dont_wait_for_connection=False):
        await self.advertisement_system.advertisement_event.wait()
        if not dont_wait_for_connection:
            await self.connection_system.connection_event.wait()

        packet = MQTTSNPacket.build({
            "message_type": message_type,
            "message": message,
        })
        await self.transport.send_packet(packet, self.advertisement_system.advertised_address)
        print(f"==> {message_type} ({len(packet)}b)")

    async def broadcast_packet(self, message_type: MsgType, message: Any):
        packet = MQTTSNPacket.build({
            "message_type": message_type,
            "message": message,
        })

        await self.transport.broadcast_packet(packet)
        print(f"=B> {message_type} ({len(packet)}b)")

    def on_receive(self, raw, address):
        now = time.monotonic()

        packet = MQTTSNPacket.parse(raw)

        message_type = MsgType(packet.message_type)
        message = packet.message

        print(f"<== {message_type} ({len(raw)}b) | ", end="")

        if message_type in self._callbacks:
            callbacks = self._callbacks[message_type]
            for callback in callbacks:
                if len(signature(callback).parameters) == 2:
                    callback(message_type, message)
                else:
                    # Used for advertisements
                    callback(message_type, message, address)
        else:
            print(" (IGNORED)")
