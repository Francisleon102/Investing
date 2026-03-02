# realtime.py
from collections import deque

from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed
import asyncio, os
from queue import Full
from account import API_KEY, API_SECRET

SYMBOL = "AAPL"
StockData = deque()
def run(mp_q):
    print("Realtime PID:", os.getpid())

    stocklive = StockDataStream(API_KEY, API_SECRET, raw_data=True, feed=DataFeed.SIP)

    async def stock_trade_handler(msg):
        try:
            mp_q.put_nowait(("stock_trade", msg))  # msg is dict (picklable)
            StockData.append(msg)
        except Full:
            pass

    stocklive.subscribe_trades(stock_trade_handler, SYMBOL)
    try:
        asyncio.run(stocklive._run_forever())
    except KeyboardInterrupt:
        stocklive.stop_ws()
        print("connection closed")
