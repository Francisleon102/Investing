from alpaca.data.live import StockDataStream, OptionDataStream
from alpaca.data.enums import DataFeed, OptionsFeed
from collections import deque

import asyncio
from account import API_KEY, API_SECRET
import os
import numpy as np

import test 
print("Realtime PID:", os.getpid())
SYMBOL = "AAPL"
OPTIONSTR = "AAPL260227C00200000"


last_price = None
last_time = None
last_size = None 


def update(q):
    global last_price, last_time

    Pnow = q["s"]
    ts = q["t"]
    Tnow = ts.seconds + ts.nanoseconds * 1e-9

    if last_price is not None:
        dt = Tnow - last_time
        if dt > 0:
            rate = (Pnow - last_price) / dt
            
            test.rate  = rate
            
    last_price = Pnow
    last_time = Tnow


# persistent buffers
stock_quotes = deque()
stock_trades = deque()
opt_quotes   = deque()
opt_trades   = deque()

stocklive = StockDataStream(API_KEY, API_SECRET,raw_data=True, feed=DataFeed.SIP)
optionlive = OptionDataStream(API_KEY, API_SECRET, raw_data=False, feed=OptionsFeed.OPRA)

# --- handlers ---
async def stock_trade_handler(q):
  
    update(q)

async def stock_quote_handler(q):
    stock_quotes.append(q)
    #print(q)

async def option_quote_handler(q):
    opt_quotes.append(q)
    print(f"OPT QUOTE {q.symbol} bid={q.bid_price}@{q.bid_size} ask={q.ask_price}@{q.ask_size} t={q.timestamp}")

async def option_trade_handler(t):
    opt_trades.append(t)
   # print(f"OPT TRADE {t.symbol} price={t.price} size={t.size} t={t.timestamp}")

# --- subscribe ---
#stocklive.subscribe_quotes(stock_quote_handler, SYMBOL)
#optionlive.subscribe_quotes(option_quote_handler, OPTIONSTR)
#optionlive.subscribe_trades(option_trade_handler, OPTIONSTR)
stocklive.subscribe_trades(stock_trade_handler,SYMBOL)
#stocklive.subscribe_quotes(stock_quote_handler, SYMBOL)

# --- run both ---
async def main():
    await asyncio.gather(
       stocklive._run_forever(),   # internal runner used by run()
       # optionlive._run_forever()

    )

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Stopping...")
    # best-effort stop (if available in your version)
    for s in (stocklive, optionlive):
        stop = getattr(s, "stop_ws", None)
        if callable(stop):
            r = stop()
            if asyncio.iscoroutine(r):
                asyncio.run(r)





