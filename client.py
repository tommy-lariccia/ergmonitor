import bleak
import asyncio


class ErgBLEClient:
    """
    Implements low-level bleak write and read frames to and from a single erg.
    """

    def __init__(self):
        self._reqlock = asyncio.Lock()

    async def write(self, frame: bytes):
        await self._reqlock.acquire()

    async def read(self) -> bytes:
        assert self._reqlock.locked()
        self._reqlock.release()
        return b'\xF1\xAB\xAB\xF3'

    async def free(self):
        self._reqlock.release()
