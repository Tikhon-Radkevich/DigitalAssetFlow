import logging
import asyncio
import json
import time

import websockets
import aiohttp


class CustomWebSocket:
    UPDATE_SPEED = 1000  # ms
    SOCKET_LIFETIME = 12*60*60
    STREAM_URL = "wss://stream.binance.com:443/ws/"

    def __init__(self, symbols: list, limits=1000):
        self._symbols: list = symbols
        self._limits: int = limits
        self._order_book: dict = self._create_order_book()
        self._symbols_for_snapshot: list = symbols.copy()
        self._end_time = None

    async def get_order_book(self, symbol):
        book = {
            "symbol": symbol,
            "bids": self._order_book[symbol]["bids"],
            "asks": self._order_book[symbol]["asks"]
        }
        return book

    async def subscribe(self, close_timeout=0.2, ping_timeout=40):
        url = self.STREAM_URL + "/".join([f"{symbol.lower()}@depth@{self.UPDATE_SPEED}ms" for symbol in self._symbols])
        while True:
            self._end_time = time.time() + self.SOCKET_LIFETIME
            try:
                async with websockets.connect(url, close_timeout=close_timeout, ping_timeout=ping_timeout) as websocket:
                    i = 0
                    while True:
                        # todo remove debug print
                        i += 1
                        if i > 3: i = 0
                        print("tick"+"."*i)
                        if time.time() > self._end_time:
                            logging.info("socket reconnect")
                            break
                        if len(self._symbols_for_snapshot) > 0:
                            await self._make_snapshot()
                        for _ in range(len(self._symbols)):
                            message = await websocket.recv()
                            await self._handle_message(json.loads(message))
            except Exception as e:
                error_message = f"Socket Dropped: \n\n{e} \n\n{message}"
                logging.error(error_message, exc_info=True)

    async def _handle_message(self, message):
        last_update_id = self._order_book[message["s"]]["lastUpdateId"]
        if message["u"] <= last_update_id:
            return
        if message["U"] <= last_update_id + 1 <= message["u"]:
            await self._process_updates(message)
        else:
            self._symbols_for_snapshot.append(message["s"])

    async def _make_snapshot(self):
        logging.warning(f" snapshot: {', '.join(self._symbols_for_snapshot)}")
        async with aiohttp.ClientSession() as session:
            tasks = [self._get_depth(symbol, session) for symbol in self._symbols_for_snapshot]
            results = await asyncio.gather(*tasks)
        for message in results:
            await self._process_updates(message)
        self._symbols_for_snapshot.clear()

    async def _process_updates(self, message):
        self._order_book[message["s"]]["lastUpdateId"] = message["u"]
        for (n, name) in [("b", "bids"), ("a", "asks")]:
            for value in message[n]:
                price, volume = float(value[0]), float(value[1])
                if volume == 0:
                    self._order_book[message["s"]][name].pop(price, None)
                else:
                    self._order_book[message["s"]][name][price] = volume

    async def _get_depth(self, symbol, session):
        snapshot_url = f"https://api.binance.com/api/v3/depth?symbol={symbol.upper()}&limit={self._limits}"
        async with session.get(snapshot_url) as response:
            response_json = await response.json()
            depth = {
                "s": symbol,
                "u": response_json["lastUpdateId"],
                "b": response_json["bids"],
                "a": response_json["asks"]
            }
            return depth

    def _create_order_book(self):
        order_book = {}
        for symbol in self._symbols:
            order_book[symbol] = {
                "lastUpdateId": 0,
                "bids": {},
                "asks": {},
            }
        return order_book


if __name__ == "__main__":
    pass
