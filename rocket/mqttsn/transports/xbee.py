from random import random
import traceback
import asyncio
from functools import partial
from construct import Int16ub
from .generic import MQTTSN_Transport
from .constructs.xbee import APIDataTransmitRequest, APIFrame


class XBEE_MQTTSN_Transport(MQTTSN_Transport, asyncio.Protocol):
    transport_event: asyncio.Event
    transport: asyncio.Transport
    partial: bytes = b""

    def __init__(self) -> None:
        super().__init__()
        self.transport_event = asyncio.Event()

    def connection_made(self, transport):
        self.transport = transport
        self.transport_event.set()

    def data_received(self, data):
        self.partial += data

        i = 0
        while len(self.partial) - i > 3:
            if self.partial[i] != 0x7e:
                print(
                    f"WARNING: expected start delimiter, got {self.partial[i]:02x}"
                )
                i += 1
                continue
            try:
                # start byte + length + n + checksum = n + 4
                length = Int16ub.parse(self.partial[i + 1:i + 3]) + 4

                if len(self.partial) - i < length:
                    break

                packet = APIFrame.parse(self.partial[i:i + length])
                frame_data = packet.content.value.frame_data.value

                if packet.content.value.frame_type == 0x8A:
                    print(f"Modem status: {frame_data.modem_status:#04x}")
                elif packet.content.value.frame_type == 0x90:
                    try:
                        self.receive_callback(
                            frame_data.message,
                            f"{frame_data.source_address:016x}",
                        )
                    except Exception:
                        traceback.print_exc()
                        print(
                            "WARNING: Exception occurred in receive_callback")
                else:
                    print(packet)

                i = i + length

            except Exception:
                traceback.print_exc()
                print(
                    "WARNING: Error decoding packed, finding next candidate start byte"
                )
                i += 1

        self.partial = self.partial[i:]

    async def send_packet(self, packet: bytes, address: str):
        payload = APIDataTransmitRequest.build({
            "destination_address":
            int(address, 16),
            "message":
            packet,
        })

        frame = APIFrame.build({
            "content": {
                "value": {
                    "frame_type": 0x10,
                    "frame_data": {
                        "data": payload
                    }
                }
            }
        })

        await self.transport_event.wait()

        self.transport.write(frame)

    async def broadcast_packet(self, packet: bytes):
        await self.send_packet(packet, "0x000000000000FFFF")
