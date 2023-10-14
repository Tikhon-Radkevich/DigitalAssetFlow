import numpy as np


def filter_asks(asks, pct_change, order_book_length):
    """ Filters and aligns the ask prices in the order book
    based on the provided percentage change and desired length.

    :param asks: Array of asks where each element is a tuple of (price, volume).
    :param pct_change: The percentage price change to determine the filter range.
    :param order_book_length: The desired length of the processed order book.
    :return: Array of volumes aligned with new ask price levels.
    """
    max_price = asks[0][0] * (1 + pct_change)
    step = (max_price - asks[0][0]) / order_book_length
    new_prices = np.arange(asks[0][0], max_price, step)
    volumes = np.zeros(order_book_length)
    i = 0
    # Iterate through new price levels and sum up ask volumes
    for volume_idx, new_price in enumerate(new_prices):
        while (i < len(asks)) and (asks[i][0] <= new_price):
            volumes[volume_idx] += asks[i][1]
            i += 1
    return volumes


def filter_bids(bids, pct_change, order_book_length):
    """ Filters and aligns the bid prices """

    min_price = bids[0][0] * (1 - pct_change)
    step = (bids[0][0] - min_price) / order_book_length
    new_prices = np.arange(bids[0][0], min_price, -step)
    volumes = np.zeros(order_book_length)

    i = 0
    for volume_idx, new_price in enumerate(new_prices):
        while (i < len(bids)) and (bids[i][0] >= new_price):
            volumes[volume_idx] += bids[i][1]
            i += 1
    return volumes


def get_order_book(order_book_json, pct_chang=0.032):
    """ Processes the order book data to ensure uniform inputs for the model.
    It filters and aligns bids and asks to have the same length and a consistent
    percentage price change. Then, it retains only the volume values.

    :param order_book_json: JSON data containing the order book
    :param pct_chang: The percentage price change to determine the length of the processed order book
    :return: Processed order book data
    """

    # Calculate the length of the processed order book based on the provided percentage change
    book_length = int(pct_chang * 20 * 100)

    data = {}
    for dtime_ms, order_book in order_book_json.items():
        # Process bids
        bids = np.array(order_book["bids"])
        max_bid_price = bids[0][0]  # Get the current highest bid price
        if max_bid_price < bids[1][0]:
            raise ValueError("The order book is not sorted correctly")
        bids = filter_bids(bids, pct_chang, book_length)

        # Process asks
        asks = np.array(order_book["asks"])
        min_asks_price = asks[0][0]  # Get the current lowest ask price
        if min_asks_price > asks[1][0]:
            raise ValueError("The order book is not sorted correctly")
        asks = filter_asks(asks, pct_chang, book_length)

        data[dtime_ms] = {
            "bids": bids.tolist(),
            "max_bids_price": max_bid_price,  # Current selling price
            "asks": asks.tolist(),
            "min_asks_price": min_asks_price,  # Current purchase price
        }
    return data
