import bleak
import asyncio


class ErgTracking:
    ergs = []

    async def _find_ergs(timeout=None):
        running = True
        async def _run_out():
            nonlocal running
            if timeout is None:
                return
            await asyncio.sleep(timeout)
            running = False
        asyncio.create_task(_run_out())
        async with bleak.BleakScanner() as scanner:
            print('Scanning...')
            async for bd, ad in scanner.advertisement_data():
                if ad.local_name is not None and ad.local_name.startswith('PM5'):
                    print(bd)
                    print('Found!')
                    ergdev = bd
                if not running:
                    break


    async def run():
        async with asyncio.TaskGroup() as tg:
            tg.create_task(ErgTracking._find_ergs())


async def main():
    ergdev = None
    async with bleak.BleakScanner() as scanner:
        print('Scanning...')
        async for bd, ad in scanner.advertisement_data():
            if ad.local_name is not None and ad.local_name.startswith('PM5'):
                print(bd)
                print('Found!')
                ergdev = bd
                break
    print('Connecting...')
    async with bleak.BleakClient(ergdev) as client:
        print('Connected!')
        print('Discovering services...')
        for service in client.services:
            print("Service:", service)
            for char in service.characteristics:
                print(char.uuid, char.properties, char.description)
        print('Testing...')
        i = 0
        from csafe.csafe import make_standard_frame
        await client.write_gatt_char("ce060021-43e5-11e4-916c-0800200c9a66",
                                     make_standard_frame(), True)
        print(await
              client.read_gatt_char("ce060022-43e5-11e4-916c-0800200c9a66"))


if __name__ == '__main__':
    asyncio.run(main())
