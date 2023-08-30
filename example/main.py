import logging
import asyncio

from FSM.Storage import Storage
from FSM.Dispatcher import Dispatcher
from process_handler import router


BINANCE_SYMBOLS = [
        "KLAY/USDT", "MANA/USDT", "SAND/USDT", "ALGO/USDT", "HBAR/USDT", "ADA/USDT", "ALPHA/USDT", "CRV/USDT",
        "PEOPLE/USDT", "SHIB/USDT", "EOS/USDT", "CFX/USDT", "XRP/USDT", "TRX/USDT", "DOGE/USDT", "ETH/USDT",
        "APT/USDT", "OP/USDT", "STX/USDT", "LQTY/USDT", "GALA/USDT", "DYDX/USDT"
    ]
ANALISE_INTERVALS = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1W", "1M"]


async def main():
    logging.basicConfig(
        filename="../debug.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    storage = Storage()
    dp = Dispatcher(storage, BINANCE_SYMBOLS[:2], ANALISE_INTERVALS[:2], depth_limit=5)
    dp.register_router(router)
    await dp.run()


if __name__ == "__main__":
    asyncio.run(main())
