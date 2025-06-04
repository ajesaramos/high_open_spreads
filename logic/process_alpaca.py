import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ..api.stock_historical import _get_stock_bars, _create_request_params
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient

# Auth en el cliente que usaremos
client = StockHistoricalDataClient("PKRG42CG4171IN1NQ7DS","Ai940qy5GnA06ic0cu7l8vF7BFKYebZ1hut8GkJW")

def _get_ticker(bars) -> list:
    return (ticker for ticker in bars.data.keys())

def _get_timestamp(bars):
    dates = []
    for ticker in _get_ticker(bars):
        for bar in bars.data[ticker]:
            dates.append(bar.timestamp.strftime("%Y-%m-%d"))
    return dates

def _get_opens(bars):
    opens = []
    for ticker in _get_ticker(bars):
        for bar in bars.data[ticker]:
            opens.append(bar.open)
    return opens

def _get_highs(bars):
    highs = []
    for ticker in _get_ticker(bars):
        for bar in bars.data[ticker]:
            highs.append(bar.high)
    return highs

def _get_delta(opens, highs):
    return [int((x - y)*10000)/10000 for x,y in zip(highs,opens)]

def _get_performance(bars):
    deltas = _get_delta(_get_opens(bars), _get_highs(bars))
    final_list = [delta for delta in deltas if delta >= 0.1000]
    return final_list

def _get_highest(highs):
    return max(highs) if highs else []

def _get_last_daily_high(bars):
    if bars:
        symbol = next(iter(bars.data))
        dates = [item.timestamp.date() for item in bars.data[symbol]]
        latest_high_date = max(dates)
        for item in bars.data[symbol]:
            if item.timestamp.date() == latest_high_date:
                return item.high, item.timestamp.date()
    return None

def _get_avg_high(highs):
    if len(highs) > 1:
        return sum(highs)/len(highs)
    return None


def is_candidate(ticker):
    # Parametros para la request historica
    params = _create_request_params(ticker)
    # Request bars (stock info)
    bars = _get_stock_bars(params, client)
    # get ticker list from results
    tickers = _get_ticker(bars)
    highs_list = _get_performance(bars)
    if len(highs_list) >= 8:
        return (True, highs_list, bars)
    return (False, [], None)

candidate, highs, bars = is_candidate("CLRB")
print(candidate)
print(_get_highest(highs))
print(_get_last_daily_high(bars))
print(_get_avg_high(highs))