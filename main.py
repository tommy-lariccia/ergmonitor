#!/bin/env python3

from app import *
import app.csafe
import asyncio


async def main():
    scanner = ErgScanner()
    ergcl = await scanner.find_erg()
    print('Found erg!')

    async with CommandManager(ergcl) as cm:
        print(await cm.get(b'\x80'))

if __name__ == '__main__':
    asyncio.run(main())
