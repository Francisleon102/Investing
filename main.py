#!/usr/bin/env python
# coding: utf-8

# In[1]:


#from pydoc import cli

import numpy as np
#import incoming as inc
import matplotlib.pyplot as plt
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient, OptionHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest, OptionTradesRequest, OptionBarsRequest, OptionLatestQuoteRequest
OptionBarsRequest
from alpaca.data.timeframe import TimeFrame ; import cudf as cdf 
from datetime import datetime, timezone, date
import polars as pl
from alpaca.data.live import StockDataStream, OptionDataStream
from account import API_KEY , API_SECRET


# In[2]:


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
    def stock_bars(self, symbols, timeframe, start=None, end=None, limit=None):
        req = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start,
            end=end,
            limit=limit
        )
        return self.stock_hist.get_stock_bars(req)

    def stock_trades(self, symbols, timeframe, start=None, end=None, limit=None):
        req = StockQuotesRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,

            start=start,
            end=end,
            limit=limit
        )
        return self.stock_hist.get_stock_trades(req)

    def stock_quotes(self, symbols, start=None, end=None
, limit=None):
        req = StockQuotesRequest(
            symbol_or_symbols=symbols,
            start=start,
            end=end,
            limit=limit
        )
        return self.stock_hist.get_stock_quotes(req)

    # =========================
    # HISTORICAL — OPTIONS
    # =========================
    def option_bars(self, symbols, timeframe, start=None, end=None, limit=None):
        req = OptionBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=start,
            end=end,
            limit=limit
        )
        return self.option_hist.get_option_bars(req)

    def option_trades(self, symbols, start=None, end=None, limit=None):
        req = OptionTradesRequest(
            symbol_or_symbols=symbols,
            start=start,
            end=end,
            limit=limit
        )
        return self.option_hist.get_option_trades(req)

    def option_quotes(self, symbols, start=None, end=None, limit=None):
        req = OptionTradesRequest(
            symbol_or_symbols=symbols,
            start=start,
            end=end,
            limit=limit
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


# In[3]:


yymmdd = date.today().strftime("%y%m%d")  # "260204"
yymmdd


# Calls 
# 

# In[ ]:


print("ehllo")


# ReQuests 

# In[4]:


list = ["SYM", "INTC", "NVDA", "ARM", "AMD"]
start_date = datetime(2026,1,25)
list[0]

def MakeOptionsym(sym:str, type: str, date : datetime, strike):
    date =  date.strftime("%y%m%d")

    strike = int(round(strike * 1000))

    pad = 8 - len(str(strike))
    pad = str(0).zfill(pad)
    i = sym+str(date)+type+str(pad)+str(strike)
    return i

z = MakeOptionsym(list[1],"C",datetime(2026,1,30), 75)
print(z)



# In[5]:


client  = AlpacaDataClient(API_KEY, API_SECRET) 
S_Quotes = client.stock_quotes(symbols=list[0],   start=start_date, end=datetime.today()).df
S_Bars = client.stock_bars(symbols=list[0],timeframe=TimeFrame.Minute, start=start_date, end=datetime.today()).df
S_Trades = client.stock_trades(symbols=list[0],timeframe=TimeFrame.Hour,start=datetime(2026, 1, 30), end=datetime.today()).df


# In[6]:


#Options 
#O_Quotes = client.option_quotes(z, start=start_date, end=datetime.today())
O_Bars = client.option_bars(z,timeframe=TimeFrame.Hour,start= start_date, end=datetime.today())
O_Trades = client.option_trades(z, start=start_date, end=datetime.today())


# In[ ]:





# In[7]:


S_Quotes


# In[8]:


#sum up all recurring size for a specific price: highlights where trades has occured more often 
from cudf import dtype

bid_x_size = pd.DataFrame(S_Quotes).reset_index().groupby('bid_price')['bid_size'].sum()
bid_x_size = bid_x_size.reset_index()

ask_x_size = (
    pd.DataFrame(S_Quotes)
      .reset_index()
      .groupby('ask_price')['ask_size']
      .sum()
      .reset_index()
)




# In[9]:


import pyqtgraph as pg 

offset = 0.5  # half a tick, adjust to your market

app = pg.mkQApp()
win = pg.GraphicsLayoutWidget(show=True)
p1 = win.addPlot(title = "bids")
p1.showGrid(x = True, y = True)
x1 = pg.BarGraphItem(x=bid_x_size.bid_price - offset, 
                     height=bid_x_size.bid_size, width = 0.09, 
                     size=0.3, brush = pg.mkBrush(255,255,0))
p1.addItem(x1)

p1.setLabel('bottom', 'Price')
p1.setLabel('left', 'Bid Size')

win.nextRow()

p2 = win.addPlot(title = "asks")
p2.showGrid(x = True, y = True)

x2 = pg.BarGraphItem(x=ask_x_size.ask_price, 
                     height=ask_x_size.ask_size, width = 0.09, 
                     size=0.3, brush = pg.mkBrush(0,255,255))




p2.addItem(x2)
app.exec()


# In[10]:


class Aggregations:
    def __init__(self, x: pd.DataFrame):

        pass 
    # Aggregations 



# In[11]:


S_Bars['open'].diff()


# In[8]:


import numpy as np
from collections import deque
import pyqtgraph as pg
from PyQt6 import QtCore

app = pg.mkQApp("RT Scatter")

win = pg.GraphicsLayoutWidget(title="Real-time Scatter")
p = win.addPlot()
p.showGrid(x=True, y=True)

x = np.random.normal(1,3,100)
x2 = np.random.normal(1,3,100)
y = np.random.normal(1,3,100)


l = []
def update():

    print("hello")






timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(600)   # ~60 FPS

win.show()
pg.exec()


# In[13]:


print(type(z))

