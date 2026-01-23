#from pydoc import cli

import numpy as np
#import incoming as inc
import matplotlib.pyplot as plt
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient, OptionHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest, OptionTradesRequest, OptionBarsRequest
from alpaca.data.timeframe import TimeFrame ; import cudf as cdf 
from datetime import datetime; 
import pandas as df
import polars as pl
from alpaca.data.live import StockDataStream, OptionDataStream

keys = {"action": "auth", "key": "PKO3KEBWUSH6F52XTUK44W46Q5", "secret": "12LNKiouSeFGiyUeqMK2ZXnDx146oJfyaZW8u9Vec1QE"}
API_KEY = keys['key']
API_SECRET = keys['secret']


sym = ["AMD", "SYM"]
start = datetime(2025, 12, 10)
end = datetime(2025, 12, 15)
timeframe = TimeFrame.Minute
s_rq = StockBarsRequest(symbol_or_symbols=sym[0], timeframe=timeframe, start=start, end=end)
stockclientn = StockHistoricalDataClient(API_KEY, API_SECRET)
stock_data = stockclientn.get_stock_bars(s_rq)

xdf = df.DataFrame(stock_data.df) ; xdf = xdf.reset_index()

