from datetime import datetime
from multiprocessing import Process

from graphs import run as run_graphs
from realtime import run as run_realtime


symbols = ["SYM", "INTC", "NVDA", "ARM", "AMD"]
start_date = datetime(2026,2, 25).date()
end_date = datetime.now()
x = symbols[0]



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
    p1 = Process(target=run_realtime)
    p2 = Process(target=run_graphs)
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == "__main__":
    main()