import bleak
import asyncio

WRITE_CHAR_ADDR = 'CE060021-43E5-11E4-916C-0800200C9A66'
NOTIFY_CHAR_ADDR = 'CE060022-43E5-11E4-916C-0800200C9A66'

class ErgBLEClient:
    """
    Implements low-level bleak write and read frames to and from a single erg.
    """

    def __init__(self, address: str | bleak.BLEDevice):
        self._reqlock = asyncio.Lock()
        self._addr = address
        self._bclient = bleak.BleakClient(address)
        self._future_cont = None

    async def connect(self):
        await self._bclient.connect()

    async def disconnect(self):
        await self._bclient.disconnect()

    async def _notified_cb(self, sender: bleak.BleakGATTCharacteristic, data:
                           bytearray):
        assert self._future_cont is not None
        self._future_cont.set_result(data)
        await self._bclient.stop_notify(sender)

    async def write(self, frame: bytes):
        await self._reqlock.acquire()
        await self._bclient.write_gatt_char(WRITE_CHAR_ADDR, frame, True)

    async def read(self) -> bytes:
        assert self._reqlock.locked()
        self._future_cont = asyncio.get_running_loop().create_future()
        await self._bclient.start_notify(NOTIFY_CHAR_ADDR, self._notified_cb)
        res = await self._future_cont
        self._future_cont = None
        self._reqlock.release()
        return res

    async def free(self):
        self._reqlock.release()

    async def __aenter__(self, *args):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.disconnect()


async def main():
    cldev = None
    async with bleak.BleakScanner() as scanner:
        async for dev, adata in scanner.advertisement_data():
            if adata.local_name is not None and adata.local_name.startswith('PM'):
                cldev = dev
                break

    async with ErgBLEClient(cldev) as client:
        await \
        client.write(b'\xF1\x76\x07\x01\x01\01\x13\x02\x01\x01\x61\xF2')
        print(await client.read())


if __name__ == '__main__':
    asyncio.run(main())
