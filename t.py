from client import ErgBLEClient
from command_manager import CommandManager
import asyncio
import bleak


def notified(sender, data):
    print(sender)
    print(data)


async def main():
    cldev = None
    async with bleak.BleakScanner() as scanner:
        async for dev, adata in scanner.advertisement_data():
            if adata.local_name is not None and adata.local_name.startswith('PM'):
                cldev = dev
                break
    print('Found!')

    async with bleak.BleakClient(cldev) as client:
        for service in client.services:
            print(service)
            for char in service.characteristics:
                print(char, char.description, char.properties)
        print('Connected!')
        a = b'\xf1\xab\x91\x91\xab\xf2'
        b = b'\xf1\xab\xab\xf2'
        c = b'\xf1\x21\x03\x02\x00\x21\x1A\x07\x05\x05\x80\xF4\x01\x00\x00\x34\x03\xC8\x00\x58\x24\x02\x00\x00\xE8\xF2'
        await client.write_gatt_char('CE060021-43E5-11E4-916C-0800200C9A66', b,
                                     True)
        print('wmmw')
        await client.start_notify('CE060022-43E5-11E4-916C-0800200C9A66',
                                  notified)

if __name__ == '__main__':
    asyncio.run(main())

