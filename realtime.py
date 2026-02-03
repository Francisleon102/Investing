from alpaca.data.live import StockDataStream, OptionDataStream
from collections import deque
import pandas as pd
import asyncio

keys = {"action": "auth", "key": "PKO3KEBWUSH6F52XTUK44W46Q5", "secret": "12LNKiouSeFGiyUeqMK2ZXnDx146oJfyaZW8u9Vec1QE"}
API_KEY = keys['key']
API_SECRET = keys['secret']


stocklive = StockDataStream(API_KEY, API_SECRET)
print(stocklive._auth)
async def Quote_handler(data):
   print(data)

stocklive.subscribe_bars(Quote_handler, "SYM")
stocklive.run()





