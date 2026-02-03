from alpaca.trading.client import TradingClient
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

live = 0
if(live):
    API_KEY = "AKSHCBQYQY26TM3B4YYR2N4BAH"
    API_SECRET = "GwZY3m3GnVenU3iwXEcWC5Z7wHrNe5U7vdBd2H9kVLuk"
else: 
    API_KEY = "PKZ5LNGJM7SBOQVBTCIJ2XRSTW"
    API_SECRET = "6yrJoBL5Qn5yNCNeYR5GCKK5mh6dorWArbTPFQozZYYG"

client = TradingClient(API_KEY, API_SECRET, paper=True)
account = client.get_account()

print(account.buying_power)

