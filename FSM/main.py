import asyncio

from Dispatcher import Dispatcher
from process_handler import router


async def main():
    dp = Dispatcher(router)
    await dp.run()


if __name__ == "__main__":
    asyncio.run(main())
