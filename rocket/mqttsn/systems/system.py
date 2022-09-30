from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..client import MQTTSNClient


class System:
    client: "MQTTSNClient"

    def __init__(self, client: "MQTTSNClient") -> None:
        self.client = client

    async def main():
        raise NotImplementedError()
