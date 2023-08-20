from typing import List
import logging
import asyncio
import time

from TradingView.CustomRequest import CustomRequest
from CustomSocket import CustomWebSocket
from Storage import Storage
from Router import Router


class Dispatcher:
    def __init__(self, storage: Storage, symbols: List[str], intervals: List[str], update_time=10, depth_limit=1000):
        """
        Initialize the Dispatcher instance.

        :param storage: The storage for saving data.
        :param symbols: List of trading symbols (e.g., ["BTC/USDT", ...]).
        :param intervals: List of time intervals for technical analysis.
        """
        self.routers = []
        self.storage = storage
        self.update_time = update_time
        self.symbols = list(map(lambda x: x.replace("/", ""), symbols))
        self.depth_socket = CustomWebSocket(self.symbols, depth_limit)
        self.TechnicalAnalysis = CustomRequest(self.symbols, intervals)

    def register_router(self, router: Router):
        self.routers.append(router)

    async def _run_socket(self):
        try:
            await self.depth_socket.subscribe()
        except Exception as e:
            logging.error(e, exc_info=True)

    async def _run_main_loop(self):
        while True:
            await asyncio.sleep(self.update_time)
            start = time.time()
            depth = await self.depth_socket.get_order_book(self.symbols[0])
            depth_time = time.time()
            # print("depth:", depth_time-start)
            analysis = await self.TechnicalAnalysis.get_analysis()
            # print("analysis:", time.time()-depth_time)
            for router in self.routers:
                router(depth=depth, analysis=analysis, storage=self.storage)

    async def run(self):
        await asyncio.gather(self._run_socket(), self._run_main_loop())
