import logging
import asyncio

from CustomSocket import MyWebSocket
from Router import Router


class Dispatcher:
    BINANCE_SYMBOLS = [
        "KLAY/USDT", "MANA/USDT", "SAND/USDT", "ALGO/USDT", "HBAR/USDT", "ADA/USDT", "ALPHA/USDT", "CRV/USDT",
        "PEOPLE/USDT", "SHIB/USDT", "EOS/USDT", "CFX/USDT", "XRP/USDT", "TRX/USDT", "DOGE/USDT", "ETH/USDT",
        "APT/USDT", "OP/USDT", "STX/USDT", "LQTY/USDT", "GALA/USDT", "DYDX/USDT"
    ]
    symbols = list(map(lambda x: x.replace("/", ""), BINANCE_SYMBOLS))

    def __init__(self, router: Router):
        self.router = router
        self.depth = []
        self.depth_socket = MyWebSocket(self.symbols, 1000)

    async def _run_socket(self):
        try:
            await self.depth_socket.subscribe()
        except Exception as e:
            logging.error(e, exc_info=True)

    async def _run_main_loop(self):
        while True:
            await asyncio.sleep(10)
            depth = await self.depth_socket.get_order_book(self.symbols[0])
            self.router(depth=depth)

    async def run(self):
        await asyncio.gather(self._run_socket(), self._run_main_loop())

