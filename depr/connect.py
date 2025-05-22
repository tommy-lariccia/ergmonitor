import bleak
import asyncio


class ErgScanner:
    BASE_UUID: str = "ce06{}-43e5-11e4-916c-0800200c9a66"
    WRITE_UUID: str = BASE_UUID.format("0021")
    READ_UUID: str = BASE_UUID.format("0022")

    def __init__(self):
        self.scanner = bleak.BleakScanner()

    async def find_ergs(self):
        async for bd, ad in self.scanner.advertisement_data():
            print('wnwn')
            if ad.local_name is not None and ad.local_name.startswith('PM5'):
                yield Erg(bd)

    async def find_erg(self):
        async for erg in self.find_ergs():
            return erg

    async def start(self):
        await self.scanner.start()

    async def stop(self):
        await self.scanner.stop()

    async def __aenter__(self, *args):
        await self.start()
        return self

    async def __aexit__(self, *args):
        await self.stop()


class Erg:
    def __init__(self, bd):
        self.ble_name = bd.name
        self.ble_address = bd.address
        self.ble_client = bleak.BleakClient(bd)

    async def connect(self):
        await self.ble_client.connect()

    async def disconnect(self):
        await self.ble_client.disconnect()


async def main():
    async with ErgScanner() as scanner:
        erg = await scanner.find_erg()


if __name__ == '__main__':
    asyncio.run(main())
