from asyncio import DatagramProtocol, DatagramTransport

from rocket.mqttsn.transports.constructs.mqttsn import MQTTSNPacket, MsgType
from .generic import MQTTSN_Transport


class UDP_MQTTSN_Transport(MQTTSN_Transport, DatagramProtocol):
    transport: DatagramTransport

    def __init__(self) -> None:
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        """Called when some datagram is received."""
        if self.receive_callback:
            self.receive_callback(data, str(addr))

    def error_received(self, exc):
        """Called when a send or receive operation raises an OSError.

        (Other than BlockingIOError or InterruptedError.)
        """
        print("error_received:", exc)


    async def send_packet(self, packet: bytes, address: str):
        self.transport.sendto(packet, address)

    async def broadcast_packet(self, packet: bytes):
        # Assume sending GWSEARCH
        # Reply with a fake GWINFO
        self.receive_callback(MQTTSNPacket.build({
            "message_type": MsgType.ADVERTISE,
            "message": {
                "gateway_id": 0,
                "duration": 65535,
            },
        }), ("127.0.0.1", 10000))
