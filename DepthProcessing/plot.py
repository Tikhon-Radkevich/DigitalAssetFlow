import json
import os

import plotly.graph_objects as go
from tqdm import tqdm
import numpy as np

from tag_data import get_labeled_data


LABELED_DATA_PATH = "../data/LabeledDepthData"
FILTERED_DATA_PATH = "../data/FilteredDepthData"


def box_plot_positive_change_frequency_over_time():
    labeled_files_list = os.listdir(FILTERED_DATA_PATH)[10:11]

    # Create an empty list to store data for the box plot
    data_for_box_plot = []

    # Iterate through labeled files and collect data for the box plot
    for file_name in tqdm(labeled_files_list):
        with open(f"{FILTERED_DATA_PATH}/{file_name}", "r") as file:
            labeled_data = get_labeled_data(json.load(file))
            for val in labeled_data.values():
                grow = np.array(val["grow_times"])
                for g in grow:
                    if g != -1:
                        data_for_box_plot.append(g)

    # Create a box plot
    trace = go.Box(y=data_for_box_plot, jitter=0.3, pointpos=-1.8)
    layout = go.Layout(
        title=f"Distribution of Positive Changes Amount Over Time",
        yaxis=dict(title="Amount"),
        xaxis=dict(title="Time Intervals"),
        template="plotly_dark"
    )
    fig = go.Figure(data=[trace], layout=layout)
    fig.show()


def display_positive_change_frequency_over_time():
    labeled_files_list = os.listdir(FILTERED_DATA_PATH)[10:15]
    y = np.array([0]*123, dtype="float64")
    for file_name in tqdm(labeled_files_list):
        with open(f"{FILTERED_DATA_PATH}/{file_name}", "r") as file:
            labeled_data = get_labeled_data(json.load(file))
            for val in labeled_data.values():
                grow = np.array(val["grow_times"])
                for g in grow:
                    if g != -1:
                        y[g] += 1

    y /= np.max(y)
    x = np.arange(start=0, stop=len(y), step=1/6)

    trace = go.Bar(x=x, y=y)
    layout = go.Layout(
        title=f"Positive Changes Amount",
        yaxis=dict(title="Amount (%)"),
        xaxis=dict(title=f"Period (min)"),
        template="plotly_dark"
    )
    fig = go.Figure(data=trace, layout=layout)
    fig.show()


def show_positive_percent(data):
    x = np.array(list(data.keys()))
    y = list(map(lambda val: round(val*100, 2), data.values()))
    average_pct = round((sum(y) / len(y)), 2)
    text = np.array([f"{val}%" for val in y])

    trace = go.Bar(x=x, y=np.array(y), text=text, textposition="outside")
    layout = go.Layout(
        title=f"Positive Changes (average: {average_pct}%)",
        yaxis=dict(title="percent"),
        xaxis=dict(title=f"Month Period"),
        template="plotly_dark"
    )
    fig = go.Figure(data=trace, layout=layout)
    fig.show()


def main():
    labeled_files_list = os.listdir(LABELED_DATA_PATH)
    data = {}
    for file_name in tqdm(labeled_files_list):
        with open(f"{LABELED_DATA_PATH}/{file_name}", "r") as file:
            labeled_data = json.load(file)
            for symbol in labeled_data.keys():
                y = labeled_data[symbol]["y"]
                pct = data.get(symbol, 0)
                pct += (y.count(1) / len(y)) / len(labeled_files_list)
                data[symbol] = pct
    show_positive_percent(data)


if __name__ == "__main__":
    box_plot_positive_change_frequency_over_time()
