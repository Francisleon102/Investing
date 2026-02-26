from ast import main

from clients import  API_KEY,API_SECRET, tradeClient

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


list = ["SYM", "INTC", "NVDA", "ARM", "AMD"]
start_date = datetime(2026,2, 25).date()
end_date = datetime.now()
x = list[0]



def MakeOptionsym(sym: list, type: str, date: datetime, strike: list):
    symbols = []
    date = date.strftime("%y%m%d")

    for s in sym:
        for i in strike:
            strike_val = int(round(i * 1000))
            pad = 8 - len(str(strike_val))
            pad = "0" * pad

            symbols.append(s + str(date) + type + pad + str(strike_val))

    return symbols

syms = ["INTC", "NVDA"]
strikes = [10, 30, 50]

z = MakeOptionsym(syms, "C", datetime(2026,4,24), strikes)
print(z)


def main ():
    print("We up ")

if __name__ == "__main__":
    main()