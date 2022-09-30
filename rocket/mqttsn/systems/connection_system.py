from asyncio import Event, Queue, create_task, sleep, wait_for
import random
import time

from ..transports.constructs.mqttsn import MsgType, ReturnCode
from .system import System

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from ..client import MQTTSNClient

KEEPALIVE_DURATION = 60
CLIENT_ID = "rocket"
CONNECT_TIMEOUT = 10


class ConnectionSystem(System):
    connection_event: Event
    _connection_packet_queue: "Queue[(MsgType, Any)]"

    def __init__(self, client: "MQTTSNClient") -> None:
        super().__init__(client)

        client.register_callback(MsgType.CONNACK, self.handle_packet)

        self.connection_event = Event()
        self._connection_packet_queue = Queue()

        create_task(self._connect_coroutine())

    async def _connect_coroutine(self):
        while True:
            await self.client.send_packet(MsgType.CONNECT, {
                "flags": {
                    "clean_session": True,
                    "will": False
                },
                "duration": KEEPALIVE_DURATION,
                "client_id": CLIENT_ID,
            },
                                          dont_wait_for_connection=True)

            try:
                _, message = await wait_for(
                self._connection_packet_queue.get(), CONNECT_TIMEOUT)
            except:
                continue

            return_code = ReturnCode(message.return_code)

            if return_code == ReturnCode.ACCEPTED:
                break
            else:
                print(
                    f"Error connecting: {repr(return_code)}, {repr(ReturnCode.ACCEPTED)}"
                )
                await sleep(CONNECT_TIMEOUT)

        print("Connected Successfully")
        self.connection_event.set()
        # TODO: Handle Disconnects

    def handle_packet(self, message_type: MsgType, message: Any):
        self._connection_packet_queue.put_nowait((message_type, message))
        print("QUEUED")
