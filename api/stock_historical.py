from datetime import datetime
from dateutil.relativedelta import relativedelta
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient

def _end_date():
    return datetime.today() - relativedelta(days=1)


def _start_date():
    return _end_date() - relativedelta(months=1)


def _time_frame(timeframe: list=[
 1, TimeFrameUnit.Day]):
    return TimeFrame(timeframe[0], timeframe[1])


def _create_request_params(symbols, start: datetime=None, end: datetime=None, timeframe: TimeFrame=None):
    if start is None:
        start = _start_date()
    if end is None:
        end = _end_date()
    if timeframe is None:
        timeframe = _time_frame()
    return StockBarsRequest(symbol_or_symbols=symbols,
      start=start,
      end=end,
      timeframe=timeframe)


def _get_stock_bars(request_params: StockBarsRequest, stock_historical_client: StockHistoricalDataClient):
    return stock_historical_client.get_stock_bars(request_params)