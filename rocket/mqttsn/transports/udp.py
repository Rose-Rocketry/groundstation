from asyncio import DatagramProtocol, DatagramTransport
from .generic import MQTTSN_Transport


class UDP_MQTTSN_Transport(MQTTSN_Transport, DatagramProtocol):
    transport: DatagramTransport

    def __init__(self) -> None:
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        """Called when some datagram is received."""
        print(f"UDP Packet received from {addr}: {data}")
        if self.receive_callback:
            self.receive_callback(data)

    def error_received(self, exc):
        """Called when a send or receive operation raises an OSError.

        (Other than BlockingIOError or InterruptedError.)
        """
        print("error_received:", exc)
