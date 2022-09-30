from re import I
import time
from typing import Any
from asyncio import Event, create_task, sleep
from .transports.generic import MQTTSN_Transport
from .transports.constructs.mqttsn import MQTTSNPacket, MsgType

MAX_MISSED_ADVERTISEMENTS = 5
GW_SEARCH_TIMEOUT = 10
# GWInfo has no TTL, default to 60
GW_INFO_TTL = 60


class MQTTSNClient:
    transport: MQTTSN_Transport
    advertisement_event: Event
    advertised_address: str
    advertisement_expires: int

    def __init__(self, transport: MQTTSN_Transport) -> None:
        self.transport = transport
        self.advertised_address = None
        self.advertisement_event = Event()
        self.advertisement_expires = 0

        transport.set_receive_callback(self.on_receive)

        create_task(self.search_coroutine())

    async def search_coroutine(self):
        await sleep(1)

        while True:
            now = time.monotonic()
            if not self.advertisement_event.is_set():
                await self.broadcast_packet(MsgType.SEARCHGW, {"radius": 0})
                await sleep(GW_SEARCH_TIMEOUT)
                continue
            
            if now < self.advertisement_expires:
                await sleep(self.advertisement_expires - now)
                continue
            
            if self.advertised_address is None or time.monotonic() > self.advertisement_expires:
                self.advertisement_event.clear()
                print("Cleared expired advertisement")


    async def test_coroutine(self):
        await self.wait_for_advertisement()
        print("Got Advertisement!")

    async def wait_for_advertisement(self):
        if self.advertisement_event.is_set():
            if self.advertised_address is None or time.monotonic(
            ) > self.advertisement_expires:
                self.advertisement_event.clear()
                print("Cleared expired advertisement")

            print("Waiting for advertisement...")
            await self.advertisement_event.wait()

    async def send_packet(self, message_type: MsgType, message: Any):
        await self.wait_for_advertisement()

        packet = MQTTSNPacket.build({
            "message_type": message_type,
            "message": message,
        })
        await self.transport.send_packet(packet, self.advertised_address)
        print(f"==> {message_type} ({len(packet)}b)")

    async def broadcast_packet(self, message_type: MsgType, message: Any):
        await self.wait_for_advertisement()

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

        if message_type == MsgType.ADVERTISE or MsgType.GWINFO:
            duration = 0

            if message_type == MsgType.ADVERTISE:
                duration = message.duration
                print(f"address={address} ttl={duration} | ", end="")
            else:
                duration = GW_INFO_TTL
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

        if self.advertised_address is None:
            print("IGNORED, no advertisement received")

        if now > self.advertisement_expires:
            print("IGNORED, advertisement is expired")

        if MsgType == 1234:
            pass
        else:
            print("IGNORED")
