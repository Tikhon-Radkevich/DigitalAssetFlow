

def tag_timeline(timeline, required_growth: float, acceptable_loss: float, required_positive_duration: int):
    """
    This function tags the timeline data with buy (1) or wait (0) labels. It
    iterates segments in direct order, but takes each segment starting from
    the end of timeline.

    :param timeline: List with order_book data.
    :param required_growth: Minimum growth threshold for a buy signal (take-profit)
    :param acceptable_loss: Maximum loss threshold for a buy signal (stop-loss)
    :param required_positive_duration: Minimum number of consecutive time intervals
                                      with positive growth for a buy signal.
    """
    for i in range(1, len(timeline)):
        # If the current data point is already tagged as "buy" (1)
        if timeline[-i]["y"] == 1:
            continue  # move to the next point

        # Extract timeline segment for analysis.
        segment = timeline[-i:]
        min_ask = segment[0]["min_asks_price"]  # buy price
        positive_duration = 0

        # Analyzing segment changes from the beginning
        for j, order_book in enumerate(segment, start=1):
            change = ((order_book["max_bid_price"] / min_ask) - 1)

            # Check if the change in price exceeds the required growth threshold
            if change > required_growth:
                positive_duration += 1
            # Check if the change in price goes below the acceptable loss threshold
            elif change < -acceptable_loss:
                # Exit the function, marking this point as "wait" (0)
                return  # Skip other segment in this timeline

            # Check if the minimum positive duration is met.
            if positive_duration >= required_positive_duration:
                # Mark this point as "buy" (1) and record the grow_time.
                timeline[-i]["y"] = 1
                timeline[-i]["grow_time"] = j - required_positive_duration
                break  # Exit the loop as we have found the necessary conditions.
