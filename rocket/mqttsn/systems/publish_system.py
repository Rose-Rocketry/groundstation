from .system import System
from ..transports.constructs.mqttsn import MsgType, TopicIdType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..client import MQTTSNClient

class PublishSystem(System):
    _next_message_id: int

    def __init__(self, client: "MQTTSNClient") -> None:
        super().__init__(client)
        self._next_message_id = 1

    async def publish(self, topic_name: str, qos: int, data: bytes, retain = False, register = True):
        if qos != 0:
            raise NotImplementedError()

        if not 0 <= qos <= 2:
            raise ValueError(f"Invalid QoS {qos}")

        if register:
            topic_id = await self.client.topic_system.get_topic_id(topic_name)

        if qos == 0:
            message_id = 0
        else:
            message_id = self._next_message_id
            self._next_message_id += 1
            if self._next_message_id > 65535:
                self._next_message_id = 1

        await self.client.send_packet(
            MsgType.PUBLISH, {
                "flags": {
                    "dup": False,
                    "qos": qos,
                    "retain": retain,
                    "topic_id_type": TopicIdType.ID
                },
                "topic_id": topic_id,
                "message_id": message_id,
                "data": data,
            })


        if qos <= 0:
            return

        # TODO: What is PUBACK?
        # Wait for PUBREC, or retransmit

        if qos <= 1:
            return

        # TODO: PUBREL & PUBCOMP
