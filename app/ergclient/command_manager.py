from .client import ErgBLEClient
import app.csafe

import asyncio
import queue
import uuid

from typing import List


class _TaskedCommand:
    def __init__(self, uuid_: str, command: str, cargs: [], fut: asyncio.Future):
        self.uuid_ = uuid_
        self.command = command
        self.cargs = []
        self.fut = fut
        self._csafe_eq = None

    def get_csafe_bytes(self) -> bytes:
        if self._csafe_eq is None:
            self._csafe_eq = csafe.make_command(self.command)
        return self._csafe_eq

    def get_length(self) -> int:
        return len(self.get_csafe_bytes())


class _TaskedFrame:
    def __init__(self, comlist: List[_TaskedCommand]):
        self._comlist = comlist
        self._contents = None
        self._csafe_eq = None

    def _compile_contents(self):
        self._contents = b''.join(x.get_csafe_bytes() for x in self._comlist)

    def _set_csafe_bytes(self):
        self._compile_contents()
        self._csafe_eq = csafe.make_standard_frame(self._contents)

    def get_csafe_bytes(self):
        if self._csafe_eq is None:
            self._set_csafe_bytes()
        return self._csafe_eq

    def get_length(self):
        return len(self.get_csafe_bytes())

    def is_empty(self):
        return not len(self._comlist)

    def is_within_size_limits(self):
        return csafe.is_within_size_limits(self.get_csafe_bytes())

    def set_futures(self):
        for x in self._comlist:
            x.fut.set_result(0)


class _CommandContainer:
    def __init__(self):
        self._coms = []
        self._lock = asyncio.Lock()

    async def push(self, tcom: _TaskedCommand) -> None:
        async with self._lock:
            self._coms.append(tcom)

    async def take(self) -> _TaskedFrame:
        nframe = []
        async with self._lock:
            ncoms = []
            for x in self._coms:
                if _TaskedFrame(nframe + [x]).is_within_size_limits():
                    nframe.append(x)
                else:
                    ncoms.append(x)
            self._coms = ncoms
        return _TaskedFrame(nframe)


class CommandManager:
    def __init__(self, client: ErgBLEClient):
        self._ergcl = client
        self._comcont = _CommandContainer()
        self._consumer: asyncio.Task = None

    async def _send_frames(self):
        while True:
            await asyncio.sleep(0)
            frame = await self._comcont.take()
            if not frame.is_empty():
                print(frame.get_csafe_bytes())
                frame.set_futures()

    async def get(self, command: str):
        fut = asyncio.get_running_loop().create_future()
        uuid_ = uuid.uuid4()
        tasked_command = _TaskedCommand(uuid_, command, [], fut)
        await self._comcont.push(tasked_command)
        print(command, await fut)

    async def set(command: str) -> None:
        ...

    def begin(self):
        self._consumer = asyncio.create_task(self._send_frames())

    def end(self):
        self._consumer.cancel()

    def __enter__(self, *args):
        self.begin()
        return self

    def __exit__(self, *args):
        self.end()


async def main():
    #client = ErgBLEClient()
    cm = CommandManager(None)
    with cm as cm:
        await asyncio.gather(*[cm.get('CSAFE_GETUSERINFO_CMD'),
                               cm.get('CSAFE_GETVERSION_CMD'),
                               cm.get('CSAFE_GETVERSION_CMD')])


if __name__ == '__main__':
    asyncio.run(main())
