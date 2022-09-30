from typing import Any, Callable


class MQTTSN_Transport:
    receive_callback: Callable[[bytes, str], None]

    def __init__(self) -> None:
        self.set_receive_callback(lambda _packet, _address: None)

    @property
    def max_packet_size(self):
        raise NotImplementedError()

    def set_receive_callback(self, receive_callback: Callable[[bytes, str],
                                                              None]):
        self.receive_callback = receive_callback

    async def send_packet(self, packet: bytes, address: str):
        raise NotImplementedError()

    async def broadcast_packet(self, packet: bytes):
        raise NotImplementedError()
