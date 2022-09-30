from typing import Callable

from rocket.mqttsn.transports.constructs.xbee import APIDataReceivePacket, APIFrame


class MQTTSN_Transport:
    receive_callback: Callable[[APIFrame, APIDataReceivePacket], None] = lambda _1,_2: None
    
    @property
    def max_packet_size(self):
        raise NotImplementedError()

    def set_receive_callback(self, receive_callback: Callable[[APIFrame, APIDataReceivePacket], None]):
        self.receive_callback = receive_callback

    def send_packet(self, packet: bytes):
        raise NotImplementedError()

