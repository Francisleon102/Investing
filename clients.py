#from pydoc import cli

import numpy as np
#import incoming as inc
import matplotlib.pyplot as plt
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient, OptionHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest, OptionTradesRequest, OptionBarsRequest, OptionLatestQuoteRequest
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
import pyqtgraph as pg 

global  t2 

# alpaca_data_client.py

class AlpacaDataClient:
    def __init__(self, api_key: str, api_secret: str):
        self.stock_hist = StockHistoricalDataClient(api_key, api_secret)
        self.option_hist = OptionHistoricalDataClient(api_key, api_secret)

        
        self.stock_stream = StockDataStream(api_key, api_secret)
        self.option_stream = OptionDataStream(api_key, api_secret)

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
    


    # =========================
    # STREAMING — STOCKS
    # =========================
    def stream_stock_bars(self, symbols, handler):
        self.stock_stream.subscribe_bars(handler, *symbols)

    def stream_stock_trades(self, symbols, handler):
        self.stock_stream.subscribe_trades(handler, *symbols)

    def stream_stock_quotes(self, symbols, handler):
        self.stock_stream.subscribe_quotes(handler, *symbols)

    # =========================
    # STREAMING — OPTIONS
    # =========================
    def stream_option_trades(self, symbols, handler):
        self.option_stream.subscribe_trades(handler, *symbols)

    def stream_option_quotes(self, symbols, handler):
        self.option_stream.subscribe_quotes(handler, *symbols)

    # =========================
    # RUN STREAMS
    # =========================
    async def run_stock_stream(self):
        await self.stock_stream.run()

    async def run_option_stream(self):
        await self.option_stream.run()



client  = AlpacaDataClient(API_KEY, API_SECRET) 

    # =========================
    # Trading Client
    # =========================


class AlcapaTradingClient:
    def __init__(self, api_key: str, api_secret: str):
        self.contracts = TradingClient(
            api_key=api_key,
            secret_key=api_secret,
            paper=True
        )

    def contract(self, underlying_symbols, expiration_date,
                 strike_price_gte, strike_price_lte, type):

        req = GetOptionContractsRequest(
            underlying_symbols=underlying_symbols,  # FIXED
            expiration_date=expiration_date,
            strike_price_gte=strike_price_gte,
            strike_price_lte=strike_price_lte,
            type=type
        )

        return self.contracts.get_option_contracts(req)


tradeClient = AlcapaTradingClient(API_KEY, API_SECRET)

all_contracts = tradeClient.contract(
    underlying_symbols=["AAPL"],
    expiration_date="2026-01-21",
    strike_price_gte="150",
    strike_price_lte="200",
    type=ContractType.CALL
)