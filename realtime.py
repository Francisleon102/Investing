from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed
from collections import deque 
from queue import Queue


import asyncio
import pandas as pd
from account import API_KEY, API_SECRET

SYMBOL = "AMD"


stocklive = StockDataStream(API_KEY, API_SECRET, feed=DataFeed.SIP)


async def quote_handler(data):
    df = Queue(maxsize=10)
    df.put(data)
    s = df.get()

    print(s)
    


stocklive.subscribe_trades(quote_handler, SYMBOL)
try:
    stocklive.run()
except KeyboardInterrupt:
    print("\nStopping stream...")
    stop = getattr(stocklive, "stop_ws", None)
    if callable(stop):
        result = stop()
        if asyncio.iscoroutine(result):
            asyncio.run(result)
    print("Stream closed.")
