import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn import preprocessing
import pandas as pd
import numpy as np
import time
import json
import os
from tqdm import tqdm

path = "data/XRP_USDT/order_book"
step = 0.0001
val_count = 2000
COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]

timeframe = "15m"


def get_indicators(json_data):
    indicators = {}
    for ind_time, value in json_data.items():
        macd = value["TA"][timeframe]["indicators"]["MACD.macd"]
        indicators.update({ind_time: macd})
    return indicators


def get_MACD():
    MACD = {}
    for file_name in tqdm(os.listdir(path), unit="json", desc="Reading", colour="green"):
        with open(f"{path}/{file_name}") as file:
            content = file.read()
            json_content = json.loads(content)
            MACD.update(get_indicators(json_content))
    df = pd.DataFrame(list(MACD.items()), columns=["time", "val"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df.set_index("time", inplace=True)
    return df


def get_json():
    file_list = os.listdir(path)
    with open(f"{path}/{file_list[0]}") as file:
        content = file.read()
    return json.loads(content)


def show_order_book(title, bids, asks, yaxis_title="volume", xaxis_title="price"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=bids[:, 0], y=bids[:, 1], mode="lines", name="bids"))
    fig.add_trace(go.Scatter(x=asks[:, 0], y=asks[:, 1], mode="lines", name="asks"))
    fig.update_layout(title=title, xaxis_title=xaxis_title, yaxis_title=yaxis_title, legend=dict(x=0, y=1, traceorder="normal"), font=dict(size=12))
    fig.show()


def calc_volume(book):
    volume = 0
    for i, v in enumerate(book[:, 1]):
        volume += v
        book[i, 1] = volume
    book[:, 1] = book[:, 1] / volume
    return book


def add_vals(book):
    price = book[0, 0]
    min_price = price - (step * val_count)
    dict_book = dict(book)
    prices = np.arange(book[0, 0], min_price, -step)
    volumes = np.array([dict_book.get(round(price, 3)) or 0 for price in prices])
    return np.column_stack([prices, volumes])


def show_graph(title, data, columns, volume, yaxis_title="price", xaxis_title="timeframe"):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=data.index, y=volume, name="volume", marker=dict(color="rgba(74, 6, 151, 0.8)")), secondary_y=False)
    for сolumn in columns:
        fig.add_trace(go.Scatter(x=data.index, y=data[сolumn], mode='lines', name=сolumn), secondary_y=True)
    fig.update_layout(
        legend=dict(x=0, y=1, traceorder="normal"),
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        font=dict(size=12),
        yaxis=dict(side="right", range=[0, 3]),
        yaxis2=dict(side="left", range=[-0.5, 1.2])
    )

    fig.show()


file_list = os.listdir(path)
file_list.sort()
start_time = file_list[0].split("-")[0]
end_time = file_list[-1].split("-")[-1].split(".")[0]
data = pd.read_csv("data/XRP_USDT/ohlcv/3m/dataframe.csv", index_col=6)
# data_3m = data_3m.query(f"{start_time} < timestamp < {end_time}")
# data_5m = pd.read_csv("data/XRP_USDT/ohlcv/5m/dataframe.csv", index_col=6)
# data_5m = data_5m.query(f"{start_time} < timestamp < {end_time}")
# data = pd.read_csv("data/XRP_USDT/ohlcv/15m/dataframe.csv", index_col=6)
data = data.query(f"{start_time} < timestamp < {end_time}")

price_scaler = preprocessing.MinMaxScaler()
volume_scaler = preprocessing.MinMaxScaler()
price_scaler.fit(np.array([data[["low"]].min().values[0], data[["high"]].max().values[0]]).reshape(-1, 1))
high = price_scaler.transform(data[["high"]].values)
low = price_scaler.transform(data[["low"]].values)
volume = volume_scaler.fit_transform(data[["volume"]].values)
data[["high"]] = high
data[["low"]] = low
data[["volume"]] = volume


macd = get_MACD()
macd_scaler = preprocessing.MinMaxScaler((-1, 1))
mac_vals = macd_scaler.fit_transform(macd[["val"]])
macd[["val"]] = mac_vals
macd[["positive"]] = mac_vals
macd["positive"] = macd["val"].clip(lower=0)
macd[["negative"]] = mac_vals
macd["negative"] = macd["val"].clip(upper=0)

# print(macd)


fig = go.Figure()
fig.add_trace(go.Bar(x=macd.index, y=macd["positive"], name="MACD +", yaxis="y3", marker=dict(color="rgba(6, 168, 52, 0.8)", opacity=1)))
fig.add_trace(go.Bar(x=macd.index, y=macd["negative"], name="MACD -", yaxis="y3", marker=dict(color="rgba(165, 7, 7, 0.8)", opacity=1)))
fig.add_trace(go.Bar(x=data.index, y=data["volume"], name="volume", marker=dict(color="rgba(74, 6, 151, 0.8)")))
fig.add_trace(go.Scatter(x=data.index, y=data["high"], mode="lines", name="high", yaxis="y2"))
fig.add_trace(go.Scatter(x=data.index, y=data["low"], mode="lines", name="low", yaxis="y2"))
fig.update_layout(
    legend=dict(x=0, y=1, traceorder="normal"),
    title="XRP/USDT",
    font=dict(size=12),
    yaxis=dict(side="right", range=[0, 4]),
    yaxis2=dict(side="left", range=[-1.5, 2.6], overlaying="y",),
    yaxis3=dict(side="left", range=[-7.2, 1.2], overlaying="y",)
)

fig.show()


# show_graph(title="XRP/USDT", data=data, columns=["high", "low"], volume=data["volume"], yaxis_title="", xaxis_title="")


# json_data = get_json()
# for key, value in json_data.items():
#     ta = value["TA"]
#     for ta_key, ta_value in ta.items():
#         print(f"{ta_key} - {ta_value['analysis']}")
#     bids = np.array(value["bids"])
#     bids = add_vals(bids)
#     bids = calc_volume(bids)
#     asks = np.array(value["asks"])
#     asks = add_vals(asks)
#     asks = calc_volume(asks[::-1])
#     show_order_book("Order Book", bids, asks, yaxis_title="volume", xaxis_title="price")
#     break

