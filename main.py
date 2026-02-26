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


def MakeOptionsym(sym: str, type: str, date: datetime, strike):
    strike = [10, 30, 50, 70]   # your list
    symbols = []
    date = date.strftime("%y%m%d")
    for i in strike:
        strike_val = int(round(i * 1000))
        pad = 8 - len(str(strike_val))
        pad = "0" * pad
        symbols.append(sym + str(date) + type + pad + str(strike_val))
    return symbols


z = MakeOptionsym(list[1],"C",datetime(2026,1,30), 75)
print(z)
l = "INTC260130C00060000"
start_date


def main ():
    print("We up ")

if __name__ == "__main__":
    main()