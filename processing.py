import warnings

from tqdm import tqdm
import pandas as pd
import numpy as np
import json
import os


class Data:
    SYMBOLS = [
        "KLAY/USDT", "MANA/USDT", "SAND/USDT", "ALGO/USDT", "HBAR/USDT", "ADA/USDT", "ALPHA/USDT", "CRV/USDT",
        "PEOPLE/USDT", "SHIB/USDT", "EOS/USDT", "CFX/USDT", "XRP/USDT", "TRX/USDT", "DOGE/USDT", "ETH/USDT",
        "APT/USDT", "OP/USDT", "STX/USDT", "LQTY/USDT", "GALA/USDT", "DYDX/USDT"
    ]
    path = "data/XRP_USDT/order_book"
    XRP_USDT_step = 0.0001
    val_count = 2000
    MAX_DIF = 15000
    COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]

    @classmethod
    def check_json_continuity(cls):
        for file_name in tqdm(os.listdir(cls.path), unit="json", desc="Reading Analysis"):
            with open(f"{cls.path}/{file_name}") as file:
                json_content = json.loads(file.read())
            time_ms = np.array(list(map(int, json_content.keys())))
            cls.check_continuity(time_ms)

    @classmethod
    def check_continuity(cls, time_ms, max_diff=MAX_DIF):
        diff = time_ms[1:] - time_ms[:-1]
        if diff.max() > max_diff:
            print(f"\nSpace in data! {diff.max()}\n")

    @classmethod
    def get_dataframe(cls, coin, timeframe, start_time, end_time):
        """
        get DataFrame ["timestamp", "open", "high", "low", "close", "volume"]
        :param coin: NAME_PAIR
        :param timeframe: "15m", "5m", "3m"
        :param start_time: in ms
        :param end_time: in ms
        :return: pd.DataFrame
        """
        data = pd.read_csv(f"data/{coin}/ohlcv/{timeframe}/dataframe.csv", index_col=6)
        data = data.query(f"{start_time} <= timestamp <= {end_time}")
        return data

    @classmethod
    def get_analysis(cls):
        data = {}
        for file_name in tqdm(os.listdir(cls.path), unit="json", desc="Reading Analysis"):
            with open(f"{cls.path}/{file_name}") as file:
                json_content = json.loads(file.read())
            for time_ms, value in json_content.items():
                data[time_ms] = {}
                for timeframe, ta_data in value["TA"].items():
                    data[time_ms].update({timeframe: ta_data["analysis"]})
        return data

    @classmethod
    def get_order_book_and_min_ask_price(cls):
        min_ask_prices = []
        order_book = {}
        step, depth = 0.0001, 2000  # todo
        for file_name in tqdm(os.listdir(cls.path)[:11], unit="json", desc="Reading Order Book"):
            with open(f"{cls.path}/{file_name}") as file:
                json_content = json.loads(file.read())
            for time_ms, value in json_content.items():
                bids = np.array(value["bids"])
                bids = cls._add_vals_2(bids, step, depth)
                asks = np.array(value["asks"])
                min_ask_prices.append(asks[-1, 0])
                asks = cls._add_vals_2(asks, step, depth, is_asks=True)
                order_book[time_ms] = np.array([bids, asks[::-1]])
                # b0 > b1
                # a0 < a1
        return order_book, min_ask_prices

    @classmethod
    def _add_vals_2(cls, book, step, depth=1000, is_asks=False):
        func, cof = max, 1
        if is_asks:
            func, cof = min, -1
        price = func(book[0, 0], book[-1, 0]) / step
        dict_book = dict(book)
        volumes = np.array([dict_book.get((price - (i*cof)) * step) or 0 for i in range(depth)])
        return volumes



    # @classmethod
    # def get_order_book(cls):
    #     order_book = {}
    #     step, depth = 0.0001, 2000  # todo
    #     for file_name in tqdm(os.listdir(cls.path), unit="json", desc="Reading Order Book"):
    #         with open(f"{cls.path}/{file_name}") as file:
    #             json_content = json.loads(file.read())
    #         for time_ms, value in json_content.items():
    #             bids = np.array(value["bids"])
    #             bids = cls._add_vals(bids, step, depth)
    #             bids = cls._calc_volume(bids)
    #             asks = np.array(value["asks"])
    #             asks = cls._add_vals(asks, step, depth)
    #             asks = cls._calc_volume(asks[::-1])
    #             order_book.update({time_ms: {"bids": bids, "asks": asks}})
    #     return order_book
    #
    # @classmethod
    # def _calc_volume(cls, book):
    #     volume = 0
    #     for i, v in enumerate(book[:, 1]):
    #         volume += v
    #         book[i, 1] = volume
    #     return book
    #
    # @classmethod
    # def _add_vals(cls, book, step, depth=1000):
    #     price = book[0, 0]
    #     min_price = price - (step * depth)
    #     print(min_price)
    #     prices = np.arange(book[0, 0], min_price, -step)
    #     dict_book = dict(book)
    #     volumes = np.array([dict_book.get(round(price, 4)) or 0 for price in prices])
    #     return np.column_stack([prices, volumes])


if __name__ == "__main__":
    Data.check_continuity()
