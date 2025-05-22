from client import ErgBLEClient
import asyncio


async def main():
    ergcl = ErgBLEClient()
    await ergcl.write(b'')
    await ergcl.write(b'')
    resp = await ergcl.read()
    resp2 = await ergcl.read()
    print(resp)
    print(resp2)


if __name__ == '__main__':
    asyncio.run(main())
