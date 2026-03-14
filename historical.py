from account import API_KEY , API_SECRET

#from pydoc import cli

import numpy as np
#import incoming as inc

import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient, OptionHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest, OptionTradesRequest, OptionBarsRequest, OptionLatestQuoteRequest

from clients import AlcapaTradingClient
OptionBarsRequest
from alpaca.data.enums import DataFeed
from alpaca.trading.enums import ContractType
from alpaca.trading.client import OptionContract, TradingClient, TradeAccount, GetOptionContractsRequest
from alpaca.data.timeframe import TimeFrame ; import cudf as cdf 
from datetime import datetime, timezone, date
import polars as pl
from alpaca.data.live import StockDataStream, OptionDataStream
from account import API_KEY , API_SECRET
from collections import  deque
from pathlib import Path


global  t2 

# alpaca_data_client.py

class AlpacaDataClient:
    def __init__(self, api_key: str, api_secret: str):
        self.stock_hist = StockHistoricalDataClient(api_key, api_secret)
        self.option_hist = OptionHistoricalDataClient(api_key, api_secret)


    # =========================
    # HISTORICAL — STOCKS
    # =========================
    def stock_bars(self, symbols, timeframe, start=None, end=None, limit=None, feed=None):
        req = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start,
            end=end,
            limit=limit,
            feed=feed
        )
        return self.stock_hist.get_stock_bars(req)

    def stock_trades(self, symbols, timeframe, start=None, end=None, limit=None, feed=None):
        req = StockQuotesRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,

            start=start,
            end=end,
            limit=limit,
            feed=feed
        )
        return self.stock_hist.get_stock_trades(req)

    def stock_quotes(self, symbols, start=None, end=None
, limit=None, feed=None):
        req = StockQuotesRequest(
            symbol_or_symbols=symbols,
            start=start,
            end=end,
            limit=limit,
            feed=feed
        )
        return self.stock_hist.get_stock_quotes(req)

    # =========================
    # HISTORICAL — OPTIONS
    # =========================
    def option_bars(self, symbols, timeframe, start=None, end=None, limit=None, feed=None):
        req = OptionBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start,
            end=end,
            limit=limit, 
            feed=feed
        )
        return self.option_hist.get_option_bars(req)

    def option_trades(self, symbols, start=None, end=None, limit=None, feed=None):
        req = OptionTradesRequest(
            symbol_or_symbols=symbols,
            start=start,
            end=end,
            limit=limit,
            feed=feed
        )
        return self.option_hist.get_option_trades(req)

    def option_quotes(self, symbols, start=None, end=None, limit=None, feed=None):
        req = OptionTradesRequest(
            symbol_or_symbols=symbols,
            start=start,
            end=end,
            limit=limit,
            feed = feed
        )
        return self.option_hist.get_option_latest_quote(req)
    


client = AlpacaDataClient(API_KEY, API_SECRET)




NP_STOCK_PATH = Path("np_stock_data.npy")


def _left_pop_rows(data: np.ndarray, pop_count: int) -> np.ndarray:
    """Remove rows from the front (left-pop style)."""
    if pop_count <= 0:
        return data
    if pop_count >= len(data):
        return data[:0]
    return data[pop_count:]


def _count_tail_match(stored_data: np.ndarray, pulled_data: np.ndarray) -> int:
    """
    Count contiguous row matches from the end of both arrays.
    Example: compare stored[-1] with pulled[-1], then keep moving left.
    """
    i = len(stored_data) - 1
    j = len(pulled_data) - 1
    matches = 0

    while i >= 0 and j >= 0:
        if not np.array_equal(stored_data[i], pulled_data[j]):
            break
        matches += 1
        i -= 1
        j -= 1

    return matches


def Agg(stored_data: np.ndarray, pulled_data: np.ndarray) -> dict:
    """
    Assumes start dates are the same.
    - Match from the last index backwards.
    - Count overlap.
    - Left-pop new rows from the pulled data by overlap delta.
    """
    if stored_data.size == 0:
        return {
            "tail_match_count": 0,
            "added_rows_count": len(pulled_data),
            "aligned_pulled_data": pulled_data,
            "new_rows_only": pulled_data,
            "full_tail_match": False,
        }

    tail_match_count = _count_tail_match(stored_data, pulled_data)
    added_rows_count = max(len(pulled_data) - tail_match_count, 0)

    return {
        "tail_match_count": tail_match_count,
        "added_rows_count": added_rows_count,
        "aligned_pulled_data": _left_pop_rows(pulled_data, added_rows_count),
        "new_rows_only": pulled_data[:added_rows_count],
        "full_tail_match": tail_match_count == len(stored_data),
    }


stored_np = np.load(NP_STOCK_PATH, allow_pickle=True) if NP_STOCK_PATH.exists() else np.empty((0, 0), dtype=object)
stock_quote = client.stock_quotes(
    symbols="INTC",
    start=datetime(2026, 3, 13),
    end=datetime.today()
).df
pulled_np = stock_quote.to_numpy(dtype=object)

agg_result = Agg(stored_np, pulled_np)

if stored_np.size > 0:
    print(
        "tail_match_count=", agg_result["tail_match_count"],
        "added_rows_count=", agg_result["added_rows_count"],
        "full_tail_match=", agg_result["full_tail_match"],
    )

np.save(NP_STOCK_PATH, pulled_np)
print(f"stock data saved to {NP_STOCK_PATH} rows={len(pulled_np)}")
