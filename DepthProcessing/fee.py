fee = 0.001  # from Binance (0.1%)


def calc_profit(change):
    profit = ((1 + change) * ((1 - fee) ** 2)) - 1
    return round(profit * 100, 5)


def main(grow, los):
    pct_profit = calc_profit(grow)
    print(f"grow: {round(grow * 100, 5)}% \nprofit: {pct_profit}%")

    pct_los = -calc_profit(-los)
    print(f"\nlos: {round(los * 100, 5)}% \nlosses: {pct_los}%")

    print(f"\nMinimum model performance: {round(pct_los / (pct_profit + pct_los) * 100, 2)}%")

    """
    >>> grow: 0.4% 
    >>> 0.1993%
    
    >>> los: -0.17% 
    >>> losses: 0.36956%
    
    >>> Minimum model performance: 64.97%
    """


if __name__ == "__main__":
    main(0.0040, 0.0017)
