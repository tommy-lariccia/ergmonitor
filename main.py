#!/bin/env python3

from app import *
import asyncio
import bleak


def notified(sender, data):
    print(sender)
    print(data)


async def main():
    ...

if __name__ == '__main__':
    asyncio.run(main())
