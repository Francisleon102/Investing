import os, asyncio
from queue import Full
from alpaca.data.live import StockDataStream, OptionDataStream
from alpaca.data.enums import DataFeed, OptionsFeed
from account import API_KEY, API_SECRET

SYMBOL    = "AAPL"
OPTIONSTR = "AAPL260227C00200000"

def run(mp_q):
    print("Realtime PID:", os.getpid())

    stocklive  = StockDataStream(API_KEY, API_SECRET, raw_data=True, feed=DataFeed.SIP)
    optionlive = OptionDataStream(API_KEY, API_SECRET, raw_data=True, feed=OptionsFeed.OPRA)

    async def stock_trade_handler(msg):
        try:
            mp_q.put_nowait(("stock_trade", msg))   # dict
        except Full:
            pass

    async def stock_quotes_handler(msg):
        try:
            mp_q.put_nowait(("stock_quotes", msg))  # dict (raw_data=True)
        except Full:
            pass
    async def option_trade_handler(msg):
        try:
            mp_q.put_nowait(("option_trade", msg))  # dict (raw_data=True)
        except Full:
            pass

    async def option_quote_handler(msg):
        try:
            mp_q.put_nowait(("option_quote", msg))  # dict (raw_data=True)
        except Full:
            pass
    
    stocklive.subscribe_trades(stock_trade_handler, SYMBOL)
    stocklive.subscribe_quotes(stock_trade_handler,SYMBOL)
    optionlive.subscribe_trades(option_trade_handler, OPTIONSTR)
    optionlive.subscribe_quotes(option_quote_handler, OPTIONSTR)

    async def runner():
        try:
            await asyncio.gather(
                stocklive._run_forever(),
                optionlive._run_forever(),
            )
        finally:
            # graceful close (stop_ws is async)
            await stocklive.stop_ws()
            await optionlive.stop_ws()
            print("connection closed")

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        pass