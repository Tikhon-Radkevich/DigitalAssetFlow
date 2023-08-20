import logging
import asyncio

from Storage import Storage
from Dispatcher import Dispatcher
from process_handler import router


# BINANCE_SYMBOLS = [
#         "KLAY/USDT", "MANA/USDT", "SAND/USDT", "ALGO/USDT", "HBAR/USDT", "ADA/USDT", "ALPHA/USDT", "CRV/USDT",
#         "PEOPLE/USDT", "SHIB/USDT", "EOS/USDT", "CFX/USDT", "XRP/USDT", "TRX/USDT", "DOGE/USDT", "ETH/USDT",
#         "APT/USDT", "OP/USDT", "STX/USDT", "LQTY/USDT", "GALA/USDT", "DYDX/USDT"
#     ]
BINANCE_SYMBOLS = [
        "KLAY/USDT"
    ]
# ANALISE_INTERVALS = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d"]
ANALISE_INTERVALS = ["1W", "1M"]


async def main():
    storage = Storage()
    dp = Dispatcher(storage, BINANCE_SYMBOLS, ANALISE_INTERVALS)
    dp.register_router(router)
    await dp.run()


if __name__ == "__main__":
    asyncio.run(main())
