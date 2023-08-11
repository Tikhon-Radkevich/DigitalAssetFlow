import numpy as np
import pandas as pd

from processing import Data

order_book, min_ask_prices = Data.get_order_book_and_min_ask_price()
times = [*order_book.keys()]
order_book = [*order_book.values()]

df = Data.get_dataframe("XRP_USDT", "5m", times[0], int(times[-1])+(5*60*1000))

order_set_length = 30  # 5m
profit_change = 0.004
one_ratio = 0.33


def get_y_price(last_time, ask_price):
    mask = df["timestamp"] > int(last_time)
    if mask.any():
        index = df.loc[mask, "timestamp"].idxmin()
        high = df.at[index, "high"]
        change = (high / ask_price) - 1
        if change >= profit_change:
            return 1
        return 0
    raise Exception(f"No time {last_time} in dataframe")


def create_train():
    x_train = []
    y_train = []
    for i in range(len(times)-31):
        order_set = order_book[i:i+30]
        x_train.append(order_set)
        y_train.append(get_y_price(times[i+30], min_ask_prices[i+29]))

    extra_zeros = len(y_train) - int(y_train.count(1) / one_ratio)
    y_train = np.array(y_train)
    x_train = np.array(x_train)
    if extra_zeros > 0:
        zero_poses = np.where(y_train == 0)[0]
        random_indices = np.random.choice(zero_poses, size=extra_zeros, replace=False)
        y_train = np.delete(y_train, random_indices, axis=0)
        x_train = np.delete(x_train, random_indices, axis=0)

    indices = np.random.permutation(len(y_train))
    return x_train[indices], y_train[indices]


def get_dataset():
    x_train, y_train = create_train()
    test_length = int(y_train.shape[0]*0.1)
    return (x_train[:-test_length], y_train[:-test_length]), (x_train[-test_length:], y_train[-test_length:])


def main():
    (x_train, y_train), (x_test, y_test) = get_dataset()
    print(x_train.shape, y_train.shape)
    print(x_test.shape, y_test.shape)


if __name__ == "__main__":
    main()