import logging
import asyncio

from CryptoDataCollector.TradingView.analysis import calculate
import aiohttp


class CustomRequest:
    # Note: Please DO NOT modify the order or DELETE existing indicators, it will break the technical analysis.
    INDICATORS = [
        "Recommend.Other", "Recommend.All", "Recommend.MA", "RSI", "RSI[1]", "Stoch.K", "Stoch.D", "Stoch.K[1]",
        "Stoch.D[1]", "CCI20", "CCI20[1]", "ADX", "ADX+DI", "ADX-DI", "ADX+DI[1]", "ADX-DI[1]", "AO", "AO[1]", "Mom",
        "Mom[1]", "MACD.macd", "MACD.signal", "Rec.Stoch.RSI", "Stoch.RSI.K", "Rec.WR", "W.R", "Rec.BBPower", "BBPower",
        "Rec.UO", "UO", "close", "EMA5", "SMA5", "EMA10", "SMA10", "EMA20", "SMA20", "EMA30", "SMA30", "EMA50", "SMA50",
        "EMA100", "SMA100", "EMA200", "SMA200", "Rec.Ichimoku", "Ichimoku.BLine", "Rec.VWMA", "VWMA", "Rec.HullMA9",
        "HullMA9", "Pivot.M.Classic.S3", "Pivot.M.Classic.S2", "Pivot.M.Classic.S1", "Pivot.M.Classic.Middle",
        "Pivot.M.Classic.R1", "Pivot.M.Classic.R2", "Pivot.M.Classic.R3", "Pivot.M.Fibonacci.S3", "Pivot.M.Fibonacci.S2",
        "Pivot.M.Fibonacci.S1", "Pivot.M.Fibonacci.Middle", "Pivot.M.Fibonacci.R1", "Pivot.M.Fibonacci.R2",
        "Pivot.M.Fibonacci.R3", "Pivot.M.Camarilla.S3", "Pivot.M.Camarilla.S2", "Pivot.M.Camarilla.S1",
        "Pivot.M.Camarilla.Middle", "Pivot.M.Camarilla.R1", "Pivot.M.Camarilla.R2", "Pivot.M.Camarilla.R3",
        "Pivot.M.Woodie.S3", "Pivot.M.Woodie.S2", "Pivot.M.Woodie.S1", "Pivot.M.Woodie.Middle", "Pivot.M.Woodie.R1",
        "Pivot.M.Woodie.R2", "Pivot.M.Woodie.R3", "Pivot.M.Demark.S1", "Pivot.M.Demark.Middle", "Pivot.M.Demark.R1",
        "open", "P.SAR", "BB.lower", "BB.upper", "AO[2]", "volume", "change", "low", "high"
    ]
    INTERVALS = {
        "1m": "|1",
        "5m": "|5",
        "15m": "|15",
        "30m": "|30",
        "1h": "|60",
        "2h": "|120",
        "4h": "|240",
        "1d": "",
        "1W": "|1W",
        "1M": "|1M"
    }
    SCAN_URL = "https://scanner.tradingview.com/crypto/scan"
    HEADERS = {'User-Agent': 'tradingview_ta/3.3.0'}
    TIMEOUT = 5
    PROXIES = None

    def __init__(self, symbols, intervals, exchange="BINANCE"):
        self.intervals = intervals
        self._exchange = exchange
        self._symbols = symbols
        self._ta_to_symbol = self._create_ta_to_symbol()
        self._request_json = self._get_request_json()

    async def _request_analysis(self):
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                self.SCAN_URL, json=self._request_json, headers=self.HEADERS, timeout=self.TIMEOUT
            )
            if response.status != 200:
                raise Exception(f"Can't access TradingView's API. HTTP status code: {response.status}.")
            json_response = await response.json()
            result = json_response["data"]
            if not result:
                raise Exception("Got empty data from TradingView")
            return result

    async def get_analysis(self, request_error_count=0):
        try:
            result = await self._request_analysis()
            data = {}
            for symbol_data in result:
                symbol = self._ta_to_symbol[symbol_data["s"]]
                data[symbol] = {
                    "symbol": symbol,
                    "TA": {}
                }
                for i, interval in enumerate(self.intervals):
                    indicators_dict = {}
                    indicators_values = symbol_data["d"][i::len(self.intervals)]
                    for x in range(len(self.INDICATORS)):
                        indicators_dict[self.INDICATORS[x]] = indicators_values[x]
                    my_analysis = calculate(
                        indicators_dict,
                        self.INDICATORS.copy(),
                        symbol.replace("/", ""),
                        interval,
                        self._exchange
                    )
                    data[symbol]["TA"][interval] = {
                        "summary": my_analysis.summary,
                        "oscillators": my_analysis.oscillators,
                        "moving_averages": my_analysis.moving_averages,
                        "indicators": my_analysis.indicators
                    }
            return data
        except Exception as e:
            # todo
            logging.error(str(e))
            request_error_count += 1
            if request_error_count < 3:
                await asyncio.sleep(3)
                return await self.get_analysis(request_error_count)
            raise Exception("Can't get analysis for 3 times!")

    def _get_request_json(self):
        tickers = [f"{self._exchange}:{coin}" for coin in self._symbols]
        columns = [x + self.INTERVALS[interval] for x in self.INDICATORS for interval in self.intervals]
        return {
            "symbols": {"tickers": tickers, "query": {"types": []}},
            "columns": columns
        }

    def _create_ta_to_symbol(self):
        ta_to_symbol = {}
        for symbol in self._symbols:
            ta_to_symbol[f"{self._exchange}:{symbol}"] = symbol
        return ta_to_symbol
