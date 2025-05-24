import bleak
import asyncio
from .client import ErgBLEClient


class ErgScanner:
    def __init__(self):
        self._blescanner = bleak.BleakScanner(detection_callback=self._found_dev)
        self._fut_dev = None

    def _found_dev(self, dev, ad):
        if ad.local_name is not None and ad.local_name.startswith('PM'):
            self._fut_dev.set_result(dev)

    async def find_erg(self):
        self._fut_dev = asyncio.get_running_loop().create_future()
        await self._blescanner.start()
        res = await self._fut_dev
        self._fut_dev = None
        await self._blescanner.stop()
        return ErgBLEClient(res)
