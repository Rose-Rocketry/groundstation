from asyncio import Event, create_task, sleep
import random
import time

from ..transports.constructs.mqttsn import MsgType
from .system import System

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from ..client import MQTTSNClient

T_SEARCHGW = 5
KEEPALIVE_DURATION = 60
MAX_MISSED_ADVERTISEMENTS = 2


class AdvertisementSystem(System):
    advertisement_event: Event
    advertised_address: str
    advertisement_expires: int

    def __init__(self, client: "MQTTSNClient") -> None:
        super().__init__(client)
        self.advertisement_event = Event()
        self.advertised_address = None
        self.advertisement_expires = None

        create_task(self.search_coroutine())
        client.register_callback(MsgType.ADVERTISE,
                                 self.handle_advertisement_packet)
        client.register_callback(MsgType.GWINFO,
                                 self.handle_advertisement_packet)

    async def search_coroutine(self):
        # TODO: Rewrite with Queues
        await sleep(random.randrange(0, T_SEARCHGW))

        while True:
            now = time.monotonic()
            if not self.advertisement_event.is_set():
                await self.client.broadcast_packet(MsgType.SEARCHGW, {"radius": 0})
                await sleep(random.randrange(0, T_SEARCHGW))
                continue

            if now < self.advertisement_expires:
                await sleep(self.advertisement_expires - now)
                continue

            if self.advertised_address is None or time.monotonic(
            ) > self.advertisement_expires:
                self.advertisement_event.clear()
                print("Cleared expired advertisement")

    def handle_advertisement_packet(self, message_type: MsgType, message: Any,
                                    address: str):
        now = time.monotonic()
        duration = 0

        if message_type == MsgType.ADVERTISE:
            duration = message.duration
            print(f"address={address} ttl={duration} | ", end="")
        else:
            duration = KEEPALIVE_DURATION
            print(f"address={address} | ", end="")

        if self.advertised_address == address:
            print(
                f"REFRESHED with {self.advertisement_expires - now:.02f}s left"
            )
            self.advertised_address = address
            self.advertisement_expires = now + duration * MAX_MISSED_ADVERTISEMENTS
            self.advertisement_event.set()
        elif self.advertised_address is None or now > self.advertisement_expires:
            print(f"NEW advertisement")
            self.advertised_address = address
            self.advertisement_expires = now + duration * MAX_MISSED_ADVERTISEMENTS
            self.advertisement_event.set()
        else:
            print("IGNORED")

        return
