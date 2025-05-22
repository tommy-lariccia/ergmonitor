from client import ErgBLEClient

import asyncio


class CommandManager:
    def __init__(self, client: ErgBLEClient):
        self._ergcl = client
        self._cqueue = asyncio.Queue()
        self._futures = dict()

    async def get(command: str):
        ...

    async def set() -> None:
        ...

    async def _build_frame(self):
        ...

    async def _send_frame():
        ...

    async def _push_bytes_command():
        ...

