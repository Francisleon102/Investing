from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from alpaca.data.timeframe import TimeFrame

from historical_pull import run_historical_pull


# Editable settings
SYMBOLS = "INTC"  # or ["INTC", "AAPL"]
START = datetime(2026, 3, 13, tzinfo=timezone.utc)
END = None  # None -> now
REFRESH = False  # True -> force re-pull even if cache exists
BARS_TIMEFRAME = TimeFrame.Minute

DATA_DIR = Path("Data")
QUOTES_PATH = DATA_DIR / "np_stock_data.npy"
TRADES_PATH = DATA_DIR / "np_stock_trades.npy"
BARS_PATH = DATA_DIR / "np_stock_bars.npy"


def run():
    return run_historical_pull(
        symbols=SYMBOLS,
        start=START,
        end=END,
        refresh=REFRESH,
        bars_timeframe=BARS_TIMEFRAME,
        quotes_path=QUOTES_PATH,
        trades_path=TRADES_PATH,
        bars_path=BARS_PATH,
    )


if __name__ == "__main__":
    run()
