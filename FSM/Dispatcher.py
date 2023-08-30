from typing import List
import logging
import asyncio
import time

from FSM.TradingView.CustomRequest import CustomRequest
from FSM.CustomSocket import CustomWebSocket
from FSM.Storage import Storage
from FSM.Router import Router


class Dispatcher:
    def __init__(self, storage: Storage, symbols: List[str], intervals: List[str], update_time=10, depth_limit=1000):
        """ Initialize the Dispatcher instance.

        :param storage: The storage for saving data.
        :param symbols: List of trading symbols (e.g., ["BTC/USDT", ...]).
        :param intervals: List of time intervals for technical analysis;
                         Available: "1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1W", "1M"
        :param update_time: Int value.
        :param depth_limit: Int value.
        """

        self.routers = []
        self.__storage = storage
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
        """ This function continuously updates data at a fixed rate, executing handlers with the latest data.

        Important: Handlers should be optimized to complete within the expected 'update_time' to ensure timely updates.
        Executor: Handlers are run using the executor, ensuring that other tasks, like socket operations,
                  are not delayed by lengthy handler execution. """

        loop = asyncio.get_event_loop()
        start_time = time.time()
        while True:
            sleep_time = self.update_time - (time.time() - start_time)
            if sleep_time < 0:
                logging.warning("Handlers exceeded the expected update time.")
            else:
                await asyncio.sleep(sleep_time)
            start_time = time.time()

            depth = await self.depth_socket.get_order_book()
            analysis = await self.TechnicalAnalysis.get_analysis()

            # Run handlers asynchronously using the executor
            await loop.run_in_executor(None, self._execute_handlers, depth, analysis)

    def _execute_handlers(self, depth, analysis):
        for router in self.routers:
            router(depth=depth, analysis=analysis, storage=self.__storage)

    async def run(self):
        await asyncio.gather(self._run_socket(), self._run_main_loop())
