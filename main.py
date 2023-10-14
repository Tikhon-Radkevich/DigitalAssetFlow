import logging
import asyncio

from CryptoDataCollector.Storage import Storage
from CryptoDataCollector.Dispatcher import Dispatcher

from process_handler import router

from config import BINANCE_SYMBOLS, ANALISE_INTERVALS, DEPTH_LIMIT, UPDATE_TIME


async def main():
    logging.basicConfig(
        filename="debug.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    storage = Storage()
    dp = Dispatcher(
        storage,
        BINANCE_SYMBOLS[:2],
        ANALISE_INTERVALS[:2],
        depth_limit=DEPTH_LIMIT,
        update_time=UPDATE_TIME
    )
    dp.register_router(router)

    await dp.run()


if __name__ == "__main__":
    asyncio.run(main())
