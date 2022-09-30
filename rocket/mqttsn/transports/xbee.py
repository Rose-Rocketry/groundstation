import traceback
from .generic import MQTTSN_Transport
from construct import Int16ub
from .constructs.xbee import APIDataTransmitRequest, APIFrame
import asyncio


class XBEE_MQTTSN_Transport(MQTTSN_Transport, asyncio.Protocol):
    transport: asyncio.Transport
    partial: bytes = b""

    def connection_made(self, transport):
        self.transport = transport

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
                print(packet)

                i = i + length

            except Exception:
                print(
                    "WARNING: Error decoding packed, finding next candidate start byte"
                )
                print(traceback.format_exc())
                i += 1

        self.partial = self.partial[i:]

    def send_packet(self, packet: bytes):
        payload = APIDataTransmitRequest.build({
            "destination_address": 0x0013A20041CEFBD3,
            "message": packet
        })

        frame = APIFrame.build({
            "content": {
                "value": {
                    "frame_type": 0x10,
                    "frame_data": payload
                }
            }
        })

        self.transport.write(frame)
