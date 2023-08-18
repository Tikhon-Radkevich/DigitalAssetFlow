from tag_timeline import tag_timeline


timeline_length = 30  # (5m)
required_growth = 0.004  # (0.4%)
acceptable_loss = 0.0019  # (0.19%)
required_positive_duration = 3  # (30s)

timeline_length += required_positive_duration


def get_labeled_data(data, depth_size=64):
    labeled_data = {}
    for symbol, coin_data in data.items():
        labeled_data[symbol] = {
            "datetimes": [],
            "grow_times": [],
            "y": [],
            "min_asks_prices": [],
            "max_bids_prices": [],
            "bids": [],
            "asks": [],
        }
        timeline = []
        datetimes = sorted(list(coin_data.keys()))
        for datetime in datetimes:
            order_book = coin_data[datetime]
            order_book["y"] = 0
            order_book["datetime"] = datetime
            timeline.append(order_book)
            tag_timeline(timeline, required_growth, acceptable_loss, required_positive_duration)
            if len(timeline) > timeline_length:
                book = timeline.pop(0)
                labeled_data[symbol]["y"].append(book["y"])
                labeled_data[symbol]["grow_times"].append(book["grow_time"])
                labeled_data[symbol]["datetimes"].append(book["datetime"])
                labeled_data[symbol]["min_asks_prices"].append(book["min_asks_price"])
                labeled_data[symbol]["max_bids_prices"].append(book["max_bid_price"])
                labeled_data[symbol]["bids"].append(book["bids"][:depth_size])
                labeled_data[symbol]["asks"].append(book["asks"][:depth_size])
    return labeled_data
