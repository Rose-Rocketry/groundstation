from asyncio import Event, Queue, create_task, sleep, wait_for
from email import message
import string

from ..transports.constructs.mqttsn import MsgType, ReturnCode
from .system import System

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from ..client import MQTTSNClient

REGISTER_TIMEOUT = 3


class TopicState:
    client: "MQTTSNClient"
    topic_name: str
    topic_event: Event
    topic_id: int

    def __init__(self, client, topic_name) -> None:
        self.client = client
        self.topic_name = topic_name
        self.topic_event = Event()
        self.topic_id = None

    def set_id(self, id: int):
        self.topic_id = id
        self.topic_event.set()

    def clear_id(self):
        self.topic_id = None
        self.topic_event.clear()


class TopicSystem(System):
    _topic_states: "dict[str, TopicState]"
    _topic_message_id: "dict[int, str]"
    _topic_queue: "Queue[str]"

    def __init__(self, client: "MQTTSNClient") -> None:
        super().__init__(client)
        self._topic_states = dict()
        self._topic_message_id = dict()
        self._topic_queue = Queue()

        self.client.register_callback(MsgType.REGACK, self.handle_reg_ack)
        self.client.register_callback(MsgType.REGISTER, self.handle_reg_ack)

        create_task(self._start_coroutine())

    async def _start_coroutine(self):
        message_id = 0
        while True:
            topic_name = await self._topic_queue.get()
            event = self._topic_states[topic_name].topic_event

            message_id = (message_id + 1) % 65536
            self._topic_message_id[message_id] = topic_name
            while not event.is_set():
                print(f"Registering topic {repr(topic_name)}")
                await self.client.send_packet(
                    MsgType.REGISTER, {
                        "topic_id": 0x0000,
                        "message_id": message_id,
                        "topic_name": topic_name
                    })

                try:
                    await wait_for(event.wait(), REGISTER_TIMEOUT)
                except:
                    continue

            self._topic_queue.task_done()

    async def get_topic_id(self, topic_name: string):
        if topic_name not in self._topic_states:
            self._topic_states[topic_name] = TopicState(
                self.client, topic_name)
            await self._topic_queue.put(topic_name)

        await self._topic_states[topic_name].topic_event.wait()
        return self._topic_states[topic_name].topic_id

    def handle_reg_ack(self, _: MsgType, message: Any):
        topic_id = message.topic_id
        message_id = message.message_id
        return_code = ReturnCode(message.return_code)

        if return_code != ReturnCode.ACCEPTED:
            print(f"ERROR: {return_code}")
            return

        if message_id not in self._topic_message_id:
            print(f"ERROR: Unknown Message id {message_id}")

        topic_name = self._topic_message_id[message_id]
        self._topic_states[topic_name].set_id(topic_id)

        print(f"Registered id {topic_id} for topic {repr(topic_name)}")

    def handle_reg_push(self, _: MsgType, message: Any):
        topic_id = message.topic_id
        message_id = message.message_id
        topic_name = message.topic_name

        if topic_name not in self._topic_states:
            self._topic_states[topic_name] = TopicState(
                self.client, topic_name)

        self._topic_states[topic_name].set_id(topic_id)

        print(f"Received id {topic_id} for topic {repr(topic_name)}")

        create_task(
            self.client.send_packet(
                MsgType.REGACK, {
                    "topic_id": topic_id,
                    "message_id": message_id,
                    "return_code": ReturnCode.ACCEPTED,
                }))
